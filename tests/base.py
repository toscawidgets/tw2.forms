import os, re, pkg_resources as pk
from copy import copy
from difflib import unified_diff
from cStringIO import StringIO
from cgi import FieldStorage
from tw2.core.middleware import make_middleware
from tw2.core.template import global_engines

#try:
import xml.etree.ElementTree as etree
from xml.parsers.expat import ExpatError
#except ImportError:
#    import cElementTree as etree

rendering_extension_lookup = {'mako':'mak', 'genshi':'html', 'cheetah':'tmpl', 'kid':'kid'}
rm = pk.ResourceManager()

def remove_whitespace_nodes(node):
    new_node = copy(node)
    new_node._children = []
    if new_node.text and new_node.text.strip() == '':
        new_node.text = ''
    if new_node.tail and new_node.tail.strip() == '':
        new_node.tail = ''
    for child in node.getchildren():
        if child is not None:
            child = remove_whitespace_nodes(child)
        new_node.append(child)
    return new_node

def remove_namespace(doc):
    """Remove namespace in the passed document in place."""
    for elem in doc.getiterator():
        match = re.match('(\{.*\})(.*)', elem.tag)
        if match:
            elem.tag = match.group(2)

def replace_escape_chars(needle):
    needle = needle.replace('&nbsp;', ' ')
    needle = needle.replace(u'\xa0', ' ')
    return needle

def fix_xml(needle):
    needle = replace_escape_chars(needle)
    
    # hack to handle weird rendering of <input something="something">
    # I HAVE NO IDEA why genshi does this shit.
    if needle.startswith('<input') and not (needle.endswith('</input>') or needle.endswith('/>')):
        needle += '</input>'
    if ' checked ' in needle:
        needle = needle.replace(' checked ', ' checked="checked" ')
    try:
        needle_node = etree.fromstring(needle)
    except ExpatError:
        raise ExpatError('Could not parse %s into xml.'%needle) 
    needle_node = remove_whitespace_nodes(needle_node)
    remove_namespace(needle_node)
    needle_s = etree.tostring(needle_node)
    return needle_s

def in_xml(needle, haystack):
    try:
        needle_s = fix_xml(needle)
    except ExpatError:
        raise ExpatError('Could not parse needle: %s into xml.'%needle)
    try:
        haystack_s = fix_xml(haystack)
    except ExpatError:
        raise ExpatError('Could not parse haystack: %s into xml.'%haystack)
    return needle_s in haystack_s

def eq_xml(needle, haystack):
    needle_s, haystack_s = map(fix_xml, (needle, haystack))
    return needle_s == haystack_s

def assert_in_xml(needle, haystack):
    assert in_xml(needle, haystack), "%s not found in %s"%(needle, haystack)

def assert_eq_xml(needle, haystack):
    assert eq_xml(needle, haystack), "%s does not equal %s"%(needle, haystack)

    
import tw2.core as twc

def request_local_tst():
#    if _request_id is None:
#        raise KeyError('must be in a request')
    try:
        return _request_local[_request_id]
    except KeyError:
        rl_data = {}
        _request_local[_request_id] = rl_data
        return rl_data

import tw2.core.core
tw2.core.core.request_local = request_local_tst
from tw2.core.core import request_local

_request_local=None
_request_id=None

class WidgetTest(object):
    
    template_engine = 'string'
    params_as_vars = True
    widget = None
    attrs = {}
    params = {}
    expected = ""
    
    def request(self, requestid, mw=None):
        if mw is None:
            mw = self.mw
        global _request_id
        _request_id = requestid
        rl = request_local()
        rl.clear()
        rl['middleware'] = mw
        return request_local_tst()

    def setup(self):
        global _request_id, _request_local
        _request_local = {}
        _request_id = None
        self.mw = make_middleware(None, default_engine=self.template_engine)
        return self.request(1)
    
    def _get_all_possible_engines(self):
        template = self.widget.template
        try:
            engine, template_name = template.split(':', 1)
            yield engine
        except:
            for engine, ext in rendering_extension_lookup.iteritems():
                split = template.rsplit('.', 1)
                if(os.path.isfile(rm.resource_filename(split[0], '.'.join((split[1], ext))))):
                    yield engine

    def _check_rendering_vs_expected(self, engine, attrs, params, expected):
        _request_id = None
        mw = make_middleware(None, preferred_rendering_engines=[engine])
        self.request(1, mw)
        r = self.widget(**attrs).display(**params)
        # reset the cache as not to affect other tests
        global_engines._engine_name_cache = {}
        assert_eq_xml(expected, r)

            
    def test_display(self):
        for engine in self._get_all_possible_engines():
            yield self._check_rendering_vs_expected, engine, self.attrs, self.params, self.expected