import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class SpectrGraph(Gtk.DrawingArea):
    __gtype_name__ = 'SpectrGraph'

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.set_size_request(400, 400)

    def do_draw(self, cr):
        # paint background
        bg_color = self.get_style_context().get_background_color(Gtk.StateFlags.NORMAL)
        cr.set_source_rgba(*list(bg_color))
        cr.paint()
        # draw a diagonal line
        allocation = self.get_allocation()
        fg_color = self.get_style_context().get_color(Gtk.StateFlags.NORMAL)
        cr.set_source_rgba(*list(fg_color));
        cr.set_line_width(2)
        cr.move_to(0, 0)  # top left of the widget
        cr.line_to(allocation.width, allocation.height)
        cr.stroke()