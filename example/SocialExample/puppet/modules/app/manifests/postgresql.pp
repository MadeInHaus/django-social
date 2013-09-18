class app::postgresql{
    package{['postgresql','libpq-dev']:
        ensure => installed
    }

    service{ "postgresql":
        ensure     => running,
        enable     => true,
        hasrestart => true,
        require    => Package['postgresql']
    }

    exec{"createpguser":
        require => Package['postgresql'],
        command => "sudo -u postgres createuser --superuser vagrant",
        user => root,
        refreshonly => true,
        subscribe => Package['postgresql'],
    }

    exec{"createpgdb":
        require => Exec['createpguser'],
        command => "createdb django",
        user => postgres,
        refreshonly => true,
        subscribe => Package['postgresql'],
    }
}
