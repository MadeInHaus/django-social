node default{
    Exec { path => "/usr/bin:/usr/sbin:/bin:/sbin:/usr/local/bin:/usr/local/sbin" }
    
    stage { first: before => Stage[main] }
    stage { last: require => Stage[main] }
    
    include app
    include app::rabbitmq
    include app::redis
    include app::python
    include app::vim
    include app::git
    include app::postgresql
    # include app::mysql
    include app::libevent
    include app::pipreq
    include app::memcache
    include app::node
    include app::sass
    
}

