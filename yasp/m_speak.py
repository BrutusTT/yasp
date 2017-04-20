from __future__ import print_function
import threading
import time

from yasp.base_module                   import BaseModule
from yasp.controller.marytts            import MaryTTS
from yasp.controller.face_controller    import FaceController

pho2mou = {  #       J    E      L     U     R     D
            'A':    [.2,   .9,   .5,    0,   .5,    1  ],
            'O':    [.2,   .9,   .5,    1,   .5,   .7  ],
            'u':    [.2,   .9,   .3,   .1,   .3,   .4  ],
            'i':    [.2,   .9,   .9,   .4,   .9,   .3  ],
            '{':    [.2,   .9,   .7,   .3,   .7,   .8  ],
            'V':    [.2,   .9,   .9,   .6,   .9,   .8  ],
            'E':    [.2,   .9,   .9,   .6,   .9,   .8  ],
            'I':    [.2,   .9,   .9,   .4,   .9,   .3  ],
            'U':    [.2,   .9,   .7,   .3,   .7,   .8  ],
            '@':    [.2,   .9,   .9,   .4,   .9,   .8  ],
            'r=':   [.2,   .9,   .3,   .8,   .3,   .1  ],
            'aU':   [.2,   .9,   .5,    0,   .5,   .4  ],
            'OI':   [.2,   .9,   .3,   .1,   .3,   .2  ],
            '@U':   [.7,   .9,   .5,   .3,   .5,    1  ],
            'EI':   [.2,   .9,    1,   .4,    1,   .3  ],
            'AI':   [.2,   .9,   .9,   .4,   .9,   .3  ],
            'p':    [.2,   .9,   .5,    0,   .5,    0  ],
            't':    [.2,   .9,    1,    .5,   1,   .3  ],
            'k':    [],
            'b':    [.2,   .9,   .5,    0,   .5,    0  ],
            'd':    [.2,   .9,    1,   .5,    1,   .5  ],
            'g':    [.2,   .9,    1,   .5,    1,   .3  ],
            'tS':   [.2,   .9,   .4,   .6,   .4,   .3  ],
            'dZ':   [.2,   .9,   .4,   .6,   .4,   .3  ],
            'f':    [.2,   .9,   .5,   .1,   .5,    0  ],
            'v':    [.2,   .9,   .5,   .1,   .5,    0  ],
            'T':    [.2,   .9,    1,   .5,    1,   .3  ],
            'D':    [.2,   .9,    1,   .5,    1,   .3  ],
            's':    [.2,   .9,    1,   .5,    1,   .3  ],
            'z':    [.2,   .9,    1,   .5,    1,   .3  ],
            'S':    [.2,   .9,    1,   .5,    1,   .3  ],
            'Z':    [.2,   .9,    1,   .5,    1,   .3  ],
            'h':    [.7,   .9,   .5,    0,   .5,    1  ],
            'l':    [.2,   .9,   .9,   .7,   .9,   .3  ],
            'm':    [.2,   .9,   .6,    0,   .6,    0  ],
            'n':    [.2,   .9,    1,   .5,    1,   .3  ],
            'N':    [.2,   .9,    1,   .5,    1,   .3  ],
            'r':    [.2,   .9,   .3,   .2,   .3,   .1  ],
            'w':    [.2,   .9,   .5,    0,   .5,   .1  ],
            'j':    [.2,   .9,    1,   .6,    1,   .3  ],
            '_':    [],
            '.':    [.2,   .9,   .5,    0,   .5,    0  ],
}

class MSpeak(BaseModule):

    AUTHORS    = ( ('Ingo Keller', 'brutusthetschiepel@gmail.com'), ) 
    ENABLE_RPC = True

    PORTS = [
        
              # Text
              # Message: String
              ('input',  'text',              'buffered'),
              
             ]


    def configure(self, rf):
        BaseModule.configure(self, rf)

        self.tts  = MaryTTS()
        self.face = FaceController()

        # configure stuff
#        rf.get('speed')

        return True

    
    def updateModule(self):

        bottle = self.inputPort['text'].read()

        if bottle:
            self.onText(bottle.toString())

        return True


    def onText(self, text):
        assert isinstance(text, type(''))

        for say in text.split('.'):
            
            if say:
                say += '.'
                self.wave      = self.tts.getWaveFile(say)
                self.durations = self.tts.getRealisedDurations(say)
                self.data      = self.tts.separateRealisedDurations(self.durations)
                thread_speech  = threading.Thread(target = self.speak)
                thread_motion  = threading.Thread(target = self.move)
        
                # start both threads
                print("start say_proc")
                thread_speech.start()
        
                print("motion_proc")
                thread_motion.start()
                
                total_time = 0.0
                for x in self.data:
                    total_time += float(x[0]) / self.tts.speed
             
                print('total time ', total_time)
                time.sleep(total_time)
 
            else:
                time.sleep(0.1)


    def speak(self):
        self.tts.play(self.wave)


    def move(self):
        print('repeat after me: ')
        for x in [row for row in self.data if len(row) > 2]:
            start  = time.time()

            for idx, percent in enumerate(pho2mou.get(x[2], [])):
                self.face.setPercentage(idx, percent)

            print(x[2], x[0])

            x[0] = x[0] * self.tts.speed 
            diff = x[0] - (time.time() - start)
            if diff > 0:
                time.sleep(diff)

        self.face.setExpression('neutral')


    def respond(self, cmd, reply):

        success = False
        command = cmd.toString().split(' ')

        if command[0] == 'set':

            if command[1] == 'speed':

                print(command)
                self.tts.speed = cmd.get(2).asDouble()

                success = True

        elif command[0] == 'get':

            if command[1] == 'speed':

                print('speed ', self.tts.speed)
                success = True

        reply.addString('ack' if success else 'nack')
        return True


if __name__ == '__main__':
    MSpeak.main(MSpeak)
