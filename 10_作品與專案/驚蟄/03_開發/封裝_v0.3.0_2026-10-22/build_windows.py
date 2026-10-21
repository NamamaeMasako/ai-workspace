"""Build Windows distribution from current game and the existing Ren'Py runtime."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SOURCE = PROJECT / '03_開發' / 'JingZhe' / 'game'
RUNTIME = PROJECT / '05_成品' / '驚蟄_v0.1.2_Windows'
VERSION = '0.3.0'
OUTPUT = PROJECT / '05_成品'
FOLDER = '驚蟄_v' + VERSION + '_Windows'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def pattern_regex(pattern):
    parts = []
    i = 0
    while i < len(pattern):
        if pattern[i:i+2] == '**':
            parts.append('.*')
            i += 2
        elif pattern[i] == '*':
            parts.append('[^/]*')
            i += 1
        elif pattern[i] == '?':
            parts.append('[^/]')
            i += 1
        else:
            parts.append(re.escape(pattern[i]))
            i += 1
    return re.compile('^' + ''.join(parts) + '$', re.IGNORECASE)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--replace-draft', action='store_true')
    args = parser.parse_args()
    destination = OUTPUT / FOLDER
    archive = OUTPUT / ('JingZhe-' + VERSION + '-win.zip')
    if (destination.exists() or archive.exists()) and not args.replace_draft:
        raise RuntimeError('Refusing to overwrite an existing release.')
    if args.replace_draft:
        # Preserve the rejected draft before replacing generated output files.
        backup = HERE / 'draft1'
        backup.mkdir(exist_ok=False)
        for path in (archive, OUTPUT / ('JingZhe-' + VERSION + '-win.manifest.json'),
                     OUTPUT / ('JingZhe-' + VERSION + '-win.sha256.txt'), HERE / 'build_result.json'):
            if path.exists():
                shutil.copy2(path, backup / path.name)
    if 'define config.version = "' + VERSION + '"' not in (SOURCE / 'options.rpy').read_text(encoding='utf-8'):
        raise RuntimeError('Source version does not match release version.')
    work = Path(tempfile.mkdtemp(prefix='jz_release_030_'))
    game = work / 'game'
    print(json.dumps({'work': str(work), 'destination': str(destination)}, ensure_ascii=False), flush=True)
    shutil.copytree(SOURCE, game, ignore=shutil.ignore_patterns('saves', 'cache', '__pycache__', '*.rpyc', '*.rpyb', '*.pyc', '*.bak', '*.tmp', '*.old', '*.new'))
    source_manifest = {p.relative_to(game).as_posix(): sha(p) for p in game.rglob('*') if p.is_file()}
    exe = RUNTIME / 'lib' / 'py3-windows-x86_64' / 'python.exe'
    dump_path = work / 'build_dump.json'
    command = [str(exe), str(RUNTIME / 'JingZhe.py'), str(work), 'compile', '--keep-orphan-rpyc', '--json-dump', str(dump_path), '--savedir', str(work / 'private_saves')]
    env = os.environ.copy()
    env.pop('RENPY_SEARCHPATH', None)
    env['PYTHONUTF8'] = '1'
    with (HERE / 'compile_console.txt').open('w', encoding='utf-8') as log:
        subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=180)
    build = json.loads(dump_path.read_text(encoding='utf-8'))['build']
    (HERE / 'build_rules.json').write_text(json.dumps(build, ensure_ascii=False, indent=2), encoding='utf-8')
    patterns = [(pattern_regex(p), groups, p) for p, groups in build['base_patterns']]

    def classification(name):
        for regex, groups, pattern in patterns:
            if regex.fullmatch(name):
                return groups, pattern
        return None, '<unclassified>'

    def allowed(relative):
        if relative.parts[0] in ('saves', 'cache', '__pycache__'):
            return False, 'private or generated data'
        for parent in relative.parents:
            if str(parent) != '.':
                groups, pattern = classification('game/' + parent.as_posix() + '/')
                if groups is None:
                    return False, pattern
        groups, pattern = classification('game/' + relative.as_posix())
        return groups is not None and bool(set(groups) & {'all', 'windows', 'windows_i686'}), pattern

    destination.mkdir(exist_ok=args.replace_draft)
    for name in ('JingZhe.exe', 'JingZhe.py'):
        shutil.copy2(RUNTIME / name, destination / name)
    for name in ('lib', 'renpy'):
        shutil.copytree(RUNTIME / name, destination / name, dirs_exist_ok=args.replace_draft)
    selected = []
    excluded = []
    for path in sorted(game.rglob('*')):
        if not path.is_file():
            continue
        relative = path.relative_to(game)
        include, rule = allowed(relative)
        if not include:
            excluded.append({'path': relative.as_posix(), 'rule': rule})
            continue
        target = destination / 'game' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        selected.append(relative.as_posix())
    profiles = json.loads((destination / 'game/character_profiles.json').read_text(encoding='utf-8'))
    assert len(profiles) == 12
    assert sum(len(p['portraits']) for p in profiles) == 69
    for profile in profiles:
        for portrait in profile['portraits']:
            assert (destination / 'game' / portrait['src']).is_file(), portrait['src']
            for head in portrait.get('variants', []):
                assert (destination / 'game' / head['src']).is_file(), head['src']
    assert (destination / 'game/character_profiles.rpyc').is_file()
    assert any(p.endswith('script.rpyc') for p in selected)
    assert (destination / 'game/NotoSansTC-VF.ttf').is_file()
    assert (destination / 'game/THIRD_PARTY_LICENSES.txt').is_file()
    assert len(list((destination / 'game/audio/music').glob('*.ogg'))) == 14
    assert len(list((destination / 'game/audio/sfx').rglob('*.ogg'))) == 52
    for p in destination.rglob('*'):
        if p.is_file() and p.relative_to(destination).parts[0] == 'game':
            assert not any(part in ('cache', 'saves') for part in p.relative_to(destination).parts)
            assert not p.name.endswith(('.bak', '.save'))
    (destination / '遊玩說明.txt').write_text(
        '《驚蟄》v0.3.0 Windows 獨立版\n\n'
        '雙擊 JingZhe.exe 開始遊玩。無需另裝Ren\'Py或Python。\n'
        '分享時請傳送完整ZIP，解壓縮後再執行；不要只複製exe。\n\n'
        '本版包含完整BGM與音效、章名卡、通關後章節回看、閱讀設定、存檔章名及結局完成畫面。\n'
        '新增通關後人物介紹：12位人物介紹與逸聞，60張劇情立繪、9張彩蛋及3組附屬頭部差分。\n'
        '人物頁可左右切圖、放大檢視；所有內容於看過完整結局後一起開放。\n'
        '字級以原始大小為最大；快轉相關選項預設關閉、轉場效果預設開啟。\n\n'
        '本包不含任何玩家存檔或通關紀錄。若要沿用舊版進度，先備份，\n'
        '再將舊版game/saves內容複製至本版game/saves。舊的空白存檔名稱不會自動回填；\n'
        '讀取後到下一個章節或分歧標記再存檔，便會帶入名稱。\n\n'
        '製作名單見遊戲結尾與關於頁；字型授權見game/THIRD_PARTY_LICENSES.txt，\n'
        '引擎授權見renpy/LICENSE.txt。\n\n建置日期：2026-10-22\n', encoding='utf-8')
    files = {p.relative_to(destination).as_posix(): {'bytes': p.stat().st_size, 'sha256': sha(p)} for p in sorted(destination.rglob('*')) if p.is_file()}
    expected = {'JingZhe.exe', 'JingZhe.py', '遊玩說明.txt'}
    expected.update('game/' + name for name in selected)
    for name in ('lib', 'renpy'):
        expected.update(name + '/' + p.relative_to(RUNTIME / name).as_posix() for p in (RUNTIME / name).rglob('*') if p.is_file())
    assert set(files) == expected, 'Unexpected leftover file in draft output'
    assert all(sha(SOURCE / name) == value for name, value in source_manifest.items())
    manifest = {'version': VERSION, 'date': datetime.date.today().isoformat(), 'runtime_source': '驚蟄_v0.1.2_Windows',
                'source_game_sha256': source_manifest, 'included_game_files': selected, 'excluded_game_files': excluded,
                'files': files, 'launcher_sha256': sha(destination / 'JingZhe.exe'), 'source_unchanged': True}
    manifest_path = OUTPUT / ('JingZhe-' + VERSION + '-win.manifest.json')
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    with zipfile.ZipFile(archive, 'w' if args.replace_draft else 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for path in sorted(destination.rglob('*')):
            if path.is_file():
                z.write(path, FOLDER + '/' + path.relative_to(destination).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(files)
    checksum = sha(archive)
    (OUTPUT / ('JingZhe-' + VERSION + '-win.sha256.txt')).write_text(checksum + '  ' + archive.name + '\n', encoding='utf-8')
    result = {'version': VERSION, 'folder': str(destination), 'zip': str(archive), 'zip_bytes': archive.stat().st_size,
              'sha256': checksum, 'file_count': len(files), 'game_file_count': len(selected), 'excluded': len(excluded), 'zip_crc_ok': True}
    (HERE / 'build_result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
