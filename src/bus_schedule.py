import sys
import os

from PySide6.QtWidgets import (QWidget, QDialog, QVBoxLayout, QHBoxLayout,
                               QLabel, QPushButton, QApplication)
from PySide6.QtCore import QUrl, Slot
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtGui import QPalette, QIcon

from custom_widgets import ErrorLineEdit
# ErrorLineEdit is a version of QLineEdit which allows 
# setting of the placeholder text to an error message
from custom_functions import get_schedule
# lotta imports sorryyyy

DIRECTORY = os.path.dirname(os.path.realpath(__file__))[:-4] # Current file directory
KEY = 'ObSFSraZkt2wDW7nYvCA' # API key

class Form(QWidget):
    """ Class representing the main form window
    """
    def __init__(self):
        super().__init__()
        
        self.v_layout = QVBoxLayout(self) # Create main vertical layout
        
        ### TOP

        self.h_layout_btns = QHBoxLayout() # Horizontal layout for map navigation buttons
        
        self.back = QPushButton() # Back button
        self.back.setIcon(QIcon(os.path.join(DIRECTORY, 'res', 'back_arrow.png')))
        self.h_layout_btns.addWidget(self.back)
        self.back.clicked.connect(self.back_func)
        
        self.forward = QPushButton() # Forward button
        self.forward.setIcon(QIcon(os.path.join(DIRECTORY, 'res', 'forward_arrow.png')))
        self.h_layout_btns.addWidget(self.forward)
        self.forward.clicked.connect(self.forward_func)
        
        self.reload = QPushButton() # Reload button
        self.reload.setIcon(QIcon(os.path.join(DIRECTORY, 'res', 'reload_arrow.png')))
        self.h_layout_btns.addWidget(self.reload)
        self.reload.clicked.connect(self.reload_func)
        
        self.h_layout_btns.addStretch(4) # Add padding to the right
        
        self.v_layout.addLayout(self.h_layout_btns) # Add buttons to vertical layout
        
        ### Middle

        self.map = QWebEngineView() # Create a QWebEngineView widget

        # Translink map url
        map_url = "https://translink.maps.arcgis.com/apps/webappviewer/index.html?id=ae9b3c118ad74cea94760d7ae890267c"

        self.map.setUrl(QUrl(map_url)) # Load the url into the webview
        
        self.v_layout.addWidget(self.map) # Add map to main vertical layout
        
        ### Bottom
        
        self.h_layout = QHBoxLayout() # Horizontal layout for the text boxes and button
        
        self.stop_form = ErrorLineEdit(" Enter Stop Number")
        
        self.h_layout.addWidget(self.stop_form)
        
        self.bus_form = ErrorLineEdit(" Enter Bus Number")
        
        self.h_layout.addWidget(self.bus_form)
        
        self.button = QPushButton("Find Times")
        self.button.clicked.connect(self.find_times)
        
        self.h_layout.addWidget(self.button) # Add text boxes and button to bottom menu bar
        
        self.v_layout.addLayout(self.h_layout) # Add menu bar to the vertical layout

    @Slot()
    def find_times(self):
        """ Calls get_schedule, which returns the next bus as a string. If the api request is 
            invalid, returns an error code for processing
        """
            
        palette = QPalette().setColor(QPalette.PlaceholderText, 'red')
        
        times = get_schedule(self.stop_form.text(), self.bus_form.text(), KEY)
        if not isinstance(times, list):
        # If the time is not a list of times
            match times:
                case '3001':
                    self.stop_form.setPlaceholderText("Invalid Stop Number")
                    self.stop_form.setPalette(palette)
                    self.stop_form.clear()
                    return
                
                case '3002':
                    self.stop_form.setPlaceholderText("Stop Number Not Found")
                    self.stop_form.setPalette(palette)
                    self.stop_form.clear()
                    return
                
                case '3004':
                    self.bus_form.setPlaceholderText("Invalid Route Number")
                    self.bus_form.setPalette(palette)
                    self.bus_form.clear()
                    return

        main_window = MainWindow(times)
        # Pass the retrieved time to the new window
        main_window.exec()
        
    @Slot()
    def back_func(self):
        self.map.triggerPageAction(QWebEnginePage.Back)
    @Slot()
    def forward_func(self):
        self.map.triggerPageAction(QWebEnginePage.Forward)
    @Slot()
    def reload_func(self):
        self.map.triggerPageAction(QWebEnginePage.Reload)
        
class MainWindow(QDialog):
    """ Class representing the window displaying the bus schedule time
    """
    def __init__(self, times):
        super().__init__()

        self.setWindowTitle("Next Bus")
        self.layout = QVBoxLayout(self)

        for item in times:
            label = QLabel(item)
            self.layout.addWidget(label)

def main():
    """ Creates the initial window and starts the program loop
    """
    app = QApplication([])
    
    form = Form()
    form.resize(900, 600)
    form.setMinimumSize(810, 440)
    form.show()
    
    @Slot()
    def delete_file():
        try:
            os.remove(os.path.join(DIRECTORY, 'res', 'schedule.json'))
        except FileNotFoundError:
            pass

    app.aboutToQuit.connect(delete_file)

    sys.exit(app.exec())

if __name__ == '__main__':
    print("To execute the program, run main.py")