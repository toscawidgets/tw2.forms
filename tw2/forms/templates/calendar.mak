<%! import tw2.core as twc %>
<div>
  <input type="text" id="${w.compound_id}" name="${w.name}" class="${w.css_class or ''}" value="${w.strdate or ''}" />
  <input type="button" id="${w.compound_id}_trigger" class="date_field_button" value="${w.button_text}" />
  <script type="text/javascript">Calendar.setup({
    "inputField": "${w.compound_id}", "showsTime": ${str(w.picker_shows_time).lower()},
    "ifFormat": "${w.date_format}", "button": "${w.compound_id}_trigger"
    %for k, v in w.setup_options.items():
      , ${k}: ${isinstance(v, twc.JSSymbol) and (v.src) or '"%s"' % v}
    %endfor
  })</script>
</div>\
