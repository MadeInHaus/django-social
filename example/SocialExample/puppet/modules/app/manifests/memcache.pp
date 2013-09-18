class app::memcache{
    package{'memcached':
        ensure => installed
    }

    service{ "memcached":
        ensure     => running,
        enable     => true,
        hasrestart => true,
        require    => Package['memcached']
    }
}