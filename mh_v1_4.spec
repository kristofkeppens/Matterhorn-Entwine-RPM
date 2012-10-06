%define 	_prefix /opt/matterhorn
%define 	_data_prefix /var/matterhorn
%define 	__jar_repack 0

Name:		entwine-matterhorn	
Version:	1.4
Release:	1%{?dist}
Summary:	Entwine version of Matterhorn
#Group
License:	ECL 2.0	
URL:		http://entwinemedia.com	
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}
Source:		matterhorn-1.4.tar.gz

#BuildRequires:	
Requires: 	java-1.6.0-openjdk	

%description
This is entwine version of Matterhorn

%prep
%setup -n matterhorn-1.4

%build

%pre
getent group mh >/dev/null || groupadd mh
getent passwd mh >/dev/null || useradd -d /opt/matterhorn -m -g mh mh -r -s /bin/false -c "Matterhorn System User"

%install
rm -rf %{buildroot}
install -d -m 755 $RPM_BUILD_ROOT/%{_prefix}
install -d -m 755 $RPM_BUILD_ROOT/%{_initrddir}
install -d -m 755 $RPM_BUILD_ROOT/etc
install -d -m 755 $RPM_BUILD_ROOT/var/cache/matterhorn
install -d -m 755 $RPM_BUILD_ROOT/var/tmp/matterhorn
install -d -m 755 $RPM_BUILD_ROOT/%{_data_prefix}/distribution/downloads
install -d -m 755 $RPM_BUILD_ROOT/%{_data_prefix}/distribution/streams
install -d -m 755 $RPM_BUILD_ROOT/%{_data_prefix}/archive
install -d -m 755 $RPM_BUILD_ROOT/%{_data_prefix}/work/inbox
install -d -m 755 $RPM_BUILD_ROOT/%{_data_prefix}/work/local
install -d -m 755 $RPM_BUILD_ROOT/%{_data_prefix}/work/shared/workspace
install -d -m 755 $RPM_BUILD_ROOT/%{_data_prefix}/work/shared/files
install -d -m 755 $RPM_BUILD_ROOT/var/log/matterhorn

install -D -m 755 bin/felix.jar $RPM_BUILD_ROOT/%{_prefix}/bin/felix.jar
cp -rf  all-jars/lib $RPM_BUILD_ROOT/%{_prefix}

install -D -m 755 bin/matterhorn $RPM_BUILD_ROOT/%{_prefix}/bin/matterhorn
install -D -m 755 docs/scripts/init/matterhorn_init_d.sh \
                  $RPM_BUILD_ROOT/%{_prefix}/bin/matterhorn_init_d.sh
ln -s 	/opt/matterhorn/bin/matterhorn_init_d.sh \
	${RPM_BUILD_ROOT}%{_initrddir}/matterhorn

cp -rf etc $RPM_BUILD_ROOT/%{_prefix}
ln -s /opt/matterhorn/etc ${RPM_BUILD_ROOT}/etc/matterhorn

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
/opt/matterhorn/
/etc/matterhorn
%{_initrddir}

%attr(0755,mh,mh) /var/cache/matterhorn
%attr(0755,mh,mh) /var/tmp/matterhorn
%attr(0755,mh,mh) /var/log/matterhorn
%attr(0755,mh,mh) /var/matterhorn
#system config files
%config(noreplace) /opt/matterhorn/bin/matterhorn
%config(noreplace) /opt/matterhorn/bin/matterhorn_init_d.sh
%config(noreplace) /opt/matterhorn/etc/matterhorn.conf
%config(noreplace) /opt/matterhorn/etc/services/org.ops4j.pax.logging.properties

#MH config files
%config(noreplace) /opt/matterhorn/etc/config.properties
%config(noreplace) /opt/matterhorn/etc/load/org.apache.felix.fileinstall-dictionary.cfg
%config(noreplace) /opt/matterhorn/etc/load/org.apache.felix.fileinstall-encoding.cfg
%config(noreplace) /opt/matterhorn/etc/load/org.apache.felix.fileinstall-feeds.cfg
%config(noreplace) /opt/matterhorn/etc/load/org.apache.felix.fileinstall-security.cfg
%config(noreplace) /opt/matterhorn/etc/load/org.apache.felix.fileinstall-workflows.cfg
%config(noreplace) /opt/matterhorn/etc/load/org.opencastproject.ingest.scanner.InboxScannerService-inbox.cfg
%config(noreplace) /opt/matterhorn/etc/load/org.opencastproject.organization-mh_default_org.cfg
%config(noreplace) /opt/matterhorn/etc/services/org.opencastproject.capture.impl.ConfigurationManager.properties

%config(noreplace) /opt/matterhorn/etc/profiles/admin.properties

%post
chkconfig --add matterhorn


#Uninstall
%postun
service matterhorn stop
userdel -r mh
chkconfig --del matterhorn
rm -rf /etc/init.d/matterhorn
rm -rf /var/cache/matterhorn
rm -rf /var/tmp/matterhorn
rm -rf /var/matterhorn/
rm /etc/matterhorn


%changelog
* Sep 20 2012 Jaime Gago <jaime@entwinemedia.com>
-Version 1

