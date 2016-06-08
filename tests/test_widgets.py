from tw2.forms.widgets import *
from tw2.forms.calendars import *
from webob import Request
from webob.multidict import NestedMultiDict
from tw2.core.testbase import (
    assert_in_xml, assert_eq_xml,
    WidgetTest as _WidgetTest,
    TW2WidgetBuilder
)
from nose.tools import raises
from six.moves import StringIO
from tw2.core import EmptyField, IntValidator, ValidationError, BoolValidator
from tw2.core.middleware import make_middleware
from cgi import FieldStorage
from datetime import datetime
import six

try:
    from webob import NestedMultiDict
except ImportError:
    from webob.multidict import NestedMultiDict


class WidgetTest(_WidgetTest):
    """ Constrain tests to only run against mako and genshi.

    Even though tw2.core supports rendering widgets with templates written in
    mako, genshi, kajiki, jinja2, and chameleon, here we only run tests against
    the first two since those are the only templates provided by tw2.forms
    itself.
    """
    engines = ['mako', 'jinja', 'kajiki']


class TestInputField(WidgetTest):
    widget = InputField
    attrs = {'type': 'foo', 'css_class': 'something'}
    params = {'value': 6}
    expected = '<input type="foo" class="something" value="6"/>'

    def test_empty_value(self):
        attrs = {'type': 'email'}
        params = {'value': ''}
        expected = '<input type="email" value="" />'
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, attrs, params, expected)


class TestTextField(WidgetTest):
    widget = TextField
    attrs = {'css_class': 'something', 'size': '60',
        'placeholder': "Search..."}
    params = {'value': 6}
    expected = """<input type="text" class="something"
        placeholder="Search..." value="6" size="60"/>"""


class TestTextArea(WidgetTest):
    widget = TextArea
    attrs = {'css_class': 'something', 'rows': 6, 'cols': 10}
    params = {'value': '6'}
    expected = '<textarea class="something" rows="6" cols="10">6</textarea>'


class TestCheckbox(WidgetTest):
    widget = CheckBox
    attrs = {'css_class': 'something'}
    params = {'value': True}
    expected = '<input checked="checked" type="checkbox" class="something"/>'

    def test_value_false(self):
        params = {'value': False}
        expected = '<input type="checkbox" class="something">'
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, self.attrs, params, expected)

    def test_renders_correctly_after_failed_validation(self):
        try:
            w = self.widget(id='x', validator=BoolValidator(required=True)).validate({'x': ''})
        except ValidationError as e:
            # Should correctly render to be able to display validation error
            e.widget.display()
        else:
            raise Exception('Should have raised validation error!')


class TestRadioButton(WidgetTest):
    widget = RadioButton
    attrs = {'css_class': 'something'}
    params = {'checked': None}
    expected = '<input type="radio" class="something"/>'

    def test_checked(self):
        params = {'checked': True}
        expected = '<input checked="checked" type="radio" class="something"/>'
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, self.attrs, params, expected)


class TestPasswordField(WidgetTest):
    widget = PasswordField
    attrs = {'css_class': 'something', 'id': 'hid'}
    expected = '<input type="password" class="something" id="hid" name="hid"/>'
    validate_params = [[None, {'hid':'b'}, 'b']]

    def test_no_value(self):
        params = {'value': 'something'}
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, self.attrs, params, self.expected)


class TestFileField(WidgetTest):
    widget = FileField
    attrs = {'css_class': 'something', 'id': 'hid',
        'validator': FileValidator(extension="bdb", required=True)}
    expected = """<input id="hid" type="file"
        class="something" value="" name="hid"/>"""
    dummy_file = FieldStorage(StringIO(''))
    dummy_file.filename = 'something.ext'
    validate_params = [
        [None, {'hid': 'b'}, None, ValidationError],
        [None, {'hid': dummy_file}, None, ValidationError],
    ]


class TestHiddenField(WidgetTest):
    widget = HiddenField
    attrs = {'css_class': 'something', 'value': 'info',
        'name': 'hidden_name', 'id': 'hid'}
    expected = """<input class="something" type="hidden"
        id="hid" value="info" name="hidden_name"/>"""
    validate_params = [[None, {'hid': 'b'}, 'b']]


class TestLabelField(WidgetTest):
    widget = LabelField
    attrs = {'css_class': 'something', 'value': 'info',
        'name': 'hidden_name', 'id': 'hid'}
    expected = """<span>info<input class="something" type="hidden"
        value="info" name="hidden_name" id="hid"/></span>"""
    validate_params = [[None, {'hid': 'b'}, EmptyField]]

    def test_escape(self):
        attrs = {'value': 'line 1<br />line 2'}
        expected = '<span>line 1&lt;br /&gt;line 2<input value="line 1&lt;br /&gt;line 2" type="hidden"/></span>'
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, attrs, self.params, expected)

        attrs = {'value': 'line 1<br />line 2', 'escape': False}
        expected = '<span>line 1<br />line 2<input value="line 1<br />line 2" type="hidden"/></span>'
        for engine in self._get_all_possible_engines():
            if engine == 'kajiki':
                # Kajiki has no support for escape: False
                continue
            yield (self._check_rendering_vs_expected,
                engine, attrs, self.params, expected)


class TestLinkField(WidgetTest):
    widget = LinkField
    attrs = {'css_class': 'something', 'value': 'info',
        'name': 'hidden_name', 'text': 'some $', 'link': '/some/$'}
    expected = """<a href="/some/info" class="something">some info</a>"""

    def test_escape(self):
        attrs = {'text': 'line 1<br />line 2'}
        expected = '<a href="">line 1&lt;br /&gt;line 2</a>'
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, attrs, self.params, expected)

        attrs = {'text': 'line 1<br />line 2', 'escape': False}
        expected = '<a href="">line 1<br />line 2</a>'
        for engine in self._get_all_possible_engines():
            if engine == 'kajiki':
                # Kajiki has no support for escape: False
                continue
            yield (self._check_rendering_vs_expected,
                engine, attrs, self.params, expected)


class TestButton(WidgetTest):
    widget = Button
    attrs = {'css_class': 'something', 'value': 'info', 'name': 'hidden_name'}
    expected = """<input class="something" type="button"
        value="info" name="hidden_name"/>"""


class TestSubmitButton(WidgetTest):
    widget = SubmitButton
    attrs = {'css_class': 'something', 'value': 'info', 'name': 'hidden_name'}
    expected = """<input class="something" type="submit"
        value="info" name="hidden_name"/>"""


class TestResetButton(WidgetTest):
    widget = ResetButton
    attrs = {'css_class': 'something',
        'value': 'info', 'name': 'hidden_name'}
    expected = """<input class="something" type="reset"
        value="info" name="hidden_name"/>"""


class TestImageButton(WidgetTest):
    widget = ImageButton
    attrs = {'css_class': 'something',
        'value': 'info', 'name': 'hidden_name', 'link': '/somewhere.gif'}
    expected = """<input src="/somewhere.gif" name="hidden_name"
        value="info" alt="" type="image" class="something"/>"""


class TestSingleSelectField(WidgetTest):
    widget = SingleSelectField
    attrs = {'css_class': 'something',
        'options': ((1, 'a'), (2, 'b'), (3, 'c')), 'id': 'hid',
        'validator': IntValidator()}
    expected = """<select class="something" id="hid" name="hid">
            <option value=""></option>
            <option value="1">a</option>
            <option value="2">b</option>
            <option value="3">c</option>
        </select>"""
    validate_params = [[None, {'hid':''}, None], [None, {'hid':'1'}, 1]]

    def test_option_group(self):
        expected = """<select class="something">
                <option value="">PROMPT_TEXT</option>
                <optgroup label="group">
                    <option value=""></option>
                    <option value="1">Red</option>
                    <option value="2">Blue</option>
                </optgroup>
                <optgroup label="group2">
                    <option value=""></option>
                    <option value="Pink">Pink</option>
                    <option value="Yellow">Yellow</option>
                </optgroup>
            </select>"""
        attrs = {'css_class': 'something',
                 'prompt_text': 'PROMPT_TEXT',
                 'options': [
            ('group', ['', (1, 'Red'), (2, 'Blue')]),
            ('group2', ['', 'Pink', 'Yellow'])]}
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, attrs, self.params, expected)

    def test_option_no_values(self):
        expected = """<select class="something">
                <option value=""></option>
                <option value="a">a</option>
                <option value="b">b</option>
                <option value="c">c</option>
            </select>"""
        attrs = {'css_class': 'something', 'options': ('a', 'b', 'c')}
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, attrs, self.params, expected)

    def test_prompt_text(self):
        expected = """<select>
                <option value="">Pick one:</option>
                <option value="a">a</option>
                <option value="b">b</option>
                <option value="c">c</option>
            </select>"""
        attrs = {'options': ('a', 'b', 'c'), 'prompt_text': 'Pick one:'}
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, attrs, self.params, expected)

    def test_no_options(self):
        expected = """<select><option value=""/></select>"""
        attrs = {'options': []}
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, attrs, self.params, expected)


class TestMultipleSelectField(WidgetTest):
    widget = MultipleSelectField
    attrs = {'css_class': 'something',
        'options': (('a', '1'), ('b', '2'), ('c', '3')), 'id': 'hid'}
    expected = """
        <select class="something" multiple="multiple" id="hid" name="hid">
            <option value="a">1</option>
            <option value="b">2</option>
            <option value="c">3</option>
        </select>"""
    validate_params = [[None, {'hid': 'b'}, [six.u('b')]]]


class TestSelectionList(WidgetTest):

    widget = SelectionList
    attrs = {'css_class': 'something', 'field_type': 'test',
        'options': (('a', '1'), ('b', '2'), ('c', '3')), 'id': 'something'}
    expected = """<ul class="something" id="something">
        <li>
            <input type="test" name="something" value="a" id="something:0"/>
            <label for="something:0">1</label>
        </li><li>
            <input type="test" name="something" value="b" id="something:1"/>
            <label for="something:1">2</label>
        </li><li>
            <input type="test" name="something" value="c" id="something:2"/>
            <label for="something:2">3</label>
        </li></ul>"""


class TestRadioButtonList(WidgetTest):

    widget = RadioButtonList
    attrs = {'css_class': 'something',
        'options': (('a', '1'), ('b', '2'), ('c', '3')), 'id': 'something'}
    expected = """<ul class="something" id="something">
        <li>
            <input type="radio" name="something" value="a" id="something:0"/>
            <label for="something:0">1</label>
        </li><li>
            <input type="radio" name="something" value="b" id="something:1"/>
            <label for="something:1">2</label>
        </li><li>
            <input type="radio" name="something" value="c" id="something:2"/>
            <label for="something:2">3</label>
        </li></ul>"""


class TestCheckBoxList(WidgetTest):

    widget = CheckBoxList
    attrs = {'css_class': 'something',
        'options': (('a', '1'), ('b', '2'), ('c', '3')), 'id': 'something'}
    expected = """<ul class="something" id="something">
        <li>
            <input type="checkbox"
                name="something" value="a" id="something:0"/>
            <label for="something:0">1</label>
        </li><li>
            <input type="checkbox"
                name="something" value="b" id="something:1"/>
            <label for="something:1">2</label>
        </li><li>
            <input type="checkbox"
                name="something" value="c" id="something:2"/>
            <label for="something:2">3</label>
        </li></ul>"""

    def test_option_has_value(self):
        expected = """<ul class="something" id="something">
            <li>
                <input type="checkbox"
                    name="something" value="a" id="something:0" checked/>
                <label for="something:0">a</label>
            </li><li>
                <input type="checkbox"
                    name="something" value="b" id="something:1"/>
                <label for="something:1">b</label>
            </li><li>
                <input type="checkbox"
                    name="something" value="c" id="something:2"/>
                <label for="something:2">c</label>
            </li></ul>"""
        attrs = {'css_class': 'something',
            'options': ('a', 'b', 'c'), 'id': 'something'}
        params = {'value': 'a'}
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, attrs, params, expected)


class TestSelectionTable(WidgetTest):

    widget = SelectionTable
    attrs = {'css_class': 'something', 'field_type': 'test',
        'options': (('a', '1'), ('b', '2'), ('c', '3')), 'id': 'something'}
    expected = """<table class="something" id="something"><tbody>
        <tr>
            <td>
                <input type="test" name="something" value="a" id="something:0"/>
                <label for="something:0">1</label>
            </td>
        </tr><tr>
            <td>
                <input type="test" name="something" value="b" id="something:1"/>
                <label for="something:1">2</label>
            </td>
        </tr><tr>
            <td>
                <input type="test" name="something" value="c" id="something:2"/>
                <label for="something:2">3</label>
            </td>
        </tr>
        </tbody></table>"""

    def test_option_leftover_chunk(self):
        expected = """<table class="something" id="something"><tbody>
            <tr>
                <td>
                    <input type="test"
                        checked name="something" value="a" id="something:0"/>
                    <label for="something:0">a</label>
                </td><td>
                    <input type="test"
                        name="something" value="b" id="something:1"/>
                    <label for="something:1">b</label>
                </td>
            </tr><tr>
                <td>
                    <input type="test"
                        name="something" value="c" id="something:2"/>
                    <label for="something:2">c</label>
                </td>
                <td></td>
            </tr>
            </tbody></table>"""
        attrs = {'css_class': 'something', 'field_type': 'test', 'cols': 2,
            'options': (('group1', ('a', 'b')), 'c'), 'id': 'something'}
        params = {'value': 'a'}
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, attrs, params, expected)


class TestRadioButtonTable(WidgetTest):

    widget = RadioButtonTable
    attrs = {'css_class': 'something',
        'options': (('a', '1'), ('b', '2'), ('c', '3')), 'id': 'something'}
    expected = """<table class="something" id="something">
    <tbody>
    <tr>
        <td>
            <input type="radio" name="something" value="a" id="something:0"/>
            <label for="something:0">1</label>
        </td>
    </tr><tr>
        <td>
            <input type="radio" name="something" value="b" id="something:1"/>
            <label for="something:1">2</label>
        </td>
    </tr><tr>
        <td>
            <input type="radio" name="something" value="c" id="something:2"/>
            <label for="something:2">3</label>
        </td>
    </tr>
    </tbody>
</table>"""


class TestCheckBoxTable(WidgetTest):

    widget = CheckBoxTable
    attrs = {'css_class': 'something',
        'options': (('a', '1'), ('b', '2'), ('c', '3')), 'id': 'something'}
    expected = """<table class="something" id="something"><tbody>
        <tr>
            <td>
                <input type="checkbox"
                    name="something" value="a" id="something:0"/>
                <label for="something:0">1</label>
            </td>
        </tr><tr>
            <td>
                <input type="checkbox"
                    name="something" value="b" id="something:1"/>
                <label for="something:1">2</label>
            </td>
        </tr><tr>
            <td>
                <input type="checkbox"
                    name="something" value="c" id="something:2"/>
                <label for="something:2">3</label>
            </td>
        </tr>
        </tbody></table>"""


class TestListLayout(WidgetTest):

    widget = ListLayout
    attrs = {'children': [
        TextField(id='field1'),
        TextField(id='field2'),
        TextField(id='field3')]}
    expected = """<ul>
        <li id="field1:container" class="odd">
            <label for="field1">Field1</label>
            <input name="field1" id="field1" type="text"/>
            <span id="field1:error" class="error"></span>
        </li><li id="field2:container" class="even">
            <label for="field2">Field2</label>
            <input name="field2" id="field2" type="text"/>
            <span id="field2:error" class="error"></span>
        </li><li id="field3:container" class="odd">
            <label for="field3">Field3</label>
            <input name="field3" id="field3" type="text"/>
            <span id="field3:error" class="error"></span>
        </li><li class="error">
            <span id=":error" class="error"></span>
        </li></ul>"""
    declarative = True


class TestListLayoutErrors(TestListLayout):

    attrs = {'children': [TextField(id='field1'), ],
             'error_msg': 'bogus error'}
    expected = """<ul>
        <li id="field1:container" class="odd">
            <label for="field1">Field1</label>
            <input name="field1" id="field1" type="text"/>
            <span id="field1:error" class="error"></span>
        </li><li class="error">
            <span id=":error" class="error"><p>bogus error</p></span>
        </li></ul>"""


class TestTableLayout(WidgetTest):

    widget = TableLayout
    attrs = {'children': [
        TextField(id='field1'),
        TextField(id='field2'),
        TextField(id='field3')]}
    expected = """<table>
        <tr class="odd" id="field1:container">
            <th><label for="field1">Field1</label></th>
            <td>
                <input name="field1" id="field1" type="text"/>
                <span id="field1:error"></span>
            </td>
        </tr><tr class="even" id="field2:container">
            <th><label for="field2">Field2</label></th>
            <td>
                <input name="field2" id="field2" type="text"/>
                <span id="field2:error"></span>
            </td>
        </tr><tr class="odd" id="field3:container">
            <th><label for="field3">Field3</label></th>
            <td>
                <input name="field3" id="field3" type="text"/>
                <span id="field3:error"></span>
            </td>
        </tr><tr class="error"><td colspan="2">
            <span id=":error"></span></td>
        </tr></table>"""
    declarative = True

    def test_required(self):
        attrs = {'children': [TextField(id='field1', validator=twc.Required)]}
        expected = """<table>
            <tr class="odd required" id="field1:container">
                <th><label for="field1">Field1</label></th>
                <td>
                    <input name="field1" id="field1" type="text" value=""/>
                    <span id="field1:error"></span>
                </td>
            </tr><tr class="error"><td colspan="2">
                <span id=":error"></span></td>
            </tr></table>"""
        params = {'value': None}
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, attrs, params, expected)

    def test_fe_not_required(self):
        try:
            import formencode
        except ImportError as e:
            self.skipTest(str(e))
        attrs = {'children': [TextField(id='field1',
            validator=formencode.FancyValidator(not_empty=False))]}
        expected = """<table>
            <tr class="odd" id="field1:container">
                <th><label for="field1">Field1</label></th>
                <td>
                    <input name="field1" id="field1" type="text"/>
                    <span id="field1:error"></span>
                </td>
            </tr><tr class="error"><td colspan="2">
                <span id=":error"></span></td>
            </tr></table>"""
        params = {'value': None}
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, attrs, params, expected)

    def test_fe_required(self):
        try:
            import formencode
        except ImportError as e:
            self.skipTest(str(e))
        attrs = {'children': [TextField(id='field1',
            validator=formencode.FancyValidator(not_empty=True))]}
        expected = """<table>
            <tr class="odd required" id="field1:container">
                <th><label for="field1">Field1</label></th>
                <td>
                    <input name="field1" id="field1" type="text"/>
                    <span id="field1:error"></span>
                </td>
            </tr><tr class="error"><td colspan="2">
                <span id=":error"></span></td>
            </tr></table>"""
        params = {'value': None}
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, attrs, params, expected)


class TestRowLayout(WidgetTest):

    widget = RowLayout
    attrs = {
        'children': [
            TextField(id='field1'),
            TextField(id='field2'),
            TextField(id='field3')],
        'repetition': 1}
    expected = """<tr class="even">
        <td id="field1:container">
            <input name="field1" id="field1" type="text"/>
        </td><td id="field2:container">
            <input name="field2" id="field2" type="text"/>
        </td><td id="field3:container">
            <input name="field3" id="field3" type="text"/>
        </td><td>
        </td></tr>"""
    declarative = True


class TestGridLayout(WidgetTest):

    widget = GridLayout
    attrs = {'id': 'grid',
        'children': [
            TextField(id='field1'),
            TextField(id='field2'),
            TextField(id='field3')],
        'repetition': 1,
    }
    expected = """<table id="grid">
        <tr><th>Field1</th><th>Field2</th><th>Field3</th></tr>
        <tr class="error"><td colspan="0" id="grid:error">
        </td></tr>
        </table>"""
    declarative = True
    validate_params = [[
        None,
        {'grid:0:field1': 'something', 'grid:0:field2': 'something','grid:0:field3': 'something'},
        [{'field1': 'something', 'field2': 'something','field3': 'something'}],
        None,
    ]]


class TestSpacer(WidgetTest):

    widget = Spacer
    attrs = {}
    expected = """<div></div>"""


def test_spacer_validation():
    """Test that spacers don't inject None keys in validated data."""

    class SomeForm(TableForm):
        some_id = HiddenField
        space = Spacer

    data = SomeForm.validate({})

    assert None not in data


class TestLabel(WidgetTest):

    widget = Label
    attrs = {'text': 'something'}
    expected = """<span>something</span>"""

    def test_escape(self):
        attrs = {'text': 'line 1<br />line 2'}
        expected = '<span>line 1&lt;br /&gt;line 2</span>'
        for engine in self._get_all_possible_engines():
            yield (self._check_rendering_vs_expected,
                engine, attrs, self.params, expected)

        attrs = {'text': 'line 1<br />line 2', 'escape': False}
        expected = '<span>line 1<br />line 2</span>'
        for engine in self._get_all_possible_engines():
            if engine == 'kajiki':
                # Kajiki has no support for escape: False
                continue
            yield (self._check_rendering_vs_expected,
                engine, attrs, self.params, expected)


class TestForm(WidgetTest):

    widget = Form
    attrs = {'child': TableLayout(field1=TextField(id='field1')),
        'buttons': [SubmitButton, ResetButton()]}
    expected = """<form enctype="multipart/form-data" method="post">
        <span class="error"></span>
        <table>
            <tr class="odd" id="field1:container">
                <th><label for="field1">Field1</label></th>
                <td >
                    <input name="field1" type="text" id="field1"/>
                    <span id="field1:error"></span>
                </td>
            </tr><tr class="error"><td colspan="2">
                <span id=":error"></span>
            </td></tr>
        </table>
        <input type="submit"/>
        <input type="reset"/>
        </form>"""
    declarative = True


class TestTableForm(WidgetTest):

    widget = TableForm
    attrs = {
        'field1': TextField(id='field1'),
        'field2': TextField(id='field2'),
        'field3': TextField(id='field3')}
    expected = """<form method="post" enctype="multipart/form-data">
        <span class="error"></span>
        <table>
            <tr class="odd" id="field1:container">
                <th><label for="field1">Field1</label></th>
                <td>
                    <input name="field1" id="field1" type="text"/>
                    <span id="field1:error"></span>
                </td>
            </tr><tr class="even" id="field2:container">
                <th><label for="field2">Field2</label></th>
                <td>
                    <input name="field2" id="field2" type="text"/>
                    <span id="field2:error"></span>
                </td>
            </tr><tr class="odd" id="field3:container">
                <th><label for="field3">Field3</label></th>
                <td>
                    <input name="field3" id="field3" type="text"/>
                    <span id="field3:error"></span>
                </td>
            </tr><tr class="error"><td colspan="2">
                <span id=":error"></span>
            </td></tr>
        </table>
        <input type="submit" value="Save"/>
        </form>"""
    declarative = True


class TestListForm(WidgetTest):

    widget = ListForm
    attrs = {
        'field1': TextField(id='field1'),
        'field2': TextField(id='field2'),
        'field3': TextField(id='field3')}
    expected = """<form method="post" enctype="multipart/form-data">
        <span class="error"></span>
        <ul >
            <li id="field1:container" class="odd">
             <label for="field1">Field1</label>
                <input name="field1" id="field1" type="text"/>
                <span id="field1:error" class="error"></span>
            </li>
            <li id="field2:container" class="even">
             <label for="field2">Field2</label>
                <input name="field2" id="field2" type="text"/>
                <span id="field2:error" class="error"></span>
            </li>
            <li id="field3:container" class="odd">
             <label for="field3">Field3</label>
                <input name="field3" id="field3" type="text"/>
                <span id="field3:error" class="error"></span>
            </li>
            <li class="error"><span id=":error" class="error"></span></li>
        </ul>
        <input type="submit" value="Save"/>
        </form>"""
    declarative = True


class TestTableFieldset(WidgetTest):

    widget = TableFieldSet
    attrs = {
        'field1': TextField(id='field1'),
        'field2': TextField(id='field2'),
        'field3': TextField(id='field3')}
    expected = """<fieldset>
        <legend></legend>
        <table>
            <tr class="odd" id="field1:container">
                <th><label for="field1">Field1</label></th>
                <td>
                    <input name="field1" id="field1" type="text"/>
                    <span id="field1:error"></span>
                </td>
            </tr><tr class="even" id="field2:container">
                <th><label for="field2">Field2</label></th>
                <td>
                    <input name="field2" id="field2" type="text"/>
                    <span id="field2:error"></span>
                </td>
            </tr><tr class="odd" id="field3:container">
                <th><label for="field3">Field3</label></th>
                <td>
                    <input name="field3" id="field3" type="text"/>
                    <span id="field3:error"></span>
                </td>
            </tr><tr class="error"><td colspan="2">
                <span id=":error"></span>
            </td></tr>
        </table>
        </fieldset>"""
    declarative = True


class TestTableFieldsetWithFEValidator(WidgetTest):

    try:
        from formencode.national import USPostalCode as FEValidator
    except ImportError as e:
        FEValidator = IntValidator
    widget = TableFieldSet
    attrs = {
        'field1': TextField(id='field1'),
        'field2': TextField(id='field2'),
        'field3': TextField(id='field3', validator=FEValidator())}
    expected = """<fieldset>
        <legend></legend>
        <table>
            <tr class="odd" id="field1:container">
                <th><label for="field1">Field1</label></th>
                <td>
                    <input name="field1" id="field1" type="text"/>
                    <span id="field1:error"></span>
                </td>
            </tr><tr class="even" id="field2:container">
                <th><label for="field2">Field2</label></th>
                <td>
                    <input name="field2" id="field2" type="text"/>
                    <span id="field2:error"></span>
                </td>
            </tr><tr class="odd" id="field3:container">
                <th><label for="field3">Field3</label></th>
                <td>
                    <input name="field3" id="field3" type="text"/>
                    <span id="field3:error"></span>
                </td>
            </tr><tr class="error"><td colspan="2">
                <span id=":error"></span>
            </td></tr>
        </table>
        </fieldset>"""
    declarative = True

    def setUp(self):
        if self.FEValidator is IntValidator:
            self.skipTest('Cannot import FormEncode validator')
        super(TestTableFieldsetWithFEValidator, self).setUp()


class TestListFieldset(WidgetTest):

    widget = ListFieldSet
    attrs = {
        'field1': TextField(id='field1'),
        'field2': TextField(id='field2'),
        'field3': TextField(id='field3')}
    expected = """<fieldset>
        <legend></legend>
        <ul >
            <li id="field1:container" class="odd">
             <label for="field1">Field1</label>
                <input name="field1" id="field1" type="text"/>
                <span id="field1:error" class="error"></span>
            </li>
            <li id="field2:container" class="even">
             <label for="field2">Field2</label>
                <input name="field2" id="field2" type="text"/>
                <span id="field2:error" class="error"></span>
            </li>
            <li id="field3:container" class="odd">
             <label for="field3">Field3</label>
                <input name="field3" id="field3" type="text"/>
                <span id="field3:error" class="error"></span>
            </li>
            <li class="error"><span id=":error" class="error"></span></li>
        </ul>
        </fieldset>"""
    declarative = True


class TestFormPage(WidgetTest):

    widget = FormPage
    attrs = {
        'child': TableForm(children=[
            TextField(id='field1'),
            TextField(id='field2'),
            TextField(id='field3')]),
        'title': 'some title'}

    expected = """<html>
        <head><title>some title</title></head>
        <body id="mytestwidget:page">
            <h1>some title</h1>
            <form method="post"
                    id="mytestwidget:form" enctype="multipart/form-data">
                <span class="error"></span>
                <table id="mytestwidget">
                    <tr class="odd" id="mytestwidget:field1:container">
                        <th><label for="field1">Field1</label></th>
                        <td>
                            <input name="mytestwidget:field1"
                                id="mytestwidget:field1" type="text"/>
                            <span id="mytestwidget:field1:error"></span>
                        </td>
                    </tr><tr class="even" id="mytestwidget:field2:container">
                        <th><label for="field2">Field2</label></th>
                        <td>
                            <input name="mytestwidget:field2"
                                id="mytestwidget:field2" type="text"/>
                            <span id="mytestwidget:field2:error"></span>
                        </td>
                    </tr><tr class="odd" id="mytestwidget:field3:container">
                        <th><label for="field3">Field3</label></th>
                        <td>
                            <input name="mytestwidget:field3"
                                id="mytestwidget:field3" type="text"/>
                            <span id="mytestwidget:field3:error"></span>
                        </td>
                    </tr><tr class="error"><td colspan="2">
                        <span id="mytestwidget:error"></span>
                    </td></tr>
                </table>
            <input type="submit" value="Save" />
            </form>
        </body>
        </html>"""

    declarative = True

    def setUp(self):
        self.widget = TW2WidgetBuilder(self.widget, **self.attrs)
        self.mw = make_middleware(None, {})

    def test_request_get(self):
        environ = {'REQUEST_METHOD': 'GET'}
        req = Request(environ)
        r = self.widget().request(req)
        assert_eq_xml(r.body, """<html>
            <head><title>some title</title></head>
            <body id="mytestwidget:page">
                <h1>some title</h1>
                <form method="post"
                        id="mytestwidget:form" enctype="multipart/form-data">
                    <span class="error"></span>
                    <table id="mytestwidget">
                        <tr class="odd" id="mytestwidget:field1:container">
                            <th><label for="field1">Field1</label></th>
                            <td>
                                <input name="mytestwidget:field1"
                                    id="mytestwidget:field1" type="text"/>
                                <span id="mytestwidget:field1:error"></span>
                            </td>
                        </tr><tr class="even"
                                id="mytestwidget:field2:container">
                            <th><label for="field2">Field2</label></th>
                            <td>
                                <input name="mytestwidget:field2"
                                    id="mytestwidget:field2" type="text"/>
                                <span id="mytestwidget:field2:error"></span>
                            </td>
                        </tr><tr class="odd"
                                id="mytestwidget:field3:container">
                            <th><label for="field3">Field3</label></th>
                            <td>
                                <input name="mytestwidget:field3"
                                    id="mytestwidget:field3" type="text"/>
                                <span id="mytestwidget:field3:error"></span>
                            </td>
                        </tr><tr class="error"><td colspan="2">
                            <span id="mytestwidget:error"></span>
                        </td></tr>
                    </table>
                    <input type="submit" value="Save"/>
                </form>
            </body></html>""")

    def _test_request_post_invalid(self):
        # i have commented this because the post is in fact
        # valid, there are no arguments sent to the post, but the
        # widget does not require them
        environ = {'REQUEST_METHOD': 'POST',
            'wsgi.input': StringIO('')}
        req = Request(environ)
        r = self.widget().request(req)
        assert_eq_xml(r.body, """<html>
            <head><title>some title</title></head>
            <body id="mytestwidget:page">
                <h1>some title</h1>
                <form method="post"
                        id="mytestwidget:form" enctype="multipart/form-data">
                    <span class="error"></span>
                    <table id="mytestwidget">
                        <tr class="odd" id="mytestwidget:field1:container">
                            <th><label for="field1">Field1</label></th>
                            <td>
                                <input name="mytestwidget:field1"
                                    id="mytestwidget:field1" type="text"/>
                                <span id="mytestwidget:field1:error"></span>
                            </td>
                        </tr><tr class="even"
                                id="mytestwidget:field2:container">
                            <th><label for="field2">Field2</label></th>
                            <td>
                                <input name="mytestwidget:field2"
                                    id="mytestwidget:field2" type="text"/>
                                <span id="mytestwidget:field2:error"></span>
                            </td>
                        </tr><tr class="odd"
                                id="mytestwidget:field3:container">
                            <th><label for="field3">Field3</label></th>
                            <td>
                                <input name="mytestwidget:field3"
                                    id="mytestwidget:field3" type="text"/>
                                <span id="mytestwidget:field3:error"></span>
                            </td>
                        </tr><tr class="error"><td colspan="2">
                            <span id="mytestwidget:error"></span>
                        </td></tr>
                    </table>
                    <input type="submit" value="Save"/>
                </form>
            </body></html>""")

    def test_request_post_valid(self):
        environ = {'wsgi.input': StringIO('')}
        req = Request(environ)
        req.method = 'POST'
        attr = six.PY3 and "text" or "body"
        setattr(req, attr, ('mytestwidget:field1=a&mytestwidget'
            ':field2=b&mytestwidget:field3=c'))
        req.environ['CONTENT_LENGTH'] = str(len(req.body))
        req.environ['CONTENT_TYPE'] = 'application/x-www-form-urlencoded'

        self.mw.config.debug = True
        r = self.widget().request(req)
        target = six.b(
            "Form posted successfully {'field2': 'b', 'field3': 'c', 'field1': 'a'}"
        )
        assert(target in r.body, r.body)


def test_picker_validation():
    """ Test that CalendarDate*Pickers validate correctly. """

    class SomeForm(TableForm):
        date = CalendarDatePicker(date_format='%Y-%m-%d')
        datetime = CalendarDateTimePicker(date_format='%Y-%m-%d %H:%M')

    data = SomeForm.validate({
        'date': '2012-06-13', 'datetime': '2012-06-13 10:07'})
    for field in six.itervalues(data):
        assert isinstance(field, datetime)


def test_picker_required_validation():
    """ Test that CalendarDate*Pickers validate required fields correctly. """

    class SomeForm(TableForm):
        date = CalendarDatePicker(date_format='%Y-%m-%d', required=True)
        datetime = CalendarDateTimePicker(
            date_format='%Y-%m-%d %H:%M', required=True)

    try:
        data = SomeForm.validate({'date': '', 'datetime': '2012-06-13 10:07'})
    except ValidationError:
        pass
    else:
        assert False, data

    try:
        data = SomeForm.validate({'date': '2012-06-13', 'datetime': ''})
    except ValidationError:
        pass
    else:
        assert False, data


class TestCalendarDateTimePicker(WidgetTest):
    widget = CalendarDateTimePicker
    attrs = {'css_class': 'something', 'id': 'forceddid'}
    params = {'value': datetime(2016, 1, 1, 15, 30)}
    expected = """<div>
  <input type="text" id="forceddid" name="forceddid" class="something" value="2016-01-01 15:30" />
  <input type="button" id="forceddid_trigger" class="date_field_button" value="Choose" />
</div>"""