import numpy as np
import os

class FileHandler:
    """
    负责地形数据的加载与保存
    """
    @staticmethod
    def save_terrain(filepath, X, Y, Z):
        """
        保存地形数据到 .npz 文件
        """
        try:
            np.savez(filepath, X=X, Y=Y, Z=Z)
            return True, "保存成功"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def load_terrain(filepath):
        """
        从 .npz 文件加载地形数据
        """
        try:
            if not os.path.exists(filepath):
                return None, None, None, "文件不存在"
            
            data = np.load(filepath)
            return data['X'], data['Y'], data['Z'], "加载成功"
        except Exception as e:
            return None, None, None, str(e)
