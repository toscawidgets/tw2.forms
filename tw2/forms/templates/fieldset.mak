<%namespace name="tw" module="tw2.core.mako_util"/>\
<fieldset ${tw.attrs(attrs=w.attrs)}>
    <legend>${w.legend or ''}</legend>
    ${w.child.display() | n}
</fieldset>