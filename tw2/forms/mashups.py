import tw2.core as twc
from .widgets import CheckBox, PostlabeledInputField


class PostlabeledCheckBox(CheckBox, PostlabeledInputField):
    pass


class PostlabeledPartialRadioButton(PostlabeledInputField):
    """ This is basically a manual mixin of RadioButton and
    IgnoredField. Inheritance doesn't work. """
    type = "radio"
    checked = twc.Param(attribute=True, default=False)

    def _validate(self, value):
        return twc.EmptyField
