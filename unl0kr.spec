%define dracutlibdir %{_prefix}/lib/dracut

Name:           unl0kr
Version:        {{{ git_dir_version }}}
Release:        1%{?dist}
Summary:        Framebuffer-based disk unlocker for the initramfs based on LVGL 
License:        GPLv3
URL:            https://gitlab.com/cherrypicker/unl0kr

BuildRequires:  git
BuildRequires:  systemd-rpm-macros
BuildRequires:  gcc
BuildRequires:  meson >= 0.54.0
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(inih)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(scdoc)

Source1:        unl0kr-dracut-module-setup.sh
Source2:        unl0kr-ask-password.sh
Source3:        unl0kr-ask-password.path
Source4:        unl0kr-ask-password.service

# Disable debug packages
%define debug_package %{nil}

%description
Unl0kr is an osk-sdl clone written in LVGL and rendering directly to the Linux framebuffer. As a result, it doesn't depend on GPU hardware acceleration.

%package dracut
Summary: Integration of unl0kr and Dracut
Requires: %{name} = %{version}-%{release}
Requires: dracut

%description dracut
Provides a Dracut module that will ask for password with an on-screen-keyboard

%prep
git clone https://gitlab.com/cherrypicker/unl0kr.git
cd unl0kr
git submodule update --init --recursive

%build
cd unl0kr
%meson
%meson_build

%install
cd unl0kr
%meson_install
mkdir -p %{buildroot}%{dracutlibdir}/modules.d/10unl0kr
install -p -m 0644 %{SOURCE1} %{buildroot}%{dracutlibdir}/modules.d/10unl0kr/module-setup.sh
install -p -m 0755 %{SOURCE2} %{buildroot}%{dracutlibdir}/modules.d/10unl0kr/unl0kr-ask-password.sh
mkdir -p %{buildroot}%{_unitdir}/sysinit.target.wants
install -p -m 0755 %{SOURCE3} %{buildroot}%{_unitdir}/unl0kr-ask-password.path
install -p -m 0755 %{SOURCE4} %{buildroot}%{_unitdir}/unl0kr-ask-password.service
ln -s ../unl0kr-ask-password.path %{buildroot}%{_unitdir}/sysinit.target.wants/

# This lists all the files that are included in the rpm package and that
# are going to be installed into target system where the rpm is installed.
%files
%license unl0kr/COPYING
%{_bindir}/%{name}
%{_sysconfdir}/%{name}.conf
%{_mandir}/man*/%{name}.*

%files dracut
%{dracutlibdir}/modules.d/10unl0kr
%{_unitdir}/unl0kr-ask-password.path
%{_unitdir}/unl0kr-ask-password.service
%{_unitdir}/sysinit.target.wants/unl0kr-ask-password.path

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
{{{ git_dir_changelog }}}
