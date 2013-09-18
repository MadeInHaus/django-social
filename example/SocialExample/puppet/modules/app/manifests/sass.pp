class app::sass{
    package {['sass','rb-inotify', 'listen', 'compass', 'oily_png']:
        provider => 'gem',  
        ensure => installed
    }
}
