<%namespace name="tw" module="tw2.core.mako_util"/>\
<span>\
% if w.escape:
${w.value or ''}\
% else:
${w.value or '' | n}\
% endif
<input ${tw.attrs(attrs=w.attrs)}/></span>
