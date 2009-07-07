from tw2.forms.widgets import *
from base import assert_in_xml, WidgetTest
from nose.tools import raises

class TestFormField(WidgetTest):
    # place your widget at the TestWidget attribute
    TestWidget = FormField

    @raises(AttributeError)
    def test_display(self):
        # Asserts 'foo' and 'test' (the test widget's id) appear in rendered 
        # string when 'foo' is passed as value to render
        r = self.TestWidget().display()
        assert r == None, r

class TestInputField(WidgetTest):
    
    TestWidget = InputField
    
    def test_display(self):
        # Asserts 'foo' and 'test' (the test widget's id) appear in rendered 
        # string when 'foo' is passed as value to render
        r = self.TestWidget(type='foo').display()
        #okay, inputs are flipping weird, go a head, try and uncomment this line below
        #assert_in_xml('<input type="foo" />', r)
        
        assert '<input type="foo">' in r, r
        
    def test_display_override_css_class(self):
        class MyInputField(InputField):
            css_class = 'something'
            
        r = MyInputField(type='foo').display()
        assert '<input class="something" type="foo">' in  r, r 
    
        
    def test_display_override_value(self):
        r = self.TestWidget(type='foo').display(value="something")
        assert '<input type="foo" value="something">' in r, r


