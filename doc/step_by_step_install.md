# Step-By-Step Installation Guide

The YASP package uses two main components in order to create the lip synchronization for the iCub.

It uses the MaryTTS server to create a the utterances and to retrieve the duration of each phoneme which is translated by the MSpeak module into motor control commands. The MSpeak module is also responsible for a synchronized start of the audio and motor commands.

In principle MaryTTS can be installed on any computer that is accessible through HTTP. However, the MSpeak module needs to run from the computer that has a speaker connected. It can runned either on the head directly (given the dependencies are installed) or from any computer but this one needs to have the speakers attached then. 

Also stay away from speakers connected via bluetooth as the bluetooth stack will introduce a small latency before audio is started. This is usually around 200-500ms but it desynchronizes the visual and the audio cue.

## Dependencies

### MaryTTS

Prerequisits: working Java installation

	git clone https://github.com/marytts/marytts-installer.git
	cd marytts-installer
	./marytts install:*
	./marytts
	
1. Clones marytts from github into the current directory
2. Enters marytts freshly cloned repo directory
3. Installs all marytts dependencies including all voices. This might take a while. If you are only interested in specific voices you can replace the * with them.
4. Runs marytts as a server. To check if it runs properly visit http://127.0.0.1:59125 It should show you the MaryTTS online demo page.

### numpy and pyaudio

Usually the yasp package installs both libraries during its setup step. However, if you run into trouble with it you also can install them yourself by running the following command.

	pip install numpy pyaudio

### YARP

The full install instructions for yarp can be found here: http://www.yarp.it/install.html

The YASP package is written in Python which means the Python bindings need to be compiled for YARP.

## Installing YASP

	git clone https://github.com/BrutusTT/yasp
	cd yasp
	python setup.py install

1. Clones YASP from github into the current directory
2. Enters YASP's freshly cloned repo directory
3. Installs YASP and its Python dependencies.

If you are using Python2 you need to manually change MSpeak executable. To find it run the following command.

	which MSpeak
	
Open the file and replace python3 with python. Thats it. From now on you can start the MSpeak module by just typing MSpeak in the command line. For more information about how to run it see the README.md