class app::configuration-actions {
    exec{'setup-default-ssh-directory':
        command => "echo 'cd /var/www' >> /home/vagrant/.bashrc",
        unless  => "grep -c 'cd /var/www' /home/vagrant/.bashrc",
        user    => vagrant,
    }

}