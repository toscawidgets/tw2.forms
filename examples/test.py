import webob as wo, wsgiref.simple_server as wrs, cgi
import tw2.core as twc, tw2.forms as twf


MyForm = twf.Form(child=
    twf.TableLayout(id='a',
        children = [
            twf.TextField(id='name', validator=twc.Required),
            twf.TextField(id='email', validator=twc.EmailValidator),
        ]
    )
)


def simple_app(environ, start_response):
    req = wo.Request(environ)
    resp = wo.Response(request=req, content_type="text/html; charset=UTF8")
    if req.method == 'GET':
        resp.body = MyForm.idisplay().encode('utf-8')
    elif req.method == 'POST':
        try:
            data = MyForm.validate(req.POST)
            resp.body = 'Posted successfully ' + cgi.escape(repr(data))
        except twc.ValidationError, e:
            resp.body = e.widget.display().encode('utf-8')
    return resp(environ, start_response)


middleware = twc.TwMiddleware(simple_app)

if __name__ == "__main__":
    wrs.make_server('', 8000, middleware).serve_forever()
