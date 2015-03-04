#
# spec file for package 
#

%define _topdir     %(pwd)/rpmbuild
%define _tmppath    %{_topdir}/tmp
# add version and relase, so we can update rpm later if new change is committed
%define version     1.1 
%define release     2

Name:           webservicefib
Version:        %{version}
Release:        %{release}
License:        Copyright (C) 2015, All Rights Reserved, by Bo Yang
Summary:        WebService for Fib
Url:            http://10.5.115.43
Group:          ASD/EMC
BuildRoot:      %{_topdir}/BUILD

%description
WebService for Fibonacci Func

#%prep
#%build
#we reply on Makefile to build, so skip these steps

#%install
#%make_install

%files
%defattr(-,root,root)
/etc/init.d/webservice_fib
/etc/logrotate.d/webservice_fib.lr
/var/webservice/fib.py
/var/webservice/daemon.py
/var/webservice/httpserverthread.py

%pre
# stop it first for rpm update
if [ $1 -eq 2 ]; then
    service webservice_fib stop
    sleep 2
fi

exit 0

%post
chkconfig webservice_fib on
service webservice_fib start

%preun
# if remove, do clean up
if [ $1 -eq 0 ]; then
    service webservice_fib stop
    chkconfig webservice_fib off
fi

exit 0

%postun

%changelog
