import wsgiref.simple_server as wrs
import tw2.core as twc, tw2.forms as twf

mw = twc.TwMiddleware(None, controller_prefix='/')

class Index(twf.FormPage):
    id = 'bob'
    title = 'GridLayout Validation'
    class child(twf.Form):
        class child(twf.GridLayout):
            repetitions = 5
            name = twf.TextField(validator=twc.Validator(required=True))
            email = twf.TextField(validator=twc.EmailValidator())

mw.controllers.register(Index, 'index')

if __name__ == '__main__':
    wrs.make_server('', 8000, mw).serve_forever()
