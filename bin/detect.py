import os
import subprocess
import click


@click.command()
@click.option("--video/--photo", default=False)
@click.argument("source", type=click.Path())
def detect(source, video):
    source = os.path.abspath(source)
    base_directory = os.getcwd()
    working_directory = os.getcwd() + '/data/yolo_input/'
    yolo_detect_command = "cd {working_directory} && {base_directory}/darknet/darknet detector ".format(working_directory=working_directory, base_directory=base_directory)
    if video:
        yolo_detect_command += "demo "
    else:
        yolo_detect_command += "test "
    yolo_detect_command += "data/obj.data yolo-obj.cfg {base_directory}/models/yolov3.weights {source} -thresh 0".format(base_directory=base_directory, source=source)
    os.system(yolo_detect_command)

if __name__ == '__main__':
    detect()
