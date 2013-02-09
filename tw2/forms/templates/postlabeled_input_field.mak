<%namespace name="tw" module="tw2.core.mako_util"/>\
<input ${tw.attrs(attrs=w.attrs)}/> <label for="${w.compound_id}" ${tw.attrs(attrs=w.text_attrs)}>${w.text}</label>