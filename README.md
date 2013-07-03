buildout.webserver
=================

Buildout installing the necessary tools to run a webserver on a specific domU.
Just boostrap the buildout and run

    python bootstrap.py -c deployment.cfg
    bin/buildout -c deployment.cfg


Note:
-----

In order to make this reusable it could also be an option to add a dedicated 
buildout profile **servername.cfg** to be explicit and potentially be able to
run this simple webserver setup on several machines (via different profiles).

Another option would be to branch the buildout for each dedicated server and
keep the master branch updated.


Provided services:
------------------

* Nginx (Port 80)
* Varnish (Port 8100)
* haproxy (Port 8200)
* runscript
* logrotation
* supervisord (controlling the isntalled zope instances)

Configuration
------------

All configuration is based in variables. In order to extend the buildout for
a new site, add or copy the relevant parts starting with "zopeX", by simply 
appending a higher number, e.g for haproxy context switching:

    acl ${sites:zope1}_cluster hdr_beg(host) -i ${hosts:zope1}
    # Check that we have at least one node up in the zope1 cluster
    acl ${sites:zope1}_cluster_up nbsrv(default) gt 0

where you would simply copy the part and replace zope1 with zope2 accordingly.

Howto
=====

In order to extend this buildout and add an additional site, follow these steps:


Update deployment.cfg
---------------------

1. Add a new variable/hostname pair to the *[hosts]* part, e.g.

```
zope1   = example.tld
zope1-1  = example2.tld 
```

Note that additional domains can be added, though you should stick to the
convention of using one main hostname per site (search engines will love this)

2. Add corresponding zope instance port to *[ports]*

```
zope1   = 8401
```

3. Update the *[supervisor]* configuration

```
40 instance-${sites:zope1}      ${zope-locations:zope1}/bin/instance [console] true ${users:zope-process}
```

Note: if you add a new site you can just copy the last line and update
the variable number


Add new virtual host to "${buildout:directory}/etc/vhosts/"
-----------------------------------------------------------

Copy the existing *example.tld* file and replace the *zopeX* variable with the 
new variable, e.g. *zope1*.


Update "/buildout.d/vhosts.cfg"
-------------------------------

Add the new vhost configuration to the *vhost.cfg* file, by appending a new
part, specifying the Zope instance location and add the corresponding
configuration file compilation

```
[buildout]
vhosts-parts =
    vhost-zopeX
    ...

[zope-locations]
zopeX         = /opt/sites/${sites:zopeX}/buildout.${sites:zopeX}
...

[vhost-zopeX]
recipe = collective.recipe.template
input = ${locations:templates}/${sites:zopeX}.conf
output =
```

Update "/buildout.d/templates/haproxy.conf"
-------------------------------------------

Configure the load balancer to now inlcude the newly added site, by copying
the relevant parts in the configuration

```
acl ${sites:zopeX}_cluster url_sub ${hosts:zopeX}
...
acl ${sites:zopeX}_cluster_up nbsrv(${sites:zopeX}) gt 0
...
use_backend ${sites:zopeX} if ${sites:zopeX}_cluster_up ${sites:zopeX}_cluster
```

Prepare the new backend that proxies to the Zope instanz, by copying an
existing backend part

```
backend ${sites:zopeX}
    balance leastconn
    rspadd X-Cluster:\ default
    server ${sites:zopeX}  ${hosts:main}:${ports:zopeX} check rise 1 weight 50 maxconn 4
```

Update "/buildout.d/templates/nginx.conf"
-----------------------------------------

Finally include the new virtual host configuration in the main webserver
congfig file by adding a single line at the bottom of the file

```
include ${locations:config}/${sites:zopeX}.conf;
````


Deploy the new configuration
=============================

In the last step login to the target deployment server and update the 
configuration, example:

``` bash

$ cd /opt/webserver/buildout.webserver
$ git pull
$ bin/buildout -N -c deployment.cfg
$ bin/supervisorctl reread
$ bin/supervisorctl update
$ bin/supervisorctl start instance-zopeX
$ bin/supervisorctl restart haproxy
$ bin/supervisorctl restart nginx

```


