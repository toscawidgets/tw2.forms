import webob as wo, wsgiref.simple_server as wrs, sqlite3, sha
import tw.core as twc, tw.forms as twf


class MyForm(twf.TableLayout):
    children = [twf.TextField(id='paj'), twf.TextField(id='joe')]



def simple_app(environ, start_response):
    req = wo.Request(environ)
    resp = wo.Response(request=req, content_type="text/html; charset=UTF8")


    resp.body = 'hello world: ' + MyForm.idisplay().encode('utf-8')
    return resp(environ, start_response)


middleware = twc.TwMiddleware(simple_app)

if __name__ == "__main__":
    wrs.make_server('', 8000, middleware).serve_forever()
