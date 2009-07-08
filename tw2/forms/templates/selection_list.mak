<%namespace name="tw" module="tw2.core.mako_util"/>\
<ul ${tw.attrs(attrs=w.attrs)}>
   % for attrs, desc in w.options:
    <li>
        <input ${tw.attrs(attrs=attrs)}/>
        <label for="${attrs['id']}">${desc}</label>
    </li>
   % endfor
</ul>