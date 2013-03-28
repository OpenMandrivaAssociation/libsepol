Summary: SELinux binary policy manipulation library 
Name: libsepol
Version: 2.0.34
Release: %mkrel 2
License: GPL
Group: System/Libraries
URL:	http://www.selinuxproject.org
Source0: http://www.nsa.gov/selinux/archives/libsepol-%{version}.tgz
#Source1: http://www.nsa.gov/selinux/archives/libsepol-%{version}.tgz.sign
#Provides: libsepol.so

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

libsepol provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package -n %{mklibname sepol 1}
Summary: SELinux binary policy manipulation library
Group: System/Libraries

%description -n %{mklibname sepol 1}
libsepol provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package -n %{mklibname sepol -d}
Summary: Header files and libraries used to build policy manipulation tools
Group: Development/C
Requires: %{mklibname sepol 1} = %{version}-%{release}
Provides: sepol-devel = %{version}-%{release}
Obsoletes: %{mklibname sepol 1 -d}

%description -n %{mklibname sepol -d}
The libsepol-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies. 

%package -n %{mklibname sepol -d -s}
Summary: Static libraries used to build policy manipulation tools
Group: Development/C
Requires: %{mklibname sepol -d} = %{version}-%{release}
Provides: sepol-static-devel = %{version}-%{release}
Obsoletes: %{mklibname sepol 1 -d -s}

%description -n %{mklibname sepol -d -s}
The libsepol-devel package contains the static libraries
needed for developing applications that manipulate binary policies. 

%prep
%setup -q
# sparc64 is an -fPIC arch, so we need to fix it here
%ifarch sparc64
sed -i 's/fpic/fPIC/g' src/Makefile
%endif

%build
%{make} clean
%{make} CFLAGS="%{optflags}" CC=%{__cc}

%install
mkdir -p %{buildroot}/%{_lib} 
mkdir -p %{buildroot}/%{_libdir} 
mkdir -p %{buildroot}%{_includedir} 
mkdir -p %{buildroot}%{_bindir} 
mkdir -p %{buildroot}%{_mandir}/man3
mkdir -p %{buildroot}%{_mandir}/man8
%{makeinstall_std} LIBDIR="%{buildroot}%{_libdir}" SHLIBDIR="%{buildroot}/%{_lib}"
rm -f %{buildroot}%{_bindir}/genpolbools
rm -f %{buildroot}%{_bindir}/genpolusers
rm -f %{buildroot}%{_bindir}/chkcon
rm -rf %{buildroot}%{_mandir}/man8

%post -n %{mklibname sepol 1}
[ -x /sbin/telinit ] && [ -p /dev/initctl ]  && /sbin/telinit U
exit 0

%files -n %{mklibname sepol 1}
/%{_lib}/libsepol.so.1

%files -n %{mklibname sepol -d}
%{_libdir}/libsepol.so
%{_includedir}/sepol/*.h
# %exclude %{_mandir}/man3/*.3*
%{_mandir}/man3/*.3*
%dir %{_includedir}/sepol
%dir %{_includedir}/sepol/policydb
%{_includedir}/sepol/policydb/*.h

%files -n %{mklibname sepol -d -s}
%{_libdir}/libsepol.a


%changelog
* Sun Sep 13 2009 Thierry Vignaud <tvignaud@mandriva.com> 2.0.34-2mdv2010.0
+ Revision: 438739
- rebuild

* Sun Nov 30 2008 David Walluck <walluck@mandriva.org> 2.0.34-1mdv2009.1
+ Revision: 308330
- 2.0.34

* Mon Nov 24 2008 David Walluck <walluck@mandriva.org> 2.0.33-1mdv2009.1
+ Revision: 306134
- 2.0.33

* Mon Jul 28 2008 David Walluck <walluck@mandriva.org> 2.0.32-1mdv2009.0
+ Revision: 250775
- don't include .sign file
- 2.0.32

* Sun Jul 27 2008 David Walluck <walluck@mandriva.org> 2.0.30-1mdv2009.0
+ Revision: 250494
- 2.0.30

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Sun Apr 20 2008 David Walluck <walluck@mandriva.org> 2.0.25-1mdv2009.0
+ Revision: 195979
- 2.0.25

* Fri Jan 04 2008 David Walluck <walluck@mandriva.org> 2.0.11-2mdv2008.1
+ Revision: 145372
- rebuild

* Wed Jan 02 2008 David Walluck <walluck@mandriva.org> 2.0.11-1mdv2008.1
+ Revision: 140258
- 2.0.11

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Sep 03 2007 Funda Wang <fundawang@mandriva.org> 2.0.1-2mdv2008.0
+ Revision: 78417
- Obsoletes old devel package

* Sun Sep 02 2007 David Walluck <walluck@mandriva.org> 2.0.1-1mdv2008.0
+ Revision: 78359
- Import libsepol

