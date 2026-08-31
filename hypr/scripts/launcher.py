#!/usr/bin/env python3

import os
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("GtkLayerShell", "0.1")

from gi.repository import (
    Gtk,
    Gio,
    Gdk,
    GtkLayerShell,
    GdkPixbuf
)

CSS_PATH = os.path.expanduser(
    "~/.config/hypr/buscador/style.css"
)

WALLPAPER = os.path.expanduser(
    "~/.config/hypr/assets/wallpapers/gothic-wallpaper.png"
)


class Launcher(Gtk.Window):

    def __init__(self):

        super().__init__(title="Launcher")

        self.set_default_size(1200, 700)
        self.set_resizable(False)
        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.CENTER)

        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(
            self,
            GtkLayerShell.Layer.OVERLAY
        )

        GtkLayerShell.set_keyboard_mode(
            self,
            GtkLayerShell.KeyboardMode.EXCLUSIVE
        )

        self.connect(
            "key-press-event",
            self.on_key
        )

        self.load_css()

        self.build_ui()

        self.cargar_apps()

        self.show_all()


    def load_css(self):

        if not os.path.exists(CSS_PATH):
            return

        provider = Gtk.CssProvider()
        provider.load_from_path(CSS_PATH)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


    def build_ui(self):

        root = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=10
        )

        root.set_border_width(20)

        self.add(root)

        # PANEL IZQUIERDO

        left = Gtk.Frame()
        left.set_size_request(390, -1)
        left.get_style_context().add_class("left-panel")

        left_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=14
        )
        left_box.set_valign(Gtk.Align.CENTER)
        left_box.set_halign(Gtk.Align.FILL)
        left_box.set_margin_start(20)
        left_box.set_margin_end(20)
        left.add(left_box)

        # Boton Configuracion
        btn_config = Gtk.Button(label="⚙  Configuración")
        btn_config.get_style_context().add_class("left-panel-btn")
        btn_config.connect("clicked", self.open_settings)
        left_box.pack_start(btn_config, False, False, 0)

        # Boton Terminal
        btn_terminal = Gtk.Button(label="  Terminal")
        btn_terminal.get_style_context().add_class("left-panel-btn")
        btn_terminal.connect("clicked", self.open_terminal)
        left_box.pack_start(btn_terminal, False, False, 0)

        # Boton Explorador de archivos
        btn_files = Gtk.Button(label="  Archivos")
        btn_files.get_style_context().add_class("left-panel-btn")
        btn_files.connect("clicked", self.open_files)
        left_box.pack_start(btn_files, False, False, 0)

        root.pack_start(
            left,
            False,
            False,
            0
        )

        # PANEL DERECHO

        right = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=14
        )

        right.get_style_context().add_class(
            "right-panel"
        )

        root.pack_start(
            right,
            True,
            True,
            0
        )

        # BUSCADOR

        self.search = Gtk.SearchEntry()

        self.search.set_placeholder_text(
            "Buscar aplicación..."
        )

        self.search.connect(
            "search-changed",
            self.on_search
        )

        right.pack_start(
            self.search,
            False,
            False,
            0
        )

        # SCROLL

        scroll = Gtk.ScrolledWindow()

        scroll.set_policy(
            Gtk.PolicyType.NEVER,
            Gtk.PolicyType.AUTOMATIC
        )

        right.pack_start(
            scroll,
            True,
            True,
            0
        )

        # LISTA

        self.listbox = Gtk.ListBox()

        self.listbox.set_activate_on_single_click(
            True
        )

        self.listbox.connect(
            "row-activated",
            self.launch
        )

        scroll.add(
            self.listbox
        )

    # BOTONES DEL PANEL IZQUIERDO

    def open_settings(self, widget):
        import subprocess
        subprocess.Popen(["flatpak", "run", "com.visualstudio.code", os.path.expanduser("~/.config/hypr")])
        Gtk.main_quit()
    def open_terminal(self, widget):
        import subprocess
        subprocess.Popen(["kitty"])
        Gtk.main_quit()

    def open_files(self, widget):
        import subprocess
        subprocess.Popen(["dolphin"])
        Gtk.main_quit()

    # CARGAR APLICACIONES

    def cargar_apps(self):

        self.apps = [
            app for app in Gio.AppInfo.get_all()
            if app.should_show()
        ]

        self.apps.sort(
            key=lambda app: app.get_name().lower()
        )

        for app in self.apps:

            row = Gtk.ListBoxRow()

            row.get_style_context().add_class(
                "app-row"
            )

            box = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL,
                spacing=16
            )

            box.set_margin_top(8)
            box.set_margin_bottom(8)
            box.set_margin_start(10)
            box.set_margin_end(10)

            # ICONO

            icon = app.get_icon()

            if icon:

                image = Gtk.Image.new_from_gicon(
                    icon,
                    Gtk.IconSize.DIALOG
                )

                image.set_pixel_size(48)

            else:

                image = Gtk.Image.new_from_icon_name(
                    "application-x-executable",
                    Gtk.IconSize.DIALOG
                )

                image.set_pixel_size(48)

            box.pack_start(
                image,
                False,
                False,
                0
            )

            # TEXTO

            label = Gtk.Label()

            label.set_text(
                app.get_name()
            )

            label.set_xalign(0)

            label.get_style_context().add_class(
                "app-label"
            )

            box.pack_start(
                label,
                True,
                True,
                0
            )

            row.add(box)

            self.listbox.add(row)

        self.listbox.show_all()

    # BUSCAR

    def on_search(self, widget):

        text = self.search.get_text().lower()

        first = None

        for row in self.listbox.get_children():

            box = row.get_child()

            label = box.get_children()[1]

            visible = (
                text in label.get_text().lower()
            )

            row.set_visible(
                visible
            )

            if visible and first is None:
                first = row

        if first:
            self.listbox.select_row(first)

    # ABRIR APP

    def launch(self, listbox, row):

        if row is None:
            return

        box = row.get_child()

        label = box.get_children()[1]

        name = label.get_text()

        for app in self.apps:

            if app.get_name() == name:

                app.launch([], None)

                Gtk.main_quit()

                return

    # TECLADO

    def focus_search(self):

        self.search.grab_focus()

        self.search.select_region(
            0,
            -1
        )

        if len(self.listbox.get_children()):

            self.listbox.select_row(
                self.listbox.get_row_at_index(0)
            )

    # MOVERSE CON LAS FLECHAS

    def move_selection(self, direction):

        rows = [
            row for row in self.listbox.get_children()
            if row.get_visible()
        ]

        if not rows:
            return

        current = self.listbox.get_selected_row()

        if current is None:

            self.listbox.select_row(rows[0])

            return

        try:

            index = rows.index(current)

        except ValueError:

            index = 0

        index += direction

        if index < 0:
            index = 0

        if index >= len(rows):
            index = len(rows) - 1

        self.listbox.select_row(
            rows[index]
        )

        rows[index].grab_focus()

    def on_key(self, widget, event):

        key = event.keyval

        if key == Gdk.KEY_Escape:

            Gtk.main_quit()

            return True

        elif key == Gdk.KEY_Down:

            self.move_selection(1)

            return True

        elif key == Gdk.KEY_Up:

            self.move_selection(-1)

            return True

        elif key == Gdk.KEY_Return:

            row = self.listbox.get_selected_row()

            if row:

                self.launch(
                    self.listbox,
                    row
                )

            return True

        return False


# MAIN

win = Launcher()

win.connect(
    "destroy",
    Gtk.main_quit
)

Gtk.main()