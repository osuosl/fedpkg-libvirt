# -*- rpm-spec -*-

%define with_xen       0%{!?_without_xen:1}
%define with_xen_proxy 0%{!?_without_xen_proxy:1}
%define with_qemu      0%{!?_without_qemu:1}
%define with_openvz    0%{!?_without_openvz:1}
%define with_lxc       0%{!?_without_lxc:1}
%define with_sasl      0%{!?_without_sasl:1}
%define with_avahi     0%{!?_without_avahi:1}
%define with_polkit    0%{!?_without_polkit:0}
%define with_python    0%{!?_without_python:1}
%define with_libvirtd  0%{!?_without_libvirtd:1}
%define with_uml       0%{!?_without_uml:1}
%define with_network   0%{!?_without_network:1}

%define with_xen           0%{!?_without_xen:1}
%define with_xen_proxy     0%{!?_without_xen_proxy:1}
%define with_qemu          0%{!?_without_qemu:1}
%define with_openvz        0%{!?_without_openvz:1}
%define with_lxc           0%{!?_without_lxc:1}
%define with_sasl          0%{!?_without_sasl:1}
%define with_avahi         0%{!?_without_avahi:1}
%define with_polkit        0%{!?_without_polkit:0}
%define with_python        0%{!?_without_python:1}
%define with_libvirtd      0%{!?_without_libvirtd:1}
%define with_uml           0%{!?_without_uml:1}
%define with_network       0%{!?_without_network:1}
%define with_storage_fs    0%{!?_without_storage_fs:1}
%define with_storage_lvm   0%{!?_without_storage_lvm:1}
%define with_storage_iscsi 0%{!?_without_storage_iscsi:1}
%define with_storage_disk  0%{!?_without_storage_disk:1}
%define with_numactl       0%{!?_without_numactl:1}


# Xen is available only on i386 x86_64 ia64
%ifnarch i386 i586 i686 x86_64 ia64
%define with_xen 0
%endif

%if ! %{with_xen}
%define with_xen_proxy 0
%endif

%if 0%{?fedora}
%ifarch ppc64
%define with_qemu 0
%endif
%endif

%if 0%{?fedora} >= 8
%define with_polkit    0%{!?_without_polkit:1}
%define with_xen_proxy 0
%endif

#
# If building on RHEL switch on the specific support
# for the specific Xen version
#
%if 0%{?fedora}
%define with_rhel5 0
%else
%define with_rhel5 1
%endif


Summary: Library providing a simple API virtualization
Name: libvirt
Version: 0.6.2
Release: 12%{?dist}%{?extra_release}
License: LGPLv2+
Group: Development/Libraries
Source: libvirt-%{version}.tar.gz

# Patches cherry-picked from upstream
Patch0: libvirt-0.6.2-qemu-drive-format.patch
# Fix shared/readonly disk labelling
Patch1: libvirt-0.6.2-shared-readonly-label.patch
# Fix <hostdev managed='yes'>
Patch2: libvirt-0.6.3-hostdev-managed.patch
# Refresh qemu caps when getCapabilities is called (bz 460649)
Patch3: libvirt-0.6.3-refresh-qemu-caps.patch
# Enable migration with qemu 0.10
Patch4: libvirt-0.6.2-enable-qemu-0-10-migration.patch
# Don't try to label a disk with no path (e.g. empty cdrom) (bz 499569)
Patch5: libvirt-0.6.2-fix-nosource-label.patch
# Fix qemu argv detection with latest qemu (bz 501923)
Patch6: libvirt-0.6.2-fix-qemu-argv-detection-with-kvm-85.patch
# Fix XML attribute escaping (bz 499791)
Patch7: libvirt-0.6.2-xml-attribute-escaping.patch
# Fix serious event handling issues causing guests to be destroyed (bz 499698)
Patch8: libvirt-0.6.2-event-handling-1.patch
Patch9: libvirt-0.6.2-event-handling-2.patch
# Don't log monitor output to domain log file (bz 499584)
Patch10: libvirt-0.6.2-do-not-log-monitor-output.patch
# Bring up the bridge, even if it doesn't have an IP address (bz 501912)
Patch11: libvirt-0.6.2-bring-up-ipless-bridge.patch
# Use the correct QEMU machine type for ppc (bz 502862)
Patch12: libvirt-0.6.2-qemu-ppc-machine-type.patch
# Fix crash with TLS connections (bz 503066)
Patch13: libvirt-0.6.2-libvirtd-double-free.patch
# Fix broken networking with newer qemu releases (bz 503275)
Patch14: libvirt-0.6.2-avoid-broken-networking-with-newer-qemu.patch

# Not for upstream. Temporary hack till PulseAudio autostart
# problems are sorted out when SELinux enforcing
Patch200: libvirt-0.6.2-svirt-sound.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
URL: http://libvirt.org/
BuildRequires: python python-devel
Requires: readline
Requires: ncurses
Requires: dnsmasq
Requires: bridge-utils
Requires: iptables
# needed for device enumeration
Requires: hal
# So remote clients can access libvirt over SSH tunnel
# (client invokes 'nc' against the UNIX socket on the server)
Requires: nc
%if %{with_sasl}
Requires: cyrus-sasl
# Not technically required, but makes 'out-of-box' config
# work correctly & doesn't have onerous dependencies
Requires: cyrus-sasl-md5
%endif
%if %{with_polkit}
Requires: PolicyKit >= 0.6
%endif
%if %{with_storage_fs}
# For mount/umount in FS driver
BuildRequires: util-linux
# For showmount in FS driver (netfs discovery)
BuildRequires: nfs-utils
Requires: nfs-utils
%endif
%if %{with_qemu}
# From QEMU RPMs
Requires: /usr/bin/qemu-img
%else
%if %{with_xen}
# From Xen RPMs
Requires: /usr/sbin/qcow-create
%endif
%endif
%if %{with_storage_lvm}
# For LVM drivers
Requires: lvm2
%endif
%if %{with_storage_iscsi}
# For ISCSI driver
Requires: iscsi-initiator-utils
%endif
%if %{with_storage_disk}
# For disk driver
Requires: parted
%endif
# For svirt support
Requires: libselinux
%if %{with_xen}
BuildRequires: xen-devel
%endif
BuildRequires: libxml2-devel
BuildRequires: xhtml1-dtds
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: gettext
BuildRequires: gnutls-devel
BuildRequires: hal-devel
%if %{with_avahi}
BuildRequires: avahi-devel
%endif
BuildRequires: libselinux-devel
BuildRequires: dnsmasq
BuildRequires: bridge-utils
%if %{with_sasl}
BuildRequires: cyrus-sasl-devel
%endif
%if %{with_polkit}
BuildRequires: PolicyKit-devel >= 0.6
%endif
%if %{with_storage_fs}
# For mount/umount in FS driver
BuildRequires: util-linux
%endif
%if %{with_qemu}
# From QEMU RPMs
BuildRequires: /usr/bin/qemu-img
%else
%if %{with_xen}
# From Xen RPMs
BuildRequires: /usr/sbin/qcow-create
%endif
%endif
%if %{with_storage_lvm}
# For LVM drivers
BuildRequires: lvm2
%endif
%if %{with_storage_iscsi}
# For ISCSI driver
BuildRequires: iscsi-initiator-utils
%endif
%if %{with_storage_disk}
# For disk driver
BuildRequires: parted-devel
%endif
%if %{with_numactl}
# For QEMU/LXC numa info
BuildRequires: numactl-devel
%endif
Obsoletes: libvir <= 0.2
Provides: libvir = %{version}-%{release}

# Fedora build root suckage
BuildRequires: gawk

%description
Libvirt is a C toolkit to interact with the virtualization capabilities
of recent versions of Linux (and other OSes).

%package devel
Summary: Libraries, includes, etc. to compile with the libvirt library
Group: Development/Libraries
Requires: libvirt = %{version}-%{release}
Requires: pkgconfig
%if %{with_xen}
Requires: xen-devel
%endif
Obsoletes: libvir-devel <= 0.2
Provides: libvir-devel = %{version}-%{release}

%description devel
Includes and documentations for the C library providing an API to use
the virtualization capabilities of recent versions of Linux (and other OSes).

%if %{with_python}
%package python
Summary: Python bindings for the libvirt library
Group: Development/Libraries
Requires: libvirt = %{version}-%{release}
Obsoletes: libvir-python <= 0.2
Provides: libvir-python = %{version}-%{release}

%description python
The libvirt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).
%endif

%prep
%setup -q

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

%patch200 -p0

mv NEWS NEWS.old
iconv -f ISO-8859-1 -t UTF-8 < NEWS.old > NEWS

%build
%if ! %{with_xen}
%define _without_xen --without-xen
%endif

%if ! %{with_qemu}
%define _without_qemu --without-qemu
%endif

%if ! %{with_openvz}
%define _without_openvz --without-openvz
%endif

%if ! %{with_lxc}
%define _without_lxc --without-lxc
%endif

%if ! %{with_sasl}
%define _without_sasl --without-sasl
%endif

%if ! %{with_avahi}
%define _without_avahi --without-avahi
%endif

%if ! %{with_polkit}
%define _without_polkit --without-polkit
%endif

%if ! %{with_python}
%define _without_python --without-python
%endif

%if ! %{with_libvirtd}
%define _without_libvirtd --without-libvirtd
%endif

%if ! %{with_uml}
%define _without_uml --without-uml
%endif

%if %{with_rhel5}
%define _with_rhel5_api --with-rhel5-api
%endif

%if ! %{with_network}
%define _without_network --without-network
%endif

%if ! %{with_storage_fs}
%define _without_storage_fs --without-storage-fs
%endif

%if ! %{with_storage_lvm}
%define _without_storage_lvm --without-storage-lvm
%endif

%if ! %{with_storage_iscsi}
%define _without_storage_iscsi --without-storage-iscsi
%endif

%if ! %{with_storage_disk}
%define _without_storage_disk --without-storage-disk
%endif

%if ! %{with_numactl}
%define _without_numactl --without-numactl
%endif

%configure %{?_without_xen} \
           %{?_without_qemu} \
           %{?_without_openvz} \
           %{?_without_lxc} \
           %{?_without_sasl} \
           %{?_without_avahi} \
           %{?_without_polkit} \
           %{?_without_python} \
           %{?_without_libvirtd} \
           %{?_without_uml} \
           %{?_without_network} \
           %{?_with_rhel5_api} \
           %{?_without_storage_fs} \
           %{?_without_storage_lvm} \
           %{?_without_storage_iscsi} \
           %{?_without_storage_disk} \
           %{?_without_numactl} \
           --with-init-script=redhat \
           --with-qemud-pid-file=%{_localstatedir}/run/libvirt_qemud.pid \
           --with-remote-file=%{_localstatedir}/run/libvirtd.pid
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

%makeinstall
(cd docs/examples ; make clean ; rm -rf .deps Makefile Makefile.in)
(cd docs/examples/python ; rm -rf .deps Makefile Makefile.in)
(cd examples/hellolibvirt ; make clean ; rm -rf .deps .libs Makefile Makefile.in)
(cd examples/domain-events/events-c ;  make clean ;rm -rf .deps .libs Makefile Makefile.in)

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/python*/site-packages/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/python*/site-packages/*.a
install -d -m 0755 $RPM_BUILD_ROOT%{_localstatedir}/run/libvirt/
# Default dir for disk images defined in SELinux policy
install -d -m 0755 $RPM_BUILD_ROOT%{_localstatedir}/lib/libvirt/images/
# Default dir for kernel+initrd images defnied in SELinux policy
install -d -m 0755 $RPM_BUILD_ROOT%{_localstatedir}/lib/libvirt/boot/
# used for virDomainMemoryPeek
install -d -m 0700 $RPM_BUILD_ROOT%{_localstatedir}/cache/libvirt/

%if %{with_qemu}
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
%else
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/default.xml
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/libvirtd_qemu.aug
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/tests/test_libvirtd_qemu.aug
%endif
%find_lang %{name}

%if ! %{with_python}
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libvirt-python-%{version}
%endif

%if ! %{with_qemu}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu.conf
%endif

%if %{with_libvirtd}
chmod 0644 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/libvirtd
%endif

%clean
rm -fr %{buildroot}

%post
/sbin/ldconfig

%if %{with_libvirtd}
%if %{with_qemu}
# We want to install the default network for initial RPM installs
# or on the first upgrade from a non-network aware libvirt only.
# We check this by looking to see if the daemon is already installed
/sbin/chkconfig --list libvirtd 1>/dev/null 2>&1
if [ $? != 0 -a ! -f %{_sysconfdir}/libvirt/qemu/networks/default.xml ]
then
    UUID=`/usr/bin/uuidgen`
    sed -e "s,</name>,</name>\n  <uuid>$UUID</uuid>," \
         < %{_datadir}/libvirt/networks/default.xml \
         > %{_sysconfdir}/libvirt/qemu/networks/default.xml
    ln -s ../default.xml %{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
fi
%endif

/sbin/chkconfig --add libvirtd
%endif

%preun
%if %{with_libvirtd}
if [ $1 = 0 ]; then
    /sbin/service libvirtd stop 1>/dev/null 2>&1
    /sbin/chkconfig --del libvirtd
fi
%endif

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-, root, root)

%doc AUTHORS ChangeLog NEWS README COPYING.LIB TODO
%doc %{_mandir}/man1/virsh.1*
%{_bindir}/virsh
%{_libdir}/lib*.so.*
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/

%if %{with_qemu}
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/networks/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/networks/autostart
%endif

%if %{with_libvirtd}
%{_sysconfdir}/rc.d/init.d/libvirtd
%config(noreplace) %{_sysconfdir}/sysconfig/libvirtd
%config(noreplace) %{_sysconfdir}/libvirt/libvirtd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd
%endif

%if %{with_qemu}
%config(noreplace) %{_sysconfdir}/libvirt/qemu.conf
%endif

%if %{with_sasl}
%config(noreplace) %{_sysconfdir}/sasl2/libvirt.conf
%endif

%if %{with_qemu}
%dir %{_datadir}/libvirt/
%dir %{_datadir}/libvirt/networks/
%{_datadir}/libvirt/networks/default.xml
%endif

%dir %{_datadir}/libvirt/
%dir %{_datadir}/libvirt/schemas/

%{_datadir}/libvirt/schemas/domain.rng
%{_datadir}/libvirt/schemas/network.rng
%{_datadir}/libvirt/schemas/storagepool.rng
%{_datadir}/libvirt/schemas/storagevol.rng
%{_datadir}/libvirt/schemas/nodedev.rng
%{_datadir}/libvirt/schemas/capability.rng

%dir %{_localstatedir}/run/libvirt/

%dir %{_localstatedir}/lib/libvirt/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/images/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/boot/
%dir %attr(0700, root, root) %{_localstatedir}/cache/libvirt/

%if %{with_qemu}
%dir %{_localstatedir}/run/libvirt/qemu/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/qemu/
%endif
%if %{with_lxc}
%dir %{_localstatedir}/run/libvirt/lxc/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/lxc/
%endif
%if %{with_uml}
%dir %{_localstatedir}/run/libvirt/uml/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/uml/
%endif
%if %{with_network}
%dir %{_localstatedir}/run/libvirt/network/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/network/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/iptables/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/iptables/filter/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/iptables/nat/
%endif

%if %{with_qemu}
%{_datadir}/augeas/lenses/libvirtd_qemu.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_qemu.aug
%endif

%if %{with_libvirtd}
%{_datadir}/augeas/lenses/libvirtd.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd.aug
%endif

%if %{with_polkit}
%{_datadir}/PolicyKit/policy/org.libvirt.unix.policy
%endif

%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/
%if %{with_qemu}
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/qemu/
%endif

%if %{with_xen_proxy}
%attr(4755, root, root) %{_libexecdir}/libvirt_proxy
%endif

%if %{with_lxc}
%attr(0755, root, root) %{_libexecdir}/libvirt_lxc
%endif

%if %{with_libvirtd}
%attr(0755, root, root) %{_libexecdir}/libvirt_parthelper
%attr(0755, root, root) %{_sbindir}/libvirtd
%endif

%doc docs/*.xml

%files devel
%defattr(-, root, root)

%{_libdir}/lib*.so
%dir %{_includedir}/libvirt
%{_includedir}/libvirt/*.h
%{_libdir}/pkgconfig/libvirt.pc
%dir %{_datadir}/gtk-doc/html/libvirt
%doc %{_datadir}/gtk-doc/html/libvirt/*.devhelp
%doc %{_datadir}/gtk-doc/html/libvirt/*.html
%doc %{_datadir}/gtk-doc/html/libvirt/*.png
%doc %{_datadir}/gtk-doc/html/libvirt/*.css

%doc docs/*.html docs/html docs/*.gif
%doc docs/examples
%doc docs/libvirt-api.xml
%doc examples

%if %{with_python}
%files python
%defattr(-, root, root)

%doc AUTHORS NEWS README COPYING.LIB
%{_libdir}/python*/site-packages/libvirt.py*
%{_libdir}/python*/site-packages/libvirtmod*
%doc python/tests/*.py
%doc python/TODO
%doc python/libvirtclass.txt
%doc docs/examples/python
%endif

%changelog
* Fri Jun  5 2009 Mark McLoughlin <markmc@redhat.com> - 0.6.2-12.fc11
- Use the correct QEMU machine type for ppc (bug #502862)
- Fix crash with TLS connections (bug #503066)
- Fix broken networking with newer qemu releases (bug #503275)
- Remove the qemu BuildRequires

* Mon May 25 2009 Mark McLoughlin <markmc@redhat.com> - 0.6.2-11.fc11
- Bring up the bridge, even if it doesn't have an IP address (bug #501912)

* Fri May 22 2009 Mark McLoughlin <markmc@redhat.com> - 0.6.2-10.fc11
- Don't log monitor output to domain log file (bug #499584)

* Thu May 21 2009 Mark McLoughlin <markmc@redhat.com> - 0.6.2-9.fc11
- Fix qemu argv detection with latest qemu (bug #501923)
- Fix XML attribute escaping (bug #499791)
- Fix serious event handling issues causing guests to be destroyed (bug #499698)

* Sun May 10 2009 Cole Robinson <crobinso@redhat.com> - 0.6.2-8.fc11
- Don't try to label a disk with no path (e.g. empty cdrom) (bug #499569)

* Thu May  7 2009 Mark McLoughlin <markmc@redhat.com> - 0.6.2-7.fc11
- Enable migration for qemu 0.10 (bug #499704)

* Wed May  6 2009 Cole Robinson <crobinso@redhat.com> - 0.6.2-6.fc11
- Refresh qemu caps when getCapabilities is called (bug #460649)

* Wed May  6 2009 Mark McLoughlin <markmc@redhat.com> - 0.6.2-5.fc11
- Fix handling of <hostdev managed='yes'> (bug #499386)

* Tue May  5 2009 Daniel P. Berrange <berrange@redhat.com> - 0.6.2-4.fc11
- Fix labelling of shared/readonly disks (rhbz #493692)

* Tue Apr 28 2009 Daniel Veillard <veillard@redhat.com> - 0.6.2-3.fc11
- Fix missing directories in spec (#496945 and gtk-doc)

* Thu Apr 16 2009 Mark McLoughlin <markmc@redhat.com> - 0.6.2-2.fc11
- Fix qemu drive format specification (#496092)

* Fri Apr  3 2009 Daniel Veillard <veillard@redhat.com> - 0.6.2-1.fc11
- release of 0.6.2
- memory ballooning in QEMU
- SCSI HBA storage pool support
- support SASL auth for VNC server
- PCI passthrough in Xen driver
- assorted bug fixes

* Fri Apr  3 2009 Daniel P. Berrange  <berrange@redhat.com> - 0.6.1-6.fc11
- Fix typo in previous patch

* Tue Mar 17 2009 Daniel P. Berrange <berrange@redhat.com> - 0.6.1-5.fc11
- Don't relabel shared/readonly disks
- Disable sound cards when running sVirt

* Tue Mar 17 2009 Daniel P. Berrange <berrange@redhat.com> - 0.6.1-4.fc11
- Fix memory allocation for xend lookup
- Avoid crash if storage volume deletion fails
- Fix multiple FD leaks
- Fix bug in dispatch FD events when a callback is marked deleted
- Fix parsing of storage volume owner/group/mode
- Fix memory allocation for virDomainGetVcpus RPC handler
- Avoid deadlock in setting vCPU count
- Use correct driver name in Xen block detach

* Mon Mar  9 2009 Cole Robinson <crobinso@redhat.com> - 0.6.1-3.fc11
- Add Requires: libselinux

* Fri Mar  6 2009 Daniel P. Berrange <berrange@redhat.com> - 0.6.1-2.fc11
- Fix crash after storage vol deletion fails
- Add patch to enable VNC SASL authentication

* Wed Mar  4 2009 Daniel Veillard <veillard@redhat.com> - 0.6.1-1.fc11
- upstream release 0.6.1
- support for node device detach reattach and reset
- sVirt mandatory access control support
- many bug fixes and small improvements

* Mon Mar  2 2009 Daniel Veillard <veillard@redhat.com> - 0.6.0-6.fc11
- make sure Xen is handled in i586 new default 32bits x86 packages

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-5.fc11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Daniel P. Berrange <berrange@redhat.com> - 0.6.0-4.fc11
- Fix QEMU startup timeout/race (rhbz #484649)
- Setup DBus threading. Don't allow dbus to call _exit / change SIGPIPE (rhbz #484553)
- Fix timeout when autostarting session daemon

* Wed Feb 11 2009 Richard W.M. Jones <rjones@redhat.com> - 0.6.0-3.fc11
- Multiple fixes to remove rpmlint warnings/errors (rhbz #226055)

* Fri Feb  6 2009 Daniel P. Berrange <berrange@redhat.com> - 0.6.0-2.fc11
- Fix libvirtd --timeout usage
- Fix RPC call problems and QEMU startup handling (rhbz #484414)
- Fix unowned directories (rhbz #483442)

* Sat Jan 31 2009 Daniel Veillard <veillard@redhat.com> - 0.6.0-1.fc11
- upstream release 0.6.0
- thread safety of API
- allow QEmu/KVM domains to survive daemon restart
- extended logging capabilities
- support copy on write storage volumes for QEmu/KVM
- support of storage cache control options for QEmu/KVM
- a lot of bug fixes

* Wed Dec 17 2008 Daniel Veillard <veillard@redhat.com> - 0.5.1-2.fc11
- fix missing read-only access checks, fixes CVE-2008-5086

* Fri Dec  5 2008 Daniel Veillard <veillard@redhat.com> - 0.5.1-1.fc11
- upstream release 0.5.1
- mostly bugfixes e.g #473071
- some driver improvments

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.5.0-2
- Rebuild for Python 2.6

* Wed Nov 26 2008 Daniel Veillard <veillard@redhat.com> - 0.5.0-1.fc11
- upstream release 0.5.0
- domain lifecycle event support
- node device enumeration
- KVM/QEmu migration support
- improved LXC support
- SDL display configuration
- User Mode Linux driver (Daniel Berrange)

* Wed Sep 24 2008 Daniel Veillard <veillard@redhat.com> - 0.4.6-3.fc10
- apply the python makefile patch for #463733

* Wed Sep 24 2008 Daniel Veillard <veillard@redhat.com> - 0.4.6-2.fc10
- upstream release 0.4.6
- fixes some problems with 0.4.5

* Tue Sep  9 2008 Daniel Veillard <veillard@redhat.com> - 0.4.5-2.fc10
- fix a crash if a QEmu/KVM domain is defined without an emulator path

* Mon Sep  8 2008 Daniel Veillard <veillard@redhat.com> - 0.4.5-1.fc10
- upstream release 0.4.5
- a lot of bug fixes
- major updates to QEmu/KVM and Linux containers drivers
- support for OpenVZ if installed

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.4.4-3.fc10
- fix license tag

* Tue Jul  8 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.4-2.fc10
- Fix booting of CDROM images with KVM (rhbz #452355)

* Wed Jun 25 2008 Daniel Veillard <veillard@redhat.com> - 0.4.4-1.fc10
- upstream release 0.4.4
- fix a few bugs in previous release

* Thu Jun 12 2008 Daniel Veillard <veillard@redhat.com> - 0.4.3-1.fc10
- upstream release 0.4.3
- many bug fixes
- many small improvements
- serious xenner fixes

* Wed Jun  4 2008 Mark McLoughlin <markmc@redhat.com> - 0.4.2-6.fc10
- Disable lokkit support again (#449996, #447633)
- Ensure %-fedora is evaluated correctly

* Thu May 15 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.2-5.fc10
- Rebuild with policy enabled (rhbz #446616)

* Fri May  9 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.2-4.fc10
- Added directory for initrd/kernel images for SELinux policy

* Mon Apr 28 2008 Mark McLoughlin <markmc@redhat.com> - 0.4.2-3.fc10
- Simplify the way arch conditionals are handled

* Mon Apr 28 2008 Mark McLoughlin <markmc@redhat.com> - 0.4.2-2.fc10
- Enable lokkit support (#443796)

* Tue Apr  8 2008 Daniel Veillard <veillard@redhat.com> - 0.4.2-1.fc9
- upstream release 0.4.2
- many bug fixes
- localization updates

* Thu Apr  4 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.1-7.fc9
- Don't run polkit-auth as root
- Don't request polkit auth if client is root

* Fri Mar 28 2008 Chris Lalancette <clalance@redhat.com> - 0.4.1-6.fc9
- When dumping XML for a storage pool, make the <source> directory tag
  match the <dir> tag used for specifying the pool in the first place

* Thu Mar 27 2008 Chris Lalancette <clalance@redhat.com> - 0.4.1-5.fc9
- Do iscsiadm sendtarget before trying to do login
- Do sysfs scanning for iSCSI LUNs instead of trying to parse them from
  iscsiadm session output

* Thu Mar 13 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.1-4.fc9
- Fix QEMU tap device setup
- Fix Xen boot device XML processing
- Fixed QEMU cdrom media change

* Mon Mar 10 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.1-3.fc9
- Fixed daemon startup when run with --daemon flag

* Mon Mar  3 2008 Daniel Veillard <veillard@redhat.com> - 0.4.1-2.fc9
- 2 patches found just after the release

* Mon Mar  3 2008 Daniel Veillard <veillard@redhat.com> - 0.4.1-1.fc9
- Release of 0.4.1
- Storage APIs
- xenner support
- lots of assorted improvements, bugfixes and cleanups
- documentation and localization improvements

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.4.0-5
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.0-4.fc9
- Fix SSH tunnelling (rhbz #428743)
- Fix back-compat for nodeinfo call changes.

* Sun Jan 13 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.0-3.fc9
- Fix crash when no auth callback

* Wed Jan  2 2008 Daniel P. Berrange <berrange@redhat.com> - 0.4.0-2.fc9
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
- fixing spec file, added %-dist, -devel requires pkgconfig and xen-devel
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
