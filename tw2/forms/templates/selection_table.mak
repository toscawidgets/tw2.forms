<%namespace name="tw" module="tw2.core.mako_util"/>\
<table ${tw.attrs(attrs=w.attrs)}>
    <tbody>
   % for row in w.options_rows:
    <tr>
       % for attrs, desc in row:
        <td>
            <input ${tw.attrs(attrs=attrs)} />
            <label for="${attrs['id']}">${desc}</label>
        </td>
       % endfor
       % for j in range(w.cols - len(row)):
        <td/>
       % endfor
    </tr>
   % endfor
    </tbody>
</table>
