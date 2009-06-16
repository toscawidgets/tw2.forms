import webob as wo, wsgiref.simple_server as wrs
import tw2.core as twc, tw2.forms as twf, os


class TestPage(twc.Page):
    resources = [twc.CSSLink(filename='myapp.css')]
    template = 'genshi:%s/myapp.html' % os.getcwd()
    title = 'ToscaWidgets Tutorial'
    class child(twf.TableForm):
        id = 'xx'
        name = twf.TextField(validator=twc.Required)
        group = twf.SingleSelectField(options=['', 'Red', 'Green', 'Blue'])
        notes = twf.TextArea(validator=twc.StringLengthValidator(min=10))


def app(environ, start_response):
    req = wo.Request(environ)
    resp = wo.Response(request=req, content_type="text/html; charset=UTF8")
    if req.method == 'GET':
        resp.body = TestPage.idisplay().encode('utf-8')
    elif req.method == 'POST':
        try:
            data = TestPage.validate(req.POST)
            resp.body = 'Posted successfully ' + wo.html_escape(repr(data))
        except twc.ValidationError, e:
            resp.body = e.widget.display().encode('utf-8')
    return resp(environ, start_response)


if __name__ == "__main__":
    wrs.make_server('', 8000, twc.TwMiddleware(app)).serve_forever()
