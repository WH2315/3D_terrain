import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import cm, colors
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

    def plot_terrain(self, X, Y, Z, cmap='viridis', wireframe=False, contours=False, color_data=None):
        """
        绘制地形
        :param color_data: 用于着色的数据（例如坡度），如果为 None 则使用 Z 高度着色
        """
        self.axes.clear()
        
        if wireframe:
            self.axes.plot_wireframe(X, Y, Z, rstride=2, cstride=2, cmap=cmap)
        else:
            if color_data is not None:
                # 如果提供了自定义着色数据（如坡度）
                norm = colors.Normalize(vmin=color_data.min(), vmax=color_data.max())
                m = cm.ScalarMappable(norm=norm, cmap=cmap)
                fcolors = m.to_rgba(color_data)
                self.axes.plot_surface(X, Y, Z, facecolors=fcolors, linewidth=0, antialiased=False, shade=False)
            else:
                # 默认使用 Z 高度着色
                self.axes.plot_surface(X, Y, Z, cmap=cmap, linewidth=0, antialiased=False)
            
        if contours:
            # 在 Z 轴底部绘制等高线
            offset = Z.min()
            self.axes.contour(X, Y, Z, zdir='z', offset=offset, cmap=cmap)
        
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
