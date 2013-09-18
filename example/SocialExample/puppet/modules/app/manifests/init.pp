class app {
    class{'app::apt-get-update': stage => first }
    class{'app::pipreq': stage => last }
    class{'app::configuration-actions': stage => last }
}

file { "/var/www":
    ensure => "directory",
}
