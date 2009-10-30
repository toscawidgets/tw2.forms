<%namespace name="tw" module="tw2.core.mako_util"/>\
<div>
    <input type="text" ${tw.attrs(
        [('id', w.id),
         ('class', w.css_class),
         ('name', w.name),
         ('value', w.strdate)],
        attrs=w.attrs
    )} />
    <input type="button" class="date_field_button" ${tw.attrs(
        [('id', '%s_trigger' % w.id),
         ('value', w.button_text)],
        attrs=w.attrs
    )} />
</div>\
