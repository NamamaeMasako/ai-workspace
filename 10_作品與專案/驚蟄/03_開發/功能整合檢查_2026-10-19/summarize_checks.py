"""Summarize the accepted native test runs, retaining their raw evidence."""
from pathlib import Path
import collections
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ACCEPTED = [
    '20261019_171300_jz_qa',
    '20261019_171028_jz_controls',
    '20261019_171028_jz_render_assets',
    '20261019_170904_jz_audio_decode',
    '20261019_171310_jz_prefs_write',
    '20261019_171320_jz_prefs_read',
    '20261019_171330_jz_replay_early_exit',
    '20261019_171424_lint',
]


def main():
    summary = {'runs': [], 'cases_passed': 0, 'assertions_passed': 0}
    for name in ACCEPTED:
        directory = HERE / 'results' / name
        run = json.loads((directory / 'run.json').read_text(encoding='utf-8'))
        text = (directory / 'console.txt').read_text(encoding='utf-8')
        cases = re.search(r'Test cases\s*:\s*\d+\s*\|\s*(\d+) passed', text)
        assertions = re.search(r'Assertions\s*:\s*\d+\s*\|\s*(\d+) passed', text)
        summary['cases_passed'] += int(cases[1]) if cases else 0
        summary['assertions_passed'] += int(assertions[1]) if assertions else 0
        summary['runs'].append({'directory': name, 'exit_code': run['exit_code'],
                                'native_status': run['native_status'],
                                'source_manifest_unchanged': run['source_manifest_unchanged']})
    events = [json.loads(line) for line in (HERE / 'results' / ACCEPTED[0] / 'events.jsonl').read_text(encoding='utf-8').splitlines()]
    summary['normal_labels'] = dict(collections.Counter(e['label'] for e in events if e['kind'] == 'label' and not e['replay']))
    summary['replay_labels'] = dict(collections.Counter(e['label'] for e in events if e['kind'] == 'label' and e['replay']))
    render_events = [json.loads(line) for line in (HERE / 'results' / ACCEPTED[2] / 'events.jsonl').read_text(encoding='utf-8').splitlines()]
    summary['rendered_images'] = next(len(e['names']) for e in render_events if e['kind'] == 'rendered_assets')
    audio_events = [json.loads(line) for line in (HERE / 'results' / ACCEPTED[3] / 'events.jsonl').read_text(encoding='utf-8').splitlines()]
    summary['loaded_audio_files'] = len([e for e in audio_events if e['kind'] == 'audio_decoded' and e['duration'] > 0])
    audit = json.loads((HERE / 'asset_audit.json').read_text(encoding='utf-8'))
    saves = HERE.parent / 'JingZhe' / 'game' / 'saves'
    after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in saves.glob('*') if p.is_file()}
    summary['player_saves_unchanged'] = after == audit['player_saves_before']
    summary['missing_required_assets'] = audit['missing_required']
    summary['all_passed'] = all(r['exit_code'] == 0 and r['source_manifest_unchanged'] for r in summary['runs']) and summary['player_saves_unchanged'] and not summary['missing_required_assets']
    (HERE / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in summary.items() if k not in ('runs', 'normal_labels', 'replay_labels')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
