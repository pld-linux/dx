#
# TODO: - add samples
#	- make static subpackage
#
Summary:	Excellent tool for making visualization of data
Summary(pl):	Doskona³e narzêdzie do wizualizacji danych
Name:		dx
Version:	4.3.2
Release:	2
License:	IPL
Group:		Applications
Source0:	http://opendx.npaci.edu/source/%{name}-%{version}.tar.gz
# Source0-md5:	201afdd86a5ddcfda0dc60fc7b6d3fea
Source1:	http://opendx.npaci.edu/source/%{name}samples-%{version}.tar.gz
# Source1-md5:	940eece74fc2bf001a8017f9df18daac
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.opendx.org/
BuildRequires:	ImageMagick-devel
BuildRequires:	OpenGL-devel-base
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	hdf-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtool
BuildRequires:	libtiff-devel
BuildRequires:	motif-devel
BuildRequires:	netcdf-devel
Requires:	%{name}-libs = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia32	-fomit-frame-pointer

%description
OpenDX is a uniquely powerful, full-featured software package for the
visualization of scientific, engineering and analytical data: Its open
system design is built on a standard interface environments. And its
sophisticated data model provides users with great flexibility in
creating visualizations.

%description -l pl
OpenDX jest w pe³ni funkcjonalnym, o unikalnych mo¿liwo¶ciach,
pakietem do wizualizacji danych naukowych, in¿ynierskich i
analitycznych. Zosta³ zaprojektowany w sposób otwarty, w oparciu o
standardowe ¶rodowiska interfejstów. Jego przemy¶lany model danych
daje u¿ytkownikom du¿± elastyczno¶æ w tworzeniu wizualizacji.

%package libs
Summary:	OpenDX shared libraries
Summary(pl):	Biblioteki wspó³dzielone OpenDX
Group:		Libraries

%description libs
OpenDX shared libraries.

%description libs -l pl
Biblioteki wspó³dzielone OpenDX.

%package devel
Summary:	OpenDX development files
Summary(pl):	Pliki nag³ówkowe OpenDX
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}

%description devel
OpenDX development files.

%description devel -l pl
Pliki nag³ówkowe OpenDX oraz inne pliki, potrzebne do budowania.

%package doc
Summary:	OpenDX documentation
Summary(pl):	Dokumentacja OpenDX
Group:		Documentation

%description doc
Online help and html documentation for OpenDX.

%description doc -l pl
Podrêczna pomoc oraz dokumentacja html dla OpenDX.

%prep
%setup  -q
#%patch0 -p1

%build
rm -f missing aclocal.m4
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--prefix=%{_datadir} \
	--enable-shared \
	--disable-static \
	--disable-dependency-tracking \
	--enable-smp-linux \
	--enable-new-keylayout \
	--without-javadx

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_includedir},%{_mandir}} \
	$RPM_BUILD_ROOT%{_docdir}/%{name}-doc-%{version}

mv $RPM_BUILD_ROOT%{_datadir}/bin/dx $RPM_BUILD_ROOT%{_bindir}
mv $RPM_BUILD_ROOT%{_datadir}/dx/man/manl $RPM_BUILD_ROOT%{_mandir}
mv $RPM_BUILD_ROOT%{_datadir}/dx/include/* $RPM_BUILD_ROOT%{_includedir}
mv $RPM_BUILD_ROOT%{_datadir}/dx/h* $RPM_BUILD_ROOT%{_docdir}/%{name}-doc-%{version}
mv $RPM_BUILD_ROOT%{_datadir}/dx/lib_linux $RPM_BUILD_ROOT%{_libdir}/dx
mv $RPM_BUILD_ROOT%{_datadir}/dx/bin_linux $RPM_BUILD_ROOT%{_libdir}/dx
ln -s %{_libdir}/dx $RPM_BUILD_ROOT%{_datadir}/dx/lib_linux
ln -s %{_libdir}/dx/bin_linux $RPM_BUILD_ROOT%{_datadir}/dx
ln -s %{_docdir}/%{name}-doc-%{version}/help $RPM_BUILD_ROOT%{_datadir}/dx/help
ln -s %{_docdir}/%{name}-doc-%{version}/html $RPM_BUILD_ROOT%{_datadir}/dx/html
rm -rf $RPM_BUILD_ROOT%{_datadir}/{bin,dx/{bin/dx,man,include,doc}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/dx
%attr(755,root,root) %{_datadir}/dx/bin
%{_datadir}/dx/bin_linux
%{_datadir}/dx/fonts
%{_datadir}/dx/lib
%{_datadir}/dx/lib_linux
%{_datadir}/dx/ui
%doc doc/README*
%{_mandir}/manl/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*
%exclude %{_libdir}/dx/*.mak
%exclude %{_libdir}/dx/*.la
%exclude %{_libdir}/dx/*.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_libdir}/dx/*.mak
%{_libdir}/dx/*.la
%{_libdir}/dx/*.so

%files doc
%defattr(644,root,root,755)
%{_docdir}/%{name}-doc-%{version}
%{_datadir}/dx/h*
