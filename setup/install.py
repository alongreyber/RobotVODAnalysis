import click
import subprocess
import os

@click.command()
@click.option("--cuda/--no-cuda", default=False)
@click.option("--opencv/--no-opencv", default=False)
def setup(cuda, opencv):
    click.echo('Starting setup')
    # Check if cuda toolkit is installed
    status, result = subprocess.getstatusoutput("nvcc --version")
    if status != 0:
        click.echo("Cuda not found! Please install the nvidia driver and cuda toolkit")
        exit()

    # Download weights for darknet
    click.echo("Downloading weights")
    os.system("cd models && wget -nc https://pjreddie.com/media/files/yolov3.weights")
    
    # Download and build darknet tool
    if not os.path.isdir("./darknet"):
        os.system("git clone https://github.com/AlexeyAB/darknet.git")
        click.echo("Building Darknet")
        # Enable building .so files
        os.system("sed -i 's/LIBSO=0/LIBSO=1/g' darknet/Makefile")
        if cuda:
            click.echo("With CUDA GPU")
            os.system("sed -i 's/GPU=0/GPU=1/g' darknet/Makefile")
        if opencv:
            click.echo("With OpenCV")
            os.system("sed -i 's/OPENCV=0/OPENCV=1/g' darknet/Makefile")
        os.system("cd darknet && make")
    else:
        click.echo("Found darknet, not installing")

if __name__ == '__main__':
    setup()
