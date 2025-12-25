import numpy as np

class TerrainGenerator:
    """
    负责生成模拟的地形数据
    """
    @staticmethod
    def generate_terrain(width=100, height=100, scale=0.1, seed=None):
        """
        生成基于简单数学函数的合成地形数据
        :param width: X轴网格数
        :param height: Y轴网格数
        :param scale: 缩放因子
        :param seed: 随机种子
        :return: X, Y, Z 网格数据
        """
        if seed is not None:
            np.random.seed(seed)
        
        x = np.linspace(-5, 5, width)
        y = np.linspace(-5, 5, height)
        X, Y = np.meshgrid(x, y)
        
        # 使用混合的高斯函数和正弦函数模拟山峰和地形起伏
        Z = np.sin(np.sqrt(X**2 + Y**2) * scale * 5) * 2
        Z += np.cos(X * scale * 3) * np.sin(Y * scale * 3)
        
        # 添加一些随机噪声模拟粗糙表面
        noise = np.random.normal(0, 0.1, (height, width))
        Z += noise
        
        return X, Y, Z

    @staticmethod
    def generate_peaks(width=100, height=100):
        """
        生成多峰地形
        """
        x = np.linspace(-3, 3, width)
        y = np.linspace(-3, 3, height)
        X, Y = np.meshgrid(x, y)
        
        # 著名的 Peaks 函数
        Z = 3 * (1 - X)**2 * np.exp(-(X**2) - (Y + 1)**2) \
            - 10 * (X / 5 - X**3 - Y**5) * np.exp(-X**2 - Y**2) \
            - 1 / 3 * np.exp(-(X + 1)**2 - Y**2)
            
        return X, Y, Z
