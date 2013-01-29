class app::sass{
    package {['sass','rb-inotify', 'listen', 'compass']:
        provider => 'gem',  
        ensure => installed
    }
}