<%namespace name="tw" module="tw2.core.mako_util"/>\
<tr\
 ${tw.attrs(attrs=w.attrs)}>
   % for c in w.children_non_hidden:
    <td id="${c.compound_id or ''}:container">
        ${c.display() | n}
       % if c.error_msg:
        <img src="${w.resources.error.link}" title="${c.error_msg}"/>
       % endif
    </td>
   % endfor
    <td>
       % for c in w.children_hidden:
        ${c.display() | n}
       % endfor
       % if w.error_msg:
        <img src="${w.resources.error.link}" title="${w.error_msg}"/>
       % endif
    </td>
</tr>
