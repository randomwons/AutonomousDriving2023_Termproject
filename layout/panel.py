import open3d as o3d
import open3d.visualization.gui as gui
from util.create_ui import create_button, create_label

class Panel(gui.Vert):
    def __init__(self, event, vspacing, margins, parent=None):
        super().__init__(vspacing, margins)
        self.event = event
        
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
        data_layout.add_stretch()
        self.add_child(data_layout)
        self.add_stretch()
        
        ## Parameters
        parameter_layout = gui.Vert()
        self.paramter = create_label("Parameters (Down Key, Up Key)", parameter_layout)
        self.ground_threshold = create_label("Ground threshold (C, V) : ", parameter_layout)
        self.voxel_size = create_label("Voxel Size (Z, X) : ", parameter_layout)
        self.dbscan_eps = create_label("DBSCAN EPS (A, S) : ", parameter_layout)
        self.dbscan_min_points = create_label("DBSCAN min points (D, F) : ", parameter_layout)
        self.add_child(parameter_layout)
    
    def update_image(self, image):
        
        o3d_image = o3d.geometry.Image(image)
        self.image_widget.update_image(o3d_image)
        
    def update_datas(self, datas):
    
        self.data_step.text = f"Data Step : {datas['index']}"
        self.vx.text = f"Vx : {datas['vx'] * 3.6:.2f} km/h"
        self.yawrate.text = f"Yawrate : {datas['yawrate']} deg/s"
        self.swa.text = f"SWA : {datas['sas_angle']} deg"
            
    def update_parameters(self):
        
        self.ground_threshold.text = f"Ground threshold (C, V) : {self.event.ground:.2f}"
        self.voxel_size.text = f"Voxel Size (Z, X) : {self.event.voxel_size:.2f}"
        self.dbscan_eps.text = f"DBSCAN EPS (A, S) : {self.event.eps:.2f}"
        self.dbscan_min_points.text = f"DBSCAN min points (D, F) : {self.event.min_points}"
        
