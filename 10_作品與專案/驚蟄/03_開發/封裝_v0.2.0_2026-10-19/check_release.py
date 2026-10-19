"""Validate the actual ZIP after extraction and execute its own Windows EXE."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
import zipfile

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
QA = HERE.parent / '功能整合檢查_2026-10-19'


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def main():
    build = json.loads((HERE / 'build_result.json').read_text(encoding='utf-8'))
    archive = Path(build['zip'])
    assert sha(archive) == build['sha256']
    work = Path(tempfile.mkdtemp(prefix='jz_zip_check_020_'))
    with zipfile.ZipFile(archive) as z:
        z.extractall(work)
    package = work / Path(build['folder']).name
    manifest = json.loads((PROJECT / '05_成品/JingZhe-0.2.0-win.manifest.json').read_text(encoding='utf-8'))
    actual = {p.relative_to(package).as_posix() for p in package.rglob('*') if p.is_file()}
    assert actual == set(manifest['files'])
    for name, entry in manifest['files'].items():
        assert sha(package / name) == entry['sha256'], name
    tests = work / 'external_tests'
    tests.mkdir()
    # First extracted run reached the ending transition just beyond 45 seconds.
    # Allow slower machines more time without changing shipped game timing.
    suite_source = (QA / 'functional_suite.rpy').read_text(encoding='utf-8')
    suite_source = suite_source.replace('_test.timeout = 15.0', '_test.timeout = 45.0')
    suite_source = suite_source.replace('pause until screen "jz_ending_complete" timeout 45',
                                        'pause until screen "jz_ending_complete" timeout 90')
    (tests / 'functional_suite.rpy').write_text(suite_source, encoding='utf-8')
    (tests / 'release_meta.rpy').write_text(
        'testcase jz_release_meta:\n'
        '    assert eval (config.version == "0.2.0") timeout 5\n'
        '    assert eval (config.basedir == _qa_os.environ["JZ_RELEASE_BASE"]) timeout 5\n'
        '    assert eval (config.renpy_base == config.basedir) timeout 5\n'
        '    assert eval (renpy.music.get_playing(channel="music") == config.main_menu_music) timeout 5\n'
        '    assert eval (not renpy.loadable("audio/music/bgm_before_storm.ogg")) timeout 5\n'
        '    assert eval (not renpy.loadable("audio/ambience/amb_inn_wood_room.ogg")) timeout 5\n'
        '    screenshot "standalone_main_menu.png"\n', encoding='utf-8')
    saves = work / 'private_saves'
    saves.mkdir()
    source_saves = PROJECT / '03_開發/JingZhe/game/saves'
    original = {p.name: sha(p) for p in source_saves.glob('*') if p.is_file()}
    legacy = sorted(source_saves.glob('*.save'), key=lambda p: p.stat().st_mtime)[:2]
    for i, path in enumerate(legacy, 1):
        shutil.copy2(path, saves / ('legacy-' + str(i) + '-LT1.save'))
    runs = []
    for suite in ('jz_release_meta', 'jz_qa', 'lint'):
        output = HERE / 'release_checks_final' / suite
        output.mkdir(parents=True, exist_ok=False)
        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'
        env['JZ_RELEASE_BASE'] = str(package)
        env['JZ_QA_OUTPUT'] = str(output)
        if suite == 'lint':
            env.pop('RENPY_SEARCHPATH', None)
            command = [str(package / 'JingZhe.exe'), str(package), 'lint', str(output / 'lint.txt'), '--error-code', '--all-problems', '--check-unclosed-tags']
        else:
            env['RENPY_SEARCHPATH'] = str(tests)
            command = [str(package / 'JingZhe.exe'), str(package), 'test', suite, '--report-detailed']
        command += ['--savedir', str(saves)]
        startup = subprocess.STARTUPINFO()
        startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startup.wShowWindow = 0
        started = time.time()
        native_status = None
        with (output / 'console.txt').open('w', encoding='utf-8') as console:
            process = subprocess.Popen(command, env=env, stdout=console, stderr=subprocess.STDOUT, startupinfo=startup)
            deadline = time.monotonic() + 600
            while process.poll() is None:
                time.sleep(.5)
                log = (output / 'console.txt').read_text(encoding='utf-8', errors='replace')
                if '[rpytest] Status: PASSED' in log or '[rpytest] Status: FAILED' in log:
                    native_status = 'PASSED' if '[rpytest] Status: PASSED' in log else 'FAILED'
                    process.terminate()
                    break
                if time.monotonic() > deadline:
                    process.terminate()
                    native_status = 'TIMEOUT'
                    break
            process.wait(timeout=20)
        code = (0 if native_status == 'PASSED' else 1) if native_status else process.returncode
        for name in ('log.txt', 'errors.txt', 'traceback.txt'):
            path = package / name
            if path.exists() and path.stat().st_mtime >= started:
                shutil.copy2(path, output / name)
        result = {'suite': suite, 'exit_code': code, 'native_status': native_status,
                  'executable': str(package / 'JingZhe.exe'), 'command': command}
        (output / 'run.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False), flush=True)
        runs.append(result)
        if code != 0:
            raise RuntimeError('Standalone package check failed: ' + suite)
    assert original == {p.name: sha(p) for p in source_saves.glob('*') if p.is_file()}
    assert sha(archive) == build['sha256']
    result = {'version': '0.2.0', 'archive_sha256': build['sha256'], 'extraction_hashes_match': True,
              'verified_files': len(actual), 'actual_exe': str(package / 'JingZhe.exe'),
              'runs': runs, 'player_saves_unchanged': True, 'package_zip_unchanged': True,
              'all_passed': True}
    (HERE / 'release_check_result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
