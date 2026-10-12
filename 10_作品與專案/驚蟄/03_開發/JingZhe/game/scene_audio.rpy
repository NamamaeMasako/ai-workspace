# Continuous scene ambience is independent of music and one-shot story sounds.
# It shares the existing sfx mixer, so the sound-volume control covers both.
init python:
    renpy.music.register_channel("ambience", mixer="sfx", loop=True)
