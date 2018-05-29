#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2017-2018 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


import gzip
import pandas as pd
from pathlib import Path
from pyannote.core import Segment
from pyannote.core import Annotation
from pyannote.database import Database
from pyannote.database.protocol import SpeakerDiarizationProtocol


class Subtitles(SpeakerDiarizationProtocol):
    """TRECVID protocols"""

    def _subset(self, subset):

        path = Path(__file__).parent / 'data' / f'subtitles.{subset}.txt.gz'
        names = ['uri', 'start', 'stop', 'track', 'label', 'subtitle']
        with gzip.open(path, 'rb') as fp:
            data = pd.read_table(fp, sep="|", names=names,
                                 converters={'uri': str})

        for uri, datum in data.groupby('uri'):

            annotation = Annotation(uri=uri, modality='subtitles')
            subtitles = dict()
            for _, row in datum.iterrows():
                segment = Segment(row.start, row.stop)
                annotation[segment, row.track] = row.label
                subtitles[segment, row.track] = row.subtitle

            current_file = {
                'database': 'Eastenders',
                'uri': uri,
                'annotation': annotation,
                'subtitles': subtitles}

            yield current_file

    def dev_iter(self):
        return self._subset('dev')

    def tst_iter(self):
        return self._subset('tst')


class Shots(SpeakerDiarizationProtocol):
    """TRECVID protocols"""

    def _subset(self, subset):

        path = Path(__file__).parent / 'data' / f'shots.{subset}.txt.gz'
        names = ['uri', 'start', 'stop', 'shot_id']
        with gzip.open(path, 'rb') as fp:
            data = pd.read_table(fp, delim_whitespace=True, names=names,
                                 converters={'uri': str})

        for uri, datum in data.groupby('uri'):

            annotation = Annotation(uri=uri, modality='shots')
            for _, row in datum.iterrows():
                segment = Segment(row.start, row.stop)
                annotation[segment, row.shot_id] = 'shot'

            current_file = {
                'database': 'Eastenders',
                'uri': uri,
                'annotation': annotation}

            yield current_file

    def dev_iter(self):
        return self._subset('dev')

    def tst_iter(self):
        return self._subset('tst')


class Eastenders(Database):
    """Eastenders database"""

    def __init__(self, preprocessors={}, **kwargs):
        super(Eastenders, self).__init__(preprocessors=preprocessors, **kwargs)
        self.register_protocol('SpeakerDiarization', 'Subtitles', Subtitles)
        self.register_protocol('SpeakerDiarization', 'Shots', Shots)
