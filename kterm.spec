%define	name	kterm
%define	version	6.2.0
%define	release	%mkrel 30

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
BuildRequires:	libxp-devel
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
install -m 755 -d $RPM_BUILD_ROOT%{_datadir}/applications

cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=KTerm
Comment=Kanji Terminal Emulator
Exec=%{_bindir}/%{name}
Icon=terminals_section
Terminal=false
Type=Application
Categories=TerminalEmulator;Systenalm;Utility;
EOF

# install japanese man page
cat kterm.jman | iconv -f iso-2022-jp -t euc-jp > kterm.man.euc
install -m644 kterm.man.euc -D $RPM_BUILD_ROOT%{_mandir}/ja/man1/kterm.1

#(peroyvind) remove unpackaged files
rm -f $RPM_BUILD_ROOT/usr/lib/X11/app-defaults

%post
%if %mdkversion < 200900
%{update_menus}
%endif
update-alternatives --install %{_prefix}/X11R6/bin/xvt xvt %{_prefix}/X11R6/bin/kterm 15

%postun
%if %mdkversion < 200900
%{clean_menus}
%endif
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
%{_datadir}/applications/mandriva-%{name}.desktop



%changelog
* Thu Sep 10 2009 Thierry Vignaud <tvignaud@mandriva.com> 6.2.0-30mdv2010.0
+ Revision: 436441
- BR libxp-devel
- rebuild
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Tue Jan 08 2008 Thierry Vignaud <tvignaud@mandriva.com> 6.2.0-27mdv2008.1
+ Revision: 146657
- fix removing unpackaged files on x86_64
- better cat
- drop not hardcode icon extension
- drop old menu
- kill re-definition of %%buildroot on Pixel's request
- kill icon tag (unused and breaks build with iurt)
- import kterm

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Mon Sep 18 2006 Gwenole Beauchesne <gbeauchesne@mandriva.com> 6.2.0-27mdv2007.0
- Rebuild

* Sun Aug 13 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 6.2.0-26
- rebuild for fixed libxaw soname
- binary and manfile moved out of X11R6 dir
- xdg menu
- html file not generated (?)

* Sun Jul 02 2006 Stefan van der Eijk <stefan@mandriva.org> 6.2.0-25
- BuildRequires
- %%mkrel

* Sun Apr 30 2006 Stefan van der Eijk <stefan@eijk.nu> 6.2.0-24mdk
- rebuild for sparc

* Tue Aug 23 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 6.2.0-23mdk
- varargs fixes

* Sat Dec 25 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 6.2.0-22mdk
- fix buildrequires
- fix summary-ended-with-dot
- fix non-conffile-in-etc

* Tue Jun 08 2004 Per �yvind Karlsen <peroyvind@linux-mandrake.com> 6.2.0-21mdk
- fix gcc-3.4 build (P5)

* Tue Jan 27 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 6.2.0-20mdk
- fix unpackaged files
- cosmetics
- generate menu item during install
- rm -rf $RPM_BUILD_ROOT at the beginning of %%install, not %%prep
- drop P3 which was not applied
- add url

* Wed Oct  8 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 6.2.0-19mdk
- lib64 fixes

* Thu Feb 27 2003 David BAUDENS <baudens@mandrakesoft.com> 6.2.0-18mdk
- Add icon

* Thu Jan 09 2003 Pablo Saratxaga <pablo@mandrakesoft.com> 6.2.0-17mdk
- fixed encoding of man page, use iconv to do the conversion
- added mandrake menu
- uudecoded the sample file

* Sun Oct 28 2001 Stefan van der Eijk <stefan@eijk.nu> 6.2.0-16mdk
- BuildRequires revisited
- Copyright --> License
- Remove use of RPM SOURCE DIR (rpmlint)

* Fri Feb  9 2001 Etienne Faure  <etienne@mandrakesoft.com> 6.2.0-15mdk
- add as alternative xvt weight:15

* Mon Sep 25 2000 Stefan van der Eijk <s.vandereijk@chello.nl> 6.2.0-14mdk
- BM + macro's

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 6.2.0-13mdk
- automatically added BuildRequires

* Thu Apr 20 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 6.2.0-12mdk
- fixed group

* Fri Jan  7 2000 Pixel <pixel@mandrakesoft.com>
- add requires locales.ja

* Sat Oct 30 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- added patch to handle Hanzi-in code \e$(E as \e$A (I don't know much
  about this, but playing whith jis2gb and gb2jis I saw only difference on
  one kanji on the texts I have; so it is worth to add it as displayable,
  even if not 100%% correct)
- added a little patch to KTerm.ad ressources file so the full font list
  is included, so multilingual support is ready out of the box.
  (do "cat DEMO.kt.uu | uudecode" on kterm to see it; of course you need
  the proper fonts installed)
- corrected the type of ressources and wmconfig files (they must be %%config !)
- install the japanese man page

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions
- handle RPM_OPT_FLAGS

* Fri Mar 26 1999 Erik Troan <ewt@redhat.com>
- added unix98 pty support

* Wed Mar 24 1999 Erik Troan <ewt@redhat.com>
- added utemper support
- turn off setuid bit

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Thu Jan  7 1999 Bill Nottingham <notting@redhat.com>
- built for glibc2.1
- this package doesn't change much, does it?

* Fri May 01 1998 Prospector System <bugs@redhat.com>

- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- fixed build problems for manhattan

* Tue Oct 21 1997 Otto Hammersmith <otto@redhat.com>
- updated source
- added wmconfig entries
- fixed source url

* Tue Oct 07 1997 Erik Troan <ewt@redhat.com>
- needed patch for glibc on the alpha as TIOCSLTC is defined for OSF 
  compatibility

* Thu Jul 31 1997 Erik Troan <ewt@redhat.com>
- built against glibc


