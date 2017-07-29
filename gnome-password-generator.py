#!/usr/bin/python3

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
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
####

import gi
import os.path
import sys
import random

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk  # noqa
from gi.repository import Gdk  # noqa
from gi.repository import GdkPixbuf  # noqa
from gi.repository import Gio  # noqa
from gi.repository import GLib  # noqa


VERSION = '2.0'
PYTHON_VERSION = (3, 4)

NAME = 'Gnome Password Generator'
COPYRIGHT = '''Copyright (c) 2004-2008 Chris Ladd
Copyright (c) 2017 Julien Enselme
'''
AUTHORS = [
    'Chris Ladd',
    'Steve Tyler',
    'Julien Enselme <jujens@jujens.eu>',
]
WEBSITE = 'https://github.com/Jenselme/gnome-password-generator'

PIXMAPDIR = '/usr/share/pixmaps'
ICON_FILE = os.path.join(PIXMAPDIR, 'gnome-password-generator.png')

PW_LEN_MIN = 1
PW_LEN_MAX = 256
PW_LEN_DEFAULT = 12
PW_STEP_INCREMENT = 1
PW_PAGE_INCREMENT = 1
PW_PAGE_SIZE = 0


class CharacterSet:
    def __init__(self, description, characters):
        self.description = description
        self.characters = characters

    def __len__(self):
        return len(self.characters)

    def __getitem__(self, index):
        return self.characters[index]


def generate_passwords(password_length, password_count, character_set):
    passwords = []

    for _ in range(password_count):
        passwords.append(generate_password(password_length, character_set))

    return passwords


def generate_password(password_length, character_set):
    random_number_generator = get_random_numbers_generator()

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


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.Window.__init__(
            self,
            title=NAME,
            application=app
        )
        self.app = app
        self.set_default_size(750, 500)
        self.set_icon(self.app.image)

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        grid = Gtk.Grid()
        grid.set_row_spacing(20)
        grid.props.margin_top = 5
        grid.props.margin_bottom = 5

        option_hbox = self.create_option_hbox()
        option_hbox.set_hexpand(True)
        option_hbox.show()
        grid.attach(option_hbox, 0, 0, 1, 1)

        result_view = self.create_result_view()
        result_view.set_hexpand(True)
        result_view.show()
        grid.attach(result_view, 0, 1, 1, 1)

        self.add(grid)
        self.load_config()

    def create_option_hbox(self):
        hbox = Gtk.HBox()
        hbox.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)

        # Setup label
        length_hbox = Gtk.HBox(False, 0)
        self.length_label = Gtk.Label("Length:")
        length_hbox.pack_start(self.length_label, False, False, 0)

        # Setup the length spin button
        adjustment = Gtk.Adjustment(
            PW_LEN_DEFAULT,
            PW_LEN_MIN,
            PW_LEN_MAX,
            PW_STEP_INCREMENT,
            PW_PAGE_INCREMENT,
            PW_PAGE_SIZE
        )
        self.length_spin_button = Gtk.SpinButton()
        self.length_spin_button.set_adjustment(adjustment)
        self.length_spin_button.set_value(PW_LEN_DEFAULT)
        length_hbox.pack_start(self.length_spin_button, False, False, 6)
        hbox.pack_start(length_hbox, False, False, 6)

        # Setup the count label
        count_hbox = Gtk.HBox(False, 0)
        self.count_label = Gtk.Label("Count:")
        count_hbox.pack_start(self.count_label, False, False, 0)

        # Setup the count spin button
        adjustment = Gtk.Adjustment(1, 1, 100, 1, 1, 0)
        self.count_spin_button = Gtk.SpinButton()
        self.count_spin_button.set_adjustment(adjustment)
        self.count_spin_button.set_value(1)
        count_hbox.pack_start(self.count_spin_button, False, False, 6)
        hbox.pack_start(count_hbox, False, False, 20)

        # Setup the character set label
        char_set_hbox = Gtk.HBox(False, 0)
        self.char_set_label = Gtk.Label("Character Set:")
        char_set_hbox.pack_start(self.char_set_label, False, False, 0)

        # Setup the character set combo box
        char_set_list = Gtk.ListStore(str)
        for character_set in self.app.character_sets:
            char_set_list.append([character_set.description])
        self.char_set_combo_box = Gtk.ComboBox(model=char_set_list)
        cell = Gtk.CellRendererText()
        self.char_set_combo_box.pack_start(cell, False)
        self.char_set_combo_box.add_attribute(cell, 'text', 0)
        self.char_set_combo_box.set_active(1)
        char_set_hbox.pack_start(self.char_set_combo_box, False, False, 6)
        hbox.pack_start(char_set_hbox, False, False, 20)

        # Setup the save config button
        self.save_config_button = Gtk.Button.new_from_stock(Gtk.STOCK_SAVE)
        self.save_config_button.connect('clicked', self.on_save_config_clicked)
        self.save_config_button.set_tooltip_text('Save options for future use')
        hbox.pack_start(self.save_config_button, False, False, 6)

        # Setup the start button
        self.start_button = Gtk.Button.new_from_stock(Gtk.STOCK_EXECUTE)
        self.start_button.connect("clicked", self.on_execute_clicked)
        hbox.pack_start(self.start_button, False, False, 6)

        # Setup the copy button
        self.copy_button = Gtk.Button.new_from_stock(Gtk.STOCK_COPY)
        self.copy_button.connect('clicked', self.on_copy_clicked)
        self.copy_button.set_sensitive(False)
        hbox.pack_start(self.copy_button, False, False, 6)

        return hbox

    def create_result_view(self):
        hbox = Gtk.HBox()
        hbox.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)

        # Setup the status window
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(
            Gtk.PolicyType.AUTOMATIC,
            Gtk.PolicyType.AUTOMATIC
        )
        self.scrolled_window.set_vexpand(True)

        self.passwords_text_buffer = Gtk.TextBuffer()
        self.text_view = Gtk.TextView(buffer=self.passwords_text_buffer)
        self.text_view.set_editable(False)
        self.text_view.set_wrap_mode(Gtk.WrapMode.NONE)
        self.text_view.set_left_margin(10)
        self.text_view.set_top_margin(5)
        self.text_view.set_right_margin(10)
        self.text_view.set_bottom_margin(5)

        self.scrolled_window.add(self.text_view)
        hbox.pack_start(self.scrolled_window, True, True, 4)

        return hbox

    def on_execute_clicked(self, execute_button):
        passwords = generate_passwords(
            self.passwd_length,
            self.passwd_count,
            self.selected_character_set
        )
        self.passwords_text_buffer.set_text('\n'.join(passwords))
        self.copy_button.set_sensitive(True)

    def on_copy_clicked(self, copy_button):
        passwords = self.passwords_text_buffer.get_text(
            self.passwords_text_buffer.get_start_iter(),
            self.passwords_text_buffer.get_end_iter(),
            False
        )
        self.clipboard.set_text(passwords, -1)

    def on_save_config_clicked(self, save_config_button):
        self.save_config()

    def save_config(self):
        key_file = GLib.KeyFile.new()
        key_file.set_value('generate', 'length', str(self.passwd_length))
        key_file.set_value('generate', 'count', str(self.passwd_count))
        key_file.set_value(
            'generate',
            'character_set',
            str(self.char_set_combo_box.get_active())
        )
        key_file.save_to_file(self.app.CONFIG_FILE)

    def load_config(self):
        if os.path.exists(self.app.CONFIG_FILE):
            key_file = GLib.KeyFile.new()
            key_file.load_from_file(self.app.CONFIG_FILE, GLib.KeyFileFlags.NONE)
            self.passwd_length = key_file.get_value('generate', 'length')
            self.passwd_count = key_file.get_value('generate', 'count')
            self.selected_character_set = key_file.get_value(
                'generate',
                'character_set'
            )

    @property
    def selected_character_set(self):
        return self.app.character_sets[self.char_set_combo_box.get_active()]

    @selected_character_set.setter
    def selected_character_set(self, value):
        self.char_set_combo_box.set_active(int(value))

    @property
    def passwd_length(self):
        return int(self.length_spin_button.get_value())

    @passwd_length.setter
    def passwd_length(self, value):
        self.length_spin_button.set_value(int(value))

    @property
    def passwd_count(self):
        return int(self.count_spin_button.get_value())

    @passwd_count.setter
    def passwd_count(self, value):
        self.count_spin_button.set_value(int(value))


class GnomePassordGenerator(Gtk.Application):
    CONFIG_FILE = os.path.join(
        GLib.get_user_config_dir(),
        NAME.lower().replace(' ', '-') + '.conf'
    )

    def __init__(self):
        super().__init__()

        self.image = GdkPixbuf.Pixbuf.new_from_file(ICON_FILE)
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

    def do_activate(self):
        self.main_win = MainWindow(self)
        self.main_win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.create_gmenu()

    def create_gmenu(self):
        menu = Gio.Menu()
        menu.append("About", "app.about")
        menu.append("Quit", "app.quit")
        self.set_app_menu(menu)

        # option "about"
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.about_cb)
        self.add_action(about_action)

        # option "quit"
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.quit_cb)
        self.add_action(quit_action)

    def about_cb(self, action, parameter):
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_program_name(NAME)
        about_dialog.set_copyright(COPYRIGHT)
        about_dialog.set_authors(AUTHORS)
        about_dialog.set_website(WEBSITE)
        about_dialog.set_logo(self.image)

        about_dialog.set_transient_for(self.main_win)
        about_dialog.connect('response', self.on_close)
        about_dialog.show()

    def on_close(self, action, parameter):
        action.destroy()

    def quit_cb(self, action, parameter):
        self.quit()


# Start the program
if __name__ == "__main__":
    app = GnomePassordGenerator()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
