# YASP - Yet Another Speech Package

YASP provides the MSpeak module which integrates MaryTTS and mouth movements for Lip Synchronization for the iCub robot.

## Installation

1- Install the dependencies:

You need Yarp installed with the python bindings. For more details see 
[full instructions](http://wiki.icub.org/yarpdoc/install.html).

Example: OSX using [Homebrew](http://brew.sh)

    brew tap homebrew/x11
    brew install --with-python yarp


Additional dependencies:

    MaryTTS server					[https://github.com/marytts/marytts-installer]
    NumPy
    PortAudio with Python bindings


2- Download the source code: 

    git clone https://github.com/BrutusTT/yasp

3- build and install:

    cd yasp
    python setup.py install


## Running YASP Module

Before the MSpeak module can be used the MaryTTS needs to be started. YASP provides basic start/stop scripts.

	$ startMary.sh
	$ stopMary.sh

The MSpeak module can be started via the command line (see below) or as a module from the yarp manager.

    $ MSpeak [--speed <float>] [--locale <string>] [--voice <string>] [--mary_ip <string>] [--mary_port <integer>]  [--disable_port_sync]

Parameters:

	--speed				- Speed of the voice given with a float (slower < 1.0 < faster)
	--locale			- Language for the voice (Default: en_GB)
	--voice				- voice name as given by the demo website dropdown (Default: )
	--mary_ip			- IP Address for MaryTTS-Server (Default: 127.0.0.1)
	--mary_port			- Port for the MaryTTS-Server (Default: 59125)
	--disable_port_sync	- If given the LED port will not be automatically reconnected to the iCub default face port

Example:

    $ MSpeak --mary_ip 10.0.0.1 --voice 


Happy hacking!

## License

See COPYING for licensing info.
