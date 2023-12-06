import open3d as o3d
import open3d.visualization.gui as gui
from util.create_ui import create_button, create_label

class Panel(gui.Vert):
    def __init__(self, eventhandler, vspacing, margins, parent=None):
        super().__init__(vspacing, margins)
        self.eventhandler = eventhandler
        
        if parent is not None:
            parent.add_child(self)
        self.layout()
    
    def layout(self):
        
        paddings = (0.1, 0.5)
        
        ## image layout
        imagelayout = gui.Vert()
        self.image_widget = gui.ImageWidget()
        imagelayout.add_child(self.image_widget)
        imagelayout.add_fixed(20)
        self.add_child(imagelayout)
        
        ## Labels
        data_layout = gui.Vert()
        self.data_step = create_label("Data Step : ", data_layout)
        self.vx = create_label("Vx : ", data_layout)
        self.yawrate = create_label("Yawrate : ", data_layout)
        self.swa = create_label("SWA : ", data_layout)
        self.add_child(data_layout)
        
            
    
        
        
