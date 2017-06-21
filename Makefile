prefix=/usr
bindir=$(prefix)/bin
datadir=$(prefix)/share

PIXMAPDIR=$(datadir)/pixmaps
DESKTOPDIR=$(datadir)/applications

DESTDIR=

INSTALL=install

all:
	cp gnome-password-generator.py gnome-password-generator
	sed -Ei 's|/usr/share/pixmaps|$(PIXMAPDIR)|' gnome-password-generator

install:
	$(INSTALL) -d -m0755 $(DESTDIR)$(bindir)
	$(INSTALL) -m0755 gnome-password-generator $(DESTDIR)$(bindir)
	$(INSTALL) -d -m0755 $(DESTDIR)$(PIXMAPDIR)
	$(INSTALL) -m0644 gnome-password-generator.png $(DESTDIR)$(PIXMAPDIR)
	$(INSTALL) -d -m0755 $(DESTDIR)$(DESKTOPDIR)
	$(INSTALL) -m0644 gnome-password-generator.desktop $(DESTDIR)$(DESKTOPDIR)

clean:
	rm gnome-password-generator

lint:
	flake8 *.py
