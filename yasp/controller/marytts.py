####################################################################################################
#    Copyright (C) 2016 by Ingo Keller                                                             #
#    <brutusthetschiepel@gmail.com>                                                                #
####################################################################################################
from __future__ import print_function

import sys
import urllib


if sys.version_info[0] == 3:
    import io
    import urllib.request

else:
    import StringIO
    import urllib2

import audioop
import pyaudio
import wave


class MaryTTS(object):


    def __init__(self):
        self.speed       = 0.9
        self.chunk       = 1024                                 # define stream chunk
        self.locale      = 'en_GB' # 'de'
        self.voice       = 'dfki-poppy' # 'bits3'
        self.process_url = 'http://127.0.0.1:59125/process'


    def getData(self, values):
        return self.getData3(values) if sys.version_info[0] == 3 else  self.getData2(values)


    def getData2(self, values):
        data        = urllib.urlencode(values)  
        req         = urllib2.Request(self.process_url, data)
        try:
            response = urllib2.urlopen(req)
            return response.read()
        except:
            print('MaryTSS error occurred.')

    
    def getData3(self, values):
        details     = urllib.parse.urlencode(values)
        details     = details.encode('ascii')
        url         = urllib.request.Request(self.process_url, details)
        try:
            with urllib.request.urlopen(url) as response:
                return response.read()
        except:
            print('MaryTSS error occurred.')


    def say(self, text):
        self.play(self.getWaveFile(text))


    def play(self, data):
        """based on http://stackoverflow.com/questions/17657103/how-to-play-wav-file-in-python"""

        # open a wav format music
        f = wave.open(data, 'rb')

        # instantiate PyAudio
        p = pyaudio.PyAudio()
#        print(p.get_device_info_by_index(5).get('name'))

        # open stream
        stream = p.open(format   = p.get_format_from_width(f.getsampwidth()),
                        channels = f.getnchannels(),
                        rate     = 48000,
                        output   = True)#,
#                         output_device_index = 5)

        # read data
        data = f.readframes(self.chunk)

        # play stream
        while len(data) > 0:
            data, _ = audioop.ratecv(data, 2, 1, int(16000 * self.speed), 48000, None)
            stream.write(data)
            data = f.readframes(self.chunk)

        # stop stream
        stream.stop_stream()
        stream.close()

        # close PyAudio
        p.terminate()


    def getWaveFile(self, text):
        values = { 'INPUT_TYPE' :    'TEXT',
                   'AUDIO':          'WAVE_FILE',
                   'OUTPUT_TYPE':    'AUDIO',
                   'LOCALE':         self.locale,
                   'INPUT_TEXT':     text,
                   'VOICE':          self.voice }

        data = self.getData(values)
        if data:
            return io.BytesIO(data) if sys.version_info[0] == 3 else StringIO.StringIO(data)


    def storeSpeech(self, text, filename):
        with open(filename, 'w') as f:
            f.write(self.getWaveFile(text))


    def getRealisedDurations(self, text):
        values = { 'INPUT_TYPE' :    'TEXT',
                   'OUTPUT_TYPE':    'REALISED_DURATIONS',
                   'LOCALE':         self.locale,
                   'INPUT_TEXT':     text,
                   'VOICE':          self.voice }

        data = self.getData(values)
        if data:
            return data.decode('utf-8')
    
    
    def separateRealisedDurations(self, data):
        
        array     = []
        prev_time = 0.0
#        offset    = 0.0
        
        for line in data.split('\n'):
            
            if line.startswith('#') or not line:
                continue
        
            line       = line.split()
            start_time = float(line[0]) / self.speed

#            if line[2] == 'u':
#                offset_delay = 1
#            if line[2] == '_':
#                start_time += 0.3    
            line[0]    = start_time - prev_time
            prev_time  = start_time
    
            array.append(line)
#        array.append([0.1, '', '.'])
        return array


if __name__ == '__main__':
    m = MaryTTS()
    m.say('Return a tuple consisting of the minimum and maximum values of all samples in the sound fragment.')
