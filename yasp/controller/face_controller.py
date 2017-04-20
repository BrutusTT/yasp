from __future__ import print_function

import yarp
import time

from yasp.controller.rpc_controller import RpcController
from yasp.controller.marytts        import MaryTTS


class FaceController(RpcController):
    """Class for controlling iCub face via its RPC port."""

    DISABLED_JOINTS = [1]


    def __init__(self):
        self._rpc_client, self._port_name = self._getClient("/icub/face/rpc:i")
        self.joint_limits = self._load_joint_limits()
        self.expressions  = self._load_expressions()
        self._setSpeed()


    def _setSpeed(self):
        for joint, speed in enumerate(self._load_joint_speeds()):
            self.setVelocity(joint, speed)


    def _load_joint_limits(self):
        
        # TODO: out-source to configuration file
        return [ [ 0,     25 ],
                 [ -160,   0 ],
                 [  -34,  34 ],
                 [  -40,   0 ],
                 [  -34,  34 ],
                 [    0,  17 ] ]


    def _load_joint_speeds(self):
        # TODO: out-source to configuration file
        return [ 50, 10, 90, 90, 90, 90 ]


    def _load_expressions(self):
        return { 'neutral':  [0.25, 0.00, 0.00, 0.00, 0.00, 0.00],
                 'smile':    [0.25, -14,  1.00, 0.00, 1.00, 0.30],
                 'sad':      [0.25, -50,  15,   0,  15,  0],
                 'surprise': [0.25,  10, -20, -20, -20, 28],
                 'bored':    [0.25,  10,   0, -40,   0, 28],
                 'emotionx': [0.25, -50,  34,   0,   1, 16],
                }


    def setPosition(self, joint, pos):
        if joint in FaceController.DISABLED_JOINTS:
            return False

        joint = int(joint)
        pos   = int(pos)
        limit = self.joint_limits[joint]

        assert( 0        <= joint <= 5 )
        assert( limit[0] <= pos   <=  limit[1] ), 'position[%s] exceeds the limit %s' % (pos, limit)

        bottle = yarp.Bottle()
        bottle.clear()

        bottle.addString("set")
        bottle.addString("pos")
        bottle.addInt(joint)
        bottle.addInt(pos)
        
        return self._is_success(self._execute(bottle))
        

    def setPercentage(self, joint, percent):
        limit = self.joint_limits[joint]
        pos   = int(limit[0] + ((limit[1] - limit[0]) * percent))
        return self.setPosition(joint, pos)


    def setVelocity(self, joint, vel):

        joint = int (joint)
        vel   = float(vel)

        assert(0    <= joint <= 5)
        assert(10.0 <= vel   <= 90.0)

        if joint in FaceController.DISABLED_JOINTS:
            return False

        bottle = yarp.Bottle()
        bottle.clear()

        bottle.addString("set")
        bottle.addString("vel")
        bottle.addInt(joint)
        bottle.addDouble(vel)
        
        return self._is_success(self._execute(bottle))
        

    def setExpression(self, expression):
        for idx, percent in enumerate(self.expressions.get(expression, ())):
            self.setPosition(idx, percent)



if __name__ == '__main__':
    yarp.Network.init()

    mu = MaryTTS()

    text  = 'Hello! My name is Nikita.'
    sound = mu.getWaveFile(text)
    data  = mu.separateRealisedDurations(mu.getRealisedDurations(text))
    face  = FaceController()

    pho2mou = {  #       L    U    R    D
                'h':    [0.5, 0,   0.5, 0.3],
                '@':    [0.5, 0,   0.5, 0.5],
                'l':    [0,   0,   0,   0.7],
                '@U':   [0,   0,   0,   0  ],
                'm':    [0,   0,   0,   0  ],
                'AI':   [0,   0,   0,   0  ],
                'n':    [0,   0,   0,   0  ],
                'EI':   [0,   0,   0,   0  ],
                'I':    [0,   0,   0,   0  ],
                'z':    [0,   0,   0,   0  ],
                'n':    [0,   0,   0,   0  ],
                'k':    [0,   0,   0,   0  ],
                'i':    [0,   0,   0,   0  ],
                't':    [0,   0,   0,   0  ],
                '_':    [0,   0,   0,   0  ],
               }

    time.sleep(1)

    face.setVelocity(3, 50.0)

    while True:
        time.sleep(.4)
        face.setPercentage(3, 0.1)
        time.sleep(.4)
        face.setPercentage(3, 1.0)


    yarp.Network.fini();
