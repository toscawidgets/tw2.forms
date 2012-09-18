import sys

from setuptools import setup, find_packages

try:
    import multiprocessing
    import logging
except:
    pass

# Requirements to install buffet plugins and engines
_extra_genshi = ["Genshi >= 0.3.5"]
_extra_mako = ["Mako >= 0.1.1"]
_extra_jinja = ["Jinja2"]

requires=[
    "tw2.core>=2.1.2",
]

if sys.version_info[0] == 2 and sys.version_info[1] <= 5:
    requires.append('WebOb<=1.1.1')

setup(
    name='tw2.forms',
    version='2.1.2',
    description='The basic form widgets for ToscaWidgets 2.',
    long_description = open('README.rst').read().split('\n\n', 1)[1],
    author='Paul Johnston, Christopher Perkins, Alberto Valverde & contributors',
    author_email='paj@pajhome.org.uk',
    url='http://toscawidgets.org',
    install_requires=requires,
    packages=find_packages(exclude=['ez_setup', 'tests']),
    namespace_packages = ['tw2'],
    zip_safe=False,
    include_package_data=True,
    test_suite = 'nose.collector',
    entry_points="""
        [tw2.widgets]
        # Register your widgets so they can be listed in the WidgetBrowser
        tw2.forms = tw2.forms
    """,
    keywords = [
        'toscawidgets.widgets',
    ],
    tests_require = [
        'BeautifulSoup',
        'nose',
        'FormEncode',
        'WebTest',
        'strainer',
    ] + _extra_genshi + _extra_mako + _extra_jinja,
    extras_require = {
        'genshi': _extra_genshi,
        'mako': _extra_mako,
        'jinja': _extra_jinja,
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: ToscaWidgets',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Widget Sets',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
    ],
)
