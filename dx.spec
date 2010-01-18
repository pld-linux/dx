Summary:	Excellent tool for making visualization of data
Summary(pl.UTF-8):	Doskonałe narzędzie do wizualizacji danych
Name:		dx
Version:	4.4.4
Release:	8
License:	IPL
Group:		Applications
Source0:	http://opendx.npaci.edu/source/%{name}-%{version}.tar.gz
# Source0-md5:	6da0c4cd21d3c08f97b7662e3aee5b7b
Source1:	http://opendx.npaci.edu/source/%{name}samples-4.4.0.tar.gz
# Source1-md5:	e8f43722ca0a66282608bded7c0e4f93
Source2:	%{name}.desktop
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-nolibs.patch
Patch2:		dxsamples-DESTDIR.patch
Patch3:		dxsamples-unused_bin.patch
Patch4:		%{name}-include.patch
Patch5:		%{name}-ac.patch
Patch6:		%{name}-ImageMagic.patch
Patch7:		%{name}-open.patch
Patch8:		%{name}-gcc43.patch
URL:		http://www.opendx.org/
BuildRequires:	ImageMagick-devel >= 1:6.2.4.0
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	hdf-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtool
BuildRequires:	libtiff-devel
BuildRequires:	motif-devel
BuildRequires:	netcdf-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXpm-devel
Requires:	openssh-clients
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia32	-fomit-frame-pointer

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
standardowe środowiska interfejsów. Jego przemyślany model danych
daje użytkownikom dużą elastyczność w tworzeniu wizualizacji.

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

%description doc
Online help and html documentation for OpenDX.

%description doc -l pl.UTF-8
Podręczna pomoc oraz dokumentacja html dla OpenDX.

%package examples
Summary:	OpenDX Examples
Summary(pl.UTF-8):	Przykłady dla OpenDX
Group:		Documentation

%description examples
Examples for OpenDX.

%description examples -l pl.UTF-8
Przykłady dla OpenDX.

%prep
%setup  -q -a 1
#%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
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

install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}
install src/uipp/ui/icon50.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/dx.xpm
mv $RPM_BUILD_ROOT%{_datadir}/bin/dx $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_datadir}/dx/man/manl $RPM_BUILD_ROOT%{_mandir}
mv $RPM_BUILD_ROOT%{_datadir}/dx/include/* $RPM_BUILD_ROOT%{_includedir}
mv $RPM_BUILD_ROOT%{_datadir}/dx/lib_linux $RPM_BUILD_ROOT%{_libdir}/dx
mv $RPM_BUILD_ROOT%{_datadir}/dx/bin_linux $RPM_BUILD_ROOT%{_libdir}/dx
mv $RPM_BUILD_ROOT%{_examplesdir}/dx/samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
ln -s %{_libdir}/dx $RPM_BUILD_ROOT%{_datadir}/dx/lib_linux
ln -s %{_libdir}/dx/bin_linux $RPM_BUILD_ROOT%{_datadir}/dx
rm -rf $RPM_BUILD_ROOT%{_datadir}/{bin,dx/{bin/dx,man,include,doc}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/README*
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/dx
%attr(755,root,root) %{_datadir}/dx/bin
%{_datadir}/dx/bin_linux
%{_datadir}/dx/fonts
%{_datadir}/dx/lib
%{_datadir}/dx/lib_linux
%{_datadir}/dx/ui
%{_mandir}/manl/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*

%files libs
%defattr(644,root,root,755)
%dir %{_libdir}/dx
%attr(755,root,root) %{_libdir}/dx/bin_linux
%attr(755,root,root) %{_libdir}/dx/lib*.so.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_libdir}/dx/*.mak
%{_libdir}/dx/*.la
%{_libdir}/dx/*.so

%files static
%defattr(644,root,root,755)
%{_libdir}/dx/*.a

%files doc
%defattr(644,root,root,755)
%{_datadir}/dx/h*

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
