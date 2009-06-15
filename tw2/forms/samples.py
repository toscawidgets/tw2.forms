"""
Here you can create samples of your widgets by providing default parameters,
inserting them in a container widget, mixing them with other widgets, etc...
These samples will appear in the WidgetBrowser

See http://toscawidgets.org/documentation/WidgetBrowser for more information
"""

import widgets as twf

options = ['Red', 'Orange', 'Yellow', 'Green', 'Blue']

class DemoSingleSelectField(twf.SingleSelectField):
    options = [''] + options

class DemoMultipleSelectField(twf.MultipleSelectField):
    options = options

class DemoRadioButtonList(twf.RadioButtonList):
    options = options

class DemoCheckBoxList(twf.CheckBoxList):
    options = options

class DemoRadioButtonTable(twf.RadioButtonTable):
    options = options
    cols = 2

class DemoCheckBoxTable(twf.CheckBoxTable):
    options = options
    cols = 2

demo_cld = [
    twf.TextField(id='title'),
    twf.SingleSelectField(id='priority', options=['', 'Normal', 'High']),
    twf.TextArea(id='description'),
]

class DemoTableLayout(twf.TableLayout):
    children = demo_cld

class DemoListLayout(twf.ListLayout):
    children = demo_cld

class DemoSpacer(twf.TableLayout):
    demo_for = twf.Spacer
    children = [
        twf.TextField(id='title'),
        twf.Spacer(),
        twf.TextArea(id='description'),
    ]


class DemoLabel(twf.TableLayout):
    demo_for = twf.Label
    children = [
        twf.TextField(id='title'),
        twf.Label(text='Please enter as much information as possible in the description.'),
        twf.TextArea(id='description'),
    ]

class DemoFieldSet(twf.FieldSet):
    legend = 'FieldSet'
    child = DemoTableLayout(id='x')


class DemoForm(twf.Form):
    child = DemoTableLayout(id='x')


class DemoButton(twf.Button):
    value = 'Click me'
    attrs = {'onclick': 'alert("Hello")'}


class DemoGridLayout(twf.GridLayout):
    child = twf.RowLayout(id=None, children=[
        twf.TextField(id='title'),
        twf.SingleSelectField(id='priority', options=['', 'Normal', 'High']),
    ])
    extra_reps = 3
