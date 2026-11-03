#!/usr/bin/env python3
"""Loopback-only QIDI/Moonraker fixture. Records commands; never executes or forwards them."""
import argparse
import asyncio
import copy
from contextlib import nullcontext
import hashlib
import json
from pathlib import Path
import tempfile
import time

from aiohttp import web, WSMsgType


def initial_status(boxes):
    box = {'box_count': boxes}
    colors = ['FF0000', '00FF00', '0000FF', 'FFFFFF']
    for unit in range(boxes):
        box.update({f'box{unit}_aht20_temp': 24.0, f'box{unit}_aht20_humidity': 35})
        for slot in range(4):
            prefix = f'box{unit}_filament_info_{slot}_'
            box[f'box{unit}_box_inserted_{slot}'] = 1
            box.update({prefix+'filament_type': 'PLA', prefix+'filament_str': 'PLA Rapido',
                        prefix+'vendor_str': 'QIDI', prefix+'color_rgb_str': [colors[slot]]})
    return {
        'print_stats': {'state': 'standby', 'filename': '', 'message': '', 'print_duration': 0,
                        'total_duration': 0, 'filament_used': 0, 'info': {'current_layer': 0, 'total_layer': 20}},
        'virtual_sdcard': {'progress': 0, 'is_active': False, 'file_position': 0, 'file_size': 0},
        'extruder': {'temperature': 23, 'target': 0, 'power': 0},
        'heater_bed': {'temperature': 24, 'target': 0, 'power': 0},
        'heater_generic chamber': {'temperature': 24, 'target': 0, 'power': 0},
        'toolhead': {'homed_axes': 'xyz', 'position': [0, 0, 0, 0], 'extruder': 'extruder'},
        'gcode_move': {'speed_factor': 1.0, 'extrude_factor': 1.0},
        'fan': {'speed': 0},
        'fan_generic cooling_fan': {'speed': 0},
        'fan_generic auxiliary_cooling_fan': {'speed': 0},
        'fan_generic chamber_circulation_fan': {'speed': 0},
        'output_pin caselight': {'value': 0}, 'output_pin polar_cooler': {'value': 0},
        'display_status': {'progress': 0, 'message': 'OFFLINE TEST FIXTURE'},
        'pause_resume': {'is_paused': False},
        'exclude_object': {'objects': [{'name': 'fixture_cube'}, {'name': 'fixture_tower'}], 'excluded_objects': []},
        'save_variables': {'variables': {'box_count': boxes, 'enable_noodle_detection': 1,
                                       'enable_pre_print_model_check': 1, 'noodle_sensitivity_level': 'MEDIUM'}},
        'multi_color_controller': {'identity': 'box_v1', 'box': box, 'last_load_slot': 'slot2',
                                  'auto_read_rfid': 1, 'auto_init_detect': 1,
                                  'extra': {'filament_info': {'filament_type': 'PETG', 'filament_str': 'PETG',
                                                            'vendor_str': 'Generic', 'color_rgb_str': ['808080']}}},
    }


def merge(target, update):
    for key, value in update.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            merge(target[key], value)
        else:
            target[key] = copy.deepcopy(value)


class Fixture:
    def __init__(self, boxes, log, upload_dir=None):
        self.status = initial_status(boxes)
        self.log = log
        self.clients = set()
        self.http_error = 0
        self.delay = 0
        self.invalid_camera_frame = False
        self.storage_available = True
        self.upload_dir = upload_dir
        if upload_dir is not None:
            upload_dir.mkdir(parents=True, exist_ok=True)

    def record(self, **event):
        with self.log.open('a') as stream:
            stream.write(json.dumps({'time': time.time(), **event})+'\n')

    async def notify(self, value, raw=False):
        for client in list(self.clients):
            if not client.closed:
                try:
                    if raw:
                        await client.send_str(value)
                    else:
                        await client.send_json(value)
                except (ConnectionError, RuntimeError):
                    self.clients.discard(client)

    async def admin(self, request):
        data = await request.json()
        if 'http_error' in data:
            self.http_error = int(data['http_error'])
        if 'delay' in data:
            self.delay = max(0, min(60, float(data['delay'])))
        if 'invalid_camera_frame' in data:
            self.invalid_camera_frame = bool(data['invalid_camera_frame'])
        if 'storage_available' in data:
            self.storage_available = bool(data['storage_available'])
        if 'replace' in data:
            self.status = data['replace']
        if 'update' in data:
            merge(self.status, data['update'])
        if 'update' in data or 'replace' in data:
            await self.notify({'jsonrpc': '2.0', 'method': 'notify_status_update',
                               'params': [data.get('update', self.status), time.monotonic()]})
        if 'notification' in data:
            await self.notify(data['notification'])
        if 'raw' in data:
            await self.notify(str(data['raw']), raw=True)
        if data.get('disconnect'):
            for client in list(self.clients):
                await client.close()
        self.record(admin=data)
        return web.json_response({'clients': len(self.clients), 'status': self.status})

    async def websocket(self, request):
        ws = web.WebSocketResponse(max_msg_size=2**20)
        await ws.prepare(request)
        self.clients.add(ws)
        try:
            async for message in ws:
                if message.type != WSMsgType.TEXT:
                    continue
                try:
                    data = json.loads(message.data)
                except ValueError:
                    continue
                self.record(websocket=data)
                method = data.get('method')
                result = {'connection_id': 1} if method == 'server.connection.identify' else 'ok'
                if method == 'printer.objects.subscribe':
                    result = {'status': self.status, 'eventtime': time.monotonic()}
                if 'id' in data:
                    await ws.send_json({'jsonrpc': '2.0', 'id': data['id'], 'result': result})
                if method == 'printer.objects.subscribe':
                    await ws.send_json({'jsonrpc': '2.0', 'method': 'notify_proc_stat_update',
                                        'params': [{'config_items': {'printing.polar_cooler': '1'}}]})
        finally:
            self.clients.discard(ws)
        return ws

    async def handle(self, request):
        path = request.path
        if path == '/__fixture__/state':
            return await self.admin(request)
        # Record arrival before injected latency, including requests cancelled
        # while the client closes. Keep completion/body records separate.
        self.record(request_received={'method': request.method, 'path': path})
        if self.delay:
            await asyncio.sleep(self.delay)
        if self.http_error:
            self.record(method=request.method, path=path, injected_http_error=self.http_error)
            return web.json_response({'error': {'message': 'Injected fixture failure'}}, status=self.http_error)
        if path == '/websocket':
            return await self.websocket(request)
        body = await request.text() if request.can_read_body and path != '/server/files/upload' else ''
        self.record(method=request.method, path=path, query=dict(request.query), body=body)
        result = 'ok'
        if path == '/webcam/' and request.query.get('action') == 'snapshot':
            frame = b'invalid image data' if self.invalid_camera_frame else (
                Path(__file__).resolve().parents[1] / 'fixtures/qidi-camera.jpg').read_bytes()
            return web.Response(body=frame, content_type='image/jpeg')
        elif path == '/server/info':
            result = {'machine_name': 'OFFLINE MAX4 FIXTURE', 'hostname': 'offline-fixture',
                      'moonraker_version': 'fixture', 'klippy_state': 'ready', 'components': ['file_manager']}
        elif path == '/printer/info':
            result = {'state': 'ready', 'state_message': 'OFFLINE TEST FIXTURE', 'hostname': 'offline-fixture'}
        elif path == '/printer/objects/list':
            result = {'objects': list(self.status)}
        elif path == '/printer/objects/query':
            result = {'status': self.status, 'eventtime': time.monotonic()}
        elif path == '/server/files/directory':
            free = 10**9 if self.storage_available else 0
            result = {'dirs': [], 'files': [], 'disk_usage': {'total': 10**9, 'used': 10**9 - free, 'free': free}}
        elif path == '/server/files/list':
            result = []
        elif path == '/server/files/metadata':
            result = {'filename': request.query.get('filename', ''), 'size': 1000,
                      'estimated_time': 60, 'layer_count': 20, 'thumbnails': []}
        elif path == '/server/files/upload':
            reader = await request.multipart()
            filename = 'fixture.gcode'
            async for part in reader:
                size = 0
                digest = hashlib.sha256()
                capture = (tempfile.NamedTemporaryFile(dir=self.upload_dir, prefix='upload-',
                                                      suffix='.bin', delete=False)
                           if part.filename and self.upload_dir is not None else nullcontext())
                with capture as saved:
                    while chunk := await part.read_chunk():
                        size += len(chunk)
                        digest.update(chunk)
                        if saved is not None:
                            saved.write(chunk)
                    saved_name = Path(saved.name).name if saved is not None else None
                if part.filename:
                    filename = part.filename
                self.record(upload_field=part.name, filename=part.filename, size=size,
                            sha256=digest.hexdigest(), saved_file=saved_name)
            result = {'item': {'path': filename, 'root': 'gcodes'}, 'print_started': False, 'action': 'create_file'}
        elif request.method == 'GET':
            return web.json_response({'error': {'message': 'Fixture endpoint not implemented'}}, status=404)
        return web.json_response({'result': result})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=19025)
    parser.add_argument('--boxes', type=int, choices=range(5), default=2)
    parser.add_argument('--log', type=Path, required=True)
    parser.add_argument('--upload-dir', type=Path,
                        help='Optionally retain uploaded bytes under generated names for offline inspection')
    args = parser.parse_args()
    args.log.parent.mkdir(parents=True, exist_ok=True)
    fixture = Fixture(args.boxes, args.log, args.upload_dir)
    app = web.Application(client_max_size=2**20)
    app.router.add_route('*', '/{path:.*}', fixture.handle)
    print('OFFLINE FIXTURE: records commands only; no hardware or forwarding.', flush=True)
    web.run_app(app, host='127.0.0.1', port=args.port)


if __name__ == '__main__':
    main()
