VAGRANTFILE_API_VERSION = "2"
  
# General Vagrant VM config
Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "generic/debian12"
  config.vm.provider :libvirt do |v|
    v.memory = 512
  end

  # Configuration for web server 
  config.vm.define "server1" do |server|
    server.vm.hostname = "server1"
    server.vm.network :private_network, ip: "192.168.1.150"
  end

  # Provision configuration for Ansible
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "ansible/playbook.yml"
    ansible.config_file = "ansible/ansible.cfg"
    ansible.inventory_path = "ansible/hosts.ini"
    # ansible.verbose = "v"
  end
end
