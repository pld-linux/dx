Summary:	Excelent tool to making visualization of data
Summary(pl):	Doskona³e narzêdzie do wizualizacji danych
Name:		dx	
Version:	4.1.3
Release:	1
Group:		Applications
Group(de):	Applikationen
Group(pl):	Aplikacje
License:	IPL
Source0:	http://opendx.npaci.edu/source/%{name}-%{version}.tar.gz
Source1:	http://opendx.npaci.edu/source/%{name}samples-%{version}.tar.gz
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-acfix.patch
URL:		http://www.opendx.org	
BuildRequires:	flex
BuildRequires:	ImageMagick-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _prefix         /usr/X11R6
%define         _mandir         %{_prefix}/man

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

%prep
%setup  -q
%patch0 -p1
%patch1 -p1

%build
rm -f missing
#autoheader
#aclocal
#autoconf
#automake -a -c
%configure2_13 \
	--prefix=%{_prefix} \
	--datadir=%{_datadir} \
	--mandir=%{_mandir}	

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
#install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
#install -d $RPM_BUILD_ROOT%{_docdir}/%{name}
#install -d $RPM_BUILD_ROOT%{_includedir}/%{name}
#install -d $RPM_BUILD_ROOT%{_libdir}/%{name}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf README ChangeLog 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_includedir}/*
%{_libdir}/*
%doc *.gz
%dir %{_datadir}/dx
%{_datadir}/dx/fonts
%{_datadir}/dx/bin
%{_datadir}/dx/help
%{_datadir}/dx/ui
