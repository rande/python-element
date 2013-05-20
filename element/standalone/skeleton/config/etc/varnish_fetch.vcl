# These status codes should always pass through and never cache.
if (beresp.status == 404) {
    set beresp.http.X-Cache-Rule = "YES: but for 1m - beresp.status : " + beresp.status;
    set beresp.ttl = 10m;

    unset beresp.http.set-cookie;

    return (deliver);
}

if (beresp.status == 503 || beresp.status == 500) {
    set beresp.http.X-Cache-Rule = "NOT: beresp.status : " + beresp.status;
    set beresp.ttl = 0s;

    return (hit_for_pass);
}

if (req.url ~ "\.(jpg|jpeg|gif|png|ico|css|zip|tgz|gz|rar|bz2|pdf|txt|tar|wav|bmp|rtf|js|flv|swf|html|htm|mov|avi|mp3|mpg)$") {
    unset beresp.http.set-cookie;
    set beresp.http.X-Cache-Rule = "YES: static files";
    
    if (!beresp.ttl > 0s) {
        set beresp.ttl = 24h;
        set beresp.http.X-Cache-Rule = "Yes: static file, force beresp.ttl == 24h";
    }

    return (deliver);
}

#if (obj.http.Set-Cookie) {
#    set obj.http.X-Cache-Rule = "NO: !obj.Set-Cookie";
#    return (hit_for_pass);
#}

# No cache for Element Editor
if (req.http.Cookie ~ "element_is_editor") {
    set beresp.ttl = 0s;
    set beresp.http.X-Cache-Rule = "NO: user is an editor";

    return (hit_for_pass);
}

if (!beresp.ttl > 0s) {
    set beresp.http.X-Cache-Rule = "NO: beresp.ttl == 0";

    return (hit_for_pass);
}

# All tests passed, therefore item is cacheable
set beresp.http.X-Cache-Rule = "YES with ttl: " + beresp.ttl;

# remove cookies for cached response
unset beresp.http.set-cookie;

return (deliver);