<%namespace name="tw" module="tw2.core.mako_util"/>\
<table ${tw.attrs(attrs=w.attrs)}>
   % if w.grouped_options[0][0]:
    <thead>
        <tr>
           % for group_name, options in w.grouped_options:
            <th>${group_name}</th>
           % endfor
        </tr>
    </thead>
   % endif
    <tbody>
   % for row in w.options_rows:
    <tr>
       % for attrs, desc in row:
        % if attrs and desc:
        <td>
            <input ${tw.attrs(attrs=attrs)} />
            <label for="${attrs['id']}">${desc}</label>
        </td>
        % else:
        <td/>
        % endif
       % endfor
       % for j in range(w.cols - len(row)):
        <td/>
       % endfor
    </tr>
   % endfor
    </tbody>
</table>
