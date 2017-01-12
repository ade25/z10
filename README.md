# Webserver buildout

Buildout installing the necessary tools to run a webserver on a specific domU.
Just boostrap the buildout and run

    virtualenv .
    bin/pip install zc.buildout
    # Fix missing openssl header files
    env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include" bin/pip install cryptography
    bin/buildout -c deployment.cfg

## Note:

In order to make this work locally you need to take a view extra steps. Please
refer to the [setup local directory documentation](docs/setup.md)


## Provided services:

* Nginx (Port 80)
* Varnish (Port 8100)
* haproxy (Port 8200)
* runscript
* logrotation
* supervisord (controlling the isntalled zope instances)


## Usage

Refer to [usage documentation](docs/usage.md)
