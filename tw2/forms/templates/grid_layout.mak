<%namespace name="tw" module="tw2.core.mako_util"/>\
<table ${tw.attrs(attrs=w.attrs)}>
<tr>\
% for col in w.children[0].children_non_hidden:
    <th>${col.label}</th>
% endfor
</tr>
% for row in w.children:
    ${row.display() | n}
% endfor
    <tr class="error"><td colspan="${str(len(w.children))}" id="${w.compound_id or ''}:error">
        ${w.error_msg or ''}
    </td></tr>
</table>
