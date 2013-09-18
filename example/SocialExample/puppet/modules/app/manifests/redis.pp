class app::redis{
    
    package{'redis-server':
        ensure => installed
    }

    service{ "redis-server":
        ensure     => running,
        enable     => true,
        hasrestart => true,
        require    => Package['redis-server']
    }

    file{'redis.conf':
            path => '/etc/redis/redis.conf',
            ensure => present,
            require => Package[redis-server],
            source => "puppet:///modules/app/redis/redis.conf",
            notify  => Service['redis-server'],
            owner => root,
            group => root;
    }
}