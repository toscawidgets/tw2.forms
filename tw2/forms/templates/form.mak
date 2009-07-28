<%namespace name="tw" module="tw2.core.mako_util"/>\
<form ${tw.attrs(attrs=w.attrs)}>
     <span class="error">${w.error_msg or ''}</span>
    ${w.child.display() | n}
   % if w.submit:
    ${w.submit.display() | n}
   % endif
</form>
