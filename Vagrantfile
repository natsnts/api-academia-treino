# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"

  # VM1: cliente usado para testar a API com curl/wget
  config.vm.define "vm1" do |vm1|
    vm1.vm.hostname = "vm1"
    vm1.vm.network "private_network", ip: "192.168.56.10"

    vm1.vm.provider "virtualbox" do |vb|
      vb.name   = "vm1-cliente"
      vb.memory = 1024
    end

    vm1.vm.provision "shell", inline: <<-SHELL
      apt-get update -y
      apt-get install -y curl wget
    SHELL
  end
end
