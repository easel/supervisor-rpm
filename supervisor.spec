%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
Summary:  A System for Allowing the Control of Process State on UNIX
Name: supervisor
Version: 2.1
Release: 3%{?dist}

License: ZPL/BSD
Group: System Environment/Base
URL: http://www.plope.com/software/supervisor2/
Source: http://www.plope.com/software/supervisor2/%{name}-%{version}.tar.gz
Source1: supervisord.init
Source2: supervisord.conf
Source3: supervisor.logrotate
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: python-devel

Requires: python-meld3
Requires(preun): /sbin/service, /sbin/chkconfig
Requires(postun): /sbin/service, /sbin/chkconfig


%description
The supervisor is a client/server system that allows its users to control a
number of processes on UNIX-like operating systems.

%prep
%setup -q

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
%{__rm} -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/logrotate.d/
%{__mkdir} -p %{buildroot}/%{_initrddir}
%{__mkdir} -p %{buildroot}/%{_localstatedir}/log/%{name}
%{__chmod} 770 %{buildroot}/%{_localstatedir}/log/%{name}
%{__install} -p -m 755 %{SOURCE1} %{buildroot}/%{_initrddir}/supervisord
%{__install} -p -m 644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/supervisord.conf
%{__install} -p -m 644 %{SOURCE3} %{buildroot}/%{_sysconfdir}/logrotate.d/supervisor
%{__sed} -i s'/^#!.*//' $( find %{buildroot}/%{python_sitelib}/supervisor/ -type f)

%{__rm} -rf %{buildroot}/%{python_sitelib}/supervisor/meld3/

%clean
%{__rm} -rf %{buildroot}

%post
/sbin/chkconfig --add %{name}d || :

%preun
if [ $1 = 0 ]; then
    /sbin/service supervisord stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}d || :
fi

%files
%defattr(-,root,root,-)
%doc README.txt LICENSES.txt TODO.txt CHANGES.txt COPYRIGHT.txt
%dir %{_localstatedir}/log/%{name}
%{_initrddir}/supervisord
%{python_sitelib}/supervisor/
%{_bindir}/supervisor*

%config(noreplace) %{_sysconfdir}/supervisord.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/supervisor

%changelog
* Sun Apr 22 2007 Mike McGrath <mmcgrath@redhat.com> 2.1-3
- Added BuildRequires of python-devel

* Fri Apr 20 2007 Mike McGrath <mmcgrath@redhat.com> 2.1-2
- Added patch suggested in #153225

* Fri Apr 20 2007 Mike McGrath <mmcgrath@redhat.com> 2.1-1
- Initial packaging

