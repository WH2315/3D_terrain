import numpy as np

class TerrainAnalyzer:
    """
    负责地形数据的分析与统计
    """
    @staticmethod
    def get_statistics(Z):
        """
        计算地形的高度统计信息
        :param Z: 高度数据网格
        :return: 包含统计信息的字典
        """
        if Z is None:
            return None
            
        stats = {
            "max_height": np.max(Z),
            "min_height": np.min(Z),
            "mean_height": np.mean(Z),
            "std_dev": np.std(Z)
        }
        return stats

    @staticmethod
    def calculate_slope(Z, dx=1, dy=1):
        """
        计算地形坡度
        :param Z: 高度数据网格
        :param dx: X方向网格间距
        :param dy: Y方向网格间距
        :return: 坡度网格 (弧度)
        """
        if Z is None:
            return None
            
        # 使用梯度计算坡度
        gy, gx = np.gradient(Z, dy, dx)
        slope_rad = np.arctan(np.sqrt(gx**2 + gy**2))
        return slope_rad

    @staticmethod
    def get_average_slope(Z):
        """
        计算平均坡度（度）
        """
        slope_rad = TerrainAnalyzer.calculate_slope(Z)
        if slope_rad is None:
            return 0.0
        return np.degrees(np.mean(slope_rad))
