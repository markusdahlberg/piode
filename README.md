# Piode
One way transfer of data using two raspberry pi and a usb switch.

## Introduction

### Background
This is by no means the only way, and most likely not the best way, to perform this operation. This project was made as an experiment that grew into the current state.

### Future
We won't be putting any more time into this project, but we leave it here in case it is useful to someone, in whole or part.

### Documentation

#### Overview
The project consists of two Raspberry Pi (in our case version 3), and one USB switch. When a condition is met on the first Raspberry Pi (called 'inside') any files in a designated folder are transferred to a USB flashdrive mounted in the USB switch. The switch is then switched so that the USB flashdrive is instead connected to the second Raspberry Pi (called 'outside'), where the content is handled according to some simple rules.

#### Parts
- Rapberry Pi 3 x2
- RPI LCD1602 Add-on x2
- Startech 2 Port 2-to-1 USB 3.0 Peripheral Sharing Switch (Manufacturers product id: USB221SS)
- USB A to B cable x2
- Dupont cable female-to-male x2
- USB Flashdrive

#### Connections
Before attempting this, make sure you know what you are doing, and that this is likely to damage the parts if done incorrectly. See the [this diagram](https://github.com/VanDerGroot/piode/blob/main/connection%20sketch.png) for more details.
- The LCD modules are attatched to the Raspberry Pis as described in the modules documentation.
- USB cables are connected from each Raspberry Pi to the USB switch.
- USB flashdrive is connected to device side of USB switch.
- Dupont cables female end are connected to GPIO26 on both Raspberry Pis.
- Dupont cables male end is soldered to the pad on each button that gets pulled low when the button is pressed.

#### Installation
Make install.sh an executable file, and then run it.

### Who and why
#### Who
This project was thought up and led by Markus Dahlberg and programmed by Jim Groth

#### Why
