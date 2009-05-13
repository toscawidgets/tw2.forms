from tw.core.testutil import WidgetTestCase
from tw.forms import *

class TestWidget(WidgetTestCase):
    # place your widget at the TestWidget attribute
    TestWidget = Forms
    # Initilization args. go here 
    widget_kw = {}

    def test_render(self):
        # Asserts 'foo' and 'test' (the test widget's id) appear in rendered 
        # string when 'foo' is passed as value to render
        self.assertInOutput(['foo', 'test'], "foo")
        # Asserts 'ohlalala' does not appear in rendered string when render 
        # is called without args
        self.assertNotInOutput(['ohlalala'])
