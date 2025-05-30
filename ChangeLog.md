# Changelog

## 2025-03-30 Julien Enselme <jujens@jujens.eu> - 2.2.3
- Correct the all printable characters set.

## 2025-03-06 Julien Enselme <jujens@jujens.eu> - 2.2.2
- Correct loading of icon

## 2025-03-06 Julien Enselme <jujens@jujens.eu> - 2.2.1
- Bump version number
- Display version in about dialog

## 2025-03-06 Julien Enselme <jujens@jujens.eu> - 2.2.0
- add a new character set modeled after 1Password's "Smart Password" here: https://blog.1password.com/a-smarter-password-generator/ Contribution by @allenatdecisiv
- fix Python Gtk deprecation warnings I was getting when running from bash prompt Contribution by @allenatdecisiv
- use raw strings where it seemed appropriate Contribution by @allenatdecisiv
- Bump default password length to 16


## 2017-07-29 Julien Enselme <jujens@jujens.eu> - 2.1.0

- Can save options used to generate a password

## 2017-07-05 Julien Enselme <jujens@jujens.eu> - v2.0.3

- Remove NEWS file
- Update ChangeLog

## 2017-07-05 Julien Enselme <jujens@jujens.eu> - v2.0.2

- Improve Makefile

## 2017-07-02 Julien Enselme <jujens@jujens.eu> - v2.0.1

- Add .appdata file

## 2017-06-21 Julien Enselme <jujens@jujens.eu> - v2.0.0

- Works on Python 3 and GTK3 instead of Python 2 and GTK2
- Add a copy to cilpboard button

## 03-17-2008 Chris Ladd <caladd@particlestorm.net>

* Makefile:
  Changed build process to remove the extension on gnome-password-generator.py

* gnome-password-generator.py:
  Rewrote the menu code to use the new UIManager API in gtk [Bug 1885591]. Added file extension.

## 08-12-2007 Chris Ladd <caladd@particlestorm.net>

* gnome-password-generator:
  Added new character set selection feature. Added check
  for the minimum PyGTK and Python versions. Replaced
  deprecated gtk.TRUE and gtk.FALSE with True and False.
  Added ability to use urandom for random number generation
  if available.

## 06-07-2004 Chris Ladd <caladd@particlestorm.net>

* Makefile:
  Changed it to install the png instead of an svg.

* gnome-password-generator:
  Changed it to use gnome-password-generator.png as the image.

* gnome-password-generator.desktop:
  Changed it to use gnome-password-generator.png as the image.

## 04-05-2004 Chris Ladd <caladd@particlestorm.net>

* Makefile:
  Added a make all command to the build system. This step
  correctly specifies the pixmap directory.

## 04-05-2004 Chris Ladd <caladd@particlestorm.net>

* Makefile:
  Changed the install system to use make install.

* install.sh:
  Removed it.

* gnome-password-generator:
  Added a PIXMAPDIR variable to get overwritten with the
  correct directory location by the Makefile.

* gnome-password-generator.desktop:
  Cleanups to the Comment field.

## 03-15-2004 Chris Ladd <caladd@particlestorm.net>

* gnome-password-generator:
  Added a check at the beginning of the program for the
  proper version of PyGTK. If an older than needed version
  is found a error dialog is displayed.
