%define major	1
%define libname %mklibname sepol %{major}
%define devname %mklibname sepol -d
%define statname %mklibname sepol -d -s
# for static lib
%define _disable_lto 1

Summary:	SELinux binary policy manipulation library 
Name:		libsepol
Version:	2.8
Release:	2
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.selinuxproject.org
Source0:	https://github.com/SELinuxProject/selinux/releases/download/20180524/%{name}-%{version}.tar.gz
BuildRequires:	flex-devel

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

%package -n %{libname}
Summary:	SELinux binary policy manipulation library
Group:		System/Libraries

%description -n %{libname}
libsepol provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package -n %{devname}
Summary:	Header files and libraries used to build policy manipulation tools
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	sepol-devel = %{version}-%{release}

%description -n %{devname}
The libsepol-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies. 

%package -n %{statname}
Summary:	Static libraries used to build policy manipulation tools
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Provides:	sepol-static-devel = %{version}-%{release}

%description -n %{statname}
The libsepol-devel package contains the static libraries
needed for developing applications that manipulate binary policies. 

%prep
%setup -q
# sparc64 is an -fPIC arch, so we need to fix it here
%ifarch sparc64
sed -i 's/fpic/fPIC/g' src/Makefile
%endif

%build
%make clean
%make CFLAGS="%{optflags}" CC=%{__cc}

%install
mkdir -p %{buildroot}/%{_lib} 
mkdir -p %{buildroot}/%{_libdir} 
mkdir -p %{buildroot}%{_includedir} 
mkdir -p %{buildroot}%{_bindir} 
mkdir -p %{buildroot}%{_mandir}/man3
mkdir -p %{buildroot}%{_mandir}/man8
%makeinstall_std LIBDIR="/%{_libdir}" SHLIBDIR="/%{_lib}"
rm %{buildroot}%{_bindir}/chkcon
rm -r %{buildroot}%{_mandir}/man8

%post -n %{libname}
[ -x /sbin/telinit ] && [ -p /dev/initctl ]  && /sbin/telinit U
exit 0

%files -n %{libname}
/%{_lib}/libsepol.so.1

%files -n %{devname}
%{_libdir}/libsepol.so
%{_libdir}/pkgconfig/libsepol.pc
%{_includedir}/sepol/*.h
%dir %{_includedir}/sepol/cil
%{_includedir}/sepol/cil/*.h
%{_mandir}/man3/*.3*
%dir %{_includedir}/sepol
%dir %{_includedir}/sepol/policydb
%{_includedir}/sepol/policydb/*.h

%files -n %{statname}
%{_libdir}/libsepol.a
