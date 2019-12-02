%global gh_commit   77e3805d1662034339c3c19bcdaaa62a56c1fa7e
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    alanxz
%global gh_project  rabbitmq-c
%bcond_with docs

Name:      librabbitmq
Summary:   Client library for AMQP
Version:	0.10.0
Release:	1
License:   MIT
Group:     System/Libraries
URL:       https://github.com/alanxz/rabbitmq-c

Source0:   https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRequires: cmake > 2.8
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(popt)
%if %{with docs}
BuildRequires: xmlto
%endif


%description
This is a C-language AMQP client library for use with AMQP servers
speaking protocol versions 0-9-1.

#--------------------------------------------------------------------

%define libname_major 4
%define libname %mklibname rabbitmq %{libname_major}

%package -n %libname
Summary:    Header files and development libraries for %{name}
Group:      System/Libraries

%description -n %libname
This package contains the header files and development libraries
for %{name}.

%files -n %libname
%{!?_licensedir:%global license %%doc}
%license LICENSE-MIT
%{_libdir}/librabbitmq.so.%{libname_major}{,.*}

#--------------------------------------------------------------------

%define develname %mklibname rabbitmq -d

%package -n %develname
Summary:    Header files and development libraries for %{name}
Group:      Development/Other
Requires:   %libname = %{version}-%{release}

%description -n %develname
This package contains the header files and development libraries
for %{name}.

%files -n %develname
%doc AUTHORS THANKS TODO *.md
%doc Examples
%{_libdir}/librabbitmq.so
%{_includedir}/amqp*
%{_libdir}/pkgconfig/librabbitmq.pc

#--------------------------------------------------------------------

%package tools
Summary:    Example tools built using the librabbitmq package
Group:      Development/Other
Requires:   %libname = %{version}

%description tools
This package contains example tools built using %{name}.

It provides:
amqp-consume        Consume messages from a queue on an AMQP server
amqp-declare-queue  Declare a queue on an AMQP server
amqp-delete-queue   Delete a queue from an AMQP server
amqp-get            Get a message from a queue on an AMQP server
amqp-publish        Publish a message on an AMQP server


%files tools
%{_bindir}/amqp-*
%if %{with docs}
%doc %{_mandir}/man1/amqp-*.1*
%doc %{_mandir}/man7/librabbitmq-tools.7*
%endif

#--------------------------------------------------------------------

%prep
%setup -q -n %{gh_project}-%{gh_commit}
%autopatch -p1

# Copy sources to be included in -devel docs.
cp -pr examples Examples


%build
# static lib required for tests
%cmake \
  -DBUILD_TOOLS_DOCS:BOOL=ON \
  -DBUILD_STATIC_LIBS:BOOL=ON

%make_build


%install
%make_install -C build

rm %{buildroot}%{_libdir}/librabbitmq.a

%check
#: check .pc is usable
#grep @ %{buildroot}%{_libdir}/pkgconfig/librabbitmq.pc && exit 1

#: upstream tests
# broken
#make_build test -C build
