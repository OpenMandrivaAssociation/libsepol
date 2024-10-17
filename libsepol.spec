# major is the part of the library name after the .so
%define major 2
%define libname %mklibname sepol
%define develname %mklibname sepol -d
%define stdevelname %mklibname sepol -d -s

# For static lib
%define _disable_lto 1

# Work around build system deficiency
%undefine _debugsource_packages

Summary: 	SELinux binary policy manipulation library
Name: 		libsepol
Version: 	3.7
Release: 	1
License: 	GPL
Group: 		System/Libraries
URL:		https://www.selinuxproject.org
Source0:	https://github.com/SELinuxProject/selinux/releases/download/%{version}/libsepol-%{version}.tar.gz
BuildRequires:	flex

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
Summary: SELinux binary policy manipulation library
Group: System/Libraries
Provides: libsepol = %{version}-%{release}

%description -n %{libname}
libsepol provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package -n %{develname}
Summary: Header files and libraries used to build policy manipulation tools
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}
Provides: sepol-devel = %{version}-%{release}

%description -n %{develname}
The libsepol-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies.

%package -n %{stdevelname}
Summary: Static libraries used to build policy manipulation tools
Group: Development/C
Requires: %{develname} = %{version}-%{release}
Provides: %{name}-static-devel = %{version}-%{release}
Provides: sepol-static-devel = %{version}-%{release}

%description -n %{stdevelname}
The libsepol-devel package contains the static libraries
needed for developing applications that manipulate binary policies.

%prep
%autosetup -p1

%build
%make clean
%make CFLAGS="%{optflags}" CC="%{__cc}" LDFLAGS="%{build_ldflags}"

%install
mkdir -p %{buildroot}/%{_lib}
mkdir -p %{buildroot}/%{_libdir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man3
mkdir -p %{buildroot}%{_mandir}/man8
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_libdir}" install
rm -f %{buildroot}%{_bindir}/genpolbools
rm -f %{buildroot}%{_bindir}/genpolusers
rm -f %{buildroot}%{_bindir}/chkcon
rm -rf %{buildroot}%{_mandir}/man8
rm -rf %{buildroot}%{_mandir}/ru/man8

# Get rid of -I/usr/include and -L/usr/lib64 nastiness
sed -i -e '/^Cflags:/d' -e 's/-L\${libdir} //g' %{buildroot}%{_libdir}/pkgconfig/*.pc

%files
%{_bindir}/sepol_check_access
%{_bindir}/sepol_compute_av
%{_bindir}/sepol_compute_member
%{_bindir}/sepol_compute_relabel
%{_bindir}/sepol_validate_transition

%files -n %{libname}
%{_libdir}/libsepol.so.%{major}

%files -n %{develname}
%{_mandir}/man3/*.3.*
%{_libdir}/libsepol.so
%{_libdir}/pkgconfig/libsepol.pc
%{_includedir}/sepol

%files -n %{stdevelname}
%{_libdir}/libsepol.a
