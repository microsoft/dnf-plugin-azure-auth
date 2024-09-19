VERSION?=0.1.0
DIST=$(shell rpm --eval %{dist})


rpmbuild/.rpmsetuptree:
	mkdir -p rpmbuild/BUILD rpmbuild/SOURCES rpmbuild/RPMS rpmbuild/SRPMS rpmbuild/SPECS
	touch rpmbuild/.rpmsetuptree

rpmbuild/SOURCES/dnf-plugin-azure-auth-$(VERSION).tar.gz: rpmbuild/.rpmsetuptree azure_auth.conf azure_auth.py
	tar czf dnf-plugin-azure-auth-$(VERSION).tar.gz --xform "s+^+dnf-plugin-azure-auth-$(VERSION)/+" azure_auth.conf azure_auth.py
	mv dnf-plugin-azure-auth-$(VERSION).tar.gz rpmbuild/SOURCES/

rpmbuild/SPECS/dnf-plugin-azure-auth.spec: dnf-plugin-azure-auth.spec rpmbuild/.rpmsetuptree
	cp dnf-plugin-azure-auth.spec rpmbuild/SPECS/
	sed -i "s/%%version%%/$(VERSION)/" rpmbuild/SPECS/dnf-plugin-azure-auth.spec

rpmbuild/RPMS/x86_64/dnf-plugin-azure-auth-$(VERSION)-1$(DIST).x86_64.rpm: rpmbuild/SPECS/dnf-plugin-azure-auth.spec rpmbuild/SOURCES/dnf-plugin-azure-auth-$(VERSION).tar.gz
	rpmbuild -D "_topdir $(shell pwd)/rpmbuild" -ba rpmbuild/SPECS/dnf-plugin-azure-auth.spec

rpm: rpmbuild/RPMS/x86_64/dnf-plugin-azure-auth-$(VERSION)-1$(DIST).x86_64.rpm
