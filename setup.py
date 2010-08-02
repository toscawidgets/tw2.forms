from setuptools import setup, find_packages

setup(
    name='tw2.forms',
    version='2.0b4',
    description='The basic form widgets for ToscaWidgets 2.',
    long_description = open('README.txt').read().split('\n\n', 1)[1],
    author='Paul Johnston, Christopher Perkins, Alberto Valverde & contributors',
    author_email='paj@pajhome.org.uk',
    url='http://toscawidgets.org/docs/tw2.core/',
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
    tests_require = ['BeautifulSoup'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: ToscaWidgets',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Widget Sets',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
