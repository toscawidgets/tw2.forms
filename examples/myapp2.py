import webob as wo, wsgiref.simple_server as wrs
import tw2.core as twc, tw2.forms as twf, os


class TestPage(twf.FormPage):
    title = 'ToscaWidgets Tutorial'
    class child(twf.Form):
        class child(twf.TableLayout):
            id = 'xx'
            email = twf.TextField(validator=twc.EmailValidator(required=True))
            confirm_email = twf.TextField()
            validator = twc.MatchValidator('email', 'confirm_email')


def app(environ, start_response):
    req = wo.Request(environ)
    resp = wo.Response(status="404 Not Found")
    return resp(environ, start_response)


if __name__ == "__main__":
    mw = twc.TwMiddleware(app)
    mw.controllers.register(TestPage, 'test')
    wrs.make_server('', 8000, mw).serve_forever()
