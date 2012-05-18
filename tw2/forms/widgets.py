import tw2.core as twc
import itertools
import webob
import cgi
import math


#--
# Basic Fields
#--
class FormField(twc.Widget):
    name = twc.Variable(
        'dom name',
        request_local=False,
        attribute=True,
        default=property(lambda s: s.compound_id)
    )

    @property
    def required(self):
        return self.validator and (
            getattr(self.validator, 'required', None) or
            getattr(self.validator, 'not_empty', None)
        )


class InputField(FormField):
    type = twc.Variable('Type of input field',
                        default=twc.Required,
                        attribute=True)
    value = twc.Param(attribute=True)
    template = "tw2.forms.templates.input_field"


class PostlabeledInputField(InputField):
    """ Inherits :class:`InputField`, but with a :attr:`text`
    label that follows the input field """
    text = twc.Param('Text to display after the field.')
    text_attrs = twc.Param('Dict of attributes to inject into the label.',
                           default={})
    template = "tw2.forms.templates.postlabeled_input_field"


class TextField(InputField):
    size = twc.Param('Size of the field', default=None, attribute=True)
    placeholder = twc.Param(
        'Placeholder text (HTML5 Only)', attribute=True, default=None)
    type = 'text'


class TextArea(FormField):
    rows = twc.Param('Number of rows', default=None, attribute=True)
    cols = twc.Param('Number of columns', default=None, attribute=True)
    placeholder = twc.Param(
        'Placeholder text (HTML5 Only)', attribute=True, default=None)
    template = "tw2.forms.templates.textarea"


class CheckBox(InputField):
    type = "checkbox"
    validator = twc.BoolValidator

    def prepare(self):
        super(CheckBox, self).prepare()
        self.safe_modify('attrs')
        self.attrs['checked'] = self.value and 'checked' or None
        self.attrs['value'] = None


class RadioButton(InputField):
    type = "radio"
    checked = twc.Param('Whether the field is selected',
                        attribute=True,
                        default=False)


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
    """Validate a file upload field

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
            if self.required and not getattr(value, 'filename', None):
                raise twc.ValidationError('required', self)

            if self.extension is not None and \
               not value.filename.endswith(self.extension):
                raise twc.ValidationError('badext', self)
        elif value:
            raise twc.ValidationError('corrupt', self)
        elif self.required:
            raise twc.ValidationError('required', self)


class FileField(InputField):
    """
    A field for uploading files.  The returned object has (at least) two
    properties of note:

     * filename:
        the name of the uploaded file
     * value:
        a bytestring of the contents of the uploaded file, suitable for being
        written to disk
    """

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
    A hidden field.
    """
    type = 'hidden'


class IgnoredField(HiddenField):
    """
    A hidden field. The value is never included in validated data.
    """
    def _validate(self, value):
        super(IgnoredField, self)._validate(value)
        return twc.EmptyField


class LabelField(InputField):
    """
    A read-only label showing the value of a field. The value is stored in a
    hidden field, so it remains through validation failures. However, the
    value is never included in validated data.
    """
    type = 'hidden'
    template = "tw2.forms.templates.label_field"
    validator = twc.BlankValidator


class LinkField(twc.Widget):
    """
    A dynamic link based on the value of a field. If either *link* or *text*
    contain a $, it is replaced with the field value. If the value is None,
    and there is no default, the entire link is hidden.
    """
    template = "tw2.forms.templates.link_field"
    link = twc.Param('Link target', default='')
    text = twc.Param('Link text', default='')
    value = twc.Param("Value to replace $ with in the link/text")
    validator = twc.BlankValidator

    def prepare(self):
        super(LinkField, self).prepare()
        self.safe_modify('attrs')
        self.attrs['href'] = self.link.replace('$', unicode(self.value or ''))
        self.text = \
                self.value and \
                self.text.replace('$', unicode(self.value)) or \
                ''


class Button(InputField):
    """ Generic button. You can override the text using `value` and define a
    JavaScript action using `attrs['onclick']`.
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
    width = twc.Param('Width of image in pixels',
                      attribute=True,
                      default=None)
    height = twc.Param('Height of image in pixels',
                       attribute=True,
                       default=None)
    alt = twc.Param('Alternate text', attribute=True, default='')
    src = twc.Variable(attribute=True)

    def prepare(self):
        super(ImageButton, self).prepare()
        self.src = self.link
        self.safe_modify('attrs')
        self.attrs['src'] = self.src  # TBD: hack!


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
     * A mixed list of values and tuples. If the code is not specified, it
       defaults to the value. e.g.
       ``['', (1, 'Red'), (2, 'Blue')]``
     * Attributes can be specified for individual items, e.g.
       ``[(1, 'Red', {'style':'background-color:red'})]``
     * A list of groups, e.g.
       ``[('group1', [(1, 'Red')]), ('group2', ['Pink', 'Yellow'])]``
    """

    options = twc.Param('Options to be displayed')
    prompt_text = twc.Param('Text to prompt user to select an option.',
                            default=None)

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
            group = isinstance(optgroup[1], (list, tuple))
            for option in self._iterate_options(
                group and optgroup[1] or [optgroup]):

                if len(option) is 2:
                    option_attrs = {}
                elif len(option) is 3:
                    option_attrs = dict(option[2])
                option_attrs['value'] = option[0]
                if self.field_type:
                    option_attrs['type'] = self.field_type
                    option_attrs['name'] = self.compound_id
                    option_attrs['id'] = ':'.join([
                        self.compound_id, str(counter.next())
                    ])
                if self._opt_matches_value(option[0]):
                    option_attrs[self.selected_verb] = self.selected_verb
                opts.append((option_attrs, option[1]))
            self.options.extend(opts)
            if group:
                self.grouped_options.append((unicode(optgroup[0]), opts))

        if self.prompt_text is not None:
            self.options = [('', self.prompt_text)] + self.options
        if not self.grouped_options:
            self.grouped_options = [(None, self.options)]
        elif self.prompt_text is not None:
            self.grouped_options = \
                    [(None, [('', self.prompt_text)])] + self.grouped_options

    def _opt_matches_value(self, opt):
        return unicode(opt) == unicode(self.value)

    def _iterate_options(self, optlist):
        for option in optlist:
            if not isinstance(option, (tuple, list)):
                yield (option, option)
            else:
                yield option


class MultipleSelectionField(SelectionField):
    item_validator = twc.Param('Validator that applies to each item',
                               default=None)

    def prepare(self):
        if not self.value:
            self.value = []
        if not isinstance(self.value, (list, tuple)):
            self.value = [self.value]
        if not hasattr(self, '_validated') and self.item_validator:
            self.value = [
                self.item_validator.from_python(v) for v in self.value
            ]
        super(MultipleSelectionField, self).prepare()

    def _opt_matches_value(self, opt):
        return unicode(opt) in self.value

    def _validate(self, value, state=None):
        value = value or []
        if not isinstance(value, (list, tuple)):
            value = [value]
        if self.validator:
            self.validator.validate_python(self.validator.to_python(value))
        if self.item_validator:
            value = [twc.safe_validate(self.item_validator, v) for v in value]
        self.value = [v for v in value if v is not twc.Invalid]
        return self.value


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
    name = None


class SeparatedSelectionTable(SelectionList):
    template = "tw2.forms.templates.separated_selection_table"


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
    name = None

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
        self.grouped_options_rows = [
            (g, self._group_rows(o, self.cols))
            for g, o in self.grouped_options
        ]


class VerticalSelectionTable(SelectionField):
    field_type = twc.Variable(default=True)
    selected_verb = "checked"
    template = "tw2.forms.templates.vertical_selection_table"
    cols = twc.Param(
        'Number of columns. If the options are grouped, this is overidden.',
        default=1)
    options_rows = twc.Variable()

    def _gen_row_single(self, single, cols):
        row_count = int(math.ceil(float(len(single)) / float(cols)))
        # This shouldn't really need spacers. It's hackish.
        # (Problem: 4 items in a 3 column table)
        spacer_count = (row_count * cols) - len(single)
        single.extend([(None, None)] * spacer_count)
        col_iters = []
        for i in range(cols):
            start = i * row_count
            col_iters.append(iter(single[start:start + row_count]))

        while True:
            row = []
            try:
                for col_iter in col_iters:
                    row.append(col_iter.next())
                yield row
            except StopIteration:
                if row:
                    yield row
                break

    def _gen_row_grouped(self, grouped_options):
        row_count = max([len(o) for g, o in grouped_options])
        col_iters = []
        for g, o in grouped_options:
            spacer_count = row_count - len(o)
            o.extend([(None, None)] * spacer_count)
            col_iters.append(hasattr(o, 'next') and o or iter(o))

        while True:
            row = []
            try:
                for col_iter in col_iters:
                    row.append(col_iter.next())
                yield row
            except StopIteration:
                if row:
                    yield row
                break

    def prepare(self):
        super(VerticalSelectionTable, self).prepare()
        if self.grouped_options[0][0]:
            self.options_rows = self._gen_row_grouped(self.grouped_options)
        else:
            self.options_rows = self._gen_row_single(self.options, self.cols)


class RadioButtonTable(SelectionTable):
    field_type = 'radio'


class SeparatedRadioButtonTable(SeparatedSelectionTable,
                                MultipleSelectionField):
    field_type = 'radio'


class VerticalRadioButtonTable(VerticalSelectionTable):
    field_type = 'radio'


class CheckBoxTable(SelectionTable,
                    MultipleSelectionField):
    field_type = 'checkbox'


class SeparatedCheckBoxTable(SeparatedSelectionTable,
                             MultipleSelectionField):
    field_type = 'checkbox'


class VerticalCheckBoxTable(VerticalSelectionTable):
    field_type = 'checkbox'
    multiple = True


#--
# Layout widgets
#--
class BaseLayout(twc.CompoundWidget):
    """
    The following CSS classes are used, on the element containing
    both a child widget and its label.

    `odd` / `even`
        On alternating rows. The first row is odd.

    `required`
        If the field is a required field.

    `error`
        If the field contains a validation error.
    """

    label = twc.ChildParam(
        'Label for the field. Auto generates this from the ' +
        'id; None supresses the label.',
        default=twc.Auto)
    help_text = twc.ChildParam('A longer description of the field',
                               default=None)
    hover_help = twc.Param('Whether to display help text as hover tips',
                           default=False)
    container_attrs = twc.ChildParam(
        'Extra attributes to include in the element containing ' +
        'the widget and its label.',
        default={})

    resources = [twc.CSSLink(modname='tw2.forms', filename='static/forms.css')]

    @property
    def children_hidden(self):
        return [c for c in self.children if isinstance(c, HiddenField)]

    @property
    def children_non_hidden(self):
        return [c for c in self.children if not isinstance(c, HiddenField)]

    @property
    def rollup_errors(self):
        errors = [
            c.error_msg for c in self.children
            if isinstance(c, HiddenField) and c.error_msg
        ]
        if self.error_msg:
            errors.insert(0, self.error_msg)
        return errors

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
    :class:`GridLayout`.
    """
    resources = [twc.Link(id='error', modname='tw2.forms',
                          filename='static/dialog-warning.png'),
                ]
    template = "tw2.forms.templates.row_layout"

    def prepare(self):
        row_class = (self.repetition % 2 and 'even') or 'odd'
        if not self.css_class or row_class not in self.css_class:
            self.css_class = ' '.join((
                self.css_class or '', row_class
            )).strip()

        super(RowLayout, self).prepare()


class StripBlanks(twc.Validator):
    def any_content(self, val):
        if type(val) == list:
            for v in val:
                if self.any_content(v):
                    return True
            return False
        elif type(val) == dict:
            for k in val:
                if k == 'id':
                    continue
                if self.any_content(val[k]):
                    return True
            return False
        else:
            return bool(val)

    def to_python(self, value):
        return [v for v in value if self.any_content(v)]


class GridLayout(twc.RepeatingWidget):
    """ Arrange labels and multiple rows of widgets in a grid. """
    child = RowLayout
    children = twc.Required
    template = "tw2.forms.templates.grid_layout"

    def _validate(self, value, state=None):
        return super(GridLayout, self)._validate(
            StripBlanks().to_python(value), state
        )


class Spacer(FormField):
    """ A blank widget, used to insert a blank row in a layout. """
    template = "tw2.forms.templates.spacer"
    id = None
    label = None


class Label(twc.Widget):
    """
    A textual label. This disables any label that would be displayed by
    a parent layout.
    """
    template = 'tw2.forms.templates.label'
    text = twc.Param('Text to appear in label')
    label = None
    id = None


class Form(twc.DisplayOnlyWidget):
    """
    A form, with a submit button. It's common to pass a
    TableLayout or ListLayout widget as the child.
    """
    template = "tw2.forms.templates.form"
    help_msg = twc.Param(
        'This message displays as a div inside the form',
        default=None)
    action = twc.Param(
        'URL to submit form data to. If this is None, the form ' +
        'submits to the same URL it was displayed on.',
        default=None, attribute=True)
    method = twc.Param('HTTP method used for form submission.',
                       default='post', attribute=True)
    submit = twc.Param('Submit button widget. If this is None, no submit ' +
                       'button is generated.',
                       default=SubmitButton(id='submit', value='Save'))
    buttons = twc.Param('List of additional buttons to be placed at the ' +
                        'bottom of the form',
                        default=[])

    attrs = {'enctype': 'multipart/form-data'}
    id_suffix = 'form'

    @classmethod
    def post_define(cls):
        if not cls.buttons:
            cls.buttons = []
        else:
            for b in range(0, len(cls.buttons)):
                if callable(cls.buttons[b]):
                    cls.buttons[b] = cls.buttons[b](parent=cls)

        if cls.submit:
            cls.submit = cls.submit(parent=cls)

    def __init__(self, **kw):
        super(Form, self).__init__(**kw)
        if self.buttons:
            for b in range(0, len(self.buttons)):
                self.buttons[b] = self.buttons[b].req()

        if self.submit:
            self.submit = self.submit.req()

    def prepare(self):
        super(Form, self).prepare()
        if self.buttons and not isinstance(self.buttons, list):
            raise AttributeError("buttons parameter must be a list or None")

        if self.submit and not \
        ['SubmitButton' in repr(b) for b in self.buttons]:
            self.buttons.append(self.submit)

        for b in self.buttons:
            b.prepare()


class FieldSet(twc.DisplayOnlyWidget):
    """
    A field set. It's common to pass a TableLayout or ListLayout
    widget as the child.
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
    A page that contains a form. The :meth:`request` method
    performs validation,
    redisplaying the form on errors. On success, it calls
    :meth:`validated_request`.
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
                resp = webob.Response(
                    request=req,
                    content_type="text/html; charset=UTF8",
                )
                resp.body = e.widget.display().encode('utf-8')
            else:
                resp = cls.validated_request(req, data)
            return resp

    @classmethod
    def validated_request(cls, req, data):
        resp = webob.Response(
            request=req,
            content_type="text/html; charset=UTF8",
        )
        resp.body = 'Form posted successfully'
        if twc.core.request_local()['middleware'].config.debug:
            resp.body += ' ' + repr(data)
        return resp
