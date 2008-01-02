%define	name	kterm
%define	version	6.2.0
%define	release	%mkrel 27

Summary:	A Kanji (Japanese character set) terminal emulator for X
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source:		ftp://ftp.sunet.se/pub/X11/R6contrib/applications/%{name}-%{version}.tar.bz2
Patch0:		kterm-6.2.0-kbd.patch.bz2
Patch1:		kterm-6.2.0-glibc.patch.bz2
Patch2:		kterm-6.2.0-utmp98.patch.bz2
#Patch3:	kterm-6.2.0-hanzi.patch.bz2
Patch4:		kterm-6.2.0-allfonts.patch.bz2
Patch5:		kterm-6.2.0-gcc3.4-fix.patch.bz2
Patch6:		kterm-6.2.0-varargs.patch.bz2
License:	GPL
Url:		http://www.asahi-net.or.jp/~hc3j-tkg/kterm/
Group:		Terminals
BuildRequires:	imake
BuildRequires:	libxaw-devel
BuildRequires:	ncurses-devel
BuildRequires:	rman
BuildRequires:	sharutils
BuildRequires:	utempter-devel
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	utempter locales-ja

%description
The kterm package provides a terminal emulator for the Kanji Japanese
character set.

Install kterm if you need a Kanji character set terminal emulator.
You'll also need to have the X Window System installed.

%prep
%setup -q
%patch0 -p1 -b .kbd
%patch1 -p1 -b .glibc
%patch2 -p1 -b .utempter
#%patch3 -p1 -b .hanzi
%patch4 -p1 -b .allfonts
%patch5 -p1 -b .gcc34
%patch6 -p1 -b .varargs
uudecode DEMO.kt.uu

%build
xmkmf
%make CDEBUGFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall_std} install.man MANPATH=/usr/share/man
chmod 755 $RPM_BUILD_ROOT%{_bindir}/kterm

# install menu
install -d $RPM_BUILD_ROOT%{_menudir}
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/applications

cat <<EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):command="%{name}" \
                icon="terminals_section.png" \
                needs="x11" \
                section="Terminals" \
                title="KTerm"\
                longtitle="Kanji Terminal Emulator" \
                xdg="true"
EOF

cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=KTerm
Comment=Kanji Terminal Emulator
Exec=%{_bindir}/%{name}
Icon=terminals_section.png
Terminal=false
Type=Application
Categories=X-MandrivaLinux-System-Terminals;TerminalEmulator;
EOF

# install japanese man page
cat kterm.jman | iconv -f iso-2022-jp -t euc-jp > kterm.man.euc
install -m644 kterm.man.euc -D $RPM_BUILD_ROOT%{_mandir}/ja/man1/kterm.1

#(peroyvind) remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/X11/app-defaults

%post
%{update_menus}
update-alternatives --install %{_prefix}/X11R6/bin/xvt xvt %{_prefix}/X11R6/bin/kterm 15

%postun
%{clean_menus}
if [ "$1" = "0" ]; then
    update-alternatives --remove xvt %{_prefix}/X11R6/bin/kterm
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc DEMO.kt README*
%{_bindir}/kterm
%config(noreplace) %{_sysconfdir}/X11/app-defaults/KTerm
%{_mandir}/man1/kterm.1x*
#{_prefix}/X11R6/lib/X11/doc/html/kterm.1.html
%lang(ja) %{_mandir}/ja/man1/kterm.1*
%{_menudir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop

