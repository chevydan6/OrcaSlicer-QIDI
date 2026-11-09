#!/usr/bin/env python3
"""Retain CI downloads in an unpublished candidate release if Actions storage is full."""
import argparse,json,os,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('assets',nargs='+',type=Path);args=p.parse_args()
repo=os.environ['GITHUB_REPOSITORY'];sha=os.environ['GITHUB_SHA']
if not re.fullmatch(r'[0-9a-f]{40}',sha):raise SystemExit('Expected an exact integration commit')
assets=[p.resolve() for p in args.assets if p.is_file() and p.stat().st_size]
if not assets:raise SystemExit('No nonempty build assets are available')
tag='qidi-main-build-'+sha[:12]
def gh(*a,check=True):return subprocess.run(['gh',*a,'--repo',repo],capture_output=True,text=True,check=check)
def existing():
 r=gh('release','view',tag,'--json','isDraft,targetCommitish,url',check=False)
 if r.returncode:return None
 info=json.loads(r.stdout)
 if not info['isDraft'] or info['targetCommitish']!=sha:raise SystemExit('Refusing to modify an existing published or mismatched release')
 return info
if existing() is None:
 notes=Path('candidate-download-notes.txt');notes.write_text('Candidate build downloads for integration commit '+sha+'.\n\nThese files are staged for verification. This release is intentionally unpublished. Check the Actions results before treating a candidate as validated.\n')
 r=gh('release','create',tag,'--draft','--target',sha,'--title','QIDI candidate build '+sha[:12],'--notes-file',str(notes),check=False)
 if r.returncode and existing() is None:raise SystemExit(r.stderr)
assert existing() is not None
r=gh('release','upload',tag,*map(str,assets),'--clobber');print('Candidate downloads retained in draft release '+tag)
