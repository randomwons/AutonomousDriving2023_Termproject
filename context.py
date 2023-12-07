import threading
import time
import traceback
from copy import deepcopy

import open3d as o3d
import open3d.visualization.gui as gui
import numpy as np
import matplotlib.pyplot as plt

from dataset import Dataset
from shader.material import Material

class Context(threading.Thread):
    def __init__(self, vis, daemon=True):
        threading.Thread.__init__(self, daemon=daemon)
        self.vis = vis
        
    def run(self):
        
        # For concise code
        app = gui.Application.instance
        to_main_thread = app.post_to_main_thread        
        event = self.vis.event
        window = self.vis.window
        
        while not event.loop_stop:
            
            self.dataset = Dataset("data/20220331T160645_ProjectData.mat")

            for datas in self.dataset:
                
                if event.loop_stop:
                    break

                if event.wait:
                    self.dataset.wait()
                    
                ### Image update
                to_main_thread(window, lambda : self.vis.panel.update_image(datas["image"]))
                
                ### Data update
                to_main_thread(window, lambda : self.vis.panel.update_datas(datas))
                
                ### Draw lanes
                to_main_thread(window, lambda : self.vis.widget.draw_spline("left", datas["poly_vision_left"], color=[0, 1, 0]))
                to_main_thread(window, lambda : self.vis.widget.draw_spline("right", datas["poly_vision_right"], color=[1, 0, 0]))
                
                ### Parameter update
                to_main_thread(window, lambda : self.vis.panel.update_parameters())
                
                ### Ground filtering
                points = datas["points"]
                points = points[points[:, 2] > event.ground]
                pcd = o3d.geometry.PointCloud()
                pcd.points = o3d.utility.Vector3dVector(points)
                pcd.paint_uniform_color([0.7, 0.5, 0.3])

                ### Voxel downsampling
                pcd = pcd.voxel_down_sample(event.voxel_size)
                
                ### DBSCAN Clustering    
                labels = np.array(pcd.cluster_dbscan(eps=event.eps, min_points=event.min_points, print_progress=False))
                max_label = labels.max()
                colors = plt.get_cmap("tab20")(labels/(max_label if max_label > 0 else 1))
                colors[labels < 0] = 0 # if event.test else 1
                pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
                
                # Cluster center points
                cluster_centers = []
                for i in range(max_label + 1):
                    cluster_points = np.asarray(pcd.points)[labels == i, :]
                    center = cluster_points.mean(axis=0)
                    cluster_centers.append(center)
                cluster_centers = np.asarray(cluster_centers)
                 
                centers = o3d.geometry.PointCloud()
                centers.points = o3d.utility.Vector3dVector(cluster_centers)
                centers.paint_uniform_color([1, 0, 0])
                to_main_thread(window, lambda : self.vis.widget.update_geometry("centers", centers, True, Material.largepoint))

                to_main_thread(window, lambda : self.vis.widget.update_geometry("pcd", pcd))
                
                time.sleep(0.03)

        event.exit_thread = True
        
        
    