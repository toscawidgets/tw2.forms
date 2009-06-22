import webob as wo, wsgiref.simple_server as wrs
import tw2.core as twc, tw2.forms as twf, os
import formencode as fe

opts = ['Red', 'Yellow', 'Green', 'Blue']

mw = twc.TwMiddleware(None, controller_prefix='/')

class Index(twc.Page):
    title = 'Data Grid'
    class child(twf.GridLayout):
        extra_reps = 0
        id = twf.LinkField(link='detail?id=$', text='View', label=None)
        a = twf.LabelField()
        b = twf.LabelField()

    def fetch_data(self, req):
        self.value = [{'id':1, 'a':'paj','b':'bob'}, {'id':2, 'a':'joe','b':'jill'}]


mw.controllers.register(Index, 'index')
wrs.make_server('', 8000, mw).serve_forever()
