# -*- rpm-spec -*-

%if "%{fedora}" >= "8"
%define with_polkit 1
%define with_proxy no
%else
%define with_polkit 0
%define with_proxy yes
%endif

%if "%{fedora}"
%ifarch ppc64
%define with_qemu 0
%else
%define with_qemu 1
%endif
%else
%define with_qemu 0
%endif

Summary: Library providing a simple API virtualization
Name: libvirt
Version: 0.4.4
Release: 2%{?dist}%{?extra_release}
License: LGPL
Group: Development/Libraries
Source: libvirt-%{version}.tar.gz
Patch1: %{name}-%{version}-boot-cdrom.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
URL: http://libvirt.org/
BuildRequires: python python-devel
Requires: libxml2
Requires: readline
Requires: ncurses
Requires: dnsmasq
Requires: bridge-utils
Requires: iptables
# So remote clients can access libvirt over SSH tunnel
# (client invokes 'nc' against the UNIX socket on the server)
Requires: nc
Requires: cyrus-sasl
# Not technically required, but makes 'out-of-box' config
# work correctly & doesn't have onerous dependencies
Requires: cyrus-sasl-md5
%if %{with_polkit}
Requires: PolicyKit >= 0.6
%endif
# For mount/umount in FS driver
BuildRequires: util-linux
# PPC64 has no Xen nor QEmu, try to build anyway
%ifnarch ppc64
%if %{with_qemu}
# From QEMU RPMs
Requires: /usr/bin/qemu-img
%else
# From Xen RPMs
Requires: /usr/sbin/qcow-create
%endif
%endif
# For LVM drivers
Requires: lvm2
# For ISCSI driver
Requires: iscsi-initiator-utils
# For disk driver
Requires: parted
%ifarch i386 x86_64 ia64
BuildRequires: xen-devel
%endif
BuildRequires: libxml2-devel
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: gettext
BuildRequires: gnutls-devel
BuildRequires: avahi-devel
BuildRequires: libselinux-devel
BuildRequires: dnsmasq
BuildRequires: bridge-utils
%if %{with_qemu}
BuildRequires: qemu
%endif
BuildRequires: cyrus-sasl-devel
%if %{with_polkit}
BuildRequires: PolicyKit-devel >= 0.6
%endif
# For mount/umount in FS driver
BuildRequires: util-linux
# PPC64 has no Xen nor QEmu, try to build anyway
%ifnarch ppc64
%if %{with_qemu}
# From QEMU RPMs
BuildRequires: /usr/bin/qemu-img
%else
# From Xen RPMs
BuildRequires: /usr/sbin/qcow-create
%endif
%endif
# For LVM drivers
BuildRequires: lvm2
# For ISCSI driver
BuildRequires: iscsi-initiator-utils
# For disk driver
BuildRequires: parted-devel
Obsoletes: libvir

# Fedora build root suckage
BuildRequires: gawk

%description
Libvirt is a C toolkit to interact with the virtualization capabilities
of recent versions of Linux (and other OSes).

%package devel
Summary: Libraries, includes, etc. to compile with the libvirt library
Group: Development/Libraries
Requires: libvirt = %{version}
Requires: pkgconfig
%ifarch i386 x86_64 ia64
Requires: xen-devel
%endif
Obsoletes: libvir-devel

%description devel
Includes and documentations for the C library providing an API to use
the virtualization capabilities of recent versions of Linux (and other OSes).

%package python
Summary: Python bindings for the libvirt library
Group: Development/Libraries
Requires: libvirt = %{version}
Obsoletes: libvir-python

%description python
The libvirt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).

%prep
%setup -q
%patch1 -p1

%build
# Xen is available only on i386 x86_64 ia64
%ifarch i386 i686 x86_64 ia64
%configure --with-init-script=redhat \
           --with-qemud-pid-file=%{_localstatedir}/run/libvirt_qemud.pid \
           --with-remote-file=%{_localstatedir}/run/libvirtd.pid \
           --with-xen-proxy=%{with_proxy}
%else
%ifnarch ppc64
%configure --without-xen \
           --with-init-script=redhat \
           --with-qemud-pid-file=%{_localstatedir}/run/libvirt_qemud.pid \
           --with-remote-file=%{_localstatedir}/run/libvirtd.pid
%else
%configure --without-xen \
           --without-qemu \
           --with-init-script=redhat \
           --with-qemud-pid-file=%{_localstatedir}/run/libvirt_qemud.pid \
           --with-remote-file=%{_localstatedir}/run/libvirtd.pid
%endif
%endif

make

%install
rm -fr %{buildroot}

%makeinstall
(cd docs/examples ; make clean ; rm -rf .deps Makefile Makefile.in)
(cd docs/examples/python ; rm -f Makefile Makefile.in)
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/python*/site-packages/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/python*/site-packages/*.a
install -d -m 0755 $RPM_BUILD_ROOT%{_localstatedir}/run/libvirt/
# Default dir for disk images defined in SELinux policy
install -d -m 0755 $RPM_BUILD_ROOT%{_localstatedir}/lib/libvirt/images/

# We don't want to install /etc/libvirt/qemu/networks in the main %files list
# because if the admin wants to delete the default network completely, we don't
# want to end up re-incarnating it on every RPM upgrade.
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/libvirt/networks/
cp $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/default.xml \
   $RPM_BUILD_ROOT%{_datadir}/libvirt/networks/default.xml
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/default.xml
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
# Strip auto-generated UUID - we need it generated per-install
sed -i -e "/<uuid>/d" $RPM_BUILD_ROOT%{_datadir}/libvirt/networks/default.xml
%find_lang %{name}

%clean
rm -fr %{buildroot}

%post
/sbin/ldconfig

# We want to install the default network for initial RPM installs
# or on the first upgrade from a non-network aware libvirt only.
# We check this by looking to see if the daemon is already installed
/sbin/chkconfig --list libvirtd 1>/dev/null 2>&1
if [ $? != 0 ]
then
    UUID=`/usr/bin/uuidgen`
    sed -e "s,</name>,</name>\n  <uuid>$UUID</uuid>," \
         < %{_datadir}/libvirt/networks/default.xml \
         > %{_sysconfdir}/libvirt/qemu/networks/default.xml
    ln -s ../default.xml %{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
fi

/sbin/chkconfig --add libvirtd

%preun
if [ $1 = 0 ]; then
    /sbin/service libvirtd stop 1>/dev/null 2>&1
    /sbin/chkconfig --del libvirtd
fi

%postun
/sbin/ldconfig

%files -f %{name}.lang
%defattr(-, root, root)

%doc AUTHORS ChangeLog NEWS README COPYING.LIB TODO
%doc %{_mandir}/man1/virsh.1*
%{_bindir}/virsh
%{_libdir}/lib*.so.*
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/networks/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/networks/autostart
%{_sysconfdir}/rc.d/init.d/libvirtd
%config(noreplace) %{_sysconfdir}/sysconfig/libvirtd
%config(noreplace) %{_sysconfdir}/libvirt/libvirtd.conf
%config(noreplace) %{_sysconfdir}/libvirt/qemu.conf
%config(noreplace) %{_sysconfdir}/sasl2/libvirt.conf
%dir %{_datadir}/libvirt/
%dir %{_datadir}/libvirt/networks/
%{_datadir}/libvirt/networks/default.xml
%dir %{_localstatedir}/run/libvirt/
%dir %{_localstatedir}/lib/libvirt/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/images/
%if %{with_polkit}
%{_datadir}/PolicyKit/policy/libvirtd.policy
%endif
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/qemu/
%if %{with_proxy} == "yes"
%attr(4755, root, root) %{_libexecdir}/libvirt_proxy
%endif
%attr(0755, root, root) %{_libexecdir}/libvirt_parthelper
%attr(0755, root, root) %{_sbindir}/libvirtd
%doc docs/*.rng
%doc docs/*.xml

%files devel
%defattr(-, root, root)

%{_libdir}/lib*.so
%dir %{_includedir}/libvirt
%{_includedir}/libvirt/*.h
%{_libdir}/pkgconfig/libvirt.pc
%doc %{_datadir}/gtk-doc/html/libvirt/*.devhelp
%doc %{_datadir}/gtk-doc/html/libvirt/*.html
%doc %{_datadir}/gtk-doc/html/libvirt/*.png
%doc %{_datadir}/gtk-doc/html/libvirt/*.css

%doc docs/*.html docs/html docs/*.gif
%doc docs/examples
%doc docs/libvirt-api.xml

%files python
%defattr(-, root, root)

%doc AUTHORS NEWS README COPYING.LIB
%{_libdir}/python*/site-packages/libvirt.py*
%{_libdir}/python*/site-packages/libvirtmod*
%doc python/tests/*.py
%doc python/TODO
%doc python/libvirtclass.txt
%doc docs/examples/python

%changelog
* Tue Jul  8 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.4-2.fc8
- Fix booting of CDROM images with KVM (rhbz #452355)

* Thu Jun 25 2008 Daniel Veillard <veillard@redhat.com> - 0.4.4-1.fc8
- upstream release 0.4.4
- fixes a couple of bugs in previous release

* Thu Jun 12 2008 Daniel Veillard <veillard@redhat.com> - 0.4.3-1.fc8
- upstream release 0.4.3
- many bug fixes
- many small improvements

* Tue Apr  8 2008 Daniel Veillard <veillard@redhat.com> 0.4.2-1.fc8
- upstream release 0.4.2
- many bug fixes
- localization updates

* Thu Apr  4 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.1-3.fc8
- Don't run polkit-auth as root
- Don't request polkit auth if client is root
- When dumping XML for a storage pool, make the <source> directory tag
  match the <dir> tag used for specifying the pool in the first place
- Do iscsiadm sendtarget before trying to do login
- Do sysfs scanning for iSCSI LUNs instead of trying to parse them from
  iscsiadm session output
- Fix QEMU tap device setup
- Fix Xen boot device XML processing
- Fixed QEMU cdrom media change

* Tue Mar 11 2008 Daniel Veillard <veillard@redhat.com> - 0.4.1-2.fc8
- Fixed daemon startup when run with --daemon flag

* Thu Mar  6 2008 Daniel Veillard <veillard@redhat.com> - 0.4.1-1.fc8
- Update to 0.4.1
- Storage APIs
- xenner support
- lots of assorted improvements, bugfixes and cleanups
- documentation and localization improvements

* Thu Jan 17 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.0-4.fc8
- Fix SSH tunnelling (rhbz #428743)

* Sun Jan 13 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.0-3.fc8
- Fix crash when no auth callback

* Wed Jan  2 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.0-2.fc8
- Fix reading large config files (rhbz #426425)
- Fix crash when connecting to a PolicyKit enabled server with not auth callback (rhbz #427107)

* Tue Dec 18 2007 Daniel Veillard <veillard@redhat.com> - 0.4.0-1.fc8
- Release of 0.4.0
- SASL based authentication
- PolicyKit authentication
- improved NUMA and statistics support
- lots of assorted improvements, bugfixes and cleanups
- documentation and localization improvements

* Mon Oct 15 2007 Daniel P. Berrange <berrange@redhat.com> - 0.3.3-2.fc8
- Added QEMU driver config file support
- Added example config files

* Sun Sep 30 2007 Daniel Veillard <veillard@redhat.com> - 0.3.3-1
- Release of 0.3.3
- Avahi support
- NUMA support
- lots of assorted improvements, bugfixes and cleanups
- documentation and localization improvements

* Fri Aug 24 2007 Daniel Veillard <veillard@redhat.com> - 0.3.2-2.fc8
- also build on arches where Xen is not available

* Tue Aug 21 2007 Daniel Veillard <veillard@redhat.com> - 0.3.2-1.fc8
- Release of 0.3.2
- API for domains migration
- APIs for collecting statistics on disks and interfaces
- lots of assorted bugfixes and cleanups
- documentation and localization improvements

* Thu Aug 16 2007 Daniel Veillard <veillard@redhat.com> - 0.3.1-4.fc8
- Fixes missing Requires for libvirt-devel

* Thu Jul 26 2007 Daniel Veillard <veillard@redhat.com> - 0.3.1-3.fc8
- adds fix for bug #249594

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 0.3.1-2
- Rebuild for RH #249435

* Tue Jul 24 2007 Daniel Veillard <veillard@redhat.com> - 0.3.1-1.fc8
- Release of 0.3.1
- localtime clock support
- PS/2 and USB input devices
- lots of assorted bugfixes and cleanups
- documentation and localization improvements

* Mon Jul  9 2007 Daniel Veillard <veillard@redhat.com> - 0.3.0-1.fc8
- Release of 0.3.0
- Secure remote access support
- unification of daemons
- lots of assorted bugfixes and cleanups
- documentation and localization improvements

* Fri Jun  8 2007 Daniel Veillard <veillard@redhat.com> - 0.2.3-1.fc8
- Release of 0.2.3
- lot of assorted bugfixes and cleanups
- support for Xen-3.1
- new scheduler API

* Tue Apr 17 2007 Daniel Veillard <veillard@redhat.com> - 0.2.2-1
- Release of 0.2.2
- lot of assorted bugfixes and cleanups
- preparing for Xen-3.0.5

* Thu Mar 22 2007 Jeremy Katz <katzj@redhat.com> - 0.2.1-2.fc7
- don't require xen; we don't need the daemon and can control non-xen now
- fix scriptlet error (need to own more directories)
- update description text

* Fri Mar 16 2007 Daniel Veillard <veillard@redhat.com> - 0.2.1-1
- Release of 0.2.1
- lot of bug and portability fixes
- Add support for network autostart and init scripts
- New API to detect the virtualization capabilities of a host
- Documentation updates

* Fri Feb 23 2007 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-4.fc7
- Fix loading of guest & network configs

* Fri Feb 16 2007 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-3.fc7
- Disable kqemu support since its not in Fedora qemu binary
- Fix for -vnc arg syntax change in 0.9.0  QEMU

* Thu Feb 15 2007 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-2.fc7
- Fixed path to qemu daemon for autostart
- Fixed generation of <features> block in XML
- Pre-create config directory at startup

* Wed Feb 14 2007 Daniel Veillard <veillard@redhat.com> 0.2.0-1.fc7
- support for KVM and QEmu
- support for network configuration
- assorted fixes

* Mon Jan 22 2007 Daniel Veillard <veillard@redhat.com> 0.1.11-1.fc7
- finish inactive Xen domains support
- memory leak fix
- RelaxNG schemas for XML configs

* Wed Dec 20 2006 Daniel Veillard <veillard@redhat.com> 0.1.10-1.fc7
- support for inactive Xen domains
- improved support for Xen display and vnc
- a few bug fixes
- localization updates

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.1.9-2
- rebuild against python 2.5

* Wed Nov 29 2006 Daniel Veillard <veillard@redhat.com> 0.1.9-1
- better error reporting
- python bindings fixes and extensions
- add support for shareable drives
- add support for non-bridge style networking
- hot plug device support
- added support for inactive domains
- API to dump core of domains
- various bug fixes, cleanups and improvements
- updated the localization

* Tue Nov  7 2006 Daniel Veillard <veillard@redhat.com> 0.1.8-3
- it's pkgconfig not pgkconfig !

* Mon Nov  6 2006 Daniel Veillard <veillard@redhat.com> 0.1.8-2
- fixing spec file, added %dist, -devel requires pkgconfig and xen-devel
- Resolves: rhbz#202320

* Mon Oct 16 2006 Daniel Veillard <veillard@redhat.com> 0.1.8-1
- fix missing page size detection code for ia64
- fix mlock size when getting domain info list from hypervisor
- vcpu number initialization
- don't label crashed domains as shut off
- fix virsh man page
- blktapdd support for alternate drivers like blktap
- memory leak fixes (xend interface and XML parsing)
- compile fix
- mlock/munlock size fixes

* Fri Sep 22 2006 Daniel Veillard <veillard@redhat.com> 0.1.7-1
- Fix bug when running against xen-3.0.3 hypercalls
- Fix memory bug when getting vcpus info from xend

* Fri Sep 22 2006 Daniel Veillard <veillard@redhat.com> 0.1.6-1
- Support for localization
- Support for new Xen-3.0.3 cdrom and disk configuration
- Support for setting VNC port
- Fix bug when running against xen-3.0.2 hypercalls
- Fix reconnection problem when talking directly to http xend

* Tue Sep  5 2006 Jeremy Katz <katzj@redhat.com> - 0.1.5-3
- patch from danpb to support new-format cd devices for HVM guests

* Tue Sep  5 2006 Daniel Veillard <veillard@redhat.com> 0.1.5-2
- reactivating ia64 support

* Tue Sep  5 2006 Daniel Veillard <veillard@redhat.com> 0.1.5-1
- new release
- bug fixes
- support for new hypervisor calls
- early code for config files and defined domains

* Mon Sep  4 2006 Daniel Berrange <berrange@redhat.com> - 0.1.4-5
- add patch to address dom0_ops API breakage in Xen 3.0.3 tree

* Mon Aug 28 2006 Jeremy Katz <katzj@redhat.com> - 0.1.4-4
- add patch to support paravirt framebuffer in Xen 

* Mon Aug 21 2006 Daniel Veillard <veillard@redhat.com> 0.1.4-3
- another patch to fix network handling in non-HVM guests

* Thu Aug 17 2006 Daniel Veillard <veillard@redhat.com> 0.1.4-2
- patch to fix virParseUUID()

* Wed Aug 16 2006 Daniel Veillard <veillard@redhat.com> 0.1.4-1
- vCPUs and affinity support
- more complete XML, console and boot options
- specific features support
- enforced read-only connections
- various improvements, bug fixes

* Wed Aug  2 2006 Jeremy Katz <katzj@redhat.com> - 0.1.3-6
- add patch from pvetere to allow getting uuid from libvirt

* Wed Aug  2 2006 Jeremy Katz <katzj@redhat.com> - 0.1.3-5
- build on ia64 now

* Thu Jul 27 2006 Jeremy Katz <katzj@redhat.com> - 0.1.3-4
- don't BR xen, we just need xen-devel

* Thu Jul 27 2006 Daniel Veillard <veillard@redhat.com> 0.1.3-3
- need rebuild since libxenstore is now versionned

* Mon Jul 24 2006 Mark McLoughlin <markmc@redhat.com> - 0.1.3-2
- Add BuildRequires: xen-devel

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.1.3-1.1
- rebuild

* Tue Jul 11 2006 Daniel Veillard <veillard@redhat.com> 0.1.3-1
- support for HVM Xen guests
- various bugfixes

* Mon Jul  3 2006 Daniel Veillard <veillard@redhat.com> 0.1.2-1
- added a proxy mechanism for read only access using httpu
- fixed header includes paths

* Wed Jun 21 2006 Daniel Veillard <veillard@redhat.com> 0.1.1-1
- extend and cleanup the driver infrastructure and code
- python examples
- extend uuid support
- bug fixes, buffer handling cleanups
- support for new Xen hypervisor API
- test driver for unit testing
- virsh --conect argument

* Mon Apr 10 2006 Daniel Veillard <veillard@redhat.com> 0.1.0-1
- various fixes
- new APIs: for Node information and Reboot
- virsh improvements and extensions
- documentation updates and man page
- enhancement and fixes of the XML description format

* Tue Feb 28 2006 Daniel Veillard <veillard@redhat.com> 0.0.6-1
- added error handling APIs
- small bug fixes
- improve python bindings
- augment documentation and regression tests

* Thu Feb 23 2006 Daniel Veillard <veillard@redhat.com> 0.0.5-1
- new domain creation API
- new UUID based APIs
- more tests, documentation, devhelp
- bug fixes

* Fri Feb 10 2006 Daniel Veillard <veillard@redhat.com> 0.0.4-1
- fixes some problems in 0.0.3 due to the change of names

* Wed Feb  8 2006 Daniel Veillard <veillard@redhat.com> 0.0.3-1
- changed library name to libvirt from libvir, complete and test the python 
  bindings

* Sun Jan 29 2006 Daniel Veillard <veillard@redhat.com> 0.0.2-1
- upstream release of 0.0.2, use xend, save and restore added, python bindings
  fixed

* Wed Nov  2 2005 Daniel Veillard <veillard@redhat.com> 0.0.1-1
- created
