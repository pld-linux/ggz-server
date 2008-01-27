# TODO:
# - update for db 4.6 (now it's ready for 4.[01234])
# - check *.dsc and *.room files. Are we need them?

Summary:	Main GGZ server
Summary(pl.UTF-8):	Główny serwer GGZ
Name:		ggz-server
Version:	0.0.14
Release:	0.1
License:	GPL v2+
Group:		Applications
Source0:	http://ftp.belnet.be/packages/ggzgamingzone/ggz/0.0.14/%{name}-%{version}.tar.gz
# Source0-md5:	7e30eedefb69834d9f76fdf7fed646ea
Source1:	%{name}.init
URL:		http://www.ggzgamingzone.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	avahi-devel
BuildRequires:	db-devel >= 4
BuildRequires:	expat-devel >= 1.95
BuildRequires:	libggz-devel >= 0.0.14
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the main GGZ server, some administrative
utilities, a game server handling library and lots of game servers.

%description -l pl.UTF-8
Ta paczka zawiera główny serwer GGZ, kilka narzędzi
administracyjnych, bibliotekę sterującą serwerem oraz dużo
serwerów gier.

%package devel
Summary:	Header files for ggz-server library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ggz-server
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libggz-devel >= 0.0.14

%description devel
Header files for ggz-server library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ggz-server.

%package static
Summary:	Static ggz-server library
Summary(pl.UTF-8):	Statyczna biblioteka ggz-server
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ggz-server library.

%description static -l pl.UTF-8
Statyczna biblioteka ggz-server.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4 -I m4/ggz
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,ggzd}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ggzd

:> $RPM_BUILD_ROOT/etc/ggzd/ggzd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add ggzd
%service ggzd restart

%preun
if [ "$1" = "0" ]; then
	%service ggzd stop
	/sbin/chkconfig --del ggzd
fi

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/ggzd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ggzd/*.conf
%doc AUTHORS ChangeLog NEWS README TODO ggzd/ggzd.conf.example
%attr(755,root,root) %{_bindir}/ggzd*
%attr(755,root,root) %{_libdir}/ggzd
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/lib*.so.6
%attr(754,root,root) /etc/rc.d/init.d/ggzd
%{_datadir}/ggz
%{_mandir}/man6/*.6*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*
%{_mandir}/man3/*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
