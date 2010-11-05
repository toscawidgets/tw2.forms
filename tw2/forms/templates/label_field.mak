<%namespace name="tw" module="tw2.core.mako_util"/>\
<span>${unicode(w.value or '')}<input ${tw.attrs(attrs=w.attrs)}/></span>