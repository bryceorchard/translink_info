from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, QSize

class ErrorLineEdit(QLineEdit):
    """ A QLineEdit which displays an error as a placeholder
    """
    def __init__(self, placeholder):
        super().__init__()
        self.original_placeholder_text = placeholder
        self.original_palette = self.palette()
        self.setPlaceholderText(placeholder)

    def focusOutEvent(self, event):
        """ When the text box is clicked away from, change the placeholder text and color
        """
        if event.reason() != Qt.ActiveWindowFocusReason and not self.hasFocus():
            self.setPlaceholderText(self.original_placeholder_text)
            self.setPalette(self.original_palette)
            
        super().focusOutEvent(event)
        
    def sizeHint(self):
        """ Automatically resize text button size 
        """
        # Get the default size hint
        default_size = super().sizeHint()
        
        # Increase the height by multiplying it with a factor (e.g., 1.5)
        new_height = int(default_size.height() * 1.5)
        
        # Return the updated size hint
        return QSize(default_size.width(), new_height)