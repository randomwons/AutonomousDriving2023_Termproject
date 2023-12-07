import open3d.visualization.rendering as rendering

class Event:
    def __init__(self, vis):
        self.vis = vis
        
        ## Window process
        self.loop_stop = False
        self.exit_thread = False
        
        ## data wait
        self.wait = False
        
        ## Values
        self.ground = 0.27
        self.voxel_size = 0.25
        self.eps = 1.0
        self.min_points = 7
        self.icp_threshold = 1.0
        self.icp_distance = 0.01
        
    def on_key(self, keyevent):
        
        if keyevent.type == keyevent.type.DOWN:

            ### Ground threshold setting
            if keyevent.key == ord('c'):
                self.ground -= 0.01
                
            if keyevent.key == ord('v'):
                self.ground += 0.01

            ### Voxel Size setting
            if keyevent.key == ord('z'):
                if self.voxel_size - 0.05 > 0.03:
                    self.voxel_size -= 0.05
                
            if keyevent.key == ord('x'):
                self.voxel_size += 0.05
            
            ### DBSCAN EPS setting
            if keyevent.key == ord('a'):
                if self.eps - 0.05 > 0:
                    self.eps -= 0.05
            
            if keyevent.key == ord('s'):
                self.eps += 0.05
            
            ### DBSCAN min points setting
            if keyevent.key == ord('d'):
                self.min_points = max(1, self.min_points - 1)
                
            if keyevent.key == ord('f'):
                self.min_points += 1
            
            ### ICP threshold setting
            if keyevent.key == ord('b'):
                self.icp_distance = max(0.1, self.icp_distance - 0.1)
            
            if keyevent.key == ord('n'):
                self.icp_distance += 0.1
                
            ### ICP distance setting
            if keyevent.key == ord('g'):
                self.icp_distance = max(0.01, self.icp_distance - 0.1)
            
            if keyevent.key == ord('h'):
                self.icp_threshold += 0.01
            
            
            if keyevent.key == 32: # space
                self.wait = not self.wait
            
            if keyevent.key == ord('t'):
                self.vis.widget.scene.camera.set_projection(60, 1.5, 0, 1000, rendering.Camera.FovType.Horizontal)
                self.vis.widget.scene.camera.look_at([2.3, 0, 1.2], [2.2, 0, 1.2], [0, 0, 1])
        
        
        
        