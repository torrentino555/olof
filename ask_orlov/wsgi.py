def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    str = "<html><body>"
    str += "<form action=\"\" method=\"post\">"
    str += "<input name=\"search\" type=\"text\" class=\"form-control\" placeholder=\"Search\">"
    str += "<input type=\"submit\" value=\"Ask!\">"
    str += "</form>"
    str += "<p>Hello world!</p>"
    str += "<p>GET: " + environ["QUERY_STRING"] + '</p>'
    try:
        size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        size = 0
    str += "<p>POST: " + environ["wsgi.input"].read(size) + '</p>'
    str += "</body></html>";
    return [str]
