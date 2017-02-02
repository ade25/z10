# Setup webserver buildout

We strive to establish a general working environment and therefore provide
this "best practice" information. In order to make a webserver buildout
usable in your local development environment you only need to follow a few
simple steps:


## Requirements

All interaction is based on the push deployment tool Fabric. In order to
bootstrap you local directory you need to setup a virtual environment and
install a few dependencies

``` bash
$ cd ~/
$ ../python/bin/virtualenv-2.7 ops
$ cd ~/ops
$ source bin/activate
$ pip install -U setuptools
$ pip install fabric
```

Next you need to setup our global fabfile collection by using a local copy of
*ade25.fabfiles* and making it available to the installed fabfile:

```bash
$ git clone git@github.com:ade25/ade25.fabfiles.git
$ cd ./ade25.fabfiles
$ python setup.py develop
```

In order to use the environment you need to clone
a dedicated webserver buildout into your working directory and run the provided
**development.cfg** profile. this will build a local fabfile holding the server
specific configuration (like hosted sites, servername etc)

```bash
$ cd ~/ops
$ git clone git@github.com:ade25/z1.git
$ cd ./z1
$ python bootstrap.py -c development.cfg
$ bin/buildout -c development.cfg
```


## Usage

In order to work with your webserver configuration and deployment setup you
need to have the *venv* always activated and local fabfiles already built.

Example:

```bash
$ cd ~/ops
$ source bin/activate
(devop)$ cd ./z1
(devop)$ fab restart_varnish
(devop)$ cd ..
(devop)$ cd ./z7
(devop)$ fab supervisorctl:status
```




