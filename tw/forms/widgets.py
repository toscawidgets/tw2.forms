import tw.core as twc, re, itertools


def name2label(name):
    """
    Convert a column name to a Human Readable name.

       1) Convert _ to spaces
       2) Convert CamelCase to Camel Case
       3) Upcase first character of Each Word
    """
    return ' '.join([s.capitalize() for s in
               re.findall(r'([A-Z][a-z0-9]+|[a-z0-9]+|[A-Z0-9]+)', name)])






#--
# Basic Fields
#--
class FormField(twc.Widget):
    name = twc.Variable('dom name', request_local=False, attribute=True, default=property(lambda s: s._compound_id, lambda s, v: 1))


class InputField(FormField):
    type = twc.Variable('Type of input field', default=twc.Required, attribute=True)
    value = twc.Param(attribute=True)
    template = "genshi:tw.forms.templates.input_field"


class TextField(InputField):
    size = twc.Param('Size of the text field', default=None, attribute=True)
    maxlength = twc.Param('Maximum length of input', default=None, attribute=True)
    type = 'text'


class TextArea(FormField):
    rows = twc.Param('Number of rows', default=None, attribute=True)
    cols = twc.Param('Number of columns', default=None, attribute=True)
    template = "genshi:tw.forms.templates.textarea"


class HiddenField(InputField):
    type = 'hidden'


class LabelHiddenField(InputField):
    """
    A hidden field, with a label showing its contents.
    """
    type = 'hidden'
    template = "genshi:tw.forms.templates.label_hidden"


class CheckBox(InputField):
    type = "checkbox"
    #validator = validators.Bool
    def prepare(self):
        super(CheckBox, self).prepare()
        self.attrs['checked'] = 'true' if self.value else None


class RadioButton(InputField):
    type = "radio"


class PasswordField(InputField):
    type = 'password'


class FileField(InputField):
    type = "file"
    # TBD file_upload = True
    # TBD
    def adapt_value(self, value):
        # This is needed because genshi doesn't seem to like displaying
        # cgi.FieldStorage instances
        return None


class Button(InputField):
    """Generic button. You can override the text using :attr:`value` and define
    a JavaScript action using :attr:`attrs['onclick']`.
    """
    type = "button"
    id = None


class SubmitButton(Button):
    """Button to submit a form."""
    type = "submit"
    @classmethod
    def post_define(cls, cls2=None):
        cls = cls2 or cls
        Button.post_define(cls)
        if cls.id_elem == 'submit':
            raise twc.ParameterError("A SubmitButton cannot have the id 'submit'")


class ResetButton(Button):
    """Button to clear the values in a form."""
    type = "reset"


class ImageButton(twc.Link):
    type = "image"
    width = twc.Param('Width of image in pixels', attribute=True, default=None)
    height = twc.Param('Height of image in pixels', attribute=True, default=None)
    alt = twc.Param('Alternate text', attribute=True, default=None)
    src = twc.Variable(attribute=True)
    def prepare(self):
        super(ImageButton, self).prepare()
        self.src = self.link


#--
# Selection fields
#--
class SelectionField(FormField):
    """
    Base class for single and multiple selection fields.
    """

    options = twc.Param('Options to be displayed')

    selected_verb = twc.Variable(default='selected')
    field_type = twc.Variable()
    multiple = twc.Variable(default=False)
    grouped_options = twc.Variable()

    def prepare(self):
        super(SelectionField, self).prepare()
        grouped_options = []
        options = []
        counter = itertools.count(0)
        # TBD: if displaying errors, validate value
        value = self.value
        if self.multiple and not value:
            value = []
        for optgroup in self._iterate_options(self.options):
            xxx = []
            if isinstance(optgroup[1], (list,tuple)):
                group = True
                optlist = optgroup[1][:]
            else:
                group = False
                optlist = [optgroup]
            for option in self._iterate_options(optlist):
                if len(option) is 2:
                    option_attrs = {}
                elif len(option) is 3:
                    option_attrs = dict(option[2])
                option_attrs['value'] = option[0]
                if self.field_type:
                    option_attrs['type'] = self.field_type
                    # TBD: These are only needed for SelectionList
                    option_attrs['name'] = self.id
                    option_attrs['id'] = self.id + ':' + str(counter.next())
                if ((self.multiple and option[0] in value) or
                        (not self.multiple and option[0] == value)):
                    option_attrs[self.selected_verb] = self.selected_verb

                xxx.append((option_attrs, option[1]))
            options.extend(xxx)
            if group:
                grouped_options.append((optgroup[0], xxx))
        # options provides a list of *flat* options leaving out any eventual
        # group, useful for backward compatibility and simpler widgets
        # TBD: needed?
        self.options = options
        self.grouped_options = grouped_options if grouped_options else [(None, options)]


    def _iterate_options(self, optlist):
        for option in optlist:
            if not isinstance(option, (tuple,list)):
                yield (option, option)
            else:
                yield option


class SingleSelectField(SelectionField):
    template = "genshi:tw.forms.templates.select_field"


class MultipleSelectField(SelectionField):
    size = twc.Param('Number of visible options', default=None, attribute=True)
    multiple = twc.Param(default=True, attribute=True)
    template = "genshi:tw.forms.templates.select_field"


class SelectionList(SelectionField):
    selected_verb = "checked"
    template = "genshi:tw.forms.templates.selection_list"


class RadioButtonList(SelectionList):
    field_type = "radio"


class CheckBoxList(SelectionList):
    field_type = "checkbox"
    multiple = True


class SelectionTable(SelectionField):
    field_type = twc.Param()
    selected_verb = "checked"
    template = "genshi:tw.forms.templates.selection_table"
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


class CheckBoxTable(SelectionTable):
    field_type = 'checkbox'
    multiple = True


#--
# Layout widgets
#--
class BaseLayout(twc.CompoundWidget):
    label = twc.ChildParam('Label for the field. If this is None, it is automatically derived from the id.', default=None)
    help_text = twc.ChildParam('A longer description of the field', default=None)
    hover_help = twc.Param('Whether to display help text as hover tips', default=False)
    container_attrs = twc.ChildParam('Extra attributes to include in the element containing the widget and its label.', default=None)

    def prepare(self):
        super(BaseLayout, self).prepare()
        for c in self.children:
            if not c.label:
                c.label = name2label(c.id_elem) if c.id_elem else ''


class TableLayout(BaseLayout):
    """
    Arrange widgets and labels in a table.
    """
    template = "genshi:tw.forms.templates.table_layout"


class ListLayout(BaseLayout):
    """
    Arrange widgets and labels in a list.
    """
    template = "genshi:tw.forms.templates.list_layout"


class GridLayout(twc.RepeatingWidget):
    """
    Arrange labels and multiple rows of widgets in a grid.
    """
    child = twc.Param('Child for this widget. This must be a RowLayout widget.')
    template = "genshi:tw.forms.templates.grid_layout"
    @classmethod
    def post_define(cls, cls2=None):
        cls = cls2 or cls
        twc.RepeatingWidget.post_define(cls)
        if hasattr(cls, 'child') and not issubclass(cls.child, RowLayout):
            raise twc.WidgetError('child for GridLayout must be a RowLayout widget')


class RowLayout(BaseLayout):
    """
    Arrange widgets in a table row. This is normally only useful as a child to
    :class:`GridLayout`.
    """
    template = "genshi:tw.forms.templates.row_layout"


class Spacer(FormField):
    """
    A blank widget, used to insert a blank row in a layout.
    """
    template = "genshi:tw.forms.templates.spacer"
    id = None


class Label(twc.Widget):
    """
    A textual label. This disables any label that would be displayed by a parent layout.
    """
    template = 'genshi:tw.forms.templates.label'
    text = twc.Param('Text to appear in label')
    label = None # suppress a container label
    id = None


class Form(twc.DisplayOnlyWidget):
    """
    A form, with a submit button. It's common to pass a TableLayout or ListLayout widget as the child.
    """
    template = "genshi:tw.forms.templates.form"
    action = twc.Param('URL to submit form data to. If this is None, the form submits to the same URL it was displayed on.', default=None, attribute=True)
    method = twc.Param('HTTP method used for form submission.', default='post', attribute=True)
    submit_text = twc.Param('Text for the submit button. If this is None, no submit button is generated.', default='Save')


class FieldSet(twc.DisplayOnlyWidget):
    """
    A field set. It's common to pass a TableLayout or ListLayout widget as the child.
    """
    template = "genshi:tw.forms.templates.fieldset"
    legend = twc.Param('Text for the legend', default=None)
