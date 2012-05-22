%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global modname tw2.forms

Name:           python-tw2-forms
Version:        2.0.2
Release:        2%{?dist}
Summary:        Forms for ToscaWidgets2

Group:          Development/Languages
License:        MIT
URL:            http://toscawidgets.org
Source0:        http://pypi.python.org/packages/source/t/%{modname}/%{modname}-%{version}.tar.gz
BuildArch:      noarch

# For building, generally
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if %{?rhel}%{!?rhel:0} >= 6
BuildRequires:  python-webob1.0 >= 0.9.7
%else
BuildRequires:  python-webob >= 0.9.7
%endif
BuildRequires:  python-tw2-core
BuildRequires:  python-paste-deploy

# Specifically for the test suite
BuildRequires:  python-nose
BuildRequires:  python-coverage
BuildRequires:  python-BeautifulSoup
BuildRequires:  python-formencode
BuildRequires:  python-webtest
BuildRequires:  python-strainer

# Templating languages for the test suite
BuildRequires:  python-mako
BuildRequires:  python-genshi
BuildRequires:  python-turbokid
BuildRequires:  python-turbocheetah


# Runtime requirements
Requires:       python-tw2-core

%description
ToscaWidgets is a web widget toolkit for Python to aid in the creation,
packaging and distribution of common view elements normally used in the web.

tw2.forms contains the basic form widgets.

%prep
%setup -q -n %{modname}-%{version}

%if %{?rhel}%{!?rhel:0} >= 6

# Make sure that epel/rhel picks up the correct version of webob
awk 'NR==1{print "import __main__; __main__.__requires__ = __requires__ = [\"WebOb>=1.0\"]; import pkg_resources"}1' setup.py > setup.py.tmp
mv setup.py.tmp setup.py

# Remove all the fancy nosetests configuration for older python
rm setup.cfg

%endif

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root %{buildroot}

%check
PYTHONPATH=$(pwd) python setup.py test

%files
%doc README.txt LICENSE.txt
%{python_sitelib}/*

%changelog
* Mon Apr 30 2012 Ralph Bean <rbean@redhat.com> - 2.0.2-2
- Removed clean section
- Removed defattr in files section
- Removed unnecessary references to buildroot

* Wed Apr 11 2012 Ralph Bean <rbean@redhat.com> - 2.0.2-1
- Update for latest tw2.forms release.
- Fixes rpmlint errors.  Execution bit in templates, wat?
- Added dist macro to release field.
- Added awk line to make sure pkg_resources picks up the right WebOb on el6

* Thu Apr 05 2012 Ralph Bean <rbean@redhat.com> - 2.0.1-1
- Update for latest tw2.forms release.

* Thu Jun 16 2011 Luke Macken <lmacken@redhat.com> - 2.0-0.1.b4
- Initial package
