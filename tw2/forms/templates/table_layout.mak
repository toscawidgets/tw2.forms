<%namespace name="tw" module="tw2.core.mako_util"/>\
<table ${tw.attrs(attrs=w.attrs)}>
   % for i,c in enumerate(w.children_non_hidden):
    <tr class="${(i % 2 and 'even' or 'odd') + ((c.validator and getattr(c.validator, 'required', getattr(c.validator, 'not_empty', False))) and ' required' or '') + (c.error_msg and ' error' or '')}" \
     %if w.hover_help and c.help_text:
      title="${c.help_text}" \
     %endif
${tw.attrs(attrs=c.container_attrs)} \
id="${c.compound_id or ''}:container">
       % if c.label:
        <th><label for="${c.id}">${c.label}</label></th>
       % endif
        <td \
       % if not c.label:
colspan="2"\
       % endif
>
            ${c.display() | n}
           % if not w.hover_help:
            ${c.help_text or ''}
           % endif
            <span id="${c.compound_id or ''}:error">${c.error_msg or ''}</span>
        </td>
    </tr>
   % endfor
    <tr class="error"><td colspan="2">
       % for c in w.children_hidden:
        ${c.display() | n}
       % endfor
        <span id="${w.compound_id or ''}:error">${w.error_msg or ''}</span>
    </td></tr>
</table>
