Name:           ryzenadj-ryzen_smu-ai300-krackan-PP
Version:        0.18.0
Release:        1%{?dist}
Summary:        AMD Ryzen AI 300 (Krackan Point) power management suite
License:        LGPL-3.0 AND GPL-2.0
URL:            https://github.com/labonsky/ryzenadj_AI300
Source0:        https://github.com/labonsky/ryzenadj_AI300/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake >= 3.9
BuildRequires:  gcc
BuildRequires:  pciutils-devel
BuildRequires:  kernel-devel
BuildRequires:  dkms

Requires:       dkms
Requires:       tuned
Requires:       python3

%description
Complete power management suite for AMD Ryzen AI 300 series (Krackan Point)
processors including Ryzen AI 5 340 and AI 7 350.

Components:
- ryzenadj: Command-line power adjustment tool (v0.18.0)
- ryzen_smu: Kernel module for SMU communication (v0.1.7, DKMS)
- Power Profiles: tuned integration with auto-switching

Power Profiles:
- ryzenadj-battery: 5W sustained, 10W burst, 60Hz screen
- ryzenadj-ac: 53W full power, 120Hz screen
- Auto-switching via udev rules
- KDE Power Profiles GUI integration

%prep
%setup -q -n ryzenadj_AI300-%{version}

%build
mkdir -p build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make %{?_smp_mflags}

%install
# ryzenadj binary and library
install -D -m 755 build/ryzenadj %{buildroot}%{_bindir}/ryzenadj
install -D -m 755 build/libryzenadj.so %{buildroot}%{_libdir}/libryzenadj.so

# ryzen_smu DKMS source
install -d %{buildroot}%{_usrsrc}/ryzen_smu-0.1.7
cp -a ryzen_smu/Makefile %{buildroot}%{_usrsrc}/ryzen_smu-0.1.7/
cp -a ryzen_smu/dkms.conf %{buildroot}%{_usrsrc}/ryzen_smu-0.1.7/
cp -a ryzen_smu/*.c %{buildroot}%{_usrsrc}/ryzen_smu-0.1.7/
cp -a ryzen_smu/*.h %{buildroot}%{_usrsrc}/ryzen_smu-0.1.7/

# tuned profiles
install -d %{buildroot}%{_sysconfdir}/tuned/profiles/ryzenadj-battery
install -d %{buildroot}%{_sysconfdir}/tuned/profiles/ryzenadj-balanced
install -d %{buildroot}%{_sysconfdir}/tuned/profiles/ryzenadj-ac
cp -a tuned-profiles/ryzenadj-battery/* %{buildroot}%{_sysconfdir}/tuned/profiles/ryzenadj-battery/
cp -a tuned-profiles/ryzenadj-balanced/* %{buildroot}%{_sysconfdir}/tuned/profiles/ryzenadj-balanced/
cp -a tuned-profiles/ryzenadj-ac/* %{buildroot}%{_sysconfdir}/tuned/profiles/ryzenadj-ac/
install -D -m 644 tuned-profiles/ppd.conf %{buildroot}%{_sysconfdir}/tuned/ppd.conf

# udev rules
install -D -m 644 tuned-profiles/99-ryzenadj-power.rules %{buildroot}%{_udevrulesdir}/99-ryzenadj-power.rules

# boot check service
install -D -m 755 tuned-profiles/ryzenadj-boot-check.sh %{buildroot}%{_bindir}/ryzenadj-boot-check.sh
install -D -m 644 tuned-profiles/ryzenadj-boot-check.service %{buildroot}%{_unitdir}/ryzenadj-boot-check.service

# power feeder service
install -D -m 755 power_feeder.py %{buildroot}%{_libexecdir}/ryzenadj/power_feeder.py
install -D -m 755 show_watts.sh %{buildroot}%{_libexecdir}/ryzenadj/show_watts.sh
install -D -m 755 show_laptop_watts.sh %{buildroot}%{_libexecdir}/ryzenadj/show_laptop_watts.sh

%post
# Register DKMS module
dkms add -m ryzen_smu -v 0.1.7 --rpm_safe_upgrade || :
dkms build -m ryzen_smu -v 0.1.7 || :
dkms install -m ryzen_smu -v 0.1.7 --force || :

# Load module
modprobe ryzen_smu || :

# Reload services
udevadm control --reload-rules || :
systemctl daemon-reload || :
systemctl enable ryzenadj-boot-check.service || :
systemctl restart tuned || :
systemctl restart tuned-ppd 2>/dev/null || :

%preun
if [ $1 -eq 0 ]; then
    # Uninstall
    systemctl disable ryzenadj-boot-check.service || :
    modprobe -r ryzen_smu || :
    dkms remove -m ryzen_smu -v 0.1.7 --all --rpm_safe_upgrade || :
fi

%files
%license LICENSE
%doc README.md KRACKAN_POINT_SUPPORT.md WIDGET_SETUP.md

# ryzenadj
%{_bindir}/ryzenadj
%{_libdir}/libryzenadj.so

# ryzen_smu DKMS
%{_usrsrc}/ryzen_smu-0.1.7/

# tuned profiles
%config(noreplace) %{_sysconfdir}/tuned/profiles/ryzenadj-battery/
%config(noreplace) %{_sysconfdir}/tuned/profiles/ryzenadj-balanced/
%config(noreplace) %{_sysconfdir}/tuned/profiles/ryzenadj-ac/
%config(noreplace) %{_sysconfdir}/tuned/ppd.conf
%{_udevrulesdir}/99-ryzenadj-power.rules

# services
%{_bindir}/ryzenadj-boot-check.sh
%{_unitdir}/ryzenadj-boot-check.service

# widget helpers
%dir %{_libexecdir}/ryzenadj
%{_libexecdir}/ryzenadj/power_feeder.py
%{_libexecdir}/ryzenadj/show_watts.sh
%{_libexecdir}/ryzenadj/show_laptop_watts.sh

%changelog
* Sat Dec 13 2025 labonsky - 0.18.0-1
- Initial unified package for Krackan Point
- ryzenadj 0.18.0 with PM table fix for 0x650005
- ryzen_smu 0.1.7 with Krackan Point detection
- tuned profiles with auto-switching and KDE integration
- Boot-time power profile detection
