# Python Web Server
Create a web server from scratch using Python

## Prerequisites
The following must be installed to run the web server on your local machine:
- python3

To deploy & provision the web server on a VM, you must have:
- Vagrant
- ansible
- libvirt (or virt-manager for GUI)

## Usage
### Option #1: Run the web server on local machine:
```bash 
cd /path/to/python_webserver/src
python3 web_server.py
```

### Option #2: Deploy & provision the web server on a VM:
```bash
cd /path/to/python_webserver/
vagrant up
```

### Option #3: Provision the web server on an existing VM:
```bash
cd /path/to/python_webserver/ansible
ansible-playbook playbook.yml
```
> Note: You may need to edit `ansible/hosts.ini` if you did not use the included `Vagrantfile`

- If you choose to deploy & provision the web server on a VM, you can access the website at [`http://192.168.1.150:8080`](http://192.168.1.150:8080).
- If you run the web server locally, you can access the website at [`http://localhost:8080`](http://localhost:8080)