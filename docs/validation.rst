Validation
----------

We can configure validation on form fields like this::

    class child(twf.TableForm):
        name = twf.TextField(validator=twc.Required)
        group = twf.SingleSelectField(options=['', 'Red', 'Green', 'Blue'])
        notes = twf.TextArea(validator=twc.StringLengthValidator(min=10))

To enable validation we also need to modify the application to handle POST requests::

    def app(environ, start_response):
        req = wo.Request(environ)
        resp = wo.Response(request=req, content_type="text/html; charset=UTF8")
        if req.method == 'GET':
            resp.body = MyForm.display().encode('utf-8')
        elif req.method == 'POST':
            try:
                data = MyForm.validate(req.POST)
                resp.body = 'Posted successfully ' + wo.html_escape(repr(data))
            except twc.ValidationError, e:
                resp.body = e.widget.display().encode('utf-8')
        return resp(environ, start_response)

If you submit the form with some invalid fields, you should see this:



**Whole Form Message**

If you want to display a message at the top of the form, when there are any errors, define the following validator::

    class MyFormValidator(twc.Validator):
        msgs = {
            'childerror': ('form_childerror', 'There were problems with the details you entered. Review the messages below to correct your submission.'),
        }

And in your form::

    validator = MyFormValidator()
