<%namespace name="tw" module="tw2.core.mako_util"/>\
<ul ${tw.attrs(attrs=w.attrs)}>
   % for c in w.children_hidden:
    ${c.display() | n}
   % endfor
   % for i,c in enumerate(w.children_non_hidden):
    <li \
class="${(i % 2 and 'even' or 'odd') + ((c.validator and getattr(c.validator, 'required', getattr(c.validator, 'not_empty', False))) and ' required' or '') + (c.error_msg and ' error' or '')}"\
     % if w.hover_help and c.help_text:
title="${c.help_text}" \
     % endif
${tw.attrs(attrs=c.container_attrs)}\
id="${c.compound_id or ''}:container">
     <label for="${c.id}">${c.label or ''}</label>
        ${c.display() | n}
        % if not w.hover_help:
${c.help_text or ''}\
        % endif
        <span id="${c.compound_id or ''}:error" class="error">${c.error_msg or ''}</span>
    </li>
   % endfor
   <li class="error"><span id="${w.compound_id or ''}:error" class="error">\
        %for error in w.rollup_errors:
            <p>${error}</p>
        %endfor
    </span></li>
</ul>
