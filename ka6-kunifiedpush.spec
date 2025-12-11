#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.12.0
%define		kframever	6.13.0
%define		qtver		6.8
%define		kaname		kunifiedpush
Summary:	Unified push
Name:		ka6-%{kaname}
Version:	25.12.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	2d0f6fd66996038d94b7ce9b5ee1c533
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6WebSockets-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcmutils-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kservice-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kunified push - client library and distributor daemon.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	ka5-%{kaname}-devel < %{version}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc README.md
%dir /etc/xdg/KDE
/etc/xdg/KDE/kunifiedpush-distributor.conf
/etc/xdg/autostart/org.kde.kunifiedpush-distributor.desktop
%attr(755,root,root) %{_bindir}/kunifiedpush-distributor
%ghost %{_libdir}/libKUnifiedPush.so.1
%{_libdir}/libKUnifiedPush.so.*.*
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_push_notifications.so
%{_desktopdir}/kcm_push_notifications.desktop
%{_datadir}/qlogging-categories6/org_kde_kunifiedpush.categories
%dir %{systemduserunitdir}/graphical-session.target.wants
%{systemduserunitdir}/graphical-session.target.wants/kunifiedpush-distributor.service
%{systemduserunitdir}/kunifiedpush-distributor.service

%files devel
%defattr(644,root,root,755)
%{_includedir}/KUnifiedPush
%{_libdir}/cmake/KUnifiedPush
%{_libdir}/libKUnifiedPush.so
