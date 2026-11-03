#!/usr/bin/env python3
"""Download a GitHub Actions artifact using gh credentials and verify its digest.

Credentials and temporary download URLs stay in memory and are never logged.
The destination is created only after verification; existing files are refused.
"""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import urllib.error
import urllib.request


class ArtifactError(RuntimeError):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


def download(artifact, destination):
    if destination.exists():
        raise ArtifactError('Destination already exists')
    result = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, check=False)
    if result.returncode or not result.stdout.strip():
        raise ArtifactError('GitHub CLI authentication is unavailable')
    headers = {'Authorization': 'Bearer ' + result.stdout.strip(),
               'Accept': 'application/vnd.github+json'}
    base = f'https://api.github.com/repos/chevydan6/OrcaSlicer-QIDI/actions/artifacts/{artifact}'
    opener = urllib.request.build_opener(NoRedirect)
    with opener.open(urllib.request.Request(base, headers=headers), timeout=30) as response:
        metadata = json.load(response)
    expected = metadata.get('digest', '')
    if not expected.startswith('sha256:') or len(expected) != 71:
        raise ArtifactError('No usable GitHub SHA-256 artifact digest')
    try:
        with opener.open(urllib.request.Request(base + '/zip', headers=headers), timeout=30):
            raise ArtifactError('Expected GitHub artifact redirect')
    except urllib.error.HTTPError as error:
        if error.code != 302 or not error.headers.get('Location', '').startswith('https://'):
            raise ArtifactError('Artifact download redirect unavailable') from None
        url = error.headers['Location']
    del headers, result
    size = metadata['size_in_bytes']
    chunk_size = 4 * 1024 * 1024

    def fetch(start):
        end = min(size, start + chunk_size) - 1
        for attempt in range(3):
            try:
                request = urllib.request.Request(url, headers={'Range': f'bytes={start}-{end}'})
                with urllib.request.urlopen(request, timeout=60) as response:
                    data = response.read()
                    if response.status != 206 or len(data) != end - start + 1:
                        raise ArtifactError('Invalid artifact range response')
                return start, data
            except Exception:
                if attempt == 2:
                    raise ArtifactError('Artifact range download failed') from None

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination.parent, prefix='.artifact-', delete=False) as stream:
            temporary = Path(stream.name)
            stream.truncate(size)
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                for start, data in pool.map(fetch, range(0, size, chunk_size)):
                    stream.seek(start)
                    stream.write(data)
        with temporary.open('rb') as stream:
            actual = 'sha256:' + hashlib.file_digest(stream, 'sha256').hexdigest()
        if actual != expected:
            raise ArtifactError('GitHub artifact digest mismatch')
        # Hard-link creation refuses a destination created during the download.
        destination.hardlink_to(temporary)
        print(json.dumps({'artifact_id': artifact, 'bytes': size, 'digest': actual, 'verified': True}))
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('artifact_id', type=int)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        download(args.artifact_id, args.output)
    except Exception as error:
        # Never format arbitrary network exceptions: they can contain signed URLs.
        message = str(error) if isinstance(error, ArtifactError) else type(error).__name__
        raise SystemExit('Artifact download failed: ' + message) from None
