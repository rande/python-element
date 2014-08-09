Running Element
===============

One Element's core feature, the ``render`` helper, is used to generated sub request processes by a dedicated controller.
The internal implementation of this feature rely on an ESI tag or SSI tag. So Element requires to be behind a reverse
proxy like Nginx or Varnish.

To run an element instance, you need a process manager like supervisord::

    [program:rabaix.net]
    command=/home/rabaix/site/bin/python start.py tornado:start -np 8 -p 5001 --bind thomas.rabaix.net
    autostart=true
    autorestart=true
    startsecs=3
    user=rabaix
    directory=/home/rabaix/site/src

This will spawn 8 independents processes to process http requests.

The Nginx configuration can be::

    server {
        listen   80;
        server_name thomas.rabaix.net;

        location / {
            ssi on;

            proxy_pass http://127.0.0.1:5001;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }

or the Varnish configuration (from the `Symfony2 documentation`_)::

    sub vcl_fetch {
        /*
        Check for ESI acknowledgement
        and remove Surrogate-Control header
        */
        if (beresp.http.Surrogate-Control ~ "ESI/1.0") {
            unset beresp.http.Surrogate-Control;

            // For Varnish >= 3.0
            set beresp.do_esi = true;
            // For Varnish < 3.0
            // esi;
        }
        /* By default Varnish ignores Cache-Control: nocache
        (https://www.varnish-cache.org/docs/3.0/tutorial/increasing_your_hitrate.html#cache-control),
        so in order avoid caching it has to be done explicitly */
        if (beresp.http.Pragma ~ "no-cache" ||
             beresp.http.Cache-Control ~ "no-cache" ||
             beresp.http.Cache-Control ~ "private") {
            return (hit_for_pass);
        }
    }


If you don't have a local reverse proxy (ie, varnish) you can use the ``proxy.py`` script which able to render ``esi:include`` tag::

    [program:rabaix.net]
    command=/home/rabaix/site/bin/python proxy.py 5001
    autostart=true
    autorestart=true
    startsecs=3
    user=rabaix
    directory=/home/rabaix/site/src


.. note::

    Depends on the use case, you can use varnish or nginx with specific caching rules, Nginx runs SSI in in parallel
    while Varnish runs ESI sequentially.


.. _Symfony2 documentation: http://symfony.com/doc/current/cookbook/cache/varnish.html


