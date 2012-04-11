from setuptools import setup, find_packages

import multiprocessing, logging

# Requirements to install buffet plugins and engines
_extra_cheetah = ["Cheetah>=1.0", "TurboCheetah>=0.9.5"]
_extra_genshi = ["Genshi >= 0.3.5"]
_extra_kid = ["kid>=0.9.5", "TurboKid>=0.9.9"]
_extra_mako = ["Mako >= 0.1.1"]

setup(
    name='tw2.forms',
    version='2.0.2',
    description='The basic form widgets for ToscaWidgets 2.',
    long_description = open('README.txt').read().split('\n\n', 1)[1],
    author='Paul Johnston, Christopher Perkins, Alberto Valverde & contributors',
    author_email='paj@pajhome.org.uk',
    url='http://toscawidgets.org',
    install_requires=[
        "tw2.core>=2.0b4",
        ],
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
    ] + _extra_cheetah + _extra_genshi + _extra_kid + _extra_mako,
    extras_require = {
        'cheetah': _extra_cheetah,
        'kid': _extra_kid,
        'genshi': _extra_genshi,
        'mako': _extra_mako,
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
