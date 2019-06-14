<!-- LICENSE NOTICE

charcoalAPI - IoT server-less API for Edge devices
Copyright (C) 2019 Anwesh Anjan Patel

This file is part of charcoalAPI.

charcoalAPI is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

charcoalAPI is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with charcoalAPI.  If not, see <https://www.gnu.org/licenses/>. -->

# Getting the Raspberry Pi Zero W ready for USN

This module takes you through the preparation of a Raspberry Pi Zero W (From scratch) for the USN usage. The [pre-configured image of Raspbian](https://www.amazon.com/clouddrive/share/P34CYAXKtVjNlBf7Ht3rXYsOBvjIQsxoN6T8soMV6w9) is available for quick install as well. You may prep the device using this image of Raspbian in section [2](#flash) and [3](#ssh) and then skip to section [6](#deploy) of this module if you choose that (look for quick install alerts).

#### Table of contents
1. [About the Raspberry Pi Zero W](#about)
2. [Flashing the SD Card](#flash)
3. [SSH into the Raspberry Pi and Headless Ops](#ssh)
4. [Docker Container Engine](#docker-1)
	1. [System Update](#sys-up)
	2. [Docker install](#docker-2)
	3. [Verify docker installation](#verify-1)
	4. [Exclude docker-ce from futher upgrades](#hold)
5. [Post installation steps](#post)
6. [Deployment set-up](#deploy)
	1. [Changing Hostname](#host)
	2. [Changing WiFi credentials](#wifi)
	3. [Docker Swarm](#swarm)

<a name="about"></a>

## About the Raspberry Pi Zero W

The Raspberry Pi Zero is a compact version of the Raspbery Pi models, based on an ARMv7 microprocessor chip. The specs given are:-

Sl. No. | Parameters | Remarks
--- | --- | ---
1 | CPU Shares | 1
2 | Architecture | ARMv6l
3 | CPU Clock speed | 1 GHz
4 | RAM (On Board) | 512MiB
5 | OS | Linux (Raspbian Lite with Docker)
6 | USB | Micro (B Type) with OTG
7 | Power | Micro USB point
8 | Steady Supply | 5V 220mA
9 | GPIOs | 28 Pins
10 | Memory Volume Support | 64 GiB (FAT)
11 | Display | Mini HDMI
12 | Camera | OV Cam

<a name = "flash"></a>

## Flashing the SD Card

In order to efficiently run all the functionalities of the USN moodule, we require a MicroSD of minimum 8 GiB, (recomended 16 GiB). Ensure the card is formatted and can be in any volume format. Follow the steps as given below:-

1. In order to flash the SD with the required OS, you must download the latest version of [Raspbian (Stretch) Lite](https://www.raspberrypi.org/downloads/raspbian/) **(Do NOT install NOOBS!)**.

2. Download and install balenaEtcher (Standard flashing software for USN)
	- **Linux Users** Follow one of the options
		1. Use App Image. Download [here](https://www.balena.io/etcher/), exctract it and move it to the ```/opt``` directory. (Installation for new users)

		2. Use ```.deb``` debian or ```.rpm``` RHEL packages and install using the following commands (Professional users, stable):-
		 
		 Debian Based
		 ```BASH
		 $ echo "deb https://deb.etcher.io stable etcher" | sudo tee /etc/apt/sources.list.d/balena-etcher.list

		 $ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 379CE192D401AB61

		 $ sudo apt-get update
		 $ sudo apt-get install balena-etcher-electron
		 ```

		 Red Hat
		 ```BASH
		 $ sudo wget https://balena.io/etcher/static/etcher-rpm.repo -O /etc/yum.repos.d/etcher-rpm.repo

		 $ sudo yum install -y balena-etcher-electron #RHEL and CentOS

		 $ sudo dnf install -y balena-etcher-electron #Fedora
		 ```
	- **Windows Users** Can download the latest installer [here](https://www.balena.io/etcher/)
	- **MacOS Users** Can download the AppImage [here](https://www.balena.io/etcher/)

3. Insert the SD card using an Adapter and etch the SD card using balenaEtcher. Select the Raspbian Image and the drive and flash.

4. Open a terminal window (or CMD) and create two new files on the ```boot``` partition of the freshly etched SD card. You can use one of the following based on your OS.

Linux and Mac
```BASH
$ touch ssh

$ touch wpa_supplicant.conf
```

Windows
```CMD
null > ssh

null > wpa_supplicant.conf
```

5. Open the ```wpa_supplicant.conf``` on a standard text editor and provide the following:-

```CONF
country=IN
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="your_wifi_ssid"
    scan_ssid=1
    psk="your_wifi_password"
    key_mgmt=WPA-PSK
}
```

6. Save the ```wpa_supplicant.conf``` and **safely eject the SD card**.

7. Place the SD card into the Pi's SD card slot and wait for 2-3 mins for it to perform initial setup.

**For the users intending to use the Raspberries in a cluster, it is recomended to change the hostname as mentioned [here](#host).**

<a name="ssh"></a>

## SSH into the Raspberry Pi and Headless Ops

THe most efficient way to work with a "Server" is to access it through a Secure Shell, SSH. Linux users have a built-in support for ssh on the BASH terminal. Windows users must install PuTTY SSH Client or similar softwares. Once done, follow the steps to operate the Pi.

1. Ping to the Pi to locate it in the network.
```BASH
ping raspberrypi.local #Same for both BASH and CMD
```

The hostname ```raspberrypi``` is set by default. It is recomended to change the hostname as per the directions given in section [6](#deploy) below, as USN is a serverless network system with many Pis in a cluster-like network. Thus, having different hostnames is neccessary.

>**Quick Install Alert!**
>
>If you are going through a quick install using the pre-configured flavour of Raspbian, you need to enter the following command instead to locate your device. This is because the hostname is set to ```pi0``` instead of ```raspbian``` in the USN image of raspbian.
>```BASH
>ping pi0.local
>```

2. **On Linux/Mac BASH**
```BASH
$ ssh pi@<ip-addr>
```

   **On Windows** Apply the ip-addr on the PuTTY Client and launch the terminal.

The usernames and passwords can also be modified. Default password is ```raspberry```

<a name="docker-1"></a>

## Docker Container Engine

Docker-CE Container engine hosts the major operations of the edge. Thus, the Docker-CE must be installed on the Raspberry pi. The steps of the same are given in the subsections below.

<a name="sys-up"></a>

### System Update

Every Raspberry Pi must be updated to the latest kernel and firmware. In order to do that, one must execute the following on a secure shell logged into the Pi.

System Software update

```BASH
$ sudo apt-get update && sudo apt-get dist-upgrade -y
```

Raspberry Pi Firmware (Not necessary)
```BASH
$ sudo rpi-update
```

Reboot
```BASH
$ sudo reboot
```

At this point, the connection shall be closed, and you need to log in again. Wait for a few minutes before pinging the raspberry pi.

<a name="docker-2"></a>

### Docker install

On the following restart, you need to update the index using 
```BASH
$ sudo apt-get update
```
Install packages to use the repository over HTTPS
```BASH
$ sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common
```

Add Docker’s official GPG key
```BASH
$ curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
```

Verify that you now have the key w/ fingerprint
```BASH
$ sudo apt-key fingerprint 0EBFCD88
```

Set up the **stable** repository for ```armhf```
```BASH
$ echo "deb [arch=armhf] https://download.docker.com/linux/raspbian \
     $(lsb_release -cs) stable" | \
     sudo tee /etc/apt/sources.list.d/docker.list
```

Update repository lists CE
```BASH
$ sudo apt-get update
```

Check for the version 18.06.2 and install
```BASH
$ apt-cache madison docker-ce
$ sudo apt-get install docker-ce=18.06.2~ce~3-0~raspbian containerd.io
```

> In general cases, we will get an Error saying
>```BASH
>Error! The dkms.conf for this module includes a BUILD_EXCLUSIVE directive
>which does not match this kernel/arch. This indicates that it should
>not be built.
>```
>
>As this occurs, perform the following steps.
>```BASH
>$ sudo nano /usr/src/aufs-4.9+20161219/dkms.conf
>```
>
>Remove the line bearing  ```BUILD_EXCLUSIVE_KERNEL="^4.9.\*"```
>
>Press ```Ctrl+X```, save the file and run the following
>```
>$ sudo apt-get remove -y docker-ce
>$ sudo apt-get install -y docker-ce=18.06.2~ce~3-0~raspbian
>```

Enable Docker (Optional)
```
$ systemctl enable --now docker
```

<a name="verify-1"></a>

### Verify docker installation

Once the installation is complete, verify the running of the container engine.

1. Check for the installed candidate
```BASH
$ sudo docker version
```

2. Run the docker hello image
```BASH
$ sudo docker run arm32v5/hello-world
```

<a name="hold"></a>

### Exclude docker-ce from further upgrades

The currently installed version of docker-ce (18.06.2 raspbian) is the best suitable one, for the architechture ARMv6l, as updated versions tend to crash. Thus, we have to exlude the the package from being upgraded in future in case we run any form of ```apt-get upgrade```.

Check for the installed package list using
```BASH
$ apt list --upgradable
```
Must give an output saying docker-ce and the number of upgradable versions available.

Hold the future upgrades using
```BASH
$ sudo apt-mark hold docker-ce
```

<a name="post"></a>

## Post installation steps

> **Caution**
> Follow these steps only if the system is deployed on an *automated production side environment*. In case of a development (with frequent power disconnections) environment, post installation steps tend to delay server autostart.

In order to automate the container engine and simplify it's operation using various other services, these steps are to be followed **mandatorily** for USN.

1. Create the docker group
```BASH
$ sudo groupadd docker
```

2. Add your user to the group
```BASH
$ sudo usermod -aG docker $USER
```

3. Reboot your Pi so that you can log in again.
```BASH
$ sudo reboot
```

4. Verify the completion of post installation steps
```BASH
$ docker version
$ docker run hello-world
```

> We must get a warning saying
> ```BASH
> WARNING: Error loading config file: /home/user/.docker/config.json - 
> stat /home/user/.docker/config.json: permission > denied
> ```
> In order to resolve this, execute the following commands:-
> ```BASH
> $ sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
> $ sudo chmod g+rwx "$HOME/.docker" -R
> ```

<a name="deploy"></a>

## Deployement set-up

In order to prepare the device for deployment, we need to perform certain additional steps. These include, changing hostname of the device, changing ssid and password and initiating a docker swarm cluster.

<a name="host"></a>

### Changing Hostname

In order to do so, we need access to the ```rootfs``` of the MicroSD, flashed with the OS. This partition is an ext4 partition, and cannot be accessed by Windows directly. Thus, additional drivers are required. Using a linux system, you can access the ```rootfs``` partition, and change the hostname directly at ```/etc/hostname```. Change the hostname from ```raspberrypi``` to the one suitable to you, and save the file.

You also need to change the domain name for your host in ```/etc/hosts```. Change the line
```CONF
127.0.0.1	localhost
```

to

```CONF
127.0.0.1	[newHostname]
```
Save the file and exit.

<a name="wifi"></a>

### Changing WiFi credentials

Create a wpa_supplicant.conf on the ```boot``` partition of the MicroSD, and input the following.

```CONF
country=IN
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="your_wifi_ssid"
    scan_ssid=1
    psk="your_wifi_password"
    key_mgmt=WPA-PSK
}
```
Save the file and **safely remove the SD card**.

<a name="swarm"></a>

### Docker Swarm

If you wish to deploy a cluster, you need to set-up a docker swarm with the Raspberry Pi nodes on the same network. This can be easily done by recognising the master device and performing the following line on it.

```BASH
# We assume the post-intsallation steps have been conpleted
$ docker swarm init
```

This must give out an output as

```BASH
Swarm initialized: current node (zx10nm5ckj1jy6wlqv1qs75ri) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join --token <access-token> <access-ip and port>

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
```

On the cluster nodes, you can now run the swarm join line to initiate the cluster.

```BASH
# Replace tocken and ip by the one you receive on master
$ docker swarm join --token <access-token> <access-ip and port>
```

Best way is to store the access tocken and ip on the service machine (the machine remotely accessing the Pis).