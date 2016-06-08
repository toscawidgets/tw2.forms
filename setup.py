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
_extra_kajiki = ["Kajiki >= 0.5.5"]

requires = [
    "tw2.core>=2.1.4",
    "six",
]

tests_require = [
    #'BeautifulSoup',
    'nose',
    'sieve',
    'coverage',
] + _extra_genshi + _extra_mako + _extra_jinja + _extra_kajiki

if sys.version_info[0] == 2 and sys.version_info[1] <= 5:
    requires.append('WebOb<=1.1.1')
    tests_require.append('WebTest<2.0')
else:
    tests_require.append('WebTest')

if sys.version_info[0] < 3:
    tests_require.append('FormEncode')

setup(
    name='tw2.forms',
    version='2.2.5',
    description='The basic form widgets for ToscaWidgets 2, a web widget toolkit.',
    long_description=open('README.rst').read().split('\n\n', 1)[1],
    author='Paul Johnston, Christopher Perkins, Alberto Valverde Gonzalez & contributors',
    author_email='toscawidgets-discuss@googlegroups.com',
    url="http://toscawidgets.org/",
    download_url="https://pypi.python.org/pypi/tw2.forms/",
    license='MIT',
    install_requires=requires,
    packages=find_packages(exclude=['ez_setup', 'tests']),
    namespace_packages=['tw2'],
    zip_safe=False,
    include_package_data=True,
    test_suite='nose.collector',
    entry_points="""
        [tw2.widgets]
        # Register your widgets so they can be listed in the WidgetBrowser
        tw2.forms = tw2.forms
    """,
    keywords=[
        'toscawidgets.widgets',
    ],
    tests_require=tests_require,
    extras_require={
        'genshi': _extra_genshi,
        'mako': _extra_mako,
        'jinja': _extra_jinja,
        'kajiki': _extra_kajiki,
        'test': tests_require,
        'tests': tests_require,
    },
    classifiers=[
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
