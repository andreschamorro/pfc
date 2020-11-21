import sys
from gi.repository import GLib, Gio, Gtk


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_resizable(False)
        self.set_deletable(False)
        self.set_default_size(420, 270)
        # a grid to attach the toolbar (see below)
        grid = Gtk.Grid()
        self.add(grid)
        # we have to show the grid (and therefore the toolbar) with show(),
        # as show_all() would show also the buttons in the toolbar that we want
        # to be hidden (such as the leave_fullscreen button)
        grid.show()

        # a builder to add the UI designed with Glade to the grid:
        builder = Gtk.Builder()
        # get the file (if it is there)
        try:
            builder.add_from_file("UI/main.glade")
        except Exception:
            print("file not found")
            sys.exit()
        # and attach it to the grid
        grid.attach(builder.get_object("main_box"), 0, 0, 1, 1)
        self.card_area = builder.get_object("cards")
        self.scoring = builder.get_object("scoring")

        # This will be in the windows group and have the "win" prefix
        max_action = Gio.SimpleAction.new_stateful(
            "maximize", None, GLib.Variant.new_boolean(False)
        )
        max_action.connect("change-state", self.on_maximize_toggle)
        self.add_action(max_action)

        # Keep it in sync with the actual state
        self.connect(
            "notify::is-maximized",
            lambda obj, pspec: max_action.set_state(
                GLib.Variant.new_boolean(obj.props.is_maximized)
            ),
        )

    def on_maximize_toggle(self, action, value):
        action.set_state(value)
        if value.get_boolean():
            self.maximize()
        else:
            self.unmaximize()


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id="org.example.pfc",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
            **kwargs
        )
        self._window = None
        self._deck = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self._window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self._window = AppWindow(application=self, title="pfc")

        card = self._deck.draw()
        # a builder to add the UI designed with Glade to the grid:
        card_builder = Gtk.Builder()
        # get the file (if it is there)
        try:
            card_builder.add_from_file("UI/flippable.glade")
        except Exception:
            print("file not found")
            sys.exit()
        # and attach it to the grid

        card_draw = card_builder.get_object("card_draw")
        card_builder.get_object("question_buffer").set_text(card.question())
        card_builder.get_object("answer_buffer").set_text(card.answer())
        self._window.card_area.add_named(card_draw,
                                         "card_draw")

        self._window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        # convert GVariantDict -> GVariant -> dict
        options = options.end().unpack()

        if "test" in options:
            # This is printed on the main instance
            print("Test argument recieved: %s" % options["test"])

        self.activate()
        return 0

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self._window, modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()

    @property
    def deck(self):
        return self._deck

    @deck.setter
    def deck(self, d):
        self._deck = d
