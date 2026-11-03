#!/usr/bin/env python3
"""Exercise the loopback fixture itself; this does not validate the slicer GUI."""
import asyncio
import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile

from aiohttp import ClientSession, FormData, WSMsgType, web
from aiohttp.test_utils import TestServer

spec = importlib.util.spec_from_file_location('qidi_fixture', Path(__file__).with_name('qidi-printer-fixture.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


async def check():
    with tempfile.TemporaryDirectory() as temporary:
        fixture = module.Fixture(2, Path(temporary)/'requests.jsonl', Path(temporary)/'uploads')
        app = web.Application()
        app.router.add_route('*', '/{path:.*}', fixture.handle)
        async with TestServer(app, host='127.0.0.1') as server, ClientSession() as client:
            base = str(server.make_url('')).rstrip('/')
            async with client.get(base+'/server/info') as response:
                assert (await response.json())['result']['klippy_state'] == 'ready'
            ws = await client.ws_connect(base+'/websocket')
            await ws.send_json({'jsonrpc': '2.0', 'method': 'printer.objects.subscribe', 'id': 1})
            first = await ws.receive_json(timeout=3)
            assert first['result']['status']['multi_color_controller']['box']['box_count'] == 2
            assert (await ws.receive_json(timeout=3))['method'] == 'notify_proc_stat_update'
            async with client.post(base+'/printer/gcode/script', json={'script': 'OFFLINE_TEST_ONLY'}) as response:
                assert (await response.json())['result'] == 'ok'
            assert fixture.status['extruder']['target'] == 0
            form = FormData()
            payload = b'offline upload bytes; never executed'
            form.add_field('file', payload, filename='../../outside.gcode', content_type='application/octet-stream')
            async with client.post(base+'/server/files/upload', data=form) as response:
                assert (await response.json())['result']['print_started'] is False
            events = [json.loads(line) for line in fixture.log.read_text().splitlines()]
            upload = next(e for e in events if e.get('upload_field') == 'file')
            assert upload['sha256'] == hashlib.sha256(payload).hexdigest()
            assert (fixture.upload_dir / upload['saved_file']).read_bytes() == payload
            assert '/' not in upload['saved_file'] and not (Path(temporary)/'outside.gcode').exists()
            for available in (False, True):
                async with client.post(base+'/__fixture__/state', json={'storage_available': available}) as response:
                    assert response.status == 200
                async with client.get(base+'/server/files/directory?path=gcodes') as response:
                    free = (await response.json())['result']['disk_usage']['free']
                    assert (free > 0) == available
            async with client.post(base+'/__fixture__/state', json={'raw': 'invalid-json', 'http_error': 503}) as response:
                assert response.status == 200
            assert (await ws.receive(timeout=3)).data == 'invalid-json'
            async with client.get(base+'/server/info') as response:
                assert response.status == 503
            async with client.post(base+'/__fixture__/state', json={
                'http_error': 0, 'update': {'multi_color_controller': {'box': {'box0_aht20_temp': 30}}}
            }) as response:
                assert response.status == 200
            assert (await ws.receive_json(timeout=3))['method'] == 'notify_status_update'
            assert fixture.status['multi_color_controller']['box']['box_count'] == 2
            async with client.post(base+'/__fixture__/state', json={'disconnect': True}) as response:
                assert response.status == 200
            assert (await ws.receive(timeout=3)).type == WSMsgType.CLOSE
            await ws.close()
            events = [json.loads(line) for line in fixture.log.read_text().splitlines()]
            assert any(e.get('body') == '{"script": "OFFLINE_TEST_ONLY"}' for e in events)
        print('PASS: loopback HTTP/WebSocket fixture, command recording, partial updates, malformed messages, HTTP failure recovery and disconnect.')
        print('No commands executed or forwarded. Custom slicer GUI validation remains separate.')


if __name__ == '__main__':
    asyncio.run(check())
