import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    """
    程序入口点
    """
    app = QApplication(sys.argv)
    
    # 设置应用程序样式，使其看起来更现代
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
