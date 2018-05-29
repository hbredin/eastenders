# Eastenders pyannote.database plugin

## Installation

```bash
$ pip install pyannote.db.eastenders
```

## Eastenders.SpeakerDiarization.Subtitles

The following `pyannote.database` protocol can be used to iterate over each subtitle in the
provided XML files.

```python
>>> from pyannote.database import get_protocol
>>> protocol = get_protocol('Eastenders.SpeakerDiarization.Subtitles')
```

### File zero

```python
>>> file_zero = next(protocol.development())
>>> print(file_zero['uri'])
5082189274976367100

>>> turns = file_zero['annotation']
>>> subtitles = file_zero['subtitles']
>>> for turn, subtitle_id, color_id in turns.itertracks(yield_label=True):
...     print(turn.start, turn.end, subtitles[turn, subtitle_id])
...     break
2.489 3.063 I can do that.
```

In the above code snippet, `subtitle_id` (`int`) is a unique identifier for
each subtitle in the original XML file, and `subtitles` contains the actual
words.

Since each subtitle may contain speech from several speakers, a heuristic
(based on the `color_id` information available in `<span>` tags in the XML
files) is used to split each subtitle into several (hopefully
speaker-homogeneous) speech `turn`s. Their duration is estimated using the
number of characters.

### Test set

```python
>>> for test_file in protocol.test():
...     print(test_file['uri'])
...     turns = test_file['annotation']
...     subtitles = test_file['subtitles']
...     # do something smart
```

## Eastenders.SpeakerDiarization.Shots
