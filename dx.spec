Summary:	Excelent tool to making visualization of data.	
Summary(pl):	Doskonale narzedzie do vizualizacji danych
Name:		dx	
Version:	4.1.0
Release:	1
Group:		Applications
Copyright:	IPL
Source0:	http://opendx.npaci.edu/source/%{name}-%{version}.tar.gz
Source1:	http://opendx.npaci.edu/source/%{name}samples-4.0.8.tar.gz
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-acfix.patch
URL:		http://www.opendx.org	
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

%prep
%setup  -q
%patch0 -p1
%patch1 -p1

%build
autoheader;autoconf;automake; 

%configure 	--prefix=%{_prefix}	\
		--datadir=%{_datadir}	\
		--mandir=%{_mandir}	

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/%{name}
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}
install -d $RPM_BUILD_ROOT%{_includedir}/%{name}
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}


%{__make} install DESTDIR=$RPM_BUILD_ROOT


gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	README ChangeLog 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_includedir}/*
%{_includedir}/dx/*
%{_libdir}/*
%doc /usr/share/doc/dx/*
%doc /usr/share/doc/dx/html/*
%{_datadir}/dx/fonts/*
%{_datadir}/dx/bin/*
%{_datadir}/dx/help/*
%{_datadir}/dx/ui/*
