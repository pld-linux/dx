Summary:	Excellent tool for making visualization of data
Summary(pl.UTF-8):	Doskonałe narzędzie do wizualizacji danych
Name:		dx
Version:	4.4.4
Release:	28
License:	IPL
Group:		Applications/Science
Source0:	http://opendx.npaci.edu/source/%{name}-%{version}.tar.gz
# Source0-md5:	6da0c4cd21d3c08f97b7662e3aee5b7b
Source1:	http://opendx.npaci.edu/source/%{name}samples-4.4.0.tar.gz
# Source1-md5:	e8f43722ca0a66282608bded7c0e4f93
Source2:	%{name}.desktop
Patch1:		%{name}-nolibs.patch
Patch2:		%{name}samples-DESTDIR.patch
Patch3:		%{name}samples-unused_bin.patch
Patch4:		%{name}-include.patch
Patch5:		%{name}-ac.patch
Patch6:		%{name}-ImageMagic.patch
Patch7:		%{name}-open.patch
Patch8:		%{name}-gcc43.patch
Patch9:		format-security.patch
Patch10:	%{name}-narrowing.patch
Patch11:	%{name}-conversion.patch
Patch12:	%{name}-c99.patch
Patch13:	%{name}-types.patch
URL:		http://www.opendx.org/
BuildRequires:	ImageMagick-devel >= 1:6.2.4.0
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	cdflib-devel
BuildRequires:	flex
BuildRequires:	hdf-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	motif-devel
BuildRequires:	netcdf-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXmu-devel
BuildRequires:	xorg-lib-libXp-devel
BuildRequires:	xorg-lib-libXpm-devel
BuildRequires:	xorg-lib-libXt-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	openssh-clients
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia32	-fomit-frame-pointer
%define		skip_post_check_so	libDXL.so.*

%description
OpenDX is a uniquely powerful, full-featured software package for the
visualization of scientific, engineering and analytical data: Its open
system design is built on a standard interface environments. And its
sophisticated data model provides users with great flexibility in
creating visualizations.

%description -l pl.UTF-8
OpenDX jest w pełni funkcjonalnym, o unikalnych możliwościach,
pakietem do wizualizacji danych naukowych, inżynierskich i
analitycznych. Został zaprojektowany w sposób otwarty, w oparciu o
standardowe środowiska interfejsów. Jego przemyślany model danych daje
użytkownikom dużą elastyczność w tworzeniu wizualizacji.

%package libs
Summary:	OpenDX shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone OpenDX
Group:		Libraries

%description libs
OpenDX shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone OpenDX.

%package devel
Summary:	OpenDX development files
Summary(pl.UTF-8):	Pliki nagłówkowe OpenDX
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
OpenDX development files.

%description devel -l pl.UTF-8
Pliki nagłówkowe OpenDX oraz inne pliki, potrzebne do budowania.

%package static
Summary:	OpenDX static libraries
Summary(pl.UTF-8):	Biblioteki statyczne OpenDX
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
OpenDX static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne OpenDX.

%package doc
Summary:	OpenDX documentation
Summary(pl.UTF-8):	Dokumentacja OpenDX
Group:		Documentation
BuildArch:	noarch

%description doc
Online help and html documentation for OpenDX.

%description doc -l pl.UTF-8
Podręczna pomoc oraz dokumentacja html dla OpenDX.

%package examples
Summary:	OpenDX Examples
Summary(pl.UTF-8):	Przykłady dla OpenDX
Group:		Documentation
BuildArch:	noarch

%description examples
Examples for OpenDX.

%description examples -l pl.UTF-8
Przykłady dla OpenDX.

%prep
%setup  -q -a 1
%patch -P 1 -p1
%patch -P 2 -p0
%patch -P 3 -p1
%patch -P 4 -p1
%patch -P 5 -p1
%patch -P 6 -p1
%patch -P 7 -p1
%patch -P 8 -p1
%patch -P 9 -p1
%patch -P 10 -p1
%patch -P 11 -p1
%patch -P 12 -p1
%patch -P 13 -p1

%build
%if "%{_ver_ge '%{cxx_version}' '11.0'}" == "1"
# lower C++ standard because C++17 std::byte conflicts with local "byte" define
export CXXFLAGS="%{rpmcxxflags} -std=c++14"
%endif
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
CPPFLAGS="%{rpmcppflags} -I/usr/include/cdf"
%configure \
	--prefix=%{_datadir} \
	--enable-shared \
	--enable-static \
	--disable-dependency-tracking \
	--enable-smp-linux \
	--enable-new-keylayout \
	--without-javadx \
	--with-rsh=%{_bindir}/ssh

cd %{name}samples-4.4.0
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--prefix=%{_examplesdir} \
	--without-javadx
cd ..

%{__make} -j1

%{__make} -j1 -C %{name}samples-4.4.0

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C %{name}samples-4.4.0 install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir},%{_mandir},%{_desktopdir},%{_pixmapsdir}}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
cp -p src/uipp/ui/icon50.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/dx.xpm
%{__mv} $RPM_BUILD_ROOT%{_datadir}/bin/dx $RPM_BUILD_ROOT%{_bindir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/dx/man/manl $RPM_BUILD_ROOT%{_mandir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/dx/include/* $RPM_BUILD_ROOT%{_includedir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/dx/lib_linux $RPM_BUILD_ROOT%{_libdir}/dx
%{__mv} $RPM_BUILD_ROOT%{_datadir}/dx/bin_linux $RPM_BUILD_ROOT%{_libdir}/dx
%{__mv} $RPM_BUILD_ROOT%{_examplesdir}/dx/samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
ln -s %{_libdir}/dx $RPM_BUILD_ROOT%{_datadir}/dx/lib_linux
ln -s %{_libdir}/dx/bin_linux $RPM_BUILD_ROOT%{_datadir}/dx
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{bin,dx/{bin/dx,man,include,doc}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/README*
%attr(755,root,root) %{_bindir}/dx
%dir %{_datadir}/dx
%attr(755,root,root) %{_datadir}/dx/bin
%{_datadir}/dx/bin_linux
%{_datadir}/dx/fonts
%{_datadir}/dx/lib
%{_datadir}/dx/lib_linux
%{_datadir}/dx/ui
# FIXME: should be dx(1)
%{_mandir}/manl/dx.l*
%{_desktopdir}/dx.desktop
%{_pixmapsdir}/dx.xpm

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/dx
%dir %{_libdir}/dx/bin_linux
%attr(755,root,root) %{_libdir}/dx/bin_linux/*
%attr(755,root,root) %{_libdir}/dx/libDX.so.*.*.*
%{_libdir}/dx/libDX.so.4
%attr(755,root,root) %{_libdir}/dx/libDXL.so.*.*.*
%{_libdir}/dx/libDXL.so.4
%attr(755,root,root) %{_libdir}/dx/libDXcallm.so.*.*.*
%{_libdir}/dx/libDXcallm.so.4
%attr(755,root,root) %{_libdir}/dx/libDXlite.so.*.*.*
%{_libdir}/dx/libDXlite.so.4

%files devel
%defattr(644,root,root,755)
%{_libdir}/dx/libDX.so
%{_libdir}/dx/libDXL.so
%{_libdir}/dx/libDXcallm.so
%{_libdir}/dx/libDXlite.so
%{_includedir}/dx
%{_includedir}/dxconfig.h
%{_includedir}/dxl.h
%{_includedir}/dxstereo.h
%{_libdir}/dx/libDX*.la
%{_libdir}/dx/arch.mak

%files static
%defattr(644,root,root,755)
%{_libdir}/dx/libDX*.a

%files doc
%defattr(644,root,root,755)
%{_datadir}/dx/help
%{_datadir}/dx/html

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
