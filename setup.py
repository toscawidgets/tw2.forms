from setuptools import setup, find_packages

setup(
    name='tw2.forms',
    version='2.0a2',
    description='',
    author='Paul Johnston, Christopher Perkins & contributors',
    author_email='paj@pajhome.org.uk',
    url='',
    install_requires=[
        "tw2.core>=2.0a2",
        ## Add other requirements here
        # "Genshi",
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
