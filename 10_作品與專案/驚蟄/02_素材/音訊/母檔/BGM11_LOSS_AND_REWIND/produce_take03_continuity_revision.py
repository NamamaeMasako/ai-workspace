"""Preserve the first take03 render and replace two auditions with excessive quiet gaps."""
import copy
import json

import produce_shorts_take03 as render


def main():
    manifest_path = render.OUT / 'generation_manifest_take03.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    render.save(render.OUT / 'generation_manifest_take03_initial.json', copy.deepcopy(manifest))
    revisions = [
        (0, (1, 'piano_strings_denial', 3831, '不可能是妳', 68,
             'A continuous quiet viola and cello suspension carries the whole cue while soft piano '
             'makes short rising two-note questions that never find an answer. The piano returns '
             'at least every two seconds, each phrase strained and unfinished. Connected audible '
             'string sustain fills every space between questions without increasing volume. '
             'Raw aching grief and disbelief, the instant a loved companion suddenly dies. '
             'Continuous musical presence, no silent middle section, no early ending.')),
        (2, (3, 'trembling_strings', 3833, '停在那一刻', 64,
             'A continuously sustained small viola and cello ensemble, soft quiet bow tremolo '
             'under an exposed fragile rising question. The strained upper suspension falls '
             'back a semitone and reaches upward again, always unresolved. Gentle connected '
             'bow changes keep audible musical tension throughout all 25 seconds without a '
             'silent break. Internal agitation and raw wounded sadness at low volume, '
             'stunned disbelief and desperate helplessness. No grand singing solo or procession.')),
    ]
    for index, spec in revisions:
        previous = manifest['candidates'][index]
        previous_path = render.OUT / (previous['ogg']['file'].removesuffix('.ogg') + '.json')
        previous['status'] = 'withheld_from_audition_long_near_silent_middle'
        previous['production_note'] = 'Replaced before user audition: quiet gap exceeded four seconds.'
        render.save(previous_path, previous)
        replacement = render.produce(spec)
        replacement['production_revision_of'] = previous['ogg']['file']
        replacement['production_reason'] = 'Keep quiet musical tension continuous under fragmented phrases.'
        render.save(render.OUT / (replacement['ogg']['file'].removesuffix('.ogg') + '.json'), replacement)
        manifest['candidates'][index] = replacement
        render.save(manifest_path, manifest)
    render.save(render.OUT / 'technical_measurements_take03.json', {
        'date': render.DATE,
        'files': [dict(file=r['ogg']['file'], **r['technical_measurements']) for r in manifest['candidates']],
    })


if __name__ == '__main__':
    main()
