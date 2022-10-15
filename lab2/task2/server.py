from wsgiref.simple_server import make_server
from datetime import datetime
from jinja2 import Template

def application(environ, start_response):
    template = Template(open('./index.html', encoding='utf-8').read())
    try:
        x, y = [i.split('=')[1] for i in environ["QUERY_STRING"].split('&')]
        x = 0 if not x else int(x)
        y = 0 if not y else int(y)
        page = template.render(sum=x+y, time=datetime.now().time())
    except:
        page = template.render()

    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(page)))
    ]
    start_response(status, response_headers)
    return [bytes(page, "utf-8")]

# Instantiate the server
httpd = make_server (
    'localhost', # The host name
    8080, # A port number where to wait for the request
    application # The application object name, in this case a function
)

httpd.serve_forever()
