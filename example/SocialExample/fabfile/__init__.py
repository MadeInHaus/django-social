import functools

from fabric.api import env, task, run, roles, cd
from fabric.context_managers import shell_env

from haus_vars import with_vars

import vagrant, prod, dev, staging
from vagrant import runall, killall, resetdb, resetall, test

env.roledefs       = {
                      'vagrant'                : ['vagrant@127.0.0.1:2222']
                     }
env.passwords      = {
                      'vagrant@127.0.0.1:2222'      :'vagrant',
                     }



