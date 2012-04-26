"""
===============
fabric-gunicorn
===============

This is a small fabric file to include in your fabfile.

Links
`````

* `github <https://github.com/jarus/fabric-gunicorn>`_
* `development version <https://github.com/jarus/fabric-gunicorn/zipball/master#egg=fabric-gunicorn>`_
* `fabric <http://fabfile.org>`_

"""

from setuptools import setup


setup(
    name='fabric-gunicorn',
    version='0.1',
    url='http://github.com/jarus/fabric-gunicorn',
    license='BSD',
    author='Christoph Heer',
    author_email='Christoph.Heer@googlemail.com',
    description='fabric file with tasks to control a gunicorn process',
    long_description=__doc__,
    py_modules=['fabric_gunicorn'],
    install_requires=[
        'fabric'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)