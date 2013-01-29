class app::rabbitmq{
    package{'rabbitmq-server':
        ensure => installed
    }

    service{ "rabbitmq-server":
        ensure     => running,
        enable     => true,
        hasrestart => true,
        require    => Package['rabbitmq-server']
    }
}