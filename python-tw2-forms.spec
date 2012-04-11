%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global modname tw2.forms

Name:           python-tw2-forms
Version:        2.0.2
Release:        1
Summary:        Forms for ToscaWidgets2

Group:          Development/Languages
License:        MIT
URL:            http://toscawidgets.org
Source0:        http://pypi.python.org/packages/source/t/%{modname}/%{modname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build \
    --install-data=%{_datadir} --root %{buildroot}

%check
PYTHONPATH=$(pwd) python setup.py test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.txt LICENSE.txt
%{python_sitelib}/*

%changelog
* Wed Apr 11 2012 Ralph Bean <rbean@redhat.com> - 2.0.2-1
- Update for latest tw2.forms release.
- Fixes rpmlint errors.  Execution bit in templates, wat?

* Thu Apr 05 2012 Ralph Bean <rbean@redhat.com> - 2.0.1-1
- Update for latest tw2.forms release.

* Thu Jun 16 2011 Luke Macken <lmacken@redhat.com> - 2.0-0.1.b4
- Initial package
