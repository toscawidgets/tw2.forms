<%namespace name="tw" module="tw2.core.mako_util"/>\
<a ${tw.attrs(attrs=w.attrs)}>\
% if w.escape:
${w.text}\
% else:
${w.text | n}\
% endif
</a>
