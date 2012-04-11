<%namespace name="tw" module="tw2.core.mako_util"/>\
<ul ${tw.attrs(attrs=w.attrs)}>
   % for group, opts in w.grouped_options:
       % if group:
        <li>
        <div class="group_header">${group}</div>
        <ul>
       % endif   
       % for attrs, desc in opts:
        <li>
            <input ${tw.attrs(attrs=attrs)}/>
            <label for="${attrs['id']}">${desc}</label>
        </li>
       % endfor
       % if group:
        </li>
        </ul>
       % endif   
   % endfor
</ul>