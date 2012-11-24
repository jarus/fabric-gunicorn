# -*- coding: utf-8 -*-
# fabric-gunicorn
# Copyright: (c) 2012 Christoph Heer <Christoph.Heer@googlemail.com>
# License: BSD, see LICENSE for more details.

from time import sleep

from fabric import colors
from fabric.api import task, env, run, cd
from fabric.utils import abort, puts
from fabric.contrib import files
from fabric.context_managers import hide


def set_env_defaults():
    env.setdefault('remote_workdir', '~')
    env.setdefault('gunicorn_pidpath', env.remote_workdir + '/gunicorn.pid')
    env.setdefault('gunicorn_bind', '127.0.0.1:8000')

set_env_defaults()


def gunicorn_running():
    return run('ls ' + env.gunicorn_pidpath, quiet=True).succeeded


def gunicorn_running_workers():
    count = None
    with hide('running', 'stdout', 'stderr'):
        count = run('ps -e -o ppid | grep `cat %s` | wc -l' %
                    env.gunicorn_pidpath)
    return count


@task
def status():
    """Show the current status of your Gunicorn process"""

    set_env_defaults()

    if gunicorn_running():
        puts(colors.green("Gunicorn is running."))
        puts(colors.yellow('Active workers: %s' % gunicorn_running_workers()))
    else:
        puts(colors.blue("Gunicorn isn't running."))


@task
def start():
    """Start the Gunicorn process"""

    set_env_defaults()

    if gunicorn_running():
        puts(colors.red("Gunicorn is already running!"))
        return

    if 'gunicorn_wsgi_app' not in env:
        abort(colors.red('env.gunicorn_wsgi_app not defined'))

    with cd(env.remote_workdir):
        prefix = []
        if 'virtualenv_dir' in env:
            prefix.append('source %s/bin/activate' % env.virtualenv_dir)
        if 'django_settings_module' in env:
            prefix.append('export DJANGO_SETTINGS_MODULE=%s' %
                          env.django_settings_module)

        prefix_string = ' && '.join(prefix)
        if len(prefix_string) > 0:
            prefix_string += ' && '

        options = [
            '--daemon',
            '--pid %s' % env.gunicorn_pidpath,
            '--bind %s' % env.gunicorn_bind,
        ]
        if 'gunicorn_workers' in env:
            options.append('--workers %s' % env.gunicorn_workers)
        if 'gunicorn_worker_class' in env:
            options.append('--worker-class %s' % env.gunicorn_worker_class)
        options_string = ' '.join(options)

        run('%s gunicorn %s %s' % (prefix_string, options_string,
                                   env.gunicorn_wsgi_app))

        if gunicorn_running():
            puts(colors.green("Gunicorn started."))
        else:
            abort(colors.red("Gunicorn wasn't started!"))


@task
def stop():
    """Stop the Gunicorn process"""

    set_env_defaults()

    if not gunicorn_running():
        puts(colors.red("Gunicorn isn't running!"))
        return

    run('kill `cat %s`' % (env.gunicorn_pidpath))

    for i in range(0, 5):
        puts('.', end='', show_prefix=i == 0)

        if gunicorn_running():
            sleep(1)
        else:
            puts('', show_prefix=False)
            puts(colors.green("Gunicorn was stopped."))
            break
    else:
        puts(colors.red("Gunicorn wasn't stopped!"))
        return


@task
def restart():
    """Restart hard the Gunicorn process"""
    stop()
    start()


@task
def reload():
    """Gracefully reload the Gunicorn process and the wsgi application"""

    set_env_defaults()
    if not gunicorn_running():
        puts(colors.red("Gunicorn isn't running!"))
        return
    puts(colors.yellow('Gracefully reloading Gunicorn...'))
    run('kill -HUP `cat %s`' % (env.gunicorn_pidpath))


@task
def add_worker():
    """Increase the number of your Gunicorn workers"""
    set_env_defaults()
    if not gunicorn_running():
        puts(colors.red("Gunicorn isn't running!"))
        return

    puts(colors.green('Increasing number of workers...'))
    run('kill -TTIN `cat %s`' % (env.gunicorn_pidpath))
    puts(colors.yellow('Active workers: %s' % gunicorn_running_workers()))


@task
def remove_worker():
    """Decrease the number of your Gunicorn workers"""
    set_env_defaults()
    if not gunicorn_running():
        puts(colors.red("Gunicorn isn't running!"))
        return

    puts(colors.green('Decreasing number of workers...'))
    run('kill -TTOU `cat %s`' % (env.gunicorn_pidpath))
    puts(colors.yellow('Active workers: %s' % gunicorn_running_workers()))
