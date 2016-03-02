from fabric.api import env
from fabric.context_managers import cd
from fabric.operations import run

env.shell = '/bin/bash -l -c'
env.user = 'd'
env.roledefs.update({
    'staging': ['stagingadmin.solebtc.com'],
    'production': ['admin.solebtc.com']
})

# Heaven will execute fab -R staging deploy:branch_name=master
def deploy(branch_name):
    print("Executing on %s as %s" % (env.host, env.user))

    run('supervisorctl stop solebtc-admin')
    run('rm -rf solebtc-admin')
    run('git clone --recursive https://github.com/freeusd/solebtc-admin.git --branch %s' % (branch_name))
    run('cp -r solebtc-admin-config/* solebtc-admin/config/')
    with cd('solebtc-admin'):
        run('npm run build')
        run('supervisorctl start solebtc-admin')
