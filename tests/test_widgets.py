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
    attrs = {'type':'foo'}
    params = {'value':6}
    expected = '<input type="foo" value="6"/>'
    
    def test_display_override_css_class(self):
        class MyInputField(InputField):
            css_class = 'something'
            
        r = MyInputField(type='foo').display()
        assert_eq_xml('<input class="something" type="foo"/>', r)
    
        
    def test_display_override_value(self):
        r = self.widget(type='foo').display(value="something")
        assert_eq_xml('<input value="something" type="foo"/>', r)


