# Python Web Server

Create a web server from scratch using Python

## Prerequisites

The following operating systems have been tested:

- Ubuntu 22.04 Server LTS
- Debian 12.4 (Bookworm)

The following software must be installed to run the web server on your local machine:

- python3

To deploy & provision the web server on a VM, you must have:

- Vagrant
- ansible
- libvirt (or virt-manager for GUI)

To deploy the web server using a Docker container, you must [install Docker](https://docs.docker.com/engine/install/)
and [Docker Compose](https://docs.docker.com/compose/install/).

## Usage

### Option #1: Run the web server on local machine

```bash
cd /path/to/python_webserver/src
python3 web_server.py
```

### Option #2: Deploy & provision the web server on a VM

```bash
cd /path/to/python_webserver/
vagrant up
```

### Option #3: Provision the web server on an existing VM

```bash
cd /path/to/python_webserver/ansible
ansible-playbook playbook.yml
```

> Note: You may need to edit `ansible/hosts.ini` if you did not use the included `Vagrantfile`.

### Option #4: Create and run a Docker container

```bash
cd /path/to/python_webserver
docker compose up -d
```

- If you choose to deploy & provision the web server on a VM, you can access the website at [`http://192.168.1.150:8080`](http://192.168.1.150:8080).
- If you run the web server locally or with a Docker container, you can access the website at [`http://localhost:8080`](http://localhost:8080).

## Resources

- [Let's Build A Web Server. Part 1.](https://ruslanspivak.com/lsbaws-part1/)
