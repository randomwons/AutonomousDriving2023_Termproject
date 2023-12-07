from scipy import io
import numpy as np
import open3d as o3d

class Dataset:
    def __init__(self, mat_path):
        self.datas = io.loadmat(mat_path)
        self.cur = 0
    
    def __len__(self):
        return len(self.datas["Ibeo_X_stack"][0])
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.cur >= len(self):
            raise StopIteration

        datas = {}
        datas["index"] = self.cur
        
        ## point clouds
        x = self.datas["Ibeo_X_stack"][0][self.cur]
        y = self.datas["Ibeo_Y_stack"][0][self.cur]
        z = self.datas["Ibeo_Z_stack"][0][self.cur]
        datas["points"] = np.vstack([x, y, z]).T
        
        datas["yawrate"] = self.datas["YAW_RATE_stack"][0][self.cur]
        datas["ax"] = self.datas["Ax_stack"][0][self.cur]
        datas["ay"] = self.datas["Ay_stack"][0][self.cur]
        datas["sas_angle"] = self.datas["SAS_Angle_stack"][0][self.cur]
        datas["vx"] = self.datas["Vx_stack"][0][self.cur]
        
        datas["poly_vision_left"] = self.datas["poly_vision_left_stack"][0][self.cur][0]
        datas["poly_vision_right"] = self.datas["poly_vision_right_stack"][0][self.cur][0]

    
        image = self.datas["dash_cam_stack"][0][self.cur][0][0][0]
        image = np.flipud(image)
        image = np.fliplr(image)
        image = np.ascontiguousarray(image, dtype=np.uint8)
        datas["image"] = image
        
        self.cur += 1
        return datas
    
    def wait(self):
        self.cur -= 1