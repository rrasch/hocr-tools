%{!?git_tag:%{error:git_tag macro must be defined}}
%{!?git_commit:%{error:git_commit macro must be defined}}

%global name hocr-tools
%global version %(echo %{git_tag} | sed 's/^v//')
%global release 1.dlts.git%{git_commit}%{?dist}
%global git_url https://github.com/rrasch/%{name}
%global _buildsubdir %{name}-%{version}
%global dev_branch rtl

Name:           %{name}
Version:        %{version}
Release:        %{release}
Summary:        Tools for working with hOCR data
License:        ASL 2.0
#URL:           https://github.com/tmbdev/%%{name}
#URL:           https://github.com/ocropus/%%{name}
URL:            %{git_url}
#Source0:       https://github.com/tmbdev/hocr-tools/archive/v%%{version}.tar.gz#/%%{name}-%%{version}.tar.gz
#Patch0:        hocr-pdf.patch
BuildArch:      noarch
BuildRequires:  pdfgrep
BuildRequires:  python3-devel
BuildRequires:  python3-reportlab
BuildRequires:  python3-lxml
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  msttcore-fonts-installer
BuildRequires:  wget
Requires:       msttcore-fonts-installer
Requires:       python3-reportlab
Requires:       python3-imaging

%description
A collection of Python tools for working with hOCR data.

%prep
#%%autosetup -n %{name}-%{version}
rm -rf %{_buildsubdir}
git clone %{git_url} %{_buildsubdir}
cd %{_buildsubdir}

%if "%{git_tag}" == "v0.0.0"
git switch %{dev_branch}
%else
git -c advice.detachedHead=false checkout %{git_tag}
%endif

%build
cd %{_buildsubdir}
%py3_build

%install
rm -rf %{buildroot}
cd %{_buildsubdir}
%py3_install

%check
cd %{_buildsubdir}
export PATH=%{buildroot}%{_bindir}:$PATH
test/tsht

%clean
rm -rf %{buildroot}

%files
%doc %{_buildsubdir}/LICENSE
%doc %{_buildsubdir}/README.md
%{python3_sitelib}/*
%{_bindir}/hocr-check
%{_bindir}/hocr-combine
%{_bindir}/hocr-cut
%{_bindir}/hocr-eval
%{_bindir}/hocr-eval-geom
%{_bindir}/hocr-eval-lines
%{_bindir}/hocr-extract-g1000
%{_bindir}/hocr-extract-images
%{_bindir}/hocr-lines
%{_bindir}/hocr-merge-dc
%{_bindir}/hocr-pdf
%{_bindir}/hocr-split
%{_bindir}/hocr-wordfreq


%changelog
* Thu Feb 12 2026 Rasan Rasch - 1.4.0-1
- Update to 1.4.0

* Sun Aug 16 2020 Rasan Rasch - 1.3.0-3
- Add --reverse option to hocr-pdf

* Tue May 12 2020 Rasan Rasch - 1.3.0-2
- Build for centos 6

* Fri Mar 22 2019 Brandon Nielsen <nielsenb@jetfuse.net> 1.3.0-1
- Update to 1.3.0

* Wed Oct 10 2018 Brandon Nielsen <nielsenb@jetfuse.net> 1.2.0-2
- Cleanup version tag

* Mon Oct 02 2017 Brandon Nielsen <nielsenb@jetfuse.net> 1.2.0-1
- Initial specfile
