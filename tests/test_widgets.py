from tw2.forms.widgets import *
from webob import Request
from webob.multidict import NestedMultiDict
from tw2.core.testbase import assert_in_xml, assert_eq_xml, WidgetTest
from nose.tools import raises
from cStringIO import StringIO
from tw2.core import EmptyField, IntValidator, ValidationError
from cgi import FieldStorage
import formencode
import formencode.national

import webob
if hasattr(webob, 'NestedMultiDict'):
    from webob import NestedMultiDict
else:
    from webob.multidict import NestedMultiDict

class TestInputField(WidgetTest):
    widget = InputField
    attrs = {'type':'foo', 'css_class':'something'}
    params = {'value':6}
    expected = '<input type="foo" class="something" value="6"/>'

class TestTextField(WidgetTest):
    widget = TextField
    attrs = {'css_class':'something', 'size':'60', 'placeholder': "Search..."}
    params = {'value':6}
    expected = '<input type="text" class="something" placeholder="Search..." value="6" size="60"/>'

class TestTextArea(WidgetTest):
    widget = TextArea
    attrs = {'css_class':'something', 'rows':6, 'cols':10}
    params = {'value':'6'}
    expected = '<textarea class="something" rows="6" cols="10">6</textarea>'

class TestCheckbox(WidgetTest):
    widget = CheckBox
    attrs = {'css_class':'something'}
    params = {'value':True}
    expected = '<input checked="checked" type="checkbox" class="something"/>'

    def test_value_false(self):
        params = {'value':False}
        expected = '<input type="checkbox" class="something">'
        for engine in self._get_all_possible_engines():
            yield self._check_rendering_vs_expected, engine, self.attrs, params, expected

class TestRadioButton(WidgetTest):
    widget = RadioButton
    attrs = {'css_class':'something'}
    params = {'checked':None}
    expected = '<input type="radio" class="something"/>'

    def test_checked(self):
        params = {'checked':True}
        expected = '<input checked="checked" type="radio" class="something">'
        for engine in self._get_all_possible_engines():
            yield self._check_rendering_vs_expected, engine, self.attrs, params, expected

class TestPasswordField(WidgetTest):
    widget = PasswordField
    attrs = {'css_class':'something', 'id':'hid'}
    expected = '<input type="password" class="something" id="hid" name="hid"/>'
    validate_params = [[None, {'hid':'b'}, 'b']]

    def test_no_value(self):
        params = {'value':'something'}
        for engine in self._get_all_possible_engines():
            yield self._check_rendering_vs_expected, engine, self.attrs, params, self.expected

class TestFileField(WidgetTest):
    widget = FileField
    attrs = {'css_class':'something', 'id':'hid', 'validator':FileValidator(extension="bdb", required=True)}
    expected = '<input id="hid" type="file" class="something" name="hid"/>'
    dummy_file = FieldStorage(StringIO(''))
    dummy_file.filename = 'something.ext'
    validate_params = [[None, {'hid':'b'}, None, ValidationError], [None, {'hid':dummy_file}, None, ValidationError]]

class TestHiddenField(WidgetTest):
    widget = HiddenField
    attrs = {'css_class':'something', 'value':'info', 'name':'hidden_name', 'id':'hid'}
    expected = '<input class="something" type="hidden" id="hid" value="info" name="hidden_name">'
    validate_params = [[None, {'hid':'b'}, 'b']]

class TestLabelField(WidgetTest):
    widget = LabelField
    attrs = {'css_class':'something', 'value':'info', 'name':'hidden_name', 'id':'hid'}
    expected = '<span>info<input class="something" type="hidden" value="info" name="hidden_name" id="hid"/></span>'
    validate_params = [[None, {'hid':'b'}, EmptyField]]

class TestLinkField(WidgetTest):
    widget = LinkField
    attrs = {'css_class':'something', 'value':'info', 'name':'hidden_name', 'text':'some $', 'link':'/some/$'}
    expected = '<a href="/some/info" class="something">some info</a>'

class TestButton(WidgetTest):
    widget = Button
    attrs = {'css_class':'something', 'value':'info', 'name':'hidden_name'}
    expected = '<input class="something" type="button" value="info" name="hidden_name">'

class TestSubmitButton(WidgetTest):
    widget = SubmitButton
    attrs = {'css_class':'something', 'value':'info', 'name':'hidden_name'}
    expected = '<input class="something" type="submit" value="info" name="hidden_name">'

class TestResetButton(WidgetTest):
    widget = ResetButton
    attrs = {'css_class':'something', 'value':'info', 'name':'hidden_name'}
    expected = '<input class="something" type="reset" value="info" name="hidden_name">'

class TestImageButton(WidgetTest):
    widget = ImageButton
    attrs = {'css_class':'something', 'value':'info', 'name':'hidden_name', 'link':'/somewhere.gif'}
    expected = '<input src="/somewhere.gif" name="hidden_name" value="info" alt="" type="image" class="something">'

class TestSingleSelectField(WidgetTest):
    widget = SingleSelectField
    attrs = {'css_class':'something',
             'options':((1, 'a'), (2, 'b'), (3, 'c')), 'id':'hid',
             'validator':IntValidator(),
             }
    expected = """<select class="something" id="hid" name="hid">
                        <option></option>
                        <option value="1">a</option>
                        <option value="2">b</option>
                        <option value="3">c</option>
                  </select>"""
    validate_params = [[None, {'hid':''}, None],[None, {'hid':'1'}, 1]]

    def test_option_group(self):
        expected = """<select class="something">
                          <option></option>
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
        attrs = {'css_class':'something', 'options':[('group', ['', (1, 'Red'), (2, 'Blue')]),
                                                     ('group2', ['', 'Pink', 'Yellow'])]}
        for engine in self._get_all_possible_engines():
            yield self._check_rendering_vs_expected, engine, attrs, self.params, expected

    def test_option_no_values(self):
        expected = """<select class="something">
                         <option></option>
                         <option value="a">a</option>
                         <option value="b">b</option>
                         <option value="c">c</option>
                      </select>"""
        attrs = {'css_class':'something', 'options':('a', 'b','c')}
        for engine in self._get_all_possible_engines():
            yield self._check_rendering_vs_expected, engine, attrs, self.params, expected

    def test_prompt_text(self):
        expected = """<select>
             <option >Pick one:</option>
             <option value="a">a</option>
             <option value="b">b</option>
             <option value="c">c</option>
            </select>"""
        attrs = {'options':('a','b','c'), 'prompt_text':'Pick one:'}
        for engine in self._get_all_possible_engines():
            yield self._check_rendering_vs_expected, engine, attrs, self.params, expected

    def test_no_options(self):
        expected = """<select>
             <option/>
            </select>"""
        attrs = {'options':[]}
        for engine in self._get_all_possible_engines():
            yield self._check_rendering_vs_expected, engine, attrs, self.params, expected



class TestMultipleSelectField(WidgetTest):
    widget = MultipleSelectField
    attrs = {'css_class':'something', 'options':(('a','1'), ('b', '2'), ('c', '3')), 'id':"hid"}
    expected = """<select class="something" multiple="multiple" id="hid" name="hid">
                      <option value="a">1</option>
                      <option value="b">2</option>
                      <option value="c">3</option>
                  </select>"""
    validate_params = [[None, {'hid':'b'}, [u'b']]]

class TestSelectionList(WidgetTest):
    widget = SelectionList
    attrs = {'css_class':'something', 'field_type':'test', 'options':(('a','1'), ('b', '2'), ('c', '3')), 'id':'something'}
    expected = """<ul class="something" id="something">
    <li>
        <input type="test" name="something" value="a" id="something:0">
        <label for="something:0">1</label>
    </li><li>
        <input type="test" name="something" value="b" id="something:1">
        <label for="something:1">2</label>
    </li><li>
        <input type="test" name="something" value="c" id="something:2">
        <label for="something:2">3</label>
    </li>
</ul>"""


class TestRadioButtonList(WidgetTest):
    widget = RadioButtonList
    attrs = {'css_class':'something', 'options':(('a','1'), ('b', '2'), ('c', '3')), 'id':'something'}
    expected = """<ul class="something" id="something">
    <li>
        <input type="radio" name="something" value="a" id="something:0">
        <label for="something:0">1</label>
    </li><li>
        <input type="radio" name="something" value="b" id="something:1">
        <label for="something:1">2</label>
    </li><li>
        <input type="radio" name="something" value="c" id="something:2">
        <label for="something:2">3</label>
    </li>
</ul>"""

class TestCheckBoxList(WidgetTest):
    widget = CheckBoxList
    attrs = {'css_class':'something', 'options':(('a','1'), ('b', '2'), ('c', '3')), 'id':'something'}
    expected = """<ul class="something" id="something">
    <li>
        <input type="checkbox" name="something" value="a" id="something:0">
        <label for="something:0">1</label>
    </li><li>
        <input type="checkbox" name="something" value="b" id="something:1">
        <label for="something:1">2</label>
    </li><li>
        <input type="checkbox" name="something" value="c" id="something:2">
        <label for="something:2">3</label>
    </li>
</ul>
"""
    def test_option_has_value(self):
        expected = """<ul class="something" id="something">
    <li>
        <input type="checkbox" name="something" value="a" id="something:0" checked>
        <label for="something:0">a</label>
    </li><li>
        <input type="checkbox" name="something" value="b" id="something:1">
        <label for="something:1">b</label>
    </li><li>
        <input type="checkbox" name="something" value="c" id="something:2">
        <label for="something:2">c</label>
    </li>
</ul>"""
        attrs = {'css_class':'something', 'options':('a', 'b','c'), 'id':'something'}
        params = {'value':'a',}
        for engine in self._get_all_possible_engines():
            yield self._check_rendering_vs_expected, engine, attrs, params, expected

class TestSelectionTable(WidgetTest):
    widget = SelectionTable
    attrs = {'css_class':'something', 'field_type':'test', 'options':(('a','1'), ('b', '2'), ('c', '3')), 'id':'something'}
    expected = """<table class="something" id="something">
    <tbody>
    <tr>
        <td>
            <input type="test" name="something" value="a" id="something:0">
            <label for="something:0">1</label>
        </td>
    </tr><tr>
        <td>
            <input type="test" name="something" value="b" id="something:1">
            <label for="something:1">2</label>
        </td>
    </tr><tr>
        <td>
            <input type="test" name="something" value="c" id="something:2">
            <label for="something:2">3</label>
        </td>
    </tr>
    </tbody>
</table>"""

    def test_option_leftover_chunk(self):
        expected = """<table class="something" id="something">
    <tbody>
    <tr>
        <td>
            <input type="test" checked name="something" value="a" id="something:0">
            <label for="something:0">a</label>
        </td><td>
            <input type="test" name="something" value="b" id="something:1">
            <label for="something:1">b</label>
        </td>
    </tr><tr>
        <td>
            <input type="test" name="something" value="c" id="something:2">
            <label for="something:2">c</label>
        </td>
        <td></td>
    </tr>
    </tbody>
</table>"""
        attrs = {'css_class':'something', 'field_type':'test', 'cols':2, 'options':(('group1', ('a', 'b')),'c'), 'id':'something'}
        params = {'value':'a',}
        for engine in self._get_all_possible_engines():
            yield self._check_rendering_vs_expected, engine, attrs, params, expected

class TestRadioButtonTable(WidgetTest):
    widget = RadioButtonTable
    attrs = {'css_class':'something', 'options':(('a','1'), ('b', '2'), ('c', '3')), 'id':'something'}
    expected = """<table class="something" id="something">
    <tbody>
    <tr>
        <td>
            <input type="radio" name="something" value="a" id="something:0">
            <label for="something:0">1</label>
        </td>
    </tr><tr>
        <td>
            <input type="radio" name="something" value="b" id="something:1">
            <label for="something:1">2</label>
        </td>
    </tr><tr>
        <td>
            <input type="radio" name="something" value="c" id="something:2">
            <label for="something:2">3</label>
        </td>
    </tr>
    </tbody>
</table>"""

class TestCheckBoxTable(WidgetTest):
    widget = CheckBoxTable
    attrs = {'css_class':'something', 'options':(('a','1'), ('b', '2'), ('c', '3')), 'id':'something'}
    expected = """<table class="something" id="something">
    <tbody>
    <tr>
        <td>
            <input type="checkbox" name="something" value="a" id="something:0">
            <label for="something:0">1</label>
        </td>
    </tr><tr>
        <td>
            <input type="checkbox" name="something" value="b" id="something:1">
            <label for="something:1">2</label>
        </td>
    </tr><tr>
        <td>
            <input type="checkbox" name="something" value="c" id="something:2">
            <label for="something:2">3</label>
        </td>
    </tr>
    </tbody>
</table>"""


class TestListLayout(WidgetTest):
    widget = ListLayout
    attrs = {'children': [TextField(id='field1'),
                          TextField(id='field2'),
                          TextField(id='field3')]}
    expected = """\
<ul>
    <li class="odd">
        <label>Field1</label>
        <input name="field1" id="field1" type="text">
        <span id="field1:error" class="error"></span>
    </li><li class="even">
        <label>Field2</label>
        <input name="field2" id="field2" type="text">
        <span id="field2:error" class="error"></span>
    </li><li class="odd">
        <label>Field3</label>
        <input name="field3" id="field3" type="text">
        <span id="field3:error" class="error"></span>
    </li>
    <li class="error"><span id=":error" class="error"></span></li>
</ul>"""
    declarative = True

class TestListLayoutErrors(TestListLayout):
    attrs = {'children': [TextField(id='field1'), ],
             'error_msg': 'bogus error'}
    expected = """\
<ul>
    <li class="odd">
        <label>Field1</label>
        <input name="field1" id="field1" type="text">
        <span id="field1:error" class="error"></span>
    </li>
    <li class="error"><span id=":error" class="error"><p>bogus error</p></span></li>
</ul>"""

class TestTableLayout(WidgetTest):
    widget = TableLayout
    attrs = {'children': [TextField(id='field1'),
                          TextField(id='field2'),
                          TextField(id='field3')]}
    expected = """<table>
    <tr class="odd" id="field1:container">
        <th>Field1</th>
        <td>
            <input name="field1" id="field1" type="text">
            <span id="field1:error"></span>
        </td>
    </tr><tr class="even" id="field2:container">
        <th>Field2</th>
        <td>
            <input name="field2" id="field2" type="text">
            <span id="field2:error"></span>
        </td>
    </tr><tr class="odd" id="field3:container">
        <th>Field3</th>
        <td>
            <input name="field3" id="field3" type="text">
            <span id="field3:error"></span>
        </td>
    </tr>
    <tr class="error"><td colspan="2">
        <span id=":error"></span>
    </td></tr>
</table>"""
    declarative = True

    def test_required(self):
        attrs = {'children': [TextField(id='field1', validator=twc.Required)]}
        expected = """<table>
    <tr class="odd required" id="field1:container">
        <th>Field1</th>
        <td>
            <input name="field1" id="field1" type="text">
            <span id="field1:error"></span>
        </td>
    </tr></table>"""

    def test_fe_not_required(self):
        attrs = {'children': [TextField(id='field1', validator=formencode.FancyValidator(not_empty=False))]}
        expected = """<table>
    <tr class="odd" id="field1:container">
        <th>Field1</th>
        <td>
            <input name="field1" id="field1" type="text">
            <span id="field1:error"></span>
        </td>
    </tr></table>"""

    def test_fe_required(self):
        attrs = {'children': [TextField(id='field1', validator=formencode.FancyValidator(not_empty=True))]}
        expected = """<table>
    <tr class="odd required" id="field1:container">
        <th>Field1</th>
        <td>
            <input name="field1" id="field1" type="text">
            <span id="field1:error"></span>
        </td>
    </tr></table>"""


class TestRowLayout(WidgetTest):
    widget = RowLayout
    attrs = {'children': [TextField(id='field1'),
                          TextField(id='field2'),
                          TextField(id='field3')],
             'repetition': 1,
             }
    expected = """<tr class="even">
    <td>
        <input name="field1" id="field1" type="text">
    </td><td>
        <input name="field2" id="field2" type="text">
    </td><td>
        <input name="field3" id="field3" type="text">
    </td>
    <td>
    </td>
</tr>"""
    declarative = True

class TestGridLayout(WidgetTest):
    widget = GridLayout
    attrs = {'children': [TextField(id='field1'),
                          TextField(id='field2'),
                          TextField(id='field3')],
             'repetition': 1,
             }
    expected = """<table>
    <tr><th>Field1</th><th>Field2</th><th>Field3</th></tr>
    <tr class="error"><td colspan="0" id=":error">
    </td></tr>
</table>"""
    declarative = True

class TestSpacer(WidgetTest):
    widget = Spacer
    attrs = {}
    expected = """<div></div>"""

class TestLabel(WidgetTest):
    widget = Label
    attrs = {'text':'something'}
    expected = """<span>something</span>"""

class TestForm(WidgetTest):
    widget = Form
    attrs = {'child': TableLayout(field1=TextField(id='field1')),
        'buttons': [SubmitButton, ResetButton()]}
    expected = """<form enctype="multipart/form-data" method="post">
     <span class="error"></span>
    <table >
    <tr class="odd"  id="field1:container">
        <th>Field1</th>
        <td >
            <input name="field1" type="text" id="field1"/>
            
            <span id="field1:error"></span>
        </td>
    </tr>
    <tr class="error"><td colspan="2">
        <span id=":error"></span>
    </td></tr>
</table>
        <input type="submit"/>
        <input type="reset"/>
</form>"""
    declarative = True

class TestTableForm(WidgetTest):
    widget = TableForm
    attrs = {'field1':TextField(id='field1'),
             'field2':TextField(id='field2'),
             'field3':TextField(id='field3'),
             }
    expected = """<form method="post" enctype="multipart/form-data">
     <span class="error"></span>
    <table>
    <tr class="odd" id="field1:container">
        <th>Field1</th>
        <td>
            <input name="field1" id="field1" type="text">
            <span id="field1:error"></span>
        </td>
    </tr><tr class="even" id="field2:container">
        <th>Field2</th>
        <td>
            <input name="field2" id="field2" type="text">
            <span id="field2:error"></span>
        </td>
    </tr><tr class="odd" id="field3:container">
        <th>Field3</th>
        <td>
            <input name="field3" id="field3" type="text">
            <span id="field3:error"></span>
        </td>
    </tr>
    <tr class="error"><td colspan="2">
        <span id=":error"></span>
    </td></tr>
</table>
    <input type="submit" id="submit" value="Save">
</form>"""
    declarative = True

class TestListForm(WidgetTest):
    widget = ListForm
    attrs = {'field1':TextField(id='field1'),
             'field2':TextField(id='field2'),
             'field3':TextField(id='field3'),
             }
    expected = """<form method="post" enctype="multipart/form-data">
     <span class="error"></span>
    <ul >
    <li class="odd">
     <label>Field1</label>
        <input name="field1" id="field1" type="text"/>
        <span id="field1:error" class="error"></span>
    </li>
    <li class="even">
     <label>Field2</label>
        <input name="field2" id="field2" type="text"/>
        <span id="field2:error" class="error"></span>
    </li>
    <li class="odd">
     <label>Field3</label>
        <input name="field3" id="field3" type="text"/>
        <span id="field3:error" class="error"></span>
    </li>
    <li class="error"><span id=":error" class="error"></span></li>
</ul>
    <input type="submit" id="submit" value="Save"/>
</form>"""
    declarative = True

class TestTableFieldset(WidgetTest):
    widget = TableFieldSet
    attrs = {'field1':TextField(id='field1'),
             'field2':TextField(id='field2'),
             'field3':TextField(id='field3'),
             }
    expected = """<fieldset>
    <legend></legend>
    <table>
    <tr class="odd" id="field1:container">
        <th>Field1</th>
        <td>
            <input name="field1" id="field1" type="text">
            <span id="field1:error"></span>
        </td>
    </tr><tr class="even" id="field2:container">
        <th>Field2</th>
        <td>
            <input name="field2" id="field2" type="text">
            <span id="field2:error"></span>
        </td>
    </tr><tr class="odd" id="field3:container">
        <th>Field3</th>
        <td>
            <input name="field3" id="field3" type="text">
            <span id="field3:error"></span>
        </td>
    </tr>
    <tr class="error"><td colspan="2">
        <span id=":error"></span>
    </td></tr>
</table>
</fieldset>"""
    declarative = True

class TestTableFieldsetWithFEValidator(WidgetTest):
    widget = TableFieldSet
    attrs = {'field1':TextField(id='field1'),
             'field2':TextField(id='field2'),
             'field3':TextField(id='field3', validator=formencode.national.USPostalCode()),
             }
    expected = """<fieldset>
    <legend></legend>
    <table>
    <tr class="odd" id="field1:container">
        <th>Field1</th>
        <td>
            <input name="field1" id="field1" type="text">
            <span id="field1:error"></span>
        </td>
    </tr><tr class="even" id="field2:container">
        <th>Field2</th>
        <td>
            <input name="field2" id="field2" type="text">
            <span id="field2:error"></span>
        </td>
    </tr><tr class="odd" id="field3:container">
        <th>Field3</th>
        <td>
            <input name="field3" id="field3" type="text">
            <span id="field3:error"></span>
        </td>
    </tr>
    <tr class="error"><td colspan="2">
        <span id=":error"></span>
    </td></tr>
</table>
</fieldset>"""
    declarative = True


class TestListFieldset(WidgetTest):
    widget = ListFieldSet
    attrs = {'field1':TextField(id='field1'),
             'field2':TextField(id='field2'),
             'field3':TextField(id='field3'),
             }
    expected = """<fieldset >
    <legend></legend>
    <ul >
    <li class="odd">
     <label>Field1</label>
        <input name="field1" id="field1" type="text"/>
        <span id="field1:error" class="error"></span>
    </li>
    <li class="even">
     <label>Field2</label>
        <input name="field2" id="field2" type="text"/>
        <span id="field2:error" class="error"></span>
    </li>
    <li class="odd">
     <label>Field3</label>
        <input name="field3" id="field3" type="text"/>
        <span id="field3:error" class="error"></span>
    </li>
    <li class="error"><span id=":error" class="error"></span></li>
</ul>
</fieldset>"""
    declarative = True

class TestFormPage(WidgetTest):
    widget = FormPage
    attrs = {'child':TableForm(children=[TextField(id='field1'),
                                         TextField(id='field2'),
                                         TextField(id='field3'),]),
             'title':'some title'
             }
    expected = """<html>
<head><title>some title</title></head>
<body id="mytestwidget:page"><h1>some title</h1><form method="post" id="mytestwidget:form" enctype="multipart/form-data">
     <span class="error"></span>
    <table id="mytestwidget">
    <tr class="odd" id="mytestwidget:field1:container">
        <th>Field1</th>
        <td>
            <input name="mytestwidget:field1" id="mytestwidget:field1" type="text">
            <span id="mytestwidget:field1:error"></span>
        </td>
    </tr><tr class="even" id="mytestwidget:field2:container">
        <th>Field2</th>
        <td>
            <input name="mytestwidget:field2" id="mytestwidget:field2" type="text">
            <span id="mytestwidget:field2:error"></span>
        </td>
    </tr><tr class="odd" id="mytestwidget:field3:container">
        <th>Field3</th>
        <td>
            <input name="mytestwidget:field3" id="mytestwidget:field3" type="text">
            <span id="mytestwidget:field3:error"></span>
        </td>
    </tr>
    <tr class="error"><td colspan="2">
        <span id="mytestwidget:error"></span>
    </td></tr>
</table>
    <input type="submit" id="submit" value="Save">
</form></body>
</html>"""

    declarative = True
    def test_request_get(self):
        environ = {'REQUEST_METHOD': 'GET',
                   }
        req=Request(environ)
        r = self.widget().request(req)
        assert_eq_xml(r.body, """<html>
<head><title>some title</title></head>
<body id="mytestwidget:page"><h1>some title</h1><form method="post" id="mytestwidget:form" enctype="multipart/form-data">
     <span class="error"></span>
    <table id="mytestwidget">
    <tr class="odd" id="mytestwidget:field1:container">
        <th>Field1</th>
        <td>
            <input name="mytestwidget:field1" id="mytestwidget:field1" type="text">
            <span id="mytestwidget:field1:error"></span>
        </td>
    </tr><tr class="even" id="mytestwidget:field2:container">
        <th>Field2</th>
        <td>
            <input name="mytestwidget:field2" id="mytestwidget:field2" type="text">
            <span id="mytestwidget:field2:error"></span>
        </td>
    </tr><tr class="odd" id="mytestwidget:field3:container">
        <th>Field3</th>
        <td>
            <input name="mytestwidget:field3" id="mytestwidget:field3" type="text">
            <span id="mytestwidget:field3:error"></span>
        </td>
    </tr>
    <tr class="error"><td colspan="2">
        <span id="mytestwidget:error"></span>
    </td></tr>
</table>
    <input type="submit" id="submit" value="Save">
</form></body>
</html>""")

    def _test_request_post_invalid(self):
        # i have commented this because the post is in fact
        # valid, there are no arguments sent to the post, but the
        # widget does not require them
        environ = {'REQUEST_METHOD': 'POST',
                   'wsgi.input': StringIO(''),

                   }
        req=Request(environ)
        r = self.widget().request(req)
        assert_eq_xml(r.body, """<html>
<head><title>some title</title></head>
<body id="mytestwidget:page"><h1>some title</h1><form method="post" id="mytestwidget:form" enctype="multipart/form-data">
     <span class="error"></span>
    <table id="mytestwidget">
    <tr class="odd" id="mytestwidget:field1:container">
        <th>Field1</th>
        <td>
            <input name="mytestwidget:field1" id="mytestwidget:field1" type="text">
            <span id="mytestwidget:field1:error"></span>
        </td>
    </tr><tr class="even" id="mytestwidget:field2:container">
        <th>Field2</th>
        <td>
            <input name="mytestwidget:field2" id="mytestwidget:field2" type="text">
            <span id="mytestwidget:field2:error"></span>
        </td>
    </tr><tr class="odd" id="mytestwidget:field3:container">
        <th>Field3</th>
        <td>
            <input name="mytestwidget:field3" id="mytestwidget:field3" type="text">
            <span id="mytestwidget:field3:error"></span>
        </td>
    </tr>
    <tr class="error"><td colspan="2">
        <span id="mytestwidget:error"></span>
    </td></tr>
</table>
    <input type="submit" id="submit" value="Save">
</form></body>
</html>""")

    def test_request_post_valid(self):
        environ = {'wsgi.input': StringIO(''),
                   }
        req=Request(environ)
        req.method = 'POST'
        req.body='mytestwidget:field1=a&mytestwidget:field2=b&mytestwidget:field3=c'
        req.environ['CONTENT_LENGTH'] = str(len(req.body))
        req.environ['CONTENT_TYPE'] = 'application/x-www-form-urlencoded'

        self.mw.config.debug = True
        r = self.widget().request(req)
        assert (
            r.body == """Form posted successfully {'field2': 'b', 'field3': 'c', 'field1': 'a'}""" or
            r.body == """Form posted successfully {'field2': u'b', 'field3': u'c', 'field1': u'a'}"""
            ), r.body
