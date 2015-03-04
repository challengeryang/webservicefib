#######################################################################
# Copyright (C) 2015 by Bo Yang
#######################################################################

MKDIR=mkdir
INSTALL=install
CP=cp
RM=rm
RPMBUILD=rpmbuild
RPM_NAME=webservicefib
VERSION=1.1
RELEASE=2
PLATFORM=x86_64

all: clean utest rpm

utest:
	@if [ -e test/ws_fib_unittest.py ]; then \
		python test/ws_fib_unittest.py; \
	fi \

rpm: ${RPM_NAME}-${VERSION}-${RELEASE}.${PLATFORM}.rpm

${RPM_NAME}-${VERSION}-${RELEASE}.${PLATFORM}.rpm:
	${MKDIR} -p rpmbuild/{SOURCES,RPMS,BUILD,tmp}; \
	${INSTALL} -m 755 -d rpmbuild/BUILD/etc/init.d/; \
	${INSTALL} -m 755 -d rpmbuild/BUILD/var/webservice/; \
	${INSTALL} -m 755 -d rpmbuild/BUILD/etc/logrotate.d/; \
	${CP} -f webservice_fib rpmbuild/BUILD/etc/init.d; \
	${CP} -f httpserverthread.py rpmbuild/BUILD/var/webservice; \
	${CP} -f fib.py rpmbuild/BUILD/var/webservice; \
	${CP} -f daemon.py rpmbuild/BUILD/var/webservice; \
	${CP} -f webservice_fib.lr rpmbuild/BUILD/etc/logrotate.d/; \
	${RPMBUILD} -bb webservice.spec; \
	${INSTALL} -m 644 -D rpmbuild/RPMS/${PLATFORM}/${RPM_NAME}-${VERSION}-${RELEASE}.${PLATFORM}.rpm ${RPM_NAME}-${VERSION}-${RELEASE}.${PLATFORM}.rpm; \


clean:
	-${RM} -rf rpmbuild
	-${RM} -rf *.rpm

