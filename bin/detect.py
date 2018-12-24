import os
import subprocess

import click


@click.command()
def detect():
    base_directory = os.getcwd()
    yolo_detect_command = f"cd {directory} && {base_directory}/darknet/darknet detector test data/obj.data yolo-obj.cfg backup/yolo-obj_final.weights data/test.png -thresh 0"
    os.system(yolo_detect_command)

if __name__ == '__main__':
    detect()
