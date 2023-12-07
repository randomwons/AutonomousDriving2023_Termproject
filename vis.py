import time

import open3d.visualization.gui as gui

from event import Event
from layout.panel import Panel
from layout.widget import Widget
from context import Context

class Vis:
    def __init__(self):
        self.event = Event(self)
    
    def run(self):
        app = gui.Application.instance
        app.initialize()
        self.window = app.create_window(
            "Autonomous Driving Term Project", 1280, 720
        )
        
        ### Panel
        vspacing = 4
        margins = gui.Margins(10, 10, 10, 10)
        self.panel = Panel(self.event, vspacing, margins, self.window)

        ### Widget
        self.widget = Widget(self.window)

        ### on event
        self.window.set_on_layout(self.layout)
        self.window.set_on_close(self.close)
        self.window.set_on_key(self.event.on_key)
        
        ### Thread context
        time.sleep(1)
        self.context = Context(self)
        self.context.start()
        app.run()
    
    def layout(self, ctx):
        rect = self.window.content_rect
        self.panel.frame = gui.Rect(rect.x, rect.y, rect.width // 4, rect.height)        
        x = self.panel.frame.get_right()
        self.widget.frame = gui.Rect(x, rect.y, rect.get_right() - x, rect.height)
    
    def close(self):
        self.event.loop_stop = True
        
        if not self.event.exit_thread:
            time.sleep(0.1)
        self.window.close()
        return True
                
if __name__ == "__main__":
    vis = Vis()
    vis.run()