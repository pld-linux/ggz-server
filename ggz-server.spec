Summary:	Main GGZ server
Summary(pl.UTF-8):	Główny serwer GGZ
Name:		ggz-server
Version:	0.0.14.1
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	http://ftp.belnet.be/packages/ggzgamingzone/ggz/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	254caaf8fe7b4a2bafcb62576abba72c
Source1:	%{name}.init
Source2:	%{name}.conf
Source3:	%{name}.logrotate
Patch0:		%{name}-db4.patch
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
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_localstatedir	/var/lib

%description
This package contains the main GGZ server, some administrative
utilities and lots of game servers.

%description -l pl.UTF-8
Ta paczka zawiera główny serwer GGZ, kilka narzędzi administracyjnych
oraz dużo serwerów gier.

%package libs
Summary:	ggz-server libraries
Summary(pl.UTF-8):	Biblioteki ggz-server
Group:		Libraries

%description libs
ggz-server libraries.

%description libs -l pl.UTF-8
Biblioteki ggz-server.

%package devel
Summary:	Header files for ggz-server library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ggz-server
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
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
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4 -I m4/ggz
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-database=db4 \
	--with-zeroconf=avahi \
	--with-reconfiguration=inotify

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,ggzd,logrotate.d},%{_var}/{lib/ggzd,log}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ggzd
sed -e 's,@LIBDIR@,%{_libdir},' %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/ggzd/ggzd.conf
install %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

:> $RPM_BUILD_ROOT%{_var}/log/ggz-server.log

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ggzd
%service ggzd restart

%preun
if [ "$1" = "0" ]; then
	%service ggzd stop
	/sbin/chkconfig --del ggzd
fi

%post libs -p /sbin/ldconfig

%postun	
libs -p /sbin/ldconfig
rm -rf /var/libs/ggzd

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO ggzd/ggzd.conf.example
%attr(755,root,root) %{_bindir}/ggzd
%attr(755,root,root) %{_bindir}/ggzduedit
%dir %{_libdir}/ggzd
%attr(755,root,root) %{_libdir}/ggzd/geekgameserver
%attr(755,root,root) %{_libdir}/ggzd/ggzd.ccheckers
%attr(755,root,root) %{_libdir}/ggzd/ggzd.chess
%attr(755,root,root) %{_libdir}/ggzd/ggzd.combat
%attr(755,root,root) %{_libdir}/ggzd/ggzd.connectx
%attr(755,root,root) %{_libdir}/ggzd/ggzd.dots
%attr(755,root,root) %{_libdir}/ggzd/ggzd.escape
%attr(755,root,root) %{_libdir}/ggzd/ggzd.ggzcards
%attr(755,root,root) %{_libdir}/ggzd/ggzd.ggzcards.ai-random
%attr(755,root,root) %{_libdir}/ggzd/ggzd.ggzcards.ai-spades
%attr(755,root,root) %{_libdir}/ggzd/ggzd.ggzcards.ai-suaro
%attr(755,root,root) %{_libdir}/ggzd/ggzd.hastings
%attr(755,root,root) %{_libdir}/ggzd/ggzd.reversi
%attr(755,root,root) %{_libdir}/ggzd/ggzd.spades
%attr(755,root,root) %{_libdir}/ggzd/ggzd.tictactoe
%attr(755,root,root) %{_libdir}/ggzd/keepalivesrv
%attr(755,root,root) %{_libdir}/ggzd/krosswater_server
%attr(755,root,root) %{_libdir}/ggzd/muehleserv
%attr(755,root,root) %{_libdir}/ggzd/tuxmanserv
%attr(755,root,root) %{_libdir}/ggzd/widelands_server
%dir %{_sysconfdir}/ggzd
%dir %{_sysconfdir}/ggzd/games
%{_sysconfdir}/ggzd/games/ccheckers.dsc
%{_sysconfdir}/ggzd/games/chess.dsc
%{_sysconfdir}/ggzd/games/combat.dsc
%{_sysconfdir}/ggzd/games/connectx.dsc
%{_sysconfdir}/ggzd/games/dots.dsc
%{_sysconfdir}/ggzd/games/escape.dsc
%{_sysconfdir}/ggzd/games/geekgame.dsc
%{_sysconfdir}/ggzd/games/ggzcards-bridge.dsc
%{_sysconfdir}/ggzd/games/ggzcards-fortytwo.dsc
%{_sysconfdir}/ggzd/games/ggzcards-hearts.dsc
%{_sysconfdir}/ggzd/games/ggzcards-lapocha.dsc
%{_sysconfdir}/ggzd/games/ggzcards-spades.dsc
%{_sysconfdir}/ggzd/games/ggzcards-suaro.dsc
%{_sysconfdir}/ggzd/games/ggzcards-sueca.dsc
%{_sysconfdir}/ggzd/games/ggzcards-whist.dsc
%{_sysconfdir}/ggzd/games/ggzcards.dsc
%{_sysconfdir}/ggzd/games/hastings.dsc
%{_sysconfdir}/ggzd/games/keepalive.dsc
%{_sysconfdir}/ggzd/games/krosswater.dsc
%{_sysconfdir}/ggzd/games/muehle.dsc
%{_sysconfdir}/ggzd/games/reversi.dsc
%{_sysconfdir}/ggzd/games/spades.dsc
%{_sysconfdir}/ggzd/games/tictactoe.dsc
%{_sysconfdir}/ggzd/games/tuxman.dsc
%{_sysconfdir}/ggzd/games/widelands.dsc
%dir %{_sysconfdir}/ggzd/rooms
%{_sysconfdir}/ggzd/rooms/ccheckers.room
%{_sysconfdir}/ggzd/rooms/chess.room
%{_sysconfdir}/ggzd/rooms/combat.room
%{_sysconfdir}/ggzd/rooms/connectx.room
%{_sysconfdir}/ggzd/rooms/dots.room
%{_sysconfdir}/ggzd/rooms/entry.room
%{_sysconfdir}/ggzd/rooms/escape.room
%{_sysconfdir}/ggzd/rooms/geekgame.room
%{_sysconfdir}/ggzd/rooms/ggzcards-bridge.room
%{_sysconfdir}/ggzd/rooms/ggzcards-fortytwo.room
%{_sysconfdir}/ggzd/rooms/ggzcards-hearts.room
%{_sysconfdir}/ggzd/rooms/ggzcards-lapocha.room
%{_sysconfdir}/ggzd/rooms/ggzcards-spades.room
%{_sysconfdir}/ggzd/rooms/ggzcards-suaro.room
%{_sysconfdir}/ggzd/rooms/ggzcards-sueca.room
%{_sysconfdir}/ggzd/rooms/ggzcards-whist.room
%{_sysconfdir}/ggzd/rooms/ggzcards.room
%{_sysconfdir}/ggzd/rooms/hastings.room
%{_sysconfdir}/ggzd/rooms/keepalive.room
%{_sysconfdir}/ggzd/rooms/krosswater.room
%{_sysconfdir}/ggzd/rooms/muehle.room
%{_sysconfdir}/ggzd/rooms/reversi.room
%{_sysconfdir}/ggzd/rooms/spades.room
%{_sysconfdir}/ggzd/rooms/tictactoe.room
%{_sysconfdir}/ggzd/rooms/tuxman.room
%{_sysconfdir}/ggzd/rooms/widelands.room
%attr(640,root,games) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ggzd/ggzd.conf
%{_sysconfdir}/ggzd/ggzd.motd
%attr(754,root,root) /etc/rc.d/init.d/ggzd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/ggz-server
%dir %{_datadir}/ggz/ggzd
%{_datadir}/ggz/ggzd/ggzcards
%{_datadir}/ggz/ggzd/hastings1066
%{_datadir}/ggz/ggzd/muehle
%{_datadir}/ggz/ggzd/tuxmanserv
%{_mandir}/man6/ggzd.6*
%{_mandir}/man6/ggzduedit.6*
%attr(770,root,games) %{_localstatedir}/ggzd
%attr(660,root,games) %config(noreplace) %verify(not md5 mtime size) %{_var}/log/ggz-server.log

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libggzdmod++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libggzdmod++.so.1
%attr(755,root,root) %{_libdir}/libggzdmod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libggzdmod.so.6

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libggzdmod++.so
%attr(755,root,root) %{_libdir}/libggzdmod.so
%{_libdir}/libggzdmod++.la
%{_libdir}/libggzdmod.la
%{_libdir}/libggzdmod++.la
%{_libdir}/libggzdmod.la
%{_includedir}/ggzdmod++
%{_includedir}/ggzdmod.h
%{_mandir}/man3/ggzdmod.h.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libggzdmod++.a
%{_libdir}/libggzdmod.a
