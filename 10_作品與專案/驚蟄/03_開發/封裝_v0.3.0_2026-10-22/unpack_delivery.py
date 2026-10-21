"""Extract the deliverable ZIP and record its file hashes before launch."""
from pathlib import Path
import hashlib
import json
import shutil
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def main():
    result = json.loads((HERE/'build_result.json').read_text(encoding='utf-8'))
    archive = Path(result['zip'])
    if sha(archive) != result['sha256']:
        raise RuntimeError('ZIP digest differs from the completed build')
    manifest = json.loads((PROJECT/'05_成品/JingZhe-0.3.0-win.manifest.json').read_text(encoding='utf-8'))
    work = Path(tempfile.mkdtemp(prefix='jz_delivery_030_'))
    with zipfile.ZipFile(archive) as source:
        source.extractall(work)
    package = work/Path(result['folder']).name
    files = {p.relative_to(package).as_posix():sha(p) for p in package.rglob('*') if p.is_file()}
    if set(files) != set(manifest['files']):
        raise RuntimeError('Extracted paths differ from the package manifest')
    for name, digest in files.items():
        if digest != manifest['files'][name]['sha256']:
            raise RuntimeError('Extracted file digest mismatch: '+name)
    saves = work/'private_saves'
    saves.mkdir()
    # Use a copy of the existing completion record for the local presentation.
    # Never write to the player's source saves or the pristine release folder.
    persistent = PROJECT/'03_開發/JingZhe/game/saves/persistent'
    copied = False
    if persistent.is_file():
        shutil.copy2(persistent,saves/'persistent')
        copied = True
    receipt = {'version':'0.3.0', 'package':str(package), 'private_saves':str(saves),
        'zip_sha256':result['sha256'], 'matched_files':len(files),
        'all_paths_and_sha_match':True, 'copied_completion_record':copied,
        'source_persistent_sha256':sha(persistent) if copied else None,
        'automated_test_suite_run':False}
    (HERE/'delivery_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,ensure_ascii=False))


if __name__ == '__main__':
    main()
