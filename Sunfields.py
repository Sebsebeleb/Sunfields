import sys
from PyQt4 import QtGui, QtCore

main_window = None  

class Sunfields(QtGui.QWidget):
    
    def __init__(self):
        super(Sunfields, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        btn = QtGui.QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(450, 550)
        btn.clicked.connect(self.generate)

        self.map_label = QtGui.QLabel(self)
        self.map_label.setGeometry(QtCore.QRect(75, 50, 500, 500))
        self.map_label.setPixmap(QtGui.QPixmap("hello.png"))

        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle('Sunfields!')    
        self.show()

    def set_map(self,picture):
        pic  = QtGui.QPixmap()
        pic.loadFromData(picture.getvalue())
        self.map_label.setPixmap(pic)
        self.repaint() #TODO: Apparently, this is not usually needed (http://www.riverbankcomputing.com/pipermail/pyqt/2009-January/021550.html) | use signalling instead

    def generate(self):
        import RandomMapGenerator as RMG
        import time
        RMG.set_widget(self)
        z = RMG.Zone((0,0),(30,30))
        time.sleep(1)

        z.densify(1.0)
        time.sleep(1)
        z.find_neighboors()
        time.sleep(1)
        z.remove_lone(RMG.LandTile, RMG.WaterTile)
        time.sleep(1)
        z.remove_lone(RMG.WaterTile, RMG.LandTile)

def set_map(picture):
    print main_window
    main_window.set_map()    
        
def main():
    global main_window
    
    app = QtGui.QApplication(sys.argv)
    main_window = Sunfields()
    print main_window
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()