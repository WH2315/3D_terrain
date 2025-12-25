from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                             QPushButton, QComboBox, QLabel, QSlider, QFileDialog, QMessageBox)
from ui.canvas import MplCanvas
from core.data_generator import TerrainGenerator
from core.file_handler import FileHandler
from core.data_analyzer import TerrainAnalyzer
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python 地形数据三维显示系统")
        self.resize(1000, 700)
        
        # 数据存储
        self.X = None
        self.Y = None
        self.Z = None
        
        # 初始化 UI
        self.init_ui()
        
        # 默认加载一个地形
        self.generate_random_terrain()

    def init_ui(self):
        # 主窗口部件
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        # 布局
        self.layout = QHBoxLayout(self.main_widget)
        
        # 左侧控制面板
        self.control_panel = QWidget()
        self.control_layout = QVBoxLayout(self.control_panel)
        self.control_panel.setFixedWidth(250)
        
        # --- 数据控制区 ---
        self.add_section_label("数据操作")
        
        self.btn_gen_random = QPushButton("生成随机地形")
        self.btn_gen_random.clicked.connect(self.generate_random_terrain)
        self.control_layout.addWidget(self.btn_gen_random)
        
        self.btn_gen_peaks = QPushButton("生成多峰地形")
        self.btn_gen_peaks.clicked.connect(self.generate_peaks_terrain)
        self.control_layout.addWidget(self.btn_gen_peaks)
        
        self.btn_load = QPushButton("加载数据 (.npz)")
        self.btn_load.clicked.connect(self.load_data)
        self.control_layout.addWidget(self.btn_load)
        
        self.btn_save = QPushButton("保存当前数据")
        self.btn_save.clicked.connect(self.save_data)
        self.control_layout.addWidget(self.btn_save)
        
        self.control_layout.addSpacing(20)
        
        # --- 显示控制区 ---
        self.add_section_label("显示设置")
        
        self.control_layout.addWidget(QLabel("颜色映射 (Colormap):"))
        self.combo_cmap = QComboBox()
        self.combo_cmap.addItems(['viridis', 'plasma', 'inferno', 'magma', 'terrain', 'ocean'])
        self.combo_cmap.currentTextChanged.connect(self.update_plot)
        self.control_layout.addWidget(self.combo_cmap)
        
        self.control_layout.addWidget(QLabel("着色模式:"))
        self.combo_color_mode = QComboBox()
        self.combo_color_mode.addItems(['高度 (Height)', '坡度 (Slope)'])
        self.combo_color_mode.currentTextChanged.connect(self.update_plot)
        self.control_layout.addWidget(self.combo_color_mode)

        self.check_wireframe = QtWidgets.QCheckBox("显示网格 (Wireframe)")
        self.check_wireframe.stateChanged.connect(self.update_plot)
        self.control_layout.addWidget(self.check_wireframe)

        self.check_contours = QtWidgets.QCheckBox("显示等高线 (Contours)")
        self.check_contours.stateChanged.connect(self.update_plot)
        self.control_layout.addWidget(self.check_contours)
        
        self.control_layout.addSpacing(20)

        # --- 数据统计区 ---
        self.add_section_label("地形统计")
        self.lbl_max_height = QLabel("最高点: N/A")
        self.control_layout.addWidget(self.lbl_max_height)
        self.lbl_min_height = QLabel("最低点: N/A")
        self.control_layout.addWidget(self.lbl_min_height)
        self.lbl_mean_height = QLabel("平均高度: N/A")
        self.control_layout.addWidget(self.lbl_mean_height)
        self.lbl_avg_slope = QLabel("平均坡度: N/A")
        self.control_layout.addWidget(self.lbl_avg_slope)
        
        self.control_layout.addSpacing(20)
        
        # --- 视角控制区 ---
        self.add_section_label("视角控制")
        
        self.control_layout.addWidget(QLabel("垂直旋转 (Elevation):"))
        self.slider_elev = QSlider(QtCore.Qt.Horizontal)
        self.slider_elev.setRange(0, 90)
        self.slider_elev.setValue(30)
        self.slider_elev.valueChanged.connect(self.update_view)
        self.control_layout.addWidget(self.slider_elev)
        
        self.control_layout.addWidget(QLabel("水平旋转 (Azimuth):"))
        self.slider_azim = QSlider(QtCore.Qt.Horizontal)
        self.slider_azim.setRange(0, 360)
        self.slider_azim.setValue(45)
        self.slider_azim.valueChanged.connect(self.update_view)
        self.control_layout.addWidget(self.slider_azim)
        
        self.btn_reset_view = QPushButton("重置视角")
        self.btn_reset_view.clicked.connect(self.reset_view)
        self.control_layout.addWidget(self.btn_reset_view)
        
        self.control_layout.addStretch()
        
        # 右侧绘图区
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        
        # 添加到主布局
        self.layout.addWidget(self.control_panel)
        self.layout.addWidget(self.canvas)

    def add_section_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
        self.control_layout.addWidget(label)

    def generate_random_terrain(self):
        self.X, self.Y, self.Z = TerrainGenerator.generate_terrain()
        self.update_plot()

    def generate_peaks_terrain(self):
        self.X, self.Y, self.Z = TerrainGenerator.generate_peaks()
        self.update_plot()

    def load_data(self):
        fname, _ = QFileDialog.getOpenFileName(self, '打开文件', './data', "NumPy Zip (*.npz)")
        if fname:
            X, Y, Z, msg = FileHandler.load_terrain(fname)
            if X is not None:
                self.X, self.Y, self.Z = X, Y, Z
                self.update_plot()
                QMessageBox.information(self, "成功", msg)
            else:
                QMessageBox.warning(self, "错误", msg)

    def save_data(self):
        if self.X is None:
            QMessageBox.warning(self, "警告", "没有数据可保存")
            return
        fname, _ = QFileDialog.getSaveFileName(self, '保存文件', './data', "NumPy Zip (*.npz)")
        if fname:
            success, msg = FileHandler.save_terrain(fname, self.X, self.Y, self.Z)
            if success:
                QMessageBox.information(self, "成功", msg)
            else:
                QMessageBox.warning(self, "错误", msg)

    def update_plot(self):
        if self.X is None:
            return
        
        cmap = self.combo_cmap.currentText()
        wireframe = self.check_wireframe.isChecked()
        contours = self.check_contours.isChecked()
        color_mode = self.combo_color_mode.currentText()
        
        color_data = None
        if '坡度' in color_mode:
            # 计算坡度用于着色
            color_data = TerrainAnalyzer.calculate_slope(self.Z)
            # 坡度通常用 degrees 显示更直观，这里转换为度
            color_data = np.degrees(color_data)
        
        self.canvas.plot_terrain(self.X, self.Y, self.Z, cmap=cmap, wireframe=wireframe, contours=contours, color_data=color_data)
        self.update_stats()

    def update_stats(self):
        if self.Z is None:
            return
            
        stats = TerrainAnalyzer.get_statistics(self.Z)
        avg_slope = TerrainAnalyzer.get_average_slope(self.Z)
        
        if stats:
            self.lbl_max_height.setText(f"最高点: {stats['max_height']:.2f}")
            self.lbl_min_height.setText(f"最低点: {stats['min_height']:.2f}")
            self.lbl_mean_height.setText(f"平均高度: {stats['mean_height']:.2f}")
            self.lbl_avg_slope.setText(f"平均坡度: {avg_slope:.2f}°")

    def update_view(self):
        elev = self.slider_elev.value()
        azim = self.slider_azim.value()
        self.canvas.set_view(elev, azim)

    def reset_view(self):
        self.slider_elev.setValue(30)
        self.slider_azim.setValue(45)
        self.update_view()
