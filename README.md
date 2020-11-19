# Piode
One way transfer of data using two raspberry pi and a usb switch.

## Introduction

### Background
This is by no means the only way, and most likely not the best way, to perform this operation. This project was made as an experiment and a proof of concept.

### Future
Feel free to continue to develop and modify the project, we will leave it here in case it is useful to someone, in whole or part.

### Documentation

#### Overview
The project consists of two Raspberry Pi (in our case version 3), and one USB switch. When a condition is met on the first Raspberry Pi (called 'inside') any files in a designated folder are transferred to a USB flashdrive mounted in the USB switch. The switch is then switched so that the USB flashdrive is instead connected to the second Raspberry Pi (called 'outside'), where the content is handled according to some simple rules.

The Raspberry Pi's chosen for this proof of concept is not suited for a production environment. The SD cards are not suited for continuous R/W and the wireless connections can be a security issue if they are not a wanted feature. Please send your suggestions for a more appropriate embedded computer to this project. 


#### Parts
- Rapberry Pi 3 x2
- RPI LCD1602 Add-on x2
- Startech 2 Port 2-to-1 USB 3.0 Peripheral Sharing Switch (Manufacturers product id: USB221SS)
- USB A to B cable x2
- Dupont cable female-to-male x2
- USB Flashdrive

#### Connections
Be careful while soldering this. If you make a mistake it is likely to damage the parts. 

![alt text](https://github.com/VanDerGroot/piode/blob/main/connection%20sketch.png "Diagram")

- The LCD modules are attached to the Raspberry Pis as described in the modules documentation.
- USB cables are connected from each Raspberry Pi to the USB switch.
- USB flashdrive is connected to device side of USB switch.
- Dupont cables female end are connected to GPIO26 on both Raspberry Pis.
- Dupont cables male end is soldered to the pad on each button that gets pulled low when the button is pressed.

#### Functional description

![alt text](https://github.com/VanDerGroot/piode/blob/main/event_flowchart.png "Flowchart")


#### Installation
Make install.sh an executable file, and then run it.

### Who and why
#### Who
This project was thought up and led by Markus Dahlberg and programmed by Jim Groth

#### Why
To make a DIY poor man's data diode, that with a small investment can keep two information systems "almost" physically separated and ensure unidirectional data flows. 


