"""Run native Ren'Py tests in a private game copy; never share player saves."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import uuid

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SOURCE = PROJECT / '03_開發' / 'JingZhe' / 'game'
ENGINE = PROJECT / '05_成品' / '驚蟄_v0.1.2_Windows'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--suite', default='jz_qa')
    ap.add_argument('--runtime-dir', type=Path)
    ap.add_argument('--lint', action='store_true')
    args = ap.parse_args()
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    runtime = args.runtime_dir or Path(tempfile.gettempdir()) / ('jz_integrity_' + stamp + '_' + uuid.uuid4().hex[:6])
    game = runtime / 'game'
    game.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for path in SOURCE.rglob('*'):
        relative = path.relative_to(SOURCE)
        if relative.parts[0] in ('audio', 'gui', 'images', 'saves', 'cache'):
            continue
        if path.is_file() and path.suffix in ('.rpy', '.ttf', '.txt'):
            target = game / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            manifest[relative.as_posix()] = digest(path)
    for name in ('audio', 'gui', 'images'):
        target = game / name
        if not target.exists():
            quote = lambda p: "'" + str(p).replace("'", "''") + "'"
            subprocess.run(['powershell', '-NoProfile', '-Command',
                            'New-Item -ItemType Junction -Path ' + quote(target) +
                            ' -Target ' + quote(SOURCE / name) + ' | Out-Null'], check=True)
    if not args.lint:
        shutil.copy2(HERE / 'functional_suite.rpy', game / '_functional_suite.rpy')
    # Both Ren'Py save locations belong to this disposable copy.
    saves = runtime / 'private_saves'
    saves.mkdir(exist_ok=True)
    legacy = []
    for index, path in enumerate(sorted((SOURCE / 'saves').glob('*.save'), key=lambda p: p.stat().st_mtime)[:2], 1):
        destination = saves / ('legacy-' + str(index) + '-LT1.save')
        if not destination.exists():
            shutil.copy2(path, destination)
        legacy.append({'source_name': path.name, 'sha256': digest(path)})
    output = HERE / 'results' / (stamp + '_' + ('lint' if args.lint else args.suite))
    output.mkdir(parents=True, exist_ok=True)
    (output / 'source_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    command = [str(ENGINE / 'lib' / 'py3-windows-x86_64' / 'python.exe'), str(ENGINE / 'JingZhe.py'), str(runtime)]
    if args.lint:
        command += ['lint', str(output / 'lint.txt'), '--error-code', '--all-problems', '--check-unclosed-tags']
    else:
        command += ['test', args.suite, '--report-detailed']
    command += ['--savedir', str(saves)]
    env = os.environ.copy()
    env.pop('RENPY_SEARCHPATH', None)
    env['JZ_QA_OUTPUT'] = str(output)
    env['PYTHONUTF8'] = '1'
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = 0
    print(json.dumps({'runtime': str(runtime), 'output': str(output), 'command': command}, ensure_ascii=False), flush=True)
    native_status = None
    started_at = time.time()
    with (output / 'console.txt').open('w', encoding='utf-8') as console:
        process = subprocess.Popen(command, env=env, stdout=console, stderr=subprocess.STDOUT, startupinfo=startup)
        deadline = time.monotonic() + 900
        while process.poll() is None:
            time.sleep(0.5)
            log = (output / 'console.txt').read_text(encoding='utf-8', errors='replace')
            if '[rpytest] Status: PASSED' in log or '[rpytest] Status: FAILED' in log:
                native_status = 'PASSED' if '[rpytest] Status: PASSED' in log else 'FAILED'
                # Native tests report completion but intentionally leave the UI open.
                process.terminate()
                break
            if time.monotonic() > deadline:
                process.terminate()
                native_status = 'TIMEOUT'
                break
        process.wait(timeout=20)
    exit_code = (0 if native_status == 'PASSED' else 1) if native_status else process.returncode
    for name in ('log.txt', 'errors.txt', 'traceback.txt'):
        path = runtime / name
        if path.exists() and path.stat().st_mtime >= started_at:
            shutil.copy2(path, output / name)
    summary = {'exit_code': exit_code, 'native_status': native_status, 'runtime': str(runtime), 'suite': args.suite,
               'legacy_copies': legacy, 'source_manifest_unchanged': all(digest(SOURCE / name) == value for name, value in manifest.items())}
    (output / 'run.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False), flush=True)
    print((output / 'console.txt').read_text(encoding='utf-8', errors='replace')[-14000:], flush=True)
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
