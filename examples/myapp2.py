import webob as wo, wsgiref.simple_server as wrs
import tw2.core as twc, tw2.forms as twf, os


class TestPage(twc.Page):
    title = 'ToscaWidgets Tutorial'
    class child(twf.Form):
        class child(twf.TableLayout):
            id = 'xx'
            email = twf.TextField(validator=twc.EmailValidator(required=True))
            confirm_email = twf.TextField()
            validator = twc.MatchValidator('email', 'confirm_email')


def app(environ, start_response):
    req = wo.Request(environ)
    resp = wo.Response(request=req, content_type="text/html; charset=UTF8")
    if req.method == 'GET':
        resp.body = TestPage.display().encode('utf-8')
    elif req.method == 'POST':
        try:
            data = TestPage.validate(req.POST)
            resp.body = 'Posted successfully ' + wo.html_escape(repr(data))
        except twc.ValidationError, e:
            resp.body = e.widget.display().encode('utf-8')
    return resp(environ, start_response)


if __name__ == "__main__":
    wrs.make_server('', 8000, twc.TwMiddleware(app)).serve_forever()
