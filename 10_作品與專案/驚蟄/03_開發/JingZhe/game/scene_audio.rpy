# The user retired continuous non-BGM ambience on 2026-10-12.
# Keep the channel registered for compatibility with earlier saves.
init python:
    renpy.music.register_channel("ambience", mixer="sfx", loop=False)

    def _zh_clear_retired_ambience():
        renpy.music.stop(channel="ambience")
        renpy.music.set_volume(0.0, channel="ambience")

    config.interact_callbacks.append(_zh_clear_retired_ambience)
    config.after_load_callbacks.append(_zh_clear_retired_ambience)
