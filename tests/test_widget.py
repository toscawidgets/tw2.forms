from tw.core.testutil import WidgetTestCase
from tw.forms import *
from base import assert_in_xml

class TestFormField(WidgetTestCase):
    # place your widget at the TestWidget attribute
    TestWidget = FormField
    # Initilization args. go here 
    widget_kw = {'name':'input'}

    def test_display(self):
        # Asserts 'foo' and 'test' (the test widget's id) appear in rendered 
        # string when 'foo' is passed as value to render
        r = self.TestWidget().display()
        assert r == None, r

class TestInputField(WidgetTestCase):
    
    TestWidget = InputField
    
    def test_display(self):
        # Asserts 'foo' and 'test' (the test widget's id) appear in rendered 
        # string when 'foo' is passed as value to render
        r = self.TestWidget().display()
        assert_in_xml('<input class="inputfield" value="" />', r)
        
    def test_display_override_css_class(self):
        class MyInputField(InputField):
            css_class = 'something'
        r = MyInputField().display()
        assert_in_xml('<input class="something" value="" />', r)
        
    def test_display_override_value(self):
        r = self.TestWidget().display(value="something")
        assert_in_xml('<input class="inputfield" value="something" />', r)
        
    
    

