import subprocess
import os

import click

@click.command()
def train():
    base_directory = os.getcwd()
    yolo_train_command = f"cd {directory} && mkdir -p backup && \
            {base_directory}/darknet/darknet detector train data/obj.data yolo-obj.cfg \
            {base_directory}/yolov3.weights -clear 1"
    click.echo("Training with command: {yolo_train_command}")
    os.system(yolo_train_command)

if __name__ == '__main__':
    train()
