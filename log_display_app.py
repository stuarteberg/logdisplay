from PyQt4.QtGui import QWidget, QVBoxLayout, QTextBrowser, QPushButton

class LogDisplayWidget(QWidget):
    
    def __init__(self, logfile_path, *args, **kwargs):
        super(LogDisplayWidget, self).__init__(*args, **kwargs)
        self.logfile_path = logfile_path
        self.text_browser = QTextBrowser(self)
        self.text_browser.setStyleSheet("font: 12pt \"Courier\";")
        button = QPushButton("Show log", clicked=self.update_log_display)

        layout = QVBoxLayout()
        layout.addWidget(self.text_browser)
        layout.addWidget(button)
        self.setLayout(layout)

    def update_log_display(self):
        """
        Open the log file and display every line in the text browser.
        TODO: Speed this up by reading/showing only the newly added log lines.
        """
        # Clear the browser
        self.text_browser.setText("")

        # Re-parse
        with open(self.logfile_path, 'r') as f:
            for line in f:
                self.add_log_line(line)

    def add_log_line(self, line):
        """
        Add a line to the display, and highlight important words if we find any.
        """
        KEY_WORDS = ["wins", "loses"]
        for word in KEY_WORDS:
            line = line.replace( word, '<span style="background-color: #FFFF00">' + word + '</span>')
        line += "<br>"
        self.text_browser.insertHtml(line)

if __name__ == "__main__":
    import sys

    # Exit on Ctrl+C
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    if len(sys.argv) == 2:
        logfile_path = sys.argv[1]
    else:
        print "Usage: {} logfile_path".format( sys.argv[0] )
        print "No logfile given. Using a dummy logfile..."

        logfile_path = '/tmp/dummy_log.txt'
        # Prepare a dummy log file to test with...
        with open(logfile_path, 'w') as f:
            f.write("Match start\n")
            f.write("Player 1 wins\n")
            f.write("Player 2 loses\n")

    # Create app/window, then show/launch
    from PyQt4.QtGui import QApplication
    app = QApplication([])
    mainwin = LogDisplayWidget(logfile_path)
    mainwin.show()
    mainwin.raise_()
    app.exec_()
