# -*- rpm-spec -*-

# A client only build will create a libvirt.so only containing
# the generic RPC driver, and test driver and no libvirtd
# Default to a full server + client build
%define client_only        0

# Now turn off server build in certain cases

# RHEL-5 builds are client-only for s390, ppc
%if 0%{?rhel} == 5
%ifnarch i386 i586 i686 x86_64 ia64
%define client_only        1
%endif
%endif

# Disable all server side drivers if client only build requested
%if %{client_only}
%define server_drivers     0
%else
%define server_drivers     1
%endif


# Now set the defaults for all the important features, independent
# of any particular OS

# First the daemon itself
%define with_libvirtd      0%{!?_without_libvirtd:%{server_drivers}}
%define with_avahi         0%{!?_without_avahi:%{server_drivers}}

# Then the hypervisor drivers that run on local host
%define with_xen           0%{!?_without_xen:%{server_drivers}}
%define with_xen_proxy     0%{!?_without_xen_proxy:%{server_drivers}}
%define with_qemu          0%{!?_without_qemu:%{server_drivers}}
%define with_openvz        0%{!?_without_openvz:%{server_drivers}}
%define with_lxc           0%{!?_without_lxc:%{server_drivers}}
%define with_vbox          0%{!?_without_vbox:%{server_drivers}}
%define with_uml           0%{!?_without_uml:%{server_drivers}}
# XXX this shouldn't be here, but it mistakenly links into libvirtd
%define with_one           0%{!?_without_one:%{server_drivers}}

# Then the hypervisor drivers that talk a native remote protocol
%define with_phyp          0%{!?_without_phyp:1}
%define with_esx           0%{!?_without_esx:1}

# Then the secondary host drivers
%define with_network       0%{!?_without_network:%{server_drivers}}
%define with_storage_fs    0%{!?_without_storage_fs:%{server_drivers}}
%define with_storage_lvm   0%{!?_without_storage_lvm:%{server_drivers}}
%define with_storage_iscsi 0%{!?_without_storage_iscsi:%{server_drivers}}
%define with_storage_disk  0%{!?_without_storage_disk:%{server_drivers}}
%define with_storage_mpath 0%{!?_without_storage_mpath:%{server_drivers}}
%define with_numactl       0%{!?_without_numactl:%{server_drivers}}
%define with_selinux       0%{!?_without_selinux:%{server_drivers}}
%define with_hal           0%{!?_without_hal:%{server_drivers}}

# A few optional bits off by default, we enable later
%define with_polkit        0%{!?_without_polkit:0}
%define with_capng         0%{!?_without_capng:0}
%define with_netcf         0%{!?_without_netcf:0}

# Non-server/HV driver defaults which are always enabled
%define with_python        0%{!?_without_python:1}
%define with_sasl          0%{!?_without_sasl:1}


# Finally set the OS / architecture specific special cases

# Xen is available only on i386 x86_64 ia64
%ifnarch i386 i586 i686 x86_64 ia64
%define with_xen 0
%endif


# RHEL doesn't ship OpenVZ, VBox, UML, OpenNebula, PowerHypervisor or ESX
%if 0%{?rhel}
%define with_openvz 0
%define with_vbox 0
%define with_uml 0
%define with_one 0
%define with_phyp 0
%define with_esx 0
%endif

# RHEL-5 has restricted QEMU to x86_64 only and is too old for LXC
%if 0%{?rhel} == 5
%ifnarch x86_64
%define with_qemu 0
%endif
%define with_lxc 0
%endif

# RHEL-6 has restricted QEMU to x86_64 only, stopped including Xen
# on all archs. Other archs all have LXC available though
%if 0%{?rhel} >= 6
%ifnarch x86_64
%define with_qemu 0
%endif
%define with_xen 0
%endif

# If Xen isn't turned on, we shouldn't build the xen proxy either
%if ! %{with_xen}
%define with_xen_proxy 0
%endif

# Fedora doesn't have any QEMU on ppc64 - only ppc
%if 0%{?fedora}
%ifarch ppc64
%define with_qemu 0
%endif
%endif

# PolicyKit was introduced in Fedora 8 / RHEL-6 or newer, allowing
# the setuid Xen proxy to be killed off
%if 0%{?fedora} >= 8 || 0%{?rhel} >= 6
%define with_polkit    0%{!?_without_polkit:1}
%define with_xen_proxy 0
%endif

# libcapng is used to manage capabilities in Fedora 12 / RHEL-6 or newer
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
%define with_capng     0%{!?_without_capng:1}
%endif

# netcf is used to manage network interfaces in Fedora 12 / RHEL-6 or newer
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
%define with_netcf     0%{!?_without_netcf:%{server_drivers}}
%endif

# Force QEMU to run as non-root
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
%define qemu_user  qemu
%define qemu_group  qemu
%else
%define qemu_user  root
%define qemu_group  root
%endif


# The RHEL-5 Xen package has some feature backports. This
# flag is set to enable use of those special bits on RHEL-5
%if 0%{?rhel} == 5
%define with_rhel5  1
%else
%define with_rhel5  0
%endif


Summary: Library providing a simple API virtualization
Name: libvirt
Version: 0.7.1
Release: 18%{?dist}%{?extra_release}
License: LGPLv2+
Group: Development/Libraries
Source: http://libvirt.org/sources/libvirt-%{version}.tar.gz

# A couple of hot-unplug memory handling fixes (#523953)
Patch01: libvirt-fix-net-hotunplug-double-free.patch
Patch02: libvirt-fix-pci-hostdev-hotunplug-leak.patch

# Don't set a bogus error in virDrvSupportsFeature()
Patch03: libvirt-fix-drv-supports-feature-bogus-error.patch

# Fix raw save format
Patch04: libvirt-fix-qemu-raw-format-save.patch

# Fix USB device passthrough (#422683)
Patch05: libvirt-fix-usb-device-passthrough.patch

# Disable sound backend (#524499, #508317)
Patch06: libvirt-disable-audio-backend.patch

# Re-label qcow2 backing files (#497131)
Patch07: libvirt-svirt-relabel-qcow2-backing-files.patch

# Change logrotate config to weekly (#526769)
Patch08: libvirt-change-logrotate-config-to-weekly.patch
Patch09: libvirt-logrotate-create-lxc-uml-dirs.patch

# Add several PCI hot-unplug typo fixes from upstream
Patch10: libvirt-fix-device-detach-typo1.patch
Patch11: libvirt-fix-device-detach-typo2.patch
Patch12: libvirt-fix-device-detach-typo3.patch

# Fix libvirtd memory leak during error reply sending (#528162)
Patch13: libvirt-fix-libvirtd-leak-in-error-reply.patch

# Fix restore of qemu guest using raw save format (#523158)
Patch14: libvirt-fix-qemu-restore-from-raw1.patch
Patch15: libvirt-fix-qemu-restore-from-raw2.patch

# Misc fixes to qemu machine types handling
Patch16: libvirt-qemu-machine-type-fixes1.patch
Patch17: libvirt-qemu-machine-type-fixes2.patch

# A couple of XML formatting fixes
Patch18: libvirt-storage-iscsi-auth-xml-formatting.patch
Patch19: libvirt-network-delay-attribute-formatting.patch

# Fix xen driver recounting (#531429)
Patch20: libvirt-fix-xen-driver-refcounting.patch

# Fix crash on virsh error (#531429)
Patch21: libvirt-double-free-on-virsh-error.patch

# Fix segfault where XML parsing fails in qemu disk hotplug
Patch22: libvirt-fix-crash-on-device-hotplug-parse-error.patch

# Fix segfault where interface target device name is ommitted (#523418)
Patch23: libvirt-fix-crash-on-missing-iface-target-dev.patch

# Avoid compressing small log files (#531030)
Patch24: libvirt-logrotate-avoid-compressing-small-logs.patch
# Fix crash with invalid QEmu URI (bz 566070)
Patch25: %{name}-%{version}-qemu-uri-crash.patch
# Fix VNC TLS crash (bz 544305)
Patch26: %{name}-%{version}-gcrypt-thread-init.patch
# Fix USB devices with high bus/addr values (bz 542639)
Patch27: %{name}-%{version}-fix-usb-busaddr.patch
# Fix save/restore with non-root guests (bz 534143, bz 532654)
Patch28: %{name}-%{version}-fix-selinux-save.patch
# Fix USB devices attached via virt-manager (bz 537227)
Patch29: %{name}-%{version}-fix-usb-product.patch
# Fix attach-device crash on cgroup cleanup (bz 556791)
Patch30: %{name}-%{version}-fix-cgroup-crash.patch
# Fix crash on bad LXC URI (bz 554191)
Patch31: %{name}-%{version}-lxc-uri-crash.patch
# Add qemu.conf options for audio workaround
Patch32: %{name}-%{version}-audio-config.patch
# Fix permissions of storage backing stores (bz 579067)
Patch33: %{name}-%{version}-backing-perms.patch
# Fix parsing certain USB sysfs files (bz 598272)
Patch34: %{name}-%{version}-fix-usb-parsing.patch
# Improve migration error reporting (bz 499750)
Patch35: %{name}-%{version}-migrate-errreport.patch
# Sanitize pool target paths (bz 494005)
Patch36: %{name}-%{version}-sanitize-pool.patch
# Add qemu.conf for clear emulator capabilities
Patch37: %{name}-%{version}-caps-option.patch
# Prevent libvirtd inside a VM from breaking network access (bz 235961)
Patch38: %{name}-%{version}-network-collision.patch
# Mention --all in 'virsh list' docs (bz 575512)
Patch39: %{name}-%{version}-man-page-list.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
URL: http://libvirt.org/
BuildRequires: python-devel

# The client side, i.e. shared libs and virsh are in a subpackage
Requires: libvirt-client = %{version}-%{release}

# Used by many of the drivers, so turn it on whenever the
# daemon is present
%if %{with_libvirtd}
Requires: bridge-utils
%endif
%if %{with_network}
Requires: dnsmasq
Requires: iptables
%endif
# needed for device enumeration
%if %{with_hal}
Requires: hal
%endif
%if %{with_polkit}
%if 0%{?fedora} >= 12 || 0%{?rhel} >=6
Requires: polkit >= 0.93
%else
Requires: PolicyKit >= 0.6
%endif
%endif
%if %{with_storage_fs}
# For mount/umount in FS driver
BuildRequires: util-linux
# For showmount in FS driver (netfs discovery)
BuildRequires: nfs-utils
Requires: nfs-utils
# For glusterfs
%if 0%{?fedora} >= 11
Requires: glusterfs-client >= 2.0.1
%endif
%endif
%if %{with_qemu}
# From QEMU RPMs
Requires: /usr/bin/qemu-img
# For image compression
Requires: gzip
Requires: bzip2
Requires: lzop
Requires: xz
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
%if %{with_storage_mpath}
# For multipath support
Requires: device-mapper
%endif
%if %{with_xen}
BuildRequires: xen-devel
%endif
%if %{with_one}
BuildRequires: xmlrpc-c-devel >= 1.14.0
%endif
BuildRequires: libxml2-devel
BuildRequires: xhtml1-dtds
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: gettext
BuildRequires: gnutls-devel
%if %{with_hal}
BuildRequires: hal-devel
%endif
%if %{with_avahi}
BuildRequires: avahi-devel
%endif
%if %{with_selinux}
BuildRequires: libselinux-devel
%endif
%if %{with_network}
BuildRequires: dnsmasq
%endif
BuildRequires: bridge-utils
%if %{with_sasl}
BuildRequires: cyrus-sasl-devel
%endif
%if %{with_polkit}
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
# Only need the binary, not -devel
BuildRequires: polkit >= 0.93
%else
BuildRequires: PolicyKit-devel >= 0.6
%endif
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
%if 0%{?rhel} == 5
# Broken RHEL-5 parted RPM is missing a dep
BuildRequires: e2fsprogs-devel
%endif
%endif
%if %{with_storage_mpath}
# For Multipath support
%if 0%{?rhel} == 5
# Broken RHEL-5 packaging has header files in main RPM :-(
BuildRequires: device-mapper
%else
BuildRequires: device-mapper-devel
%endif
%endif
%if %{with_numactl}
# For QEMU/LXC numa info
BuildRequires: numactl-devel
%endif
%if %{with_capng}
BuildRequires: libcap-ng-devel >= 0.5.0
%endif
%if %{with_phyp}
BuildRequires: libssh2-devel
%endif
%if %{with_netcf}
BuildRequires: netcf-devel
%endif

# Fedora build root suckage
BuildRequires: gawk

# Needed for libvirt-logrotate-create-lxc-uml-dirs.patch
BuildRequires: automake

%description
Libvirt is a C toolkit to interact with the virtualization capabilities
of recent versions of Linux (and other OSes). The main package includes
the libvirtd server exporting the virtualization support.

%package client
Summary: Client side library and utilities of the libvirt library
Group: Development/Libraries
Requires: readline
Requires: ncurses
# So remote clients can access libvirt over SSH tunnel
# (client invokes 'nc' against the UNIX socket on the server)
Requires: nc
%if %{with_sasl}
Requires: cyrus-sasl
# Not technically required, but makes 'out-of-box' config
# work correctly & doesn't have onerous dependencies
Requires: cyrus-sasl-md5
%endif

%description client
Shared libraries and client binaries needed to access to the
virtualization capabilities of recent versions of Linux (and other OSes).

%package devel
Summary: Libraries, includes, etc. to compile with the libvirt library
Group: Development/Libraries
Requires: libvirt-client = %{version}-%{release}
Requires: pkgconfig
%if %{with_xen}
Requires: xen-devel
%endif

%description devel
Includes and documentations for the C library providing an API to use
the virtualization capabilities of recent versions of Linux (and other OSes).

%if %{with_python}
%package python
Summary: Python bindings for the libvirt library
Group: Development/Libraries
Requires: libvirt-client = %{version}-%{release}

%description python
The libvirt-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libvirt library to use the virtualization capabilities
of recent versions of Linux (and other OSes).
%endif

%prep
%setup -q

%patch01 -p1
%patch02 -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1
%patch06 -p1
%patch07 -p1
%patch08 -p1
%patch09 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1

%build
# Needed for libvirt-logrotate-create-lxc-uml-dirs.patch
automake

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

%if ! %{with_vbox}
%define _without_vbox --without-vbox
%endif

%if ! %{with_sasl}
%define _without_sasl --without-sasl
%endif

%if ! %{with_avahi}
%define _without_avahi --without-avahi
%endif

%if ! %{with_phyp}
%define _without_phyp --without-phyp
%endif

%if ! %{with_esx}
%define _without_esx --without-esx
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

%if ! %{with_one}
%define _without_one --without-one
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

%if ! %{with_storage_mpath}
%define _without_storage_mpath --without-storage-mpath
%endif

%if ! %{with_numactl}
%define _without_numactl --without-numactl
%endif

%if ! %{with_capng}
%define _without_capng --without-capng
%endif

%if ! %{with_netcf}
%define _without_netcf --without-netcf
%endif

%if ! %{with_selinux}
%define _without_selinux --without-selinux
%endif

%if ! %{with_hal}
%define _without_hal --without-hal
%endif

%configure %{?_without_xen} \
           %{?_without_qemu} \
           %{?_without_openvz} \
           %{?_without_lxc} \
           %{?_without_vbox} \
           %{?_without_sasl} \
           %{?_without_avahi} \
           %{?_without_polkit} \
           %{?_without_python} \
           %{?_without_libvirtd} \
           %{?_without_uml} \
           %{?_without_one} \
           %{?_without_phyp} \
           %{?_without_esx} \
           %{?_without_network} \
           %{?_with_rhel5_api} \
           %{?_without_storage_fs} \
           %{?_without_storage_lvm} \
           %{?_without_storage_iscsi} \
           %{?_without_storage_disk} \
           %{?_without_storage_mpath} \
           %{?_without_numactl} \
           %{?_without_capng} \
           %{?_without_netcf} \
           %{?_without_selinux} \
           %{?_without_hal} \
           --with-qemu-user=%{qemu_user} \
           --with-qemu-group=%{qemu_group} \
           --with-init-script=redhat \
           --with-remote-pid-file=%{_localstatedir}/run/libvirtd.pid
make %{?_smp_mflags}
gzip -9 ChangeLog

%install
rm -fr %{buildroot}

%makeinstall
(cd docs/examples ; make clean ; rm -rf .deps Makefile Makefile.in)
(cd docs/examples/python ; rm -rf .deps Makefile Makefile.in)
(cd examples/hellolibvirt ; make clean ; rm -rf .deps .libs Makefile Makefile.in)
(cd examples/domain-events/events-c ;  make clean ;rm -rf .deps .libs Makefile Makefile.in)
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/python*/site-packages/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/python*/site-packages/*.a

%if %{with_network}
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
%endif
%if ! %{with_qemu}
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/libvirtd_qemu.aug
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/tests/test_libvirtd_qemu.aug
%endif
%find_lang %{name}

%if ! %{with_python}
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libvirt-python-%{version}
%endif

%if %{client_only}
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/libvirt-%{version}
%endif

%if ! %{with_qemu}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu.conf
%endif

%if %{with_libvirtd}
chmod 0644 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/libvirtd
%endif

%clean
rm -fr %{buildroot}

%pre
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
# Normally 'setup' adds this in /etc/passwd, but this is
# here for case of upgrades from earlier Fedora/RHEL. This
# UID/GID pair is reserved for qemu:qemu
getent group kvm >/dev/null || groupadd -g 36 -r kvm
getent group qemu >/dev/null || groupadd -g 107 -r qemu
getent passwd qemu >/dev/null || \
  useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
    -c "qemu user" qemu
%endif

%post

%if %{with_libvirtd}
%if %{with_network}
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
if [ "$1" -ge "1" ]; then
	/sbin/service libvirtd condrestart > /dev/null 2>&1
fi
%endif

%preun
%if %{with_libvirtd}
if [ $1 = 0 ]; then
    /sbin/service libvirtd stop 1>/dev/null 2>&1
    /sbin/chkconfig --del libvirtd
fi
%endif

%post client -p /sbin/ldconfig

%postun client -p /sbin/ldconfig

%if %{with_libvirtd}
%files
%defattr(-, root, root)

%doc AUTHORS ChangeLog.gz NEWS README COPYING.LIB TODO
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/

%if %{with_network}
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/networks/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/networks/autostart
%endif

%{_sysconfdir}/rc.d/init.d/libvirtd
%config(noreplace) %{_sysconfdir}/sysconfig/libvirtd
%config(noreplace) %{_sysconfdir}/libvirt/libvirtd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/qemu/
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/lxc/
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/uml/

%if %{with_qemu}
%config(noreplace) %{_sysconfdir}/libvirt/qemu.conf
%endif

%dir %{_datadir}/libvirt/

%if %{with_network}
%dir %{_datadir}/libvirt/networks/
%{_datadir}/libvirt/networks/default.xml
%endif

%dir %{_localstatedir}/run/libvirt/

%dir %{_localstatedir}/lib/libvirt/
%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/images/
%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/boot/
%dir %attr(0700, root, root) %{_localstatedir}/cache/libvirt/

%if %{with_qemu}
%dir %attr(0700, root, root) %{_localstatedir}/run/libvirt/qemu/
%dir %attr(0700, %{qemu_user}, %{qemu_group}) %{_localstatedir}/lib/libvirt/qemu/
%dir %attr(0700, %{qemu_user}, %{qemu_group}) %{_localstatedir}/cache/libvirt/qemu/
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

%{_datadir}/augeas/lenses/libvirtd.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd.aug

%if %{with_polkit}
%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
%{_datadir}/polkit-1/actions/org.libvirt.unix.policy
%else
%{_datadir}/PolicyKit/policy/org.libvirt.unix.policy
%endif
%endif

%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/

%if %{with_xen_proxy}
%attr(4755, root, root) %{_libexecdir}/libvirt_proxy
%endif

%if %{with_lxc}
%attr(0755, root, root) %{_libexecdir}/libvirt_lxc
%endif

%attr(0755, root, root) %{_libexecdir}/libvirt_parthelper
%attr(0755, root, root) %{_sbindir}/libvirtd

%doc docs/*.xml
%endif

%files client -f %{name}.lang
%defattr(-, root, root)
%doc AUTHORS ChangeLog.gz NEWS README COPYING.LIB TODO

%{_mandir}/man1/virsh.1*
%{_mandir}/man1/virt-xml-validate.1*
%{_bindir}/virsh
%{_bindir}/virt-xml-validate
%{_libdir}/lib*.so.*

%dir %{_datadir}/libvirt/
%dir %{_datadir}/libvirt/schemas/

%{_datadir}/libvirt/schemas/domain.rng
%{_datadir}/libvirt/schemas/network.rng
%{_datadir}/libvirt/schemas/storagepool.rng
%{_datadir}/libvirt/schemas/storagevol.rng
%{_datadir}/libvirt/schemas/nodedev.rng
%{_datadir}/libvirt/schemas/capability.rng
%{_datadir}/libvirt/schemas/interface.rng
%{_datadir}/libvirt/schemas/secret.rng
%{_datadir}/libvirt/schemas/storageencryption.rng

%if %{with_sasl}
%config(noreplace) %{_sysconfdir}/sasl2/libvirt.conf
%endif

%files devel
%defattr(-, root, root)

%{_libdir}/lib*.so
%dir %{_includedir}/libvirt
%{_includedir}/libvirt/*.h
%{_libdir}/pkgconfig/libvirt.pc
%dir %{_datadir}/gtk-doc/html/libvirt/
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
* Thu Jun 17 2010 Cole Robinson <crobinso@redhat.com> - 0.7.1-18.fc12
- Actually apply all previous patches

* Tue Jun 15 2010 Cole Robinson <crobinso@redhat.com> - 0.7.1-17.fc12
- Fix attach-device crash on cgroup cleanup (bz 556791)
- Fix crash on bad LXC URI (bz 554191)
- Add qemu.conf options for audio workaround
- Fix permissions of storage backing stores (bz 579067)
- Fix parsing certain USB sysfs files (bz 598272)
- Improve migration error reporting (bz 499750)
- Sanitize pool target paths (bz 494005)
- Add qemu.conf for clear emulator capabilities
- Prevent libvirtd inside a VM from breaking network access (bz 235961)
- Mention --all in 'virsh list' docs (bz 575512)

* Mon May 17 2010 Cole Robinson <crobinso@redhat.com> - 0.7.1-16.fc12
- Fix crash with invalid QEmu URI (bz 566070)
- Fix VNC TLS crash (bz 544305)
- Fix USB devices with high bus/addr values (bz 542639)
- Fix save/restore with non-root guests (bz 534143, bz 532654)
- Fix USB devices attached via virt-manager (bz 537227)

* Thu Oct 29 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-15
- Avoid compressing small log files (#531030)

* Thu Oct 29 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-14
- Make libvirt-devel require libvirt-client, not libvirt
- Fix xen driver recounting (#531429)
- Fix crash on virsh error (#531429)
- Fix segfault where XML parsing fails in qemu disk hotplug
- Fix segfault where interface target device name is ommitted (#523418)

* Mon Oct 19 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-13
- Misc fixes to qemu machine types handling
- A couple of XML formatting fixes

* Tue Oct 13 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-12
- Fix restore of qemu guest using raw save format (#523158)

* Fri Oct  9 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-11
- Fix libvirtd memory leak during error reply sending (#528162)
- Add several PCI hot-unplug typo fixes from upstream

* Tue Oct  6 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-10
- Create /var/log/libvirt/{lxc,uml} dirs for logrotate
- Make libvirt-python dependon on libvirt-client
- Sync misc minor changes from upstream spec

* Tue Oct  6 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-9
- Change logrotate config to weekly (#526769)

* Thu Oct  1 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-8
- Disable sound backend, even when selinux is disabled (#524499)
- Re-label qcow2 backing files (#497131)

* Wed Sep 30 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-7
- Fix USB device passthrough (#522683)

* Mon Sep 21 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.7.1-6
- rebuild for libssh2 1.2

* Mon Sep 21 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-5
- Don't set a bogus error in virDrvSupportsFeature()
- Fix raw save format

* Thu Sep 17 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-4
- A couple of hot-unplug memory handling fixes (#523953)

* Thu Sep 17 2009 Daniel Veillard <veillard@redhat.com> - 0.7.1-3
- disable numactl on s390[x]

* Thu Sep 17 2009 Daniel Veillard <veillard@redhat.com> - 0.7.1-2
- revamp of spec file for modularity and RHELs

* Tue Sep 15 2009 Daniel Veillard <veillard@redhat.com> - 0.7.1-1
- Upstream release of 0.7.1
- ESX, VBox driver updates
- mutipath support
- support for encrypted (qcow) volume
- compressed save image format for Qemu/KVM
- QEmu host PCI device hotplug support
- configuration of huge pages in guests
- a lot of fixes

* Mon Sep 14 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-0.2.gitfac3f4c
- Update to newer snapshot of 0.7.1
- Stop libvirt using untrusted 'info vcpus' PID data (#520864)
- Support relabelling of USB and PCI devices
- Enable multipath storage support
- Restart libvirtd upon RPM upgrade

* Sun Sep  6 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.1-0.1.gitg3ef2e05
- Update to pre-release git snapshot of 0.7.1
- Drop upstreamed patches

* Wed Aug 19 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.0-6
- Fix migration completion with newer versions of qemu (#516187)

* Wed Aug 19 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.0-5
- Add PCI host device hotplug support
- Allow PCI bus reset to reset other devices (#499678)
- Fix stupid PCI reset error message (bug #499678)
- Allow PM reset on multi-function PCI devices (bug #515689)
- Re-attach PCI host devices after guest shuts down (bug #499561)
- Fix list corruption after disk hot-unplug
- Fix minor 'virsh nodedev-list --tree' annoyance

* Thu Aug 13 2009 Daniel P. Berrange <berrange@redhat.com> - 0.7.0-4
- Rewrite policykit support (rhbz #499970)
- Log and ignore NUMA topology problems (rhbz #506590)

* Mon Aug 10 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.0-3
- Don't fail to start network if ipv6 modules is not loaded (#516497)

* Thu Aug  6 2009 Mark McLoughlin <markmc@redhat.com> - 0.7.0-2
- Make sure qemu can access kernel/initrd (bug #516034)
- Set perms on /var/lib/libvirt/boot to 0711 (bug #516034)

* Wed Aug  5 2009 Daniel Veillard <veillard@redhat.com> - 0.7.0-1
- ESX, VBox3, Power Hypervisor drivers
- new net filesystem glusterfs
- Storage cloning for LVM and Disk backends
- interface implementation based on netcf
- Support cgroups in QEMU driver
- QEmu hotplug NIC support
- a lot of fixes

* Fri Jul  3 2009 Daniel Veillard <veillard@redhat.com> - 0.6.5-1
- release of 0.6.5

* Fri May 29 2009 Daniel Veillard <veillard@redhat.com> - 0.6.4-1
- release of 0.6.4
- various new APIs

* Fri Apr 24 2009 Daniel Veillard <veillard@redhat.com> - 0.6.3-1
- release of 0.6.3
- VirtualBox driver

* Fri Apr  3 2009 Daniel Veillard <veillard@redhat.com> - 0.6.2-1
- release of 0.6.2

* Fri Mar  4 2009 Daniel Veillard <veillard@redhat.com> - 0.6.1-1
- release of 0.6.1

* Sat Jan 31 2009 Daniel Veillard <veillard@redhat.com> - 0.6.0-1
- release of 0.6.0

* Tue Nov 25 2008 Daniel Veillard <veillard@redhat.com> - 0.5.0-1
- release of 0.5.0

* Tue Sep 23 2008 Daniel Veillard <veillard@redhat.com> - 0.4.6-1
- release of 0.4.6

* Mon Sep  8 2008 Daniel Veillard <veillard@redhat.com> - 0.4.5-1
- release of 0.4.5

* Wed Jun 25 2008 Daniel Veillard <veillard@redhat.com> - 0.4.4-1
- release of 0.4.4
- mostly a few bug fixes from 0.4.3

* Thu Jun 12 2008 Daniel Veillard <veillard@redhat.com> - 0.4.3-1
- release of 0.4.3
- lots of bug fixes and small improvements

* Tue Apr  8 2008 Daniel Veillard <veillard@redhat.com> - 0.4.2-1
- release of 0.4.2
- lots of bug fixes and small improvements

* Mon Mar  3 2008 Daniel Veillard <veillard@redhat.com> - 0.4.1-1
- Release of 0.4.1
- Storage APIs
- xenner support
- lots of assorted improvements, bugfixes and cleanups
- documentation and localization improvements

* Tue Dec 18 2007 Daniel Veillard <veillard@redhat.com> - 0.4.0-1
- Release of 0.4.0
- SASL based authentication
- PolicyKit authentication
- improved NUMA and statistics support
- lots of assorted improvements, bugfixes and cleanups
- documentation and localization improvements

* Sun Sep 30 2007 Daniel Veillard <veillard@redhat.com> - 0.3.3-1
- Release of 0.3.3
- Avahi support
- NUMA support
- lots of assorted improvements, bugfixes and cleanups
- documentation and localization improvements

* Tue Aug 21 2007 Daniel Veillard <veillard@redhat.com> - 0.3.2-1
- Release of 0.3.2
- API for domains migration
- APIs for collecting statistics on disks and interfaces
- lots of assorted bugfixes and cleanups
- documentation and localization improvements

* Tue Jul 24 2007 Daniel Veillard <veillard@redhat.com> - 0.3.1-1
- Release of 0.3.1
- localtime clock support
- PS/2 and USB input devices
- lots of assorted bugfixes and cleanups
- documentation and localization improvements

* Mon Jul  9 2007 Daniel Veillard <veillard@redhat.com> - 0.3.0-1
- Release of 0.3.0
- Secure remote access support
- unification of daemons
- lots of assorted bugfixes and cleanups
- documentation and localization improvements

* Fri Jun  8 2007 Daniel Veillard <veillard@redhat.com> - 0.2.3-1
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
