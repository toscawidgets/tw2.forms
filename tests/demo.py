import webob as wo, wsgiref.simple_server as ws
import tw.forms as twf, tw.core as twc

#twc.framework.framework = twc.framework.FrameworkInterface()
#twc.framework.framework._request_id = None

a = twf.Form(child=twf.TableForm(id='a', children=twc.WidgetBunch([
   twf.TextArea(id='b'),
   twf.Label(text='this is a test'),
    twf.TextField(id='c'),
])))

twc.framework.framework._request_id = 1

xx = 5


def simple_app(environ, start_response):
    req = wo.Request(environ)
    resp = wo.Response(request=req, content_type="text/html; charset=UTF8")

    if req.method == 'POST':
        resp.body = a.display(displays_on='string').encode('utf-8')

    elif req.method == 'GET':
        global xx
        a.value = {'b':'hello', 'c':'world%d' % xx}
        xx += 1
        resp.body = a.display(displays_on='string').encode('utf-8')

    return resp(environ, start_response)

app = twc.middleware.make_middleware(simple_app)


if __name__ == "__main__":
    twc.framework.framework._request_id = 1
    ws.make_server('', 8000, app).serve_forever()