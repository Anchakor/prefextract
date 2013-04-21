INSTALL = install
INSTALL_PROGRAM = $(INSTALL) -p -m 755 -D
INSTALL_DATA = $(INSTALL) -p -m 644 -D
INSTALL_DIR = $(INSTALL) -p -m 755 -d

PREFIX=/usr
CONFIGDIR=/etc
APPDIR=$(PREFIX)/share/webapps
SYSTEMDDIR=$(PREFIX)/lib/systemd/system
TTRSSDIR=$(APPDIR)/tt-rss/plugins

PYTHON2EXEC=/usr/bin/env python2

all:
	@echo 'Use `make DESTDIR= install` to install to default location'

install:
	sed -e "s*PYTHON2EXEC*$(PYTHON2EXEC)*g;s*APPDIR*$(DESTDIR)$(APPDIR)*g;s*CONFIGDIR*$(DESTDIR)$(CONFIGDIR)*g" prefextract.service.in > prefextract.service
	$(INSTALL_DATA) prefextract.service $(DESTDIR)$(SYSTEMDDIR)/prefextract.service
	$(INSTALL_DATA) tt-rss-plugin/init.php $(DESTDIR)$(TTRSSDIR)/learnfilter/init.php
	$(INSTALL_DATA) tt-rss-plugin/learnfilter.js $(DESTDIR)$(TTRSSDIR)/learnfilter/learnfilter.js
	#$(INSTALL)
	#$(INSTALL_PROGRAM) foo $(bindir)/foo
	#$(INSTALL_DATA) libfoo.a $(libdir)/libfoo.a

uninstall:
	rm $(DESTDIR)$(SYSTEMDDIR)/prefextract.service
	rm $(DESTDIR)$(TTRSSDIR)/learnfilter/init.php
	rm $(DESTDIR)$(TTRSSDIR)/learnfilter/learnfilter.js
