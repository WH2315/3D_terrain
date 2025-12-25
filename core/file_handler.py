import numpy as np
import os
import matplotlib.image as mpimg

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

    @staticmethod
    def import_from_image(filepath, height_scale=10.0):
        """
        从图片导入地形 (灰度图作为高度图)
        """
        try:
            # 读取图片
            img = mpimg.imread(filepath)
            
            # 如果是 RGB/RGBA，转换为灰度
            if img.ndim == 3:
                # 简单的加权平均转灰度
                if img.shape[2] >= 3:
                    img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
            
            # 归一化到 0-1
            if img.max() > 1.0:
                img = img / 255.0
                
            # 翻转 Y 轴以匹配图片坐标系
            Z = np.flipud(img) * height_scale
            
            h, w = Z.shape
            x = np.linspace(-5, 5, w)
            y = np.linspace(-5, 5, h)
            X, Y = np.meshgrid(x, y)
            
            return X, Y, Z, "图片导入成功"
        except Exception as e:
            return None, None, None, f"图片导入失败: {str(e)}"

    @staticmethod
    def import_from_text(filepath, delimiter=None):
        """
        从文本文件导入地形 (矩阵格式)
        """
        try:
            # 尝试自动检测分隔符或使用默认空格
            Z = np.loadtxt(filepath, delimiter=delimiter)
            
            h, w = Z.shape
            x = np.linspace(-5, 5, w)
            y = np.linspace(-5, 5, h)
            X, Y = np.meshgrid(x, y)
            
            return X, Y, Z, "文本导入成功"
        except Exception as e:
            return None, None, None, f"文本导入失败: {str(e)}"
