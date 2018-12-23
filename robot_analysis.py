import click
import subprocess
import os

# Entrypoint for the entire CLI
@click.group()
def cli():
    pass

@cli.command()
def setup():
    click.echo('Starting setup')
    # Check if cuda toolkit is installed
    status, result = subprocess.getstatusoutput("nvcc --version")
    if status != 0:
        click.echo("Cuda not found! Please install the nvidia driver and cuda toolkit")
        exit()
    click.echo("Downloading weights")
    os.system("wget -nc https://pjreddie.com/media/files/yolov3.weights")
    
    if not os.path.isdir("./darknet"):
        os.system("git clone https://github.com/pjreddie/darknet && \
               cd darknet && make")
    else:
        click.echo("Found darknet, not installing")

@cli.command()
@click.argument('directory', type=click.Path(exists=True))
def train(directory):
    base_directory = os.getcwd()
    yolo_train_command = f"cd {directory} && mkdir -p backup && \
            {base_directory}/darknet/darknet detector train data/obj.data yolo-obj.cfg {base_directory}/yolov3.weights -clear 1"
    click.echo("Training with command: {yolo_train_command}")
    os.system(yolo_train_command)

@cli.command()
@click.argument('directory', type=click.Path(exists=True))
def detect(directory):
    base_directory = os.getcwd()
    yolo_detect_command = f"cd {directory} && {base_directory}/darknet/darknet detector test data/obj.data yolo-obj.cfg backup/yolo-obj_final.weights data/test.png -thresh 0"
    os.system(yolo_detect_command)

if __name__ == '__main__':
    cli()
