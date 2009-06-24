import webob as wo, wsgiref.simple_server as wrs
import tw2.core as twc, tw2.forms as twf, os
import formencode as fe

opts = ['Red', 'Yellow', 'Green', 'Blue']

mw = twc.TwMiddleware(None, controller_prefix='/')

class Index(twf.FormPage):
    title = 'tw2.forms Validation'
    id = 'index'
    class child(twf.Form):
        class child(twf.TableLayout):
            file = twf.FileField(validator=twf.FileValidator(required=True, extention='.html'))
            email = twf.TextField(validator=twc.EmailValidator(required=True))
#            confirm_email = twf.TextField()
            select = twf.SingleSelectField(options=list(enumerate(opts)), validator=twc.Validator(required=True), item_validator=twc.IntValidator())
#            msel = twf.MultipleSelectField(options=list(enumerate(opts)), validator=twc.Required, item_validator=twc.IntValidator())
#            cbl = twf.CheckBoxList(options=list(enumerate(opts)), validator=twc.Required, item_validator=twc.IntValidator())
#            rbl = twf.RadioButtonList(options=list(enumerate(opts)), validator=twc.Required, item_validator=twc.IntValidator())
#            validator = twc.MatchValidator('email', 'confirm_email')
#            a = twf.CheckBox(validator=twc.BoolValidator(required=True))
#            b = twf.FileField()
#            x = twf.TextField(validator=fe.validators.Regex('^\w+$'))
mw.controllers.register(Index, 'index')

if __name__ == "__main__":
    wrs.make_server('', 8000, mw).serve_forever()
