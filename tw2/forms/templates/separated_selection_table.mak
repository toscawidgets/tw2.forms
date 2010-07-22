<%namespace name="tw" module="tw2.core.mako_util"/>\
<table ${tw.attrs(attrs=w.attrs)}>
  %for attrs, desc in w.options:
  <tr>
    <td><input ${tw.attrs(attrs=attrs)}/></td>
    <td><label for="${attrs['id']}">${desc}</label></td>
  </tr>
  %endfor
</table>