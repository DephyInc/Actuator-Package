FlexSEA Rigid USB Control in Python.

-------------------------------------------------
Description
-------------------------------------------------
Python scripts to demonstrate control of the FlexSEA Rigid electronic controller & motor.
These scripts are acompanied by and are dependent upon C based libraries for both Windows (.dll)
and for the Rasbian OS (.so)

These scripts are written in Python 3 and have been tested on Python verson 3.6 on both Windows
10 Pro and Rasbian

-------------------------------------------------
Contact Information
-------------------------------------------------
This was developed by Dephy Inc. Specifically by:
JF Duval, email: jduval@dephy.com
Justin Cechmanek, email: jcechmanek@dephy.com

-------------------------------------------------
Quick Installation and Setup
-------------------------------------------------
--Requirements:
Python version 3.X 32 bit
Pyserial version 3.4
STM32 Virtual Com Port Driver (for windows only)

----Windows only pre setup----
Install the Virtual Com Port driver to be able to connect to the STM32 chip on the FlexSEA.
Do this by running the application:
	VCP_V1.4.0_Setup.exe
Now go to the installation directory, which is most likely:
	C:\Program Files(x86)\STMicroelectronics\Software\Virtual comport driver\Win8
and run the application corresponding to your operating system:
	dpinst_amd64.exe for 64 bit windows
	dpinst_x86.exe for 32 bit windows

-----Windows and Rasbian setup-----
Connect the FlexSEA board to your computer via a usb cable using the micro usb connection
labelled 'Mn' mounted closest to the main processor.
Note: on Rigid 0.2 there is only 1 USB connector; it's the one you need.

Your computer should see the board and assign it a COM port number. Each Python script has a
'COM' variable defined near the top. Make sure this variable matches the COM number your 
computer assigned. 
For Windows this will be something like 'COM2', or 'COM3', or 'COM4', etc
For Rasbian this will probably be '/dev/ttyACM1' or '/dev/ttyACM0'

To power the motor connect the main power leads to a 20V power supply. Sensor readings will all
work even when the motor isn't powered, but any commands sent to move the motor won't work.
Note: the supported voltage range is 15-48V. 20V is a good, safe value for initial testing.

Run the Python script of your choice. A description of each script's behavior is given at the
top of each python file, as well as described in the documenation.


-------------------------------------------------
Detailed Installation and Setup for Windows
-------------------------------------------------

---Install Python version 3.x 32 bit(most current version is 3.6 as of this writing)---
Go to python.org/downloads and download a recent version if you don't already have it on your
computer. be sure to get the 32 bit distribution as the FlexSEA libraries are made for 32 bit.

follow the Python installer instructions and they should guide you through the process rather 
painlessly. Agree to have Python and its modules be added to your PATH

verify that python is installed and is on your PATH by typing:
	python --version
 from your command line terminal
you should see:
	>>> Python 3.6.1 :: (32-bit)
 or something similar.

---Install the Pyserial library---
Versions of Python 3.4 and later come with a built-in Python library installer called pip.
Assuming you agreed to have Python modules added to your PATH during installation you will now
be able to call pip directly from your terminal.

In your command terminal type:
	pip install pyserial

This starts the download and configuring process.

If pip is not on your PATH you can still call it from within a python session or script.
From your command terminal type:
	python -m pip install pyserial

more details can be found at:
https://pyserial.readthedocs.io/en/latest/index.html

---Install the Virtual Com Port driver---
In order for your computer to be able to connect to the STM32 chip you'll need the STM32 driver 
You can install this by running the application:
	VCP_V1.4.0_Setup.exe
which should be included with the files you received

Now go to the STMicroelectronics installation directory, which is most likely:
	C:\Program Files(x86)\STMicroelectronics\Software\Virtual comport driver\Win8
and run the application corresponding to your operating system:
	dpinst_amd64.exe for 64 bit windows
	dpinst_x86.exe for 32 bit windows
The install wizard will launch and guide you through their little process

---Connect FlexSEA to your computer---
Connect the FlexSEA board to your computer via a usb cable using the micro usb connection
labelled 'Mn' mounted closest to the main processor, not 'Ex' or 'Reg'.
Note: on Rigid 0.2 there is only 1 USB connector; it's the one you need.

Your computer should see the board and assign it a COM port number. Each Python script has a
'COM' variable defined near the top. Make sure this variable matches the COM number your 
computer assigned. 
For Windows this will be something like 'COM4', or 'COM5'. You can see your computer port names
using Windows Device Manager and checking the 'Ports (COM & LPT)' section.

To power the motor connect the main power leads to a 20V power supply. Sensor readings will all
work even when the motor isn't powered, but any commands sent to move the motor won't work.
Note: the supported voltage range is 15-48V. 20V is a good, safe value for initial testing.

---Run your first program---
Run the script FlexSEA_Demo_ReadOnly.py. If everything is working then you should be seeing
realtime readings from the FlexSEA board.

To start off with simple interaction with the FlexSEA you can run and modify 
FlexSEA_Demo_UserDefined.py, which currently defines two main functions, a main_loop_fuction()
that is executed every iteration and an exiting() function that is called once when you end the
program.

-------------------------------------------------
Detailed Installation and Setup for Raspbian
-------------------------------------------------

---Python3 32-bit
Raspbian comes pre-installed with Python versions 2.7.x and Python 3.x 32-bit. Because of 
potential name conflicts you have to specify the version you want each time you call it.
To specify starting a Python3 session type:
	python3
in your terminal

---Install the Pyserial library---
Versions of Python 3.4 and later come with a built-in Python library installer called pip.
You will be able to call pip directly from your terminal to install common python libraries.

unlike the Windows setup the default pip on raspbian is configured for version 2.7 so typing:
	pip install pyserial
will install for python 2.7 but not 3.x. This isn't what we want. Instead we can call it from
within a python 3 session. From your command terminal type:
	python3 -m pip install pyserial
This starts the download and configuring process.

more details can be found at:
https://pyserial.readthedocs.io/en/latest/index.html

---Connect FlexSEA to your computer---
Connect the FlexSEA board to your computer via a usb cable using the micro usb connection
labelled 'Mn' mounted closest to the main processor, not 'Ex' or 'Reg'. 

Your computer should see the board and assign it a COM port number. Each Python script has a
'COM' variable defined near the top. Make sure this variable matches the COM number your 
computer assigned. 
For Raspbian this will be something like '/dev/ttyACM0', or '/dev/ttyACM1'. You can see your 
computer port names by typing:
	ls /dev/tty*
with your FlexSEA board disconnected and then while connected to see which port is added.

To power the motor connect the main power leads to a 20V power supply. Sensor readings will all
work even when the motor isn't powered, but any commands sent to move the motor won't work.

---Run your first program---
Run the script FlexSEA_Demo_ReadOnly.py. If everything is working then you should be seeing
realtime readings from the FlexSEA board.

To start off with simple interaction with the FlexSEA you can run and modify 
FlexSEA_Demo_UserDefined.py, which currently defines two main functions, a main_loop_fuction()
that is executed every iteration and an exiting() function that is called once when you end the
program.
-------------------------------------------------
Trouble Shooting
-------------------------------------------------

"I can't connect to FlexSEA over usb"
this is probably one of three issues:
-you have the wrong python distribution. Check that it is version 3.4 or newer and 32-bit
-you have the wrong pyserial library. Check that you have the correct one for python 3, not 2
-you're trying to connect to the wrong COM port. Check that you are renaming the 'COM' variable
to the right port name, probably 'COM4' or 'COM5' for Windows, and '/dev/ttyACM0', or 
'/dev/ttyACM1' for Raspbian.

"the refresh rate on my scripts is fluctuating a lot"
-the refresh rate we are displaying is an estimate of how quickly the python script is running,
but it's not perfect. Especially at higher speeds it's more subject to error because of 
imprecision in your system's clock.

"there's some error about not finding or loading a library"
-there are two libraries sent in this package, a .dll for Windows and a .so for Unix/Rasbian.
In the script pyFlexSEA.py in the function initPyFLexSEA() one of two commands is being called:
flexsea = cdll.LoadLibrary('lib/FlexSEA-Stack-Plan') #Windows
or
flexsea = cdll.LoadLibrary('lib/libFlexSEA-Stack-Plan.so') #Unix/Raspbian
be sure to comment out the one you don't need, depending on your system

"I can't speed up the scripts beyond ~400 Hz"
-we can't either. sorry :(

"I have a problem that isn't one the four described here"
-send us an email :)
