import webob as wo, wsgiref.simple_server as wrs
import tw2.core as twc, tw2.forms as twf, os
import formencode as fe

opts = ['Red', 'Yellow', 'Green', 'Blue']


class TestPage(twf.FormPage):
    title = 'ToscaWidgets Tutorial'
    class child(twf.Form):
        class child(twf.TableLayout):
            id = 'xx'
#            email = twf.TextField(validator=twc.EmailValidator(required=True))
#            confirm_email = twf.TextField()
#            select = twf.SingleSelectField(options=list(enumerate(['']+opts)), validator=twc.Required, item_validator=twc.IntValidator())
            msel = twf.MultipleSelectField(options=list(enumerate(opts)), validator=twc.Required, item_validator=twc.IntValidator())
            cbl = twf.CheckBoxList(options=list(enumerate(opts)), validator=twc.Required, item_validator=twc.IntValidator())
            rbl = twf.RadioButtonList(options=list(enumerate(opts)), validator=twc.Required, item_validator=twc.IntValidator())
#            validator = twc.MatchValidator('email', 'confirm_email')
            a = twf.CheckBox(validator=twc.BoolValidator(required=True))
#            b = twf.FileField()
            x = twf.TextField(validator=fe.validators.Regex('^\w+$'))

def app(environ, start_response):
    req = wo.Request(environ)
    resp = wo.Response(status="404 Not Found")
    return resp(environ, start_response)


if __name__ == "__main__":
    mw = twc.TwMiddleware(app, debug=True)
    mw.controllers.register(TestPage, 'test')
    wrs.make_server('', 8000, mw).serve_forever()
