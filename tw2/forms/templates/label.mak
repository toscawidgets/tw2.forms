<%namespace name="tw" module="tw2.core.mako_util"/>\
<span ${tw.attrs(attrs=w.attrs)}>\
% if w.escape:
${w.text}\
% else:
${w.text | n}\
% endif
</span>
