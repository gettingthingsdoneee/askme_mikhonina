from urllib.parse import parse_qs

def application(environ, start_response):
    get_params = parse_qs(environ.get('QUERY_STRING', ''))
    
   
    post_params = {}
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            post_params = parse_qs(environ['wsgi.input'].read(request_body_size).decode())
        except (ValueError, KeyError):
            pass
    
    
    response = [
        "GET parameters:\n",
        "\n".join(f"{k}: {v}" for k, v in get_params.items()),
        "\n\nPOST parameters:\n",
        "\n".join(f"{k}: {v}" for k, v in post_params.items())
    ]
    
   
    response_text = "\n".join(response)
    headers = [('Content-Type', 'text/plain')]
    start_response('200 OK', headers)
    return [response_text.encode('utf-8')]