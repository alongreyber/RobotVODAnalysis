import os
import subprocess
import click
import shutil

@click.command()
@click.option("--video/--photo", default=False)
@click.option("--threshold", type=float, default=0.1)
@click.argument("model", type=click.Path())
@click.argument("source", type=click.Path())
@click.argument("dest", type=click.Path())
def detect(model, source, dest, threshold, video):
    model = os.path.abspath(model)
    source = os.path.abspath(source)
    base_directory = os.getcwd()
    working_directory = os.getcwd() + '/data/yolo_input/'
    yolo_detect_command = "cd {working_directory} && {base_directory}/darknet/darknet detector ".format(working_directory=working_directory, base_directory=base_directory)
    if video:
        yolo_detect_command += "demo "
    else:
        yolo_detect_command += "test "
    yolo_detect_command += "data/obj.data yolo-obj.cfg {model} {source} -thresh {threshold}".format(base_directory=base_directory, source=source, threshold=threshold, model=model)
    if video:
        yolo_detect_command += " -out_filename {dest}".format(dest=dest)
    os.system(yolo_detect_command)

    # Copy to dest
    if not video:
        shutil.move("{working_directory}/predictions.jpg".format(working_directory=working_directory), dest)
if __name__ == '__main__':
    detect()
