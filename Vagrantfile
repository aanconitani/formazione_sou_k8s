# -*- mode: ruby -*-
# vi: set ft=ruby :

#Configurazione globale
Vagrant.configure("2") do |config|
  config.vm.provider "vmware_desktop" do |vmware|
    vmware.memory = 8196
    vmware.cpus = 4
#    vmware.gui = true
    vmware.allowlist_verified = true
  end

#Configurazione vm
  config.vm.define "sou1" do |sou1| 
    sou1.vm.box = "bento/rockylinux-9.3-arm64"
    sou1.vm.box_version = "202404.23.0"  
    sou1.vm.network "private_network", ip: "192.168.50.111"
    sou1.vm.hostname = "sou1"
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "./deploy.yml"
    ansible.become = true
    ansible.compatibility_mode = "2.0"
  end
end
