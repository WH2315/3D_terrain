import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

class MplCanvas(FigureCanvas):
    """
    自定义的 Matplotlib 画布类，用于嵌入 PyQt5
    """
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111, projection='3d')
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)
        
        # 初始化设置
        self.axes.set_xlabel('X Axis')
        self.axes.set_ylabel('Y Axis')
        self.axes.set_zlabel('Height')
        self.axes.mouse_init()  # 启用鼠标交互（旋转、缩放）

    def plot_terrain(self, X, Y, Z, cmap='viridis', wireframe=False):
        """
        绘制地形
        """
        self.axes.clear()
        
        if wireframe:
            self.axes.plot_wireframe(X, Y, Z, rstride=2, cstride=2, cmap=cmap)
        else:
            surf = self.axes.plot_surface(X, Y, Z, cmap=cmap, linewidth=0, antialiased=False)
            # 注意：如果需要 colorbar，需要在外部管理，或者在这里添加逻辑避免重复添加
        
        self.axes.set_xlabel('X')
        self.axes.set_ylabel('Y')
        self.axes.set_zlabel('Z')
        self.draw()

    def set_view(self, elev, azim):
        """
        设置视角
        """
        self.axes.view_init(elev=elev, azim=azim)
        self.draw()
