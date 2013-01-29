class app::python {

    $packageList = [
    'python2.7',
    'python-dev',
    'python-pip',
    'python-virtualenv',
    ]

    package { $packageList: }

    
}

