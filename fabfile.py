from fabric.api import env
import fabric_gunicorn as gunicorn

env.host_string = 'thelabmill.de'
env.port = 22
env.user = 'christoph'

#env.remote_workdir = '/home/christoph'
env.virtualenv_dir = env.remote_workdir + '/env'

env.gunicorn_wsgi_app = 'hello.wsgi:app'
#env.gunicorn_pidfile = env.remote_workdir + '/test.pid'
#env.gunicorn_bind = 'localhost:5000'
#env.django_settings_module = 'test'

