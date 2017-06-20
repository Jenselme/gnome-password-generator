#!/usr/bin/python

####
# Copyright (c) 2017 Julien Enslme
# Copyright (c) 2004-2008 Chris Ladd
# Copyright (c) 2007 Steve Tyler
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
####

import sys
import random
import gtk
import pango
import gnome
import gnome.ui

VERSION = "1.6"
PYTHON_VERSION = (2, 4)
PYGTK_VERSION = (2, 4)

PIXMAPDIR = "/usr/share/pixmaps"

PW_LEN_MIN = 1
PW_LEN_MAX = 256
PW_LEN_DEFAULT = 12


class CharacterSet:
    def __init__(self, description, characters):
        self.description = description
        self.characters = characters

    def __len__(self):
        return len(self.characters)

    def __getitem__(self, index):
        return self.characters[index]


def generate_password(password_length, password_count, character_set):
    random_number_generator = get_random_numbers_generator()

    for current_password in range(password_count):
        password = ""
        for current_character in range(password_length):
            random_number = random_number_generator.randint(
                0,
                len(character_set) - 1
            )
            password += character_set[random_number]

    return password


def get_random_numbers_generator():
    try:
        return random.SystemRandom()
    except NotImplementedError:
        return random.Random()


class Application(gnome.ui.App):
    def DeleteCallback(self, widget, event, data=None):
        return False

    def DestroyCallback(self, widget, data=None):
        gtk.main_quit()

    def ClickedCallback(self, widget, data=None):
        # Clear the textview
        buffer = self.textview.get_buffer()
        buffer.delete(buffer.get_start_iter(), buffer.get_end_iter())

        # Generate the passwords
        password = generate_password(
            self.length_spin_button.get_value_as_int(),
            self.count_spin_button.get_value_as_int(),
            self.character_sets[self.char_set_combo_box.get_active()].characters
        )
        self.PrintMessage(password+"\n")

    def AboutCallback(self, widget, data=None):
        gnome.ui.About(
            "Gnome Password Generator",
            VERSION,
            "Copyright 2008 Chris Ladd",
            "Secure Password Generator",
            ["Chris Ladd <caladd@particlestorm.net>"],
            None,
            None,
            self.image.get_pixbuf()
        ).show()

    def PrintMessage(self, message):
        # Add the text at the end
        buffer = self.textview.get_buffer()
        iter = buffer.get_end_iter()
        buffer.insert(iter, message)
        self.textview.scroll_to_iter(iter, 0.0, False, 0.0, 0.0)

        # Do any needed events
        while gtk.events_pending():
            gtk.main_iteration_do(False)

    def __init__(self):
        self.character_sets = (
            CharacterSet(
                "All printable (excluding space)",
                "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                "[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
            ),
            CharacterSet(
                "Alpha-numeric (a-z, A-Z, 0-9)",
                "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                "abcdefghijklmnopqrstuvwxyz"
            ),
            CharacterSet(
                "Alpha lower-case (a-z)",
                "abcdefghijklmnopqrstuvwxyz"
            ),
            CharacterSet(
                "Hexadecimal (0-9, A-F)",
                "0123456789ABCDEF"
            ),
            CharacterSet(
                "Decimal (0-9)",
                "0123456789"
            ),
            CharacterSet(
                "Base 64 (a-z, A-Z, 0-9, '+', '/')",
                "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                "abcdefghijklmnopqrstuvwxyz+/"
            )
        )

        # Setup the application
        gnome.ui.App.__init__(
            self,
            "Gnome Password Generator",
            "Gnome Password Generator"
        )

        # Setup the main window
        self.image = gtk.Image()
        self.image.set_from_file(PIXMAPDIR + "/gnome-password-generator.png")

        self.set_icon(self.image.get_pixbuf())

        self.connect("delete_event", self.DeleteCallback)
        self.connect("destroy", self.DestroyCallback)

        vbox = gtk.VBox(False, 0)

        # Setup the main menubar
        ui = '''<ui>
          <menubar name="MenuBar">
            <menu action="File">
              <menuitem action="Quit"/>
            </menu>
            <menu action="Help">
              <menuitem action="About"/>
            </menu>
          </menubar>
        </ui>'''

        action_group = gtk.ActionGroup("Gnome Password Generator")
        action_group.add_actions([
            ("File", None, "_File"),
            ("Quit", gtk.STOCK_QUIT, None, None, None, self.DestroyCallback),
            ("Help", None, "_Help"),
            ("About", gtk.STOCK_ABOUT, None, None, None, self.AboutCallback)
        ])

        uimanager = gtk.UIManager()
        uimanager.insert_action_group(action_group, 0)
        uimanager.add_ui_from_string(ui)

        accel_group = uimanager.get_accel_group()
        self.add_accel_group(accel_group)

        self.set_menus(uimanager.get_widget('/MenuBar'))

        # Setup the layout controls
        inner_vbox = gtk.VBox(False, 0)

        hbox_top = gtk.HBox(False, 0)
        top_vbox = gtk.VBox(False, 0)
        top_frame = gtk.Frame()

        top_vbox.pack_start(hbox_top, True, True, 6)
        top_frame.add(top_vbox)
        hbox = gtk.HBox(False, 0)
        hbox.pack_start(top_frame, True, True, 4)
        inner_vbox.pack_start(hbox, False, False, 6)

        hbox_bottom = gtk.HBox(False, 0)
        bottom_vbox = gtk.VBox(False, 0)

        bottom_vbox.pack_start(hbox_bottom, True, True, 6)
        inner_vbox.pack_start(bottom_vbox, True, True, 0)

        vbox.pack_start(inner_vbox, True, True, 0)

        # Setup the length label
        length_hbox = gtk.HBox(False, 0)
        self.length_label = gtk.Label("Length:")
        length_hbox.pack_start(self.length_label, False, False, 0)

        # Setup the length spin button
        adjustment = gtk.Adjustment(
            PW_LEN_DEFAULT,
            PW_LEN_MIN,
            PW_LEN_MAX,
            1,
            1,
            0
        )
        self.length_spin_button = gtk.SpinButton(adjustment, 0, 0)
        length_hbox.pack_start(self.length_spin_button, False, False, 6)
        hbox_top.pack_start(length_hbox, False, False, 6)

        # Setup the count label
        count_hbox = gtk.HBox(False, 0)
        self.count_label = gtk.Label("Count:")
        count_hbox.pack_start(self.count_label, False, False, 0)

        # Setup the count spin button
        adjustment = gtk.Adjustment(1, 1, 100, 1, 1, 0)
        self.count_spin_button = gtk.SpinButton(adjustment, 0, 0)
        count_hbox.pack_start(self.count_spin_button, False, False, 6)
        hbox_top.pack_start(count_hbox, False, False, 20)

        # Setup the character set label
        char_set_hbox = gtk.HBox(False, 0)
        self.char_set_label = gtk.Label("Character Set:")
        char_set_hbox.pack_start(self.char_set_label, False, False, 0)

        # Setup the character set combo box
        self.char_set_combo_box = gtk.combo_box_new_text()
        for character_set in self.character_sets:
            self.char_set_combo_box.append_text(character_set.description)
        self.char_set_combo_box.set_active(1)
        char_set_hbox.pack_start(self.char_set_combo_box, False, False, 6)
        hbox_top.pack_start(char_set_hbox, False, False, 20)

        # Setup the start button
        self.button = gtk.Button("", gtk.STOCK_EXECUTE)
        self.button.connect("clicked", self.ClickedCallback)
        hbox_top.pack_end(self.button, False, False, 6)

        # Setup the status window
        self.scrolledwindow = gtk.ScrolledWindow()
        self.scrolledwindow.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_ALWAYS)
        self.scrolledwindow.set_shadow_type(gtk.SHADOW_IN)
        self.textview = gtk.TextView()
        self.textview.set_editable(False)
        self.textview.modify_font(pango.FontDescription("Monospace 12"))
        self.textview.set_left_margin(10)
        self.scrolledwindow.add(self.textview)
        hbox_bottom.pack_start(self.scrolledwindow, True, True, 4)

        # Show everything
        self.set_contents(vbox)
        self.set_default_size(750, 500)
        self.set_focus(self.button)
        self.show_all()


def Main():
    program = gnome.init("gnome-password-generator", VERSION)  # noqa

    # Check to make sure the right versions of Python and PyGTK are installed
    message = None
    if sys.version_info < PYTHON_VERSION:
        message = (
            "You appear to be running Python version %i.%i.%i, but this "
            "program requires version %i.%i or greater.\n\n"
            "Please upgrade to a newer version."
        ) % (sys.version_info[0:3] + PYTHON_VERSION)
    elif gtk.pygtk_version < PYGTK_VERSION:
        message = (
            "You appear to be running PyGTK version %i.%i.%i, "
            "but this program requires version %i.%i or greater.\n\n"
            "Please upgrade to a newer version."
        ) % (gtk.pygtk_version + PYGTK_VERSION)

    if message is not None:
        dialog = gtk.MessageDialog(
            None,
            0,
            gtk.MESSAGE_ERROR,
            gtk.BUTTONS_CLOSE,
            message
        )
        dialog.run()
    else:
        application = Application()  # noqa

        gtk.main()

# Start the program
if __name__ == "__main__":
    Main()
