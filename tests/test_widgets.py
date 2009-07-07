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
    attrs = {'css_class':'something', 'size':'60'}
    params = {'value':6}
    expected = '<textarea class="something">6</textarea>'
