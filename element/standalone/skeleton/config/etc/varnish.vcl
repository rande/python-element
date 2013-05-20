sub vcl_recv {
    if (req.http.host == "www.mywebsite.com") {
        include "/path/to/virtualenv/site/src/config/etc/varnish_recv.vcl";
    }
}

sub vcl_fetch {
    if (req.http.host == "www.mywebsite.com") {
        include "/path/to/virtualenv/src/config/etc/varnish_fetch.vcl";
    }
}