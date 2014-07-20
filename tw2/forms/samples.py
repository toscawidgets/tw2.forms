"""
Here you can create samples of your widgets by providing default parameters,
inserting them in a container widget, mixing them with other widgets, etc...
These samples will appear in the WidgetBrowser

See http://toscawidgets.org/documentation/WidgetBrowser for more information
"""

import tw2.core as twc
from . import widgets as twf
from . import calendars as cal
from . import datagrid as dg


class DemoTextField(twf.TextField):
    placeholder = "Type up to 7 characters..."
    maxlength = 7


class DemoChildren(twc.CompoundWidget):
    title = twf.TextField()
    priority = twf.SingleSelectField(options=['', 'Normal', 'High'])
    description = twf.TextArea()


class DemoCheckBox(twf.CheckBox):
    value = True


class DemoSingleSelectField(twf.SingleSelectField):
    options = ['Red', 'Orange', 'Yellow', 'Green', 'Blue']


class DemoMultipleSelectField(twf.MultipleSelectField):
    options = ['Red', 'Orange', 'Yellow', 'Green', 'Blue']


class DemoRadioButtonList(twf.RadioButtonList):
    options = ['Red', 'Orange', 'Yellow', 'Green', 'Blue']


class DemoCheckBoxList(twf.CheckBoxList):
    options = ['Red', 'Orange', 'Yellow', 'Green', 'Blue']


class DemoRadioButtonTable(twf.RadioButtonTable):
    options = ['Red', 'Orange', 'Yellow', 'Green', 'Blue']
    cols = 2


class DemoCheckBoxTable(twf.CheckBoxTable):
    options = ['Red', 'Orange', 'Yellow', 'Green', 'Blue']
    value = ['Red', 'Green', 'Blue']  # These are the selected items
    cols = 2


class DemoTableLayout(twf.TableLayout, DemoChildren):
    pass


class DemoListLayout(twf.ListLayout, DemoChildren):
    pass


class DemoSpacer(twf.TableLayout):
    demo_for = twf.Spacer
    title = twf.TextField()
    xx = twf.Spacer()
    description = twf.TextArea()


class DemoLabel(twf.TableLayout):
    demo_for = twf.Label
    title = twf.TextField()
    xx = twf.Label(
        text='Please enter as much information as possible in the description.'
    )
    description = twf.TextArea()


class DemoFieldSet(twf.FieldSet):
    legend = 'FieldSet'
    child = DemoTableLayout()


class DemoForm(twf.Form):
    child = DemoTableLayout()
    buttons = [twf.ResetButton()]


class DemoButton(twf.Button):
    value = 'Click me'
    attrs = {'onclick': 'alert("Hello")'}


class DemoGridLayout(twf.GridLayout):
    id = 'x'
    extra_reps = 3
    title = twf.TextField()
    priority = twf.SingleSelectField(options=['', 'Normal', 'High'])


class DemoImageButton(twf.ImageButton):
    modname = 'tw2.forms'
    filename = 'static/edit-undo.png'


class DemoDataGrid(dg.DataGrid):
    class DummyObject(object):
        def __init__(self, name):
            self._name = name

        def name(self):
            return self._name

        def address(self):
            return "Fancy pancy street."

    value = [
        DummyObject("Jimmy John"),
        DummyObject("Sally Sue"),
    ]

    fields = [DummyObject.name, DummyObject.address]


class DemoEmailField(twf.EmailField):
    placeholder = 'Enter your Email-Address...'


class DemoUrlField(twf.UrlField):
    placeholder = 'http://toscawidgets.org'


class DemoNumberField(twf.NumberField):
    min = 0
    max = 10
    step = 2
    value = 8


class DemoRangeField(twf.RangeField):
    min = 0
    max = 10
    step = 2
    value = 8


class DemoCalendarDatePicker(cal.CalendarDatePicker):
    pass


class DemoCalendarDateTimePicker(cal.CalendarDateTimePicker):
    calendar_lang = 'de'
