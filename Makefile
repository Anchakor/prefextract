INSTALL = install
INSTALL_PROGRAM = $(INSTALL) -p -m 755 -D
INSTALL_DATA = $(INSTALL) -p -m 644 -D
INSTALL_DIR = $(INSTALL) -p -m 755 -d

PREFIX=/usr
CONFIGDIR=/etc
APPDIR=$(PREFIX)/share/webapps
SYSTEMDDIR=$(PREFIX)/lib/systemd/system
TTRSSDIR=$(APPDIR)/tt-rss/plugins
DATADIR=/var/lib/prefextract

PYTHON2EXEC=/usr/bin/env python2
SCRIPTS=main.py user.py config.py termextract.py tag.py

all:
	@echo 'Use `make DESTDIR= install` to install to default location'

install:
	sed -e "s*PYTHON2EXEC*$(PYTHON2EXEC)*g;s*APPDIR*$(DESTDIR)$(APPDIR)*g;s*CONFIGDIR*$(DESTDIR)$(CONFIGDIR)*g" prefextract.service.in > prefextract.service
	sed -e "s*DATADIR*$(DESTDIR)$(DATADIR)*g" prefextract.conf.in > prefextract.conf
	for script in $(SCRIPTS); do \
		$(INSTALL_DATA) $$script $(DESTDIR)$(APPDIR)/prefextract/$$script || exit 1; \
	done
	$(INSTALL_DATA) prefextract.conf $(DESTDIR)$(CONFIGDIR)/prefextract.conf
	$(INSTALL_DATA) prefextract.service $(DESTDIR)$(SYSTEMDDIR)/prefextract.service
	$(INSTALL_DATA) tt-rss-plugin/init.php $(DESTDIR)$(TTRSSDIR)/learnfilter/init.php
	$(INSTALL_DATA) tt-rss-plugin/learnfilter.js $(DESTDIR)$(TTRSSDIR)/learnfilter/learnfilter.js

uninstall:
	rm -r $(DESTDIR)$(APPDIR)/prefextract
	rm $(DESTDIR)$(CONFIGDIR)/prefextract.conf
	rm $(DESTDIR)$(SYSTEMDDIR)/prefextract.service
	rm -r $(DESTDIR)$(TTRSSDIR)/learnfilter
