import tw2.core as twc, re, itertools, webob, cgi

#--
# Basic Fields
#--
class FormField(twc.Widget):
    name = twc.Variable('dom name', request_local=False, attribute=True, default=property(lambda s: s.compound_id))

class InputField(FormField):
    type = twc.Variable('Type of input field', default=twc.Required, attribute=True)
    value = twc.Param(attribute=True)
    template = "tw2.forms.templates.input_field"


class TextField(InputField):
    size = twc.Param('Size of the field', default=None, attribute=True)
    type = 'text'


class TextArea(FormField):
    rows = twc.Param('Number of rows', default=None, attribute=True)
    cols = twc.Param('Number of columns', default=None, attribute=True)
    template = "tw2.forms.templates.textarea"


class CheckBox(InputField):
    type = "checkbox"
    validator = twc.BoolValidator
    def prepare(self):
        super(CheckBox, self).prepare()
        self.safe_modify('attrs')
        self.attrs['checked'] = self.value and 'checked' or None
        self.value = None


class RadioButton(InputField):
    type = "radio"
    checked = twc.Param('Whether the field is selected', attribute=True)


class PasswordField(InputField):
    """
    A password field. This never displays a value passed into the widget,
    although it does redisplay entered values on validation failure. If no
    password is entered, this validates as EmptyField.
    """
    type = 'password'
    def prepare(self):
        super(PasswordField, self).prepare()
        self.safe_modify('attrs')
        self.attrs['value'] = None
    def _validate(self, value, state=None):
        value = super(PasswordField, self)._validate(value, state)
        return value or twc.EmptyField


class FileValidator(twc.Validator):
    """Base class for file validators

    `extension`
        Allowed extension for the file
    """
    extension = None
    msgs = {
        'required': ('file_required', 'Select a file'),
        'badext': "File name must have '$extension' extension",
    }

    def validate_python(self, value, outer_call=None):
        if isinstance(value, cgi.FieldStorage):
            if self.extension is not None and not value.filename.endswith(self.extension):
                raise twc.ValidationError('badext', self)
        elif value:    
            raise twc.ValidationError('corrupt', self)
        elif self.required:
            raise twc.ValidationError('required', self)


class FileField(InputField):
    type = "file"
    validator = FileValidator

    def _validate(self, value, state=None):
        try:
            return super(FileField, self)._validate(value, state)
        except twc.ValidationError:
            self.value = None
            raise


class HiddenField(InputField):
    """
    A hidden field. The default validator avoids the value being included in 
    validated data. This helps prevent against parameter tampering attacks.
    """
    type = 'hidden'
    validator = twc.BlankValidator
    

class LabelField(InputField):
    """
    A read-only label showing the value of a field. The value is stored in a hidden field, so it remains through validation failures. However, the value is never included in validated data.
    """
    type = 'hidden'
    template = "tw2.forms.templates.label_field"
    validator = twc.BlankValidator


class LinkField(twc.Widget):
    """
    A dynamic link based on the value of a field. If either *link* or *text* contain a $, it is replaced with the field value.
    """
    template = "tw2.forms.templates.link_field"
    link = twc.Variable('Link target', default='')
    text = twc.Variable('Link text', default='')
    value = twc.Variable("Value to replace $ with in the link/text")
    validator = twc.BlankValidator

    def prepare(self):
        super(LinkField, self).prepare()
        self.safe_modify('attrs')
        self.attrs['href'] = self.link.replace('$', unicode(self.value or ''))
        self.text = self.value and self.text.replace('$', unicode(self.value)) or ''


class Button(InputField):
    """Generic button. You can override the text using `value` and define a JavaScript action using `attrs['onclick']`.
    """
    type = "button"
    id = None


class SubmitButton(Button):
    """Button to submit a form."""
    type = "submit"
    name = None


class ResetButton(Button):
    """Button to clear the values in a form."""
    type = "reset"


class ImageButton(twc.Link, InputField):
    type = "image"
    width = twc.Param('Width of image in pixels', attribute=True, default=None)
    height = twc.Param('Height of image in pixels', attribute=True, default=None)
    alt = twc.Param('Alternate text', attribute=True, default='')
    src = twc.Variable(attribute=True)

    def prepare(self):
        super(ImageButton, self).prepare()
        self.src = self.link
        self.safe_modify('attrs')
        self.attrs['src'] = self.src # TBD: hack!

#--
# Selection fields
#--
class SelectionField(FormField):
    """
    Base class for single and multiple selection fields.

    The `options` parameter must be a list; it can take several formats:

     * A list of values, e.g.
       ``['', 'Red', 'Blue']``
     * A list of (code, value) tuples, e.g. 
       ``[(0, ''), (1, 'Red'), (2, 'Blue')]``
     * A mixed list of values and tuples. If the code is not specified, it defaults to the value. e.g. 
       ``['', (1, 'Red'), (2, 'Blue')]``
     * Attributes can be specified for individual items, e.g. 
       ``[(1, 'Red', {'style':'background-color:red'})]``
     * A list of groups, e.g. 
       ``[('group1', [(1, 'Red')]), ('group2', ['Pink', 'Yellow'])]``
    """

    options = twc.Param('Options to be displayed')
    prompt_text = twc.Param('Text to prompt user to select an option.', default=None)

    selected_verb = twc.Variable(default='selected')
    field_type = twc.Variable(default=False)
    grouped_options = twc.Variable()

    def prepare(self):
        super(SelectionField, self).prepare()
        options = self.options
        self.options = []
        self.grouped_options = []        
        counter = itertools.count(0)

        for optgroup in self._iterate_options(options):
            opts = []
            group = isinstance(optgroup[1], (list,tuple))
            for option in self._iterate_options(group and optgroup[1] or [optgroup]):
                if len(option) is 2:
                    option_attrs = {}
                elif len(option) is 3:
                    option_attrs = dict(option[2])
                option_attrs['value'] = option[0]
                if self.field_type:
                    option_attrs['type'] = self.field_type
                    option_attrs['name'] = self.compound_id                                    
                    option_attrs['id'] = self.compound_id + ':' + str(counter.next())
                if self._opt_matches_value(option[0]):
                    option_attrs[self.selected_verb] = self.selected_verb
                opts.append((option_attrs, unicode(option[1])))
            self.options.extend(opts)
            if group:
                self.grouped_options.append((unicode(optgroup[0]), opts))            

        if self.prompt_text is not None:
            self.options = [('', self.prompt_text)] + self.options
        if not self.grouped_options:        
            self.grouped_options = [(None, self.options)]
        elif self.prompt_text is not None:
            self.grouped_options = [(None, [('', self.prompt_text)])] + self.grouped_options

    def _opt_matches_value(self, opt):
        return unicode(opt) == self.value

    def _iterate_options(self, optlist):
        for option in optlist:
            if not isinstance(option, (tuple,list)):
                yield (option, option)
            else:
                yield option


class MultipleSelectionField(SelectionField):
    item_validator = twc.Param('Validator that applies to each item', default=None)

    def prepare(self):
        if not self.value:
            self.value = []
        if not isinstance(self.value, (list, tuple)):
            self.value = [self.value]
        if not hasattr(self, '_validated') and self.item_validator:
            self.value = [self.item_validator.from_python(v) for v in self.value]
        super(MultipleSelectionField, self).prepare()

    def _opt_matches_value(self, opt):
        return unicode(opt) in self.value

    def _validate(self, value, state=None):
        if value and not isinstance(value, (list, tuple)):
            value = [value]
        value = [twc.safe_validate(self.item_validator, v) for v in (value or [])]
        return [v for v in value if v is not twc.Invalid]


class SingleSelectField(SelectionField):
    template = "tw2.forms.templates.select_field"
    prompt_text = ''


class MultipleSelectField(MultipleSelectionField):
    size = twc.Param('Number of visible options', default=None, attribute=True)
    multiple = twc.Variable(attribute=True, default='multiple')
    template = "tw2.forms.templates.select_field"


class SelectionList(SelectionField):
    selected_verb = "checked"
    template = "tw2.forms.templates.selection_list"


class RadioButtonList(SelectionList):
    field_type = "radio"


class CheckBoxList(SelectionList, MultipleSelectionField):
    field_type = "checkbox"


class SelectionTable(SelectionField):
    selected_verb = "checked"
    template = "tw2.forms.templates.selection_table"
    cols = twc.Param('Number of columns', default=1)
    options_rows = twc.Variable()
    grouped_options_rows = twc.Variable()

    def _group_rows(self, seq, size):
        if not hasattr(seq, 'next'):
            seq = iter(seq)
        while True:
            chunk = []
            try:
                for i in xrange(size):
                    chunk.append(seq.next())
                yield chunk
            except StopIteration:
                if chunk:
                    yield chunk
                break

    def prepare(self):
        super(SelectionTable, self).prepare()
        self.options_rows = self._group_rows(self.options, self.cols)
        self.grouped_options_rows = [(g, self._group_rows(o, self.cols)) for g, o in self.grouped_options]


class RadioButtonTable(SelectionTable):
    field_type = 'radio'


class CheckBoxTable(SelectionTable, MultipleSelectionField):
    field_type = 'checkbox'


#--
# Layout widgets
#--
class BaseLayout(twc.CompoundWidget):
    """
    The following CSS classes are used, on the element containing both a child widget and its label.

    `odd` / `even`
        On alternating rows. The first row is odd.

    `required`
        If the field is a required field.

    `error`
        If the field contains a validation error.
    """

    label = twc.ChildParam('Label for the field. Auto generates this from the id; None supresses the label.', default=twc.Auto)
    help_text = twc.ChildParam('A longer description of the field', default=None)
    hover_help = twc.Param('Whether to display help text as hover tips', default=False)
    container_attrs = twc.ChildParam('Extra attributes to include in the element containing the widget and its label.', default={})

    resources = [twc.CSSLink(modname='tw2.forms', filename='static/forms.css')]

    @property
    def children_hidden(self):
        return [c for c in self.children if isinstance(c, HiddenField)]

    @property
    def children_non_hidden(self):
        return [c for c in self.children if not isinstance(c, HiddenField)]

    def prepare(self):
        super(BaseLayout, self).prepare()
        for c in self.children:
            if c.label is twc.Auto:
                c.label = c.id and twc.util.name2label(c.id) or ''


class TableLayout(BaseLayout):
    __doc__ = """
    Arrange widgets and labels in a table.
    """ + BaseLayout.__doc__
    template = "tw2.forms.templates.table_layout"


class ListLayout(BaseLayout):
    __doc__ = """
    Arrange widgets and labels in a list.
    """ + BaseLayout.__doc__
    template = "tw2.forms.templates.list_layout"


class RowLayout(BaseLayout):
    """
    Arrange widgets in a table row. This is normally only useful as a child to
    `GridLayout`.
    """
    resources = [
        twc.Link(id='error', modname='tw2.forms', filename='static/dialog-warning.png'),
    ]
    template = "tw2.forms.templates.row_layout"

    def prepare(self):
        row_class = (self.repetition % 2 and 'even') or 'odd'
        if not self.css_class or row_class not in self.css_class:
            self.css_class = ' '.join((self.css_class or '', row_class)).strip()
        super(RowLayout, self).prepare()

class GridLayout(twc.RepeatingWidget):
    """
    Arrange labels and multiple rows of widgets in a grid.
    """
    child = RowLayout
    children = twc.Required
    template = "tw2.forms.templates.grid_layout"


class Spacer(FormField):
    """
    A blank widget, used to insert a blank row in a layout.
    """
    template = "tw2.forms.templates.spacer"
    id = None
    label = None


class Label(twc.Widget):
    """
    A textual label. This disables any label that would be displayed by a parent layout.
    """
    template = 'tw2.forms.templates.label'
    text = twc.Param('Text to appear in label')
    label = None
    id = None


class Form(twc.DisplayOnlyWidget):
    """
    A form, with a submit button. It's common to pass a TableLayout or ListLayout widget as the child.
    """
    template = "tw2.forms.templates.form"
    help_msg = twc.Param('This message displays as a div inside the form', default=None)
    action = twc.Param('URL to submit form data to. If this is None, the form submits to the same URL it was displayed on.', default=None, attribute=True)
    method = twc.Param('HTTP method used for form submission.', default='post', attribute=True)
    submit = twc.Param('Submit button widget. If this is None, no submit button is generated.', default=SubmitButton(id='submit', value='Save'))
    attrs = {'enctype': 'multipart/form-data'}
    id_suffix = 'form'

    @classmethod
    def post_define(cls):
        cls.submit = cls.submit(parent=cls)

    def __init__(self, **kw):
        super(Form, self).__init__(**kw)
        if self.submit:
            self.submit = self.submit.req()

    def prepare(self):
        super(Form, self).prepare()
        if self.submit:
            self.submit.prepare()

class FieldSet(twc.DisplayOnlyWidget):
    """
    A field set. It's common to pass a TableLayout or ListLayout widget as the child.
    """
    template = "tw2.forms.templates.fieldset"
    legend = twc.Param('Text for the legend', default=None)
    id_suffix = 'fieldset'

class TableForm(Form):
    """Equivalent to a Form containing a TableLayout."""
    child = twc.Variable(default=TableLayout)
    children = twc.Required

class ListForm(Form):
    """Equivalent to a Form containing a ListLayout."""
    child = twc.Variable(default=ListLayout)
    children = twc.Required

class TableFieldSet(FieldSet):
    """Equivalent to a FieldSet containing a TableLayout."""
    child = twc.Variable(default=TableLayout)
    children = twc.Required

class ListFieldSet(FieldSet):
    """Equivalent to a FieldSet containing a ListLayout."""
    child = twc.Variable(default=ListLayout)
    children = twc.Required


class FormPage(twc.Page):
    """
    A page that contains a form. The `request` method performs validation,
    redisplaying the form on errors. On success, it calls
    `validated_request`.
    """
    _no_autoid = True

    @classmethod
    def request(cls, req):
        if req.method == 'GET':
            return super(FormPage, cls).request(req)
        elif req.method == 'POST':
            try:
                data = cls.validate(req.POST)
            except twc.ValidationError, e:
                resp = webob.Response(request=req, content_type="text/html; charset=UTF8")
                resp.body = e.widget.display().encode('utf-8')
            else:
                resp = cls.validated_request(req, data)
            return resp

    @classmethod
    def validated_request(cls, req, data):
        resp = webob.Response(request=req, content_type="text/html; charset=UTF8")
        resp.body = 'Form posted successfully'
        if twc.core.request_local()['middleware'].config.debug:
            resp.body += ' ' + repr(data)
        return resp
