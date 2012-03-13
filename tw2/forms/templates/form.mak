<%namespace name="tw" module="tw2.core.mako_util"/>\
<form ${tw.attrs(attrs=w.attrs)}>
     <span class="error">${w.error_msg or ''}</span>
     % if w.help_msg:
     <div class="help">
      <p>
         ${w.help_msg}
      </p>
     </div>
     % endif
    ${w.child.display() | n}
	% for button in w.buttons:
		${button.display() | n}
	% endfor
</form>
