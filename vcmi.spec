Name:           vcmi
Summary:        Heroes of Might and Magic 3 game engine
URL:            https://vcmi.eu/

%global fuzzylite_commit  9751a751a17c0682ed5d02e583c6a0cda8bc88e5
%global fuzzylite_scommit %(c=%{fuzzylite_commit}; echo ${c:0:7})
%global fuzzylite_version 6.0


Version:        1.5.3
Release:	%autorelease

# vcmi is GPLv2+, fyzzylight is GPLv3
License:        GPL-2.0-or-later AND GPL-3.0-only

Source0:        https://github.com/vcmi/vcmi/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/fuzzylite/fuzzylite/archive/%{fuzzylite_commit}/fuzzylite-%{fuzzylite_scommit}.tar.gz

# The Koji builder gets killed here, but I don't expect people to use this there
ExcludeArch:    ppc64le

BuildRequires:  %{_bindir}/desktop-file-validate
BuildRequires:  SDL2-devel
BuildRequires:  SDL2_image-devel
BuildRequires:  SDL2_mixer-devel
BuildRequires:  SDL2_ttf-devel
BuildRequires:  boost-devel >= 1.51
BuildRequires:  cmake
BuildRequires:  gcc-c++ >= 4.7.2
BuildRequires:  libappstream-glib
BuildRequires:  luajit-devel
BuildRequires:  minizip-devel
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel
BuildRequires:  tbb-devel
BuildRequires:  zlib-devel

Requires:       hicolor-icon-theme
Requires:       %{name}-data = %{version}-%{release}
Provides:       bundled(fuzzylight) = %{fuzzylite_version}

%description
The purpose of VCMI project is to rewrite entire Heroes 3.5: WoG engine from
scratch, giving it new and extended possibilities. It will help to support
mods and new towns already made by fans but abandoned because of game code
limitations.

In its current state it already supports maps of any sizes, higher
resolutions and extended engine limits.


%package data
Summary:        Data files for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description data
Data files for the VCMI project, a %{summary}.


%prep
%autosetup -p1
# fuzzyight from Source1:
tar -xf %{SOURCE1} -C AI/FuzzyLite --strip-components=1

%build
# low effort fix of some cmake brokenness
export CXXFLAGS="%{build_cxxflags} -I/usr/include/ffmpeg"

%cmake -Wno-dev \
  -DENABLE_TEST=FALSE \
  -DENABLE_INNOEXTRACT=FALSE \
  -DENABLE_GOLDMASTER=ON \
  -UCMAKE_INSTALL_LIBDIR \
  -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON \
  -DCMAKE_INSTALL_RPATH=%{_libdir}/%{name}

%ifnarch %{ix86} x86_64 aarch64
# not enough memory in Koji for parallel build
%global _smp_mflags -j1
%endif
%cmake_build


%install
%cmake_install


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/eu.vcmi.VCMI.metainfo.xml


%files
%doc docs/Readme.md ChangeLog.md
%license license.txt AI/FuzzyLite/LICENSE.FuzzyLite
%{_bindir}/vcmibuilder
%{_bindir}/vcmiclient
%{_bindir}/vcmieditor
%{_bindir}/vcmilauncher
%{_bindir}/vcmiserver
%{_libdir}/%{name}/
# keep this in the main package, because GNOME Software etc.
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/vcmiclient.svg
%{_datadir}/icons/hicolor/*/apps/vcmiclient.png
%{_datadir}/icons/hicolor/*/apps/vcmieditor.png
%{_metainfodir}/eu.vcmi.VCMI.metainfo.xml


%files data
%{_datadir}/%{name}/


%changelog
%autochangelog
