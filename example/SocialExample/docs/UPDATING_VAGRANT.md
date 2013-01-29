

## Updating Vagrant
```bash
vagrant gem update vagrant
```

or in an old install of vagrant:
```bash
gem update vagrant
```

## Updating Virtualbox
Run the VirtualBox.app and "Check for Updates..." under the VirtualBox menu.

## Install the vagrant-vbguest plugin

VirutalBox has a number of "Guest Additions" that are version specific.  Whenever you update virtualbox you will want to upgrade these as well in all of your VM boxes.  Vagrant makes this easy with a plugin. vagrant-vbguest which will automatically install updated guest additions when they become out of date.

```bash
vagrant gem install vagrant-vbguest
```