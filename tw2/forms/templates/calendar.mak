<%namespace name="tw" module="tw2.core.mako_util"/>\
<div>
  <input type="text" ${tw.attrs(attrs=w.attrs)} value="${w.strdate or ''}" />
  <input type="button" id="${w.compound_id}_trigger" class="date_field_button" value="${w.button_text}" />
</div>\
