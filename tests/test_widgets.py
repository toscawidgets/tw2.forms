from tw2.forms.widgets import *
from base import assert_in_xml, assert_eq_xml, WidgetTest
from nose.tools import raises

class _TestFormField(WidgetTest):
    # place your widget at the TestWidget attribute
    TestWidget = FormField

    @raises(AttributeError)
    def test_display(self):
        # Asserts 'foo' and 'test' (the test widget's id) appear in rendered 
        # string when 'foo' is passed as value to render
        r = self.TestWidget().display()
        assert r == None, r

class TestInputField(WidgetTest):
    widget = InputField
    attrs = {'type':'foo', 'css_class':'something'}
    params = {'value':6}
    expected = '<input type="foo" class="something" value="6"/>'

class TestTextField(WidgetTest):
    widget = TextField
    attrs = {'css_class':'something', 'size':'60'}
    params = {'value':6}
    expected = '<input type="text" class="something" value="6" size="60"/>'

class TestTextArea(WidgetTest):
    widget = TextArea
    attrs = {'css_class':'something', 'rows':6, 'cols':10}
    params = {'value':6}
    expected = '<textarea class="something" rows="6" cols="10">6</textarea>'
    
class TestCheckbox(WidgetTest):
    widget = CheckBox
    attrs = {'css_class':'something'}
    params = {'value':True}
    expected = '<input checked="checked" value="True" type="checkbox" class="something"/>'
    
    def test_value_false(self):
        params = {'value':False}
        expected = '<input value="False" type="checkbox" class="something">'
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
    attrs = {'css_class':'something'}
    expected = '<input type="password" class="something"/>'

    def test_no_value(self):
        params = {'value':'something'}
        for engine in self._get_all_possible_engines():
            yield self._check_rendering_vs_expected, engine, self.attrs, params, self.expected

class TestFileField(WidgetTest):
    widget = FileField
    attrs = {'css_class':'something'}
    expected = '<input type="file" class="something"/>'

class TestHiddenField(WidgetTest):
    widget = HiddenField
    attrs = {'css_class':'something', 'value':'info', 'name':'hidden_name'}
    expected = '<input type="hidden" class="something" value="info" name="hidden_name"/>'

class TestLabelField(WidgetTest):
    widget = LabelField
    attrs = {'css_class':'something', 'value':'info', 'name':'hidden_name'}
    expected = '<span>info<input class="something" type="hidden" value="info" name="hidden_name"/></span>'

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
    attrs = {'css_class':'something', 'options':(('a',1), ('b', 2), ('c', 3))}
    expected = """<select class="something">
                        <option></option>
                        <option value="a">1</option>
                        <option value="b">2</option>
                        <option value="c">3</option>
                  </select>"""

    def test_option_group(self):
        expected = """<select class="something">
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

class TestMultipleSelectField(WidgetTest):
    widget = MultipleSelectField
    attrs = {'css_class':'something', 'options':(('a',1), ('b', 2), ('c', 3))}
    expected = """<select class="something" multiple="multiple">
                      <option value="a">1</option>
                      <option value="b">2</option>
                      <option value="c">3</option>
                  </select>"""

class TestSelectionList(WidgetTest):
    widget = SelectionList
    attrs = {'css_class':'something', 'options':(('a',1), ('b', 2), ('c', 3)), 'id':'something'}
    expected = """<ul class="something" id="something" name="something">
    <li>
        <input name="something" value="a" id="something:0">
        <label for="something:0">1</label>
    </li><li>
        <input name="something" value="b" id="something:1">
        <label for="something:1">2</label>
    </li><li>
        <input name="something" value="c" id="something:2">
        <label for="something:2">3</label>
    </li>
</ul>"""


class TestRadioButtonList(WidgetTest):
    widget = RadioButtonList
    attrs = {'css_class':'something', 'options':(('a',1), ('b', 2), ('c', 3)), 'id':'something'}
    expected = """<ul class="something" id="something" name="something">
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
    attrs = {'css_class':'something', 'options':(('a',1), ('b', 2), ('c', 3)), 'id':'something'}
    expected = """<ul class="something" id="something" name="something">
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
        expected = """<ul class="something" id="something" name="something">
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
    attrs = {'css_class':'something', 'options':(('a',1), ('b', 2), ('c', 3)), 'id':'something'}
    expected = """<table class="something" id="something" name="something">
    <tbody>
    <tr>
        <td>
            <input name="something" value="a" id="something:0">
            <label for="something:0">1</label>
        </td>
    </tr><tr>
        <td>
            <input name="something" value="b" id="something:1">
            <label for="something:1">2</label>
        </td>
    </tr><tr>
        <td>
            <input name="something" value="c" id="something:2">
            <label for="something:2">3</label>
        </td>
    </tr>
    </tbody>
</table>"""

class TestRadioButtonTable(WidgetTest):
    widget = RadioButtonTable
    attrs = {'css_class':'something', 'options':(('a',1), ('b', 2), ('c', 3)), 'id':'something'}
    expected = """<table class="something" id="something" name="something">
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
    attrs = {'css_class':'something', 'options':(('a',1), ('b', 2), ('c', 3)), 'id':'something'}
    expected = """<table class="something" id="something" name="something">
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
    expected = """<ul>
    <li class="odd">
        Field1
        <input name="field1" id="field1" type="text">
        <span id="field1:error"></span>
    </li><li class="even">
        Field2
        <input name="field2" id="field2" type="text">
        <span id="field2:error"></span>
    </li><li class="odd">
        Field3
        <input name="field3" id="field3" type="text">
        <span id="field3:error"></span>
    </li>
    <li class="error"><span id=":error"></span></li>
</ul>"""
    declarative = True
    

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
    <tr><th>Auto</th><th>Auto</th><th>Auto</th></tr>
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
