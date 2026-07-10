## 1. Introduction

## Installing Virtall and portable version for Windows

To install Virtaal you can go to the following site: https://virtaal.translatehouse.org/download.html

I have prepared a portable version of Virtaal for Windows. Portable means that you can download and run the virtaal.exe program form the unzipped folder without need of installing it. You can download the portable version here: https://github.com/mtuoc/VirtaalPortable/releases/tag/0.7.1

## Configuration files


The first time you run the program several configuration files are created. These configuration files are necessary to set up some features of the program. When I started the Windows Portable version the configuration files where created at: C:\Users\USER\AppData\Roaming\Virtaal where USER is the actual user name. Please, note that by default this folder is hidden so to see it in the File Browser you should set Hidden files to be visible. 

You will see the following configuration files:

virtaal.ini

plugins.ini

terminology.ini

tm.ini

weblook.ini

## Configuration of a MTUOC MT system using the Moses protocol

Virtaal is not directly compatible with the MTUOC-server, but the nice thing of MTUOC-server is that it can be stated simulatin other server's protocols. So, if we start a MTUOC-server selecting the Moses protocol (in config-server.yaml change MTUOCServer-type to Moses). Start the MTUOC-server and then you'll be able to connect with Virtaal and automatically retrieve the machine translated segments.

Now edit the tm.ini config file of Virtaal and add the following information:

```
[moses]
fr->en = http://localhost:8080
en->ca = http://192.168.0.139:8000/
```

The fr->en is sometimes present by default. In our case we are translating from en to ca (change the languages to match your project) and the server is started in a computer with IP 192.168.0.139 and in the port 8000.

Now in Virtaal go to Edit > Preferences > Connectors and select Translation Memory and Config. Make sure Moses is selected there. 