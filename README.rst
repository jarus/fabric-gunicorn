fabric-gunicorn
===============

Control your gunicorn process with fabric.

.. image:: http://files.thelabmill.de/fabric-gunicorn/fabric-gunicorn-status-start-stop.png

Install
-------

The installation is thanks to the Python Package Index and `pip <http://www.pip-installer.org/>`_ really simple.

::

   $ pip install fabric-gunicorn


First steeps
------------

Add ``import fabric_gunicorn as gunicorn`` to your new or existing fabfile.py. After this you should go in your termianl and run ``fab -l`` in your project directory. You will see something like this:

::

    Available commands:
    
    gunicorn.add_worker     Increase the number of your gunicorn workers
    gunicorn.reload         Reload gracefully the gunicorn process and the wsgi application
    gunicorn.remove_worker  Decrease the number of your gunicorn workers
    gunicorn.restart        Restart hard the gunicorn process
    gunicorn.start          Start the gunicorn process
    gunicorn.status         Show the current status of your gunicorn process
    gunicorn.stop           Stop the gunicorn process


Befor you can start a gunicorn process on your server you must set the gunicorn_wsgi_app env variable. Edit your fabfile.py and add something like: ``env.gunicorn_wsgi_app = 'hello.wsgi:app'``. The default workdir is the home directory of the connected user. You can also change this path with the env variable ``env.remote_workdir``.

Normaly you should now able to run ``fab gunicorn.start`` and the gunicorn server should start on your remote machine. Gunicorn must be installed.
Your wsgi app is now avaiable under ``http://127.0.0.1:8000``.

Configuration
-------------

fabric-gunicorn take all configuration from the fabric env variable. For gunicorn I added some variables:

env.remote_workdir
  This is normaly your project path.

env.virtualenv_dir
  If you want to use a virtualenv than you can here define the path to your 
  env directory.

env.gunicorn_wsgi_app
  There you set your wsgi app import path.
  Example: ``mydjangoproject.wsgi:application``
  
env.gunicorn_bind
  Define on which port or socket gunicorn should bind.
  Default: ``127.0.0.1:8000``

env.gunicorn_pidfile
  The path for the pidfile of the gunicorn master process.
  Default: ``remote_workdir/gunicorn.pid``

env.gunicorn_workers
  The number of gunicorn worker processes by start.
  Default: ``1``

env.gunicorn_worker_class
  The class of worker you want to use. Normal the default ``sync`` worker
  should run fine. More under: http://gunicorn.org/design.html

env.django_settings_module
  This is special for django to set the DJANGO_SETTINGS_MODULE path.
  Example: ``mydjangoproject.settings``
