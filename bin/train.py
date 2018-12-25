import subprocess
import os
import shutil

import click

yolo_weights = "models/yolov3.weights"

@click.command()
@click.option("--weights", default=yolo_weights, type=click.Path())
def train(weights):
    # If we are training with the yolo weights we need to reset the number of iterations
    clear_flag = ""
    if weights == yolo_weights:
        clear_flag = "-clear 1"
    weights = os.path.abspath(weights)
    base_directory = os.getcwd()
    train_directory = base_directory + '/data/yolo_input/'
    yolo_train_command = f"cd {train_directory} && mkdir -p backup && {base_directory}/darknet/darknet detector train data/obj.data yolo-obj.cfg {weights} {clear_flag}"
    click.echo(f"Training with command: {yolo_train_command}")
    os.system(yolo_train_command)
    shutil.copyfile(f"{train_directory}/backup/yolov3.backup", "models/")

if __name__ == '__main__':
    train()
