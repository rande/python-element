
# Allow a grace period for offering "stale" data in case backend lags
#set req.grace = 60s;
set req.grace = 5m;

remove req.http.X-Forwarded-For;
set req.http.X-Forwarded-For = client.ip;

# Force lookup if the request is a no-cache request from the client
#if (req.http.Cache-Control ~ "no-cache") {
#    return (pass);
#}

## Default request checks
if (req.request != "GET" &&
    req.request != "HEAD" &&
    req.request != "PUT" &&
    req.request != "POST" &&
    req.request != "TRACE" &&
    req.request != "OPTIONS" &&
    req.request != "DELETE") {
        # Non-RFC2616 or CONNECT which is weird.
        return (pipe);
}

if (req.request != "GET" && req.request != "HEAD") {
    # We only deal with GET and HEAD by default
    return (pass);
}

## Modified from default to allow caching if cookies are set, but not http auth
if (req.http.Authorization) {
    /* Not cacheable by default */
    return (pass);
}

# Don't cache user/application area
if (req.url ~ "^/(contact|admin).*") {
    return (pass);
}

## Don't cache editor logged-in user sessions
if (req.http.Cookie ~ "(element_is_editor)") {
    return (pass);
}

# From here, the cache is used, so we remove cookies
remove req.http.Cookie;

return (lookup);