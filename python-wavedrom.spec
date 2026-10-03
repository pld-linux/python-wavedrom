#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_with	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	WaveDrom compatible Python command line
Summary(pl.UTF-8):	Narzędzie pythonowe zgodne z WaveDrom
Name:		python-wavedrom
Version:	2.0.3.post3
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/wavedrom/
Source0:	https://files.pythonhosted.org/packages/source/w/wavedrom/wavedrom-%{version}.tar.gz
# Source0-md5:	1fa386c34d9b6b59ba5e0b0556d5939b
URL:		https://pypi.org/project/wavedrom/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm
%if %{with tests}
BuildRequires:	python-PyYAML
BuildRequires:	python-cairosvg < 2
BuildRequires:	python-pillow
BuildRequires:	python-six
BuildRequires:	python-svgwrite
BuildRequires:	python-xmldiff
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	python3-PyYAML
BuildRequires:	python3-cairosvg
BuildRequires:	python3-pillow
BuildRequires:	python3-six
BuildRequires:	python3-svgwrite
BuildRequires:	python3-xmldiff
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a Python module and command line fully compatible with
WaveDrom (<https://wavedrom.com/>), which is originally implemented in
JavaScript. It is useful if you want to generate wavedrom diagrams
from a Python environment or simply don't want to install the Node.js
environment just to use WaveDrom as simple command line.

%description -l pl.UTF-8
Ten pakiet to moduł Pythona i narzędzie linii poleceń w pełni zgodne z
WaveDrom (<https://wavedrom.com/>), który jest oryginalnie
zaimplementowany w JavaScripcie. Jest przydatny, aby generować
diagramy wavedrom ze środowiska pythonowego, albo gdy nie chcemy
instalować środowiska Node.js tylko po to, aby używać WaveDrom z linii
poleceń.

%package -n python3-wavedrom
Summary:	WaveDrom compatible Python command line
Summary(pl.UTF-8):	Narzędzie pythonowe zgodne z WaveDrom
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3

%description -n python3-wavedrom
This is a Python module and command line fully compatible with
WaveDrom (<https://wavedrom.com/>), which is originally implemented in
JavaScript. It is useful if you want to generate wavedrom diagrams
from a Python environment or simply don't want to install the Node.js
environment just to use WaveDrom as simple command line.

%description -n python3-wavedrom -l pl.UTF-8
Ten pakiet to moduł Pythona i narzędzie linii poleceń w pełni zgodne z
WaveDrom (<https://wavedrom.com/>), który jest oryginalnie
zaimplementowany w JavaScripcie. Jest przydatny, aby generować
diagramy wavedrom ze środowiska pythonowego, albo gdy nie chcemy
instalować środowiska Node.js tylko po to, aby używać WaveDrom z linii
poleceń.

%prep
%setup -q -n wavedrom-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest test
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
# test_upstream fails because of svgwrite differences
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest test -k 'not test_upstream'
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/wavedrompy{,-2}

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/wavedrompy-2
%{py_sitescriptdir}/wavedrom
%{py_sitescriptdir}/wavedrom-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-wavedrom
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/wavedrompy
%{py3_sitescriptdir}/wavedrom
%{py3_sitescriptdir}/wavedrom-%{version}-py*.egg-info
%endif
