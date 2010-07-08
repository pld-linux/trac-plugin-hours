%define		trac_ver	0.11
%define		plugin		trachours
Summary:	Trac plugin to track hours spent on tickets
Name:		trac-plugin-hours
Version:	0.3.1
Release:	2
License:	BSD-like
Group:		Applications/WWW
# Source0Download:	http://trac-hacks.org/changeset/latest/trachoursplugin?old_path=/&filename=trachoursplugin&format=zip
Source0:	trachoursplugin.zip
# Source0-md5:	7f1c462b4fbcc4a52aceaf1bf66de6d4
URL:		http://trac-hacks.org/wiki/TracHoursPlugin
BuildRequires:	python-devel
BuildRequires:	unzip
Requires:	python >= 1:2.4
Requires:	python-dateutil >= 1.3-4
Requires:	python-feedparser
Requires:	trac >= %{trac_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The goal of this plugin is to help keep trac of hours worked on
tickets.

%prep
%setup -q -n %{plugin}plugin

%build
cd %{trac_ver}
%{__python} setup.py build
%{__python} setup.py egg_info

%install
rm -rf $RPM_BUILD_ROOT
cd %{trac_ver}
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	%banner -e %{name} <<-'EOF'
	To enable the %{plugin} plugin, add to conf/trac.ini:

	[components]
	%{plugin}.* = enabled

	Add users to the group TICKET_ADD_HOURS.

	You will need to run trac-admin <env> upgrade in order to create the correct database tables.
EOF
fi

%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/%{plugin}
%{py_sitescriptdir}/*-*.egg-info
