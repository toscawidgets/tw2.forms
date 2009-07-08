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
        <input type="True" name="something" value="a" id="something:0">
        <label for="something:0">1</label>
    </li><li>
        <input type="True" name="something" value="b" id="something:1">
        <label for="something:1">2</label>
    </li><li>
        <input type="True" name="something" value="c" id="something:2">
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

class TestSelectionTable(WidgetTest):
    widget = SelectionTable
    attrs = {'css_class':'something', 'options':(('a',1), ('b', 2), ('c', 3)), 'id':'something'}
    expected = """<table class="something" id="something" name="something">
    <tbody>
    <tr>
        <td>
            <input type="True" name="something" value="a" id="something:0">
            <label for="something:0">1</label>
        </td>
    </tr><tr>
        <td>
            <input type="True" name="something" value="b" id="something:1">
            <label for="something:1">2</label>
        </td>
    </tr><tr>
        <td>
            <input type="True" name="something" value="c" id="something:2">
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

