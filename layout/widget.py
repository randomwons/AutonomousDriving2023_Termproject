import open3d as o3d
import open3d.visualization.gui as gui
import open3d.visualization.rendering as rendering
from shader.material import Material
import numpy as np


class Widget(gui.SceneWidget):
    def __init__(self, window):
        super().__init__()
        self.scene = rendering.Open3DScene(window.renderer)
        self.scene.set_background([0, 0, 0, 0])
        window.add_child(self)
        self.draw_primitives()
        
    def draw_car(self, name, pose, length, width, height):
        
        car = o3d.geometry.LineSet()
        car.points = o3d.utility.Vector3dVector([
          [length / 2, width /2, height], [length / 2, -width / 2, height],
          [-length / 2, -width / 2, height], [-length / 2, width / 2, height],
          [length / 2, width /2, 0], [length / 2, -width / 2, 0],
          [-length / 2, -width / 2, 0], [-length / 2, width / 2, 0]  
        ])
        car.lines = o3d.utility.Vector2iVector([
            [0, 1], [1, 2], [2, 3], [3, 0],
            [4, 5], [5, 6], [6, 7], [7, 4],
            [0, 4], [1, 5], [2, 6], [3, 7]
        ])
        car.paint_uniform_color([1.0, 0.0, 0.0])
        self.scene.add_geometry(name, car, Material.default)
        self.scene.set_geometry_transform(name, pose)
    
    def draw_spline(self, name, poly, color=[1.0, 0.0, 0.0], min=-30, max=30):
        self.remove_geometry(name)
        
        spline = o3d.geometry.LineSet()
        spline.points = o3d.utility.Vector3dVector([
            [i, poly[0]*i*i + poly[1] * i + poly[2], 0] for i in range(min, max, 1)
        ])
        spline.lines = o3d.utility.Vector2iVector([
            [i, i+1] for i in range(0, max-min-1)
        ])
        spline.paint_uniform_color(color)
        self.scene.add_geometry(name, spline, Material.default)
    
    def draw_primitives(self):

        self.draw_car("my_car", np.eye(4), 3.6, 1.8, 1.7)
        
        self.scene.show_axes(True)
        # self.scene.show_ground_plane(True, rendering.Scene.GroundPlane.XY)
        self.scene.camera.look_at([0, 0, 0], [0, 0, 20], [0, 0, 1])
            
    def update_geometry(self, name, geometry, show=True, mat=Material.default):
        self.remove_geometry(name)
        if show:
            self.scene.add_geometry(name, geometry, mat)
    
    def remove_geometry(self, name):
        if self.scene.has_geometry(name):
            self.scene.remove_geometry(name)