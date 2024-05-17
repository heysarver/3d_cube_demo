# /main.py
from PyQt5.QtWidgets import QApplication
import sys
from glwidget import GLWidget
import argparse
import time
import os

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--monitor', action='store_true', help='Monitor hardware stress')
args = parser.parse_args()

# Your cube object or function
cube = Cube()

# Main loop
while True:
    # If the monitor flag is passed, print the hardware stress
    if args.monitor:
        print(f'CPU Usage: {os.getloadavg()}')
        # Add more hardware stress monitoring here

    # Your cube logic here
    cube.update()

    # Sleep for a while to prevent jumping to a new cube at random intervals
    time.sleep(0.1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GLWidget()
    window.setWindowTitle('Spinning 3D Cube Demo')
    window.show()
    sys.exit(app.exec_())
