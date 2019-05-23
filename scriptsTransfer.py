import sys
import os
import platform

from PySide.QtGui import *
from PySide.QtCore import *


import helpers

icon_path = os.path.basename(__file__).replace('\\', '/') + '/icons'
# root = 'D:/WORK/Programming'

# FEATURE #
# x Design Data Model
# - Design module
# - copy file from anywhere to destination
# - Move file internal (inside destination directory)
# - Create Folder
# - Create empty file
# - rename/ remove file in destination
# - List show status for all of files in root (Moved, not moved, Ignore/do nothing)

# [opt]
# - Tag or mark files (ex. Important, frequency update, large, etc.)
# - Log activity
# - Console// Terminal
# - Apply theme
# - Export LOG

MODEL = helpers.getModel()

class FileListView(QTreeView):
    fileDropped = Signal(list)

    def __init__(self, parent=None):
        super(FileListView, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            # for url in event.mimeData().urls():
            # 	links.append(str(url.toLocalFile()))
            # self.fileDropped.emit(links)
            for url in event.mimeData().urls():
                if platform.system() == 'Darwin':
                    try:
                        from Foundation import NSURL
                    except ImportError:
                        import objc
                        _path = os.path.abspath(os.path.join(os.path.dirname(objc.__file__), '../'))
                        sys.path.append(_path)
                        from Foundation import NSURL
                    fname = str(NSURL.URLWithString_(str(url.toString())).filePathURL().path())
                    links.append(fname)
                else:
                    fname = str(url.toLocalFile())
                    links.append(fname)

            self.fileDropped.emit(links)
        else:
            event.ignore()


class ScriptTransferWindow(QMainWindow):

    setting = QSettings("Shape and light", "ScriptTransfer")

    def __init__(self, parent=None):
        super(ScriptTransferWindow, self).__init__(parent)
        self.model = QFileSystemModel()

        main_widget = QWidget()
        main_layout = QHBoxLayout()

        self.toolbar = QToolBar()
        self.toolbar.setObjectName('mainToolbar')
        self.origin_fileView = QTreeView()
        self.origin_fileView.header().setResizeMode(QHeaderView.ResizeToContents)
        self.origin_fileView.header().setStretchLastSection(False)
        self.origin_fileView.setExpandsOnDoubleClick(True)
        self.origin_fileView.setDragEnabled(True)

        self.target_fileView = FileListView()

        self.addToolBar(self.toolbar)
        main_layout.addWidget(self.origin_fileView)
        main_layout.addWidget(self.target_fileView)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.setup_toolbar()
        self.initUI()

    def initUI(self):
        self.setting.beginGroup("MainWindow")
        self.restoreGeometry(self.setting.value("geometry", self.saveGeometry()))
        self.restoreState(self.setting.value("saveState", self.saveState()))

        self.resize(self.setting.value("size", self.size()))
        self.move(self.setting.value("pos", self.pos()))
        self.setting.endGroup()

        # Init data
        self.model.setRootPath(MODEL.root())
        self.origin_fileView.setModel(self.model)
        self.origin_fileView.setRootIndex(self.model.index(MODEL.root()))

        self.target_fileView.setModel(MODEL.model())

    def closeEvent(self, *args, **kwargs):
        # print self.saveGeometry()
        self.setting.beginGroup("MainWindow")
        self.setting.setValue("geometry", self.saveGeometry())
        self.setting.setValue("saveState", self.saveState())
        self.setting.setValue("size", self.size())
        self.setting.setValue("pos", self.pos())
        self.setting.endGroup()

        super(ScriptTransferWindow, self).closeEvent(*args, **kwargs)

    def setup_toolbar(self):
        self.toolbar.addActions([
            QAction("S", self),  # Setting
            QAction("Aply", self),  # Apply
        ])

    def do_copy(self):
        raise NotImplementedError()

    def do_createDir(self):
        raise NotImplementedError()

    def do_createEmptyFile(self):
        raise NotImplementedError()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ScriptTransferWindow()
    win.show()
    app.exec_()
