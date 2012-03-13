<%namespace name="tw" module="tw2.core.mako_util"/>\
<table ${tw.attrs(attrs=w.attrs)} cellpadding="0" cellspacing="1" border="0">
    % if w.columns:
    <thead>
        <tr>
            % for i, col in enumerate(w.columns):
            <th class="col_${str(i)}">${col.title}</th>
            % endfor
        </tr>
    </thead>
    % endif
    <tbody>
        % for i, row in enumerate(w.value):
        <tr class="${i%2 and 'odd' or 'even'}">
            % for col in w.columns:
            <td ${tw.attrs(
    [('align', col.get_option('align', None)),
     ('class', col.get_option('css_class', None))],
)}>${col.get_field(row)}</td>
            % endfor
        </tr>
        % endfor
    </tbody>
</table>\
