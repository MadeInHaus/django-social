class app::mysql{
	include mysql::python
    include mysql::server
	mysql::db { 'django':
      user     => 'vagrant',
      password => 'vagrant',
      host     => 'localhost',
      grant    => ['all'],
    }
}


