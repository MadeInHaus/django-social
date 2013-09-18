# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant::Config.run do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "haus"

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  config.vm.box_url = "http://s3.amazonaws.com/haus_backend_utility/haus.box"

  # Boot with a GUI so you can see the screen. (Default is headless)
  # config.vm.boot_mode = :gui

  # Assign this VM to a host-only network IP, allowing you to access it
  # via the IP. Host-only networks can talk to the host machine as well as
  # any other machines on the same network, but cannot be accessed (through this
  # network interface) by any external networks.
  # config.vm.network :hostonly, "192.168.33.10"

  # Assign this VM to a bridged network, allowing you to connect directly to a
  # network using the host's network device. This makes the VM appear as another
  # physical device on your network.
  # config.vm.network :bridged

  # Forward a port from the guest to the host, which allows for outside
  # computers to access the VM, whereas host only networking does not.
  #config.vm.forward_port 80, 80
  #config.vm.forward_port 443, 443

  #Redis
  #config.vm.forward_port 6379, 6378

  #RabbitMQ
  #config.vm.forward_port 5672, 5673

  #Django
  config.vm.forward_port 8000, 8080

  # Share an additional folder to the guest VM. The first argument is
  # an identifier, the second is the path on the guest to mount the
  # folder, and the third is the path on the host to the actual folder.
  config.vm.share_folder "project", "/var/www", "./"

  
  #config.vm.provision :puppet, :options => "--verbose --debug" do |puppet|
  # there is a bug in 2.7
  # http://projects.puppetlabs.com/issues/9862
  # err: /File[/var/lib/puppet/rrd]: Could not evaluate: Could not find group puppet
  config.vm.provision :puppet, :options => "--no-report" do |puppet|
  #config.vm.provision :puppet do |puppet|
    puppet.manifests_path = "puppet"
    puppet.manifest_file  = "app.pp"
    puppet.module_path    = "puppet/modules"
  end
end
