import sys
from PyQt4 import QtGui, QtCore

import RandomMapGenerator as RMG

main_window = None  

class Sunfields(QtGui.QWidget):
    
    def __init__(self):
        super(Sunfields, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        btn = QtGui.QPushButton('New map', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(100, 550)
        btn.clicked.connect(self.generate)

        btn = QtGui.QPushButton('Densify', self)
        btn.resize(btn.sizeHint())
        btn.move(200, 550)
        btn.clicked.connect(self.do_densify)

        btn = QtGui.QPushButton('Remove Lone', self)
        btn.resize(btn.sizeHint())
        btn.move(275, 550)
        btn.clicked.connect(self.do_remove_lone)

        btn = QtGui.QPushButton('Smooth', self)
        btn.resize(btn.sizeHint())
        btn.move(350, 550)
        btn.clicked.connect(self.do_smoothen)


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
        RMG.set_widget(self)
        self.zone = RMG.Zone((0,0),(30,30))
        #z.find_neighboors()
        #z.densify(1.5)
        #z.find_neighboors()
        #z.remove_lone(RMG.LandTile, RMG.WaterTile)
        #z.find_neighboors()
        #z.remove_lone(RMG.WaterTile, RMG.LandTile)
        #z.find_neighboors()
        #z.smoothen(RMG.LandTile, RMG.WaterTile)

    def do_densify(self):
        self.zone.find_neighboors()
        self.zone.densify(1.0)

    def do_remove_lone(self):
        self.zone.find_neighboors()
        self.zone.remove_lone(RMG.LandTile, RMG.WaterTile)
        self.zone.find_neighboors()
        self.zone.remove_lone(RMG.WaterTile,RMG.LandTile)

    def do_smoothen(self):
        self.zone.find_neighboors()
        self.zone.smoothen(RMG.LandTile, RMG.WaterTile)
        self.zone.find_neighboors()
        self.zone.smoothen(RMG.WaterTile, RMG.LandTile)

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