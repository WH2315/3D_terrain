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
        
        # 初始化 Z
        Z = np.zeros_like(X)
        
        # 1. 基础地形：随机的大尺度起伏
        freq_base = np.random.uniform(0.5, 2.0)
        Z += np.sin(X * freq_base) * np.cos(Y * freq_base) * 2
        
        # 2. 叠加多层随机正弦波 (模拟分形噪声的简化版)
        num_layers = np.random.randint(3, 7)
        for i in range(num_layers):
            freq_x = np.random.uniform(1.0, 5.0) * (i + 1) * 0.5
            freq_y = np.random.uniform(1.0, 5.0) * (i + 1) * 0.5
            phase_x = np.random.uniform(0, 2 * np.pi)
            phase_y = np.random.uniform(0, 2 * np.pi)
            amplitude = np.random.uniform(0.5, 1.5) / (i + 1) # 高频分量振幅更小
            
            Z += amplitude * np.sin(X * freq_x + phase_x) * np.cos(Y * freq_y + phase_y)

        # 3. 随机添加一个中心隆起或凹陷
        if np.random.random() > 0.5:
            center_amp = np.random.uniform(-3, 5)
            Z += center_amp * np.exp(-(X**2 + Y**2) / 10)
        
        # 4. 添加随机噪声模拟粗糙表面
        noise = np.random.normal(0, 0.15, (height, width))
        Z += noise
        
        return X, Y, Z

    @staticmethod
    def generate_peaks(width=100, height=100, seed=None):
        """
        生成随机多峰地形 (基于随机高斯分布叠加)
        """
        if seed is not None:
            np.random.seed(seed)
            
        x = np.linspace(-3, 3, width)
        y = np.linspace(-3, 3, height)
        X, Y = np.meshgrid(x, y)
        
        Z = np.zeros_like(X)
        
        # 随机生成 5 到 10 个山峰或山谷
        num_peaks = np.random.randint(5, 11)
        
        for _ in range(num_peaks):
            # 随机参数
            amp = np.random.uniform(-6, 6)      # 高度 (正为山峰，负为山谷)
            x0 = np.random.uniform(-2.5, 2.5)   # X 中心
            y0 = np.random.uniform(-2.5, 2.5)   # Y 中心
            sigma_x = np.random.uniform(0.3, 1.0) # X 宽度
            sigma_y = np.random.uniform(0.3, 1.0) # Y 宽度
            
            # 高斯函数叠加
            Z += amp * np.exp(-((X - x0)**2 / (2 * sigma_x**2) + (Y - y0)**2 / (2 * sigma_y**2)))
            
        return X, Y, Z
