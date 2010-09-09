%define		trac_ver	0.12
%define		plugin		trachours
Summary:	Trac plugin to track hours spent on tickets
Name:		trac-plugin-hours
Version:	0.5.2
Release:	2
License:	BSD-like
Group:		Applications/WWW
Source0:	http://trac-hacks.org/changeset/latest/trachoursplugin?old_path=/&filename=trachoursplugin&format=zip#/trachoursplugin.zip
# Source0-md5:	0c51648583b3c467ff91954591c08462
URL:		http://trac-hacks.org/wiki/TracHoursPlugin
BuildRequires:	python-devel
BuildRequires:	unzip
Requires:	python >= 1:2.4
Requires:	python-dateutil >= 1.3-4
Requires:	python-feedparser
Requires:	trac >= %{trac_ver}
Requires:	trac-plugin-componentdependency
Requires:	trac-plugin-sqlhelper
Requires:	trac-plugin-ticketsidebarprovider
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The goal of this plugin is to help keep trac of hours worked on
tickets.

%prep
%setup -qc
mv %{plugin}plugin/%{trac_ver}/* .

%build
%{__python} setup.py build
%{__python} setup.py egg_info

ver=$(awk '$1 == "Version:" {print $2}' *.egg-info/PKG-INFO)
test "$ver" = %{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
trac-enableplugin "trachours.*"

if [ "$1" = "1" ]; then
	%banner -e %{name} <<-'EOF'

	Add users to the group TICKET_ADD_HOURS so they can fill hours.
	You will need to run trac-admin <env> upgrade in order to create the correct database tables.
EOF
fi

%files
%defattr(644,root,root,755)
%doc README.txt
%{py_sitescriptdir}/%{plugin}
%{py_sitescriptdir}/*-*.egg-info
