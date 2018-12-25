import click
import os
import shutil
from distutils.dir_util import copy_tree
import runpy

@click.command()
def merge():
    base_directory = os.getcwd()
    os.chdir('data/')
    # Create output directory structure
    output = os.getcwd() + '/yolo_input/'
    output_data = output + '/data/'
    output_obj = output_data + 'obj/'
    if os.path.exists(output):
        shutil.rmtree(output)
    os.mkdir(output)
    os.mkdir(output_data)
    os.mkdir(output_obj)

    first_dir = True

    # For all files and folders in current directory
    for o in os.listdir(os.getcwd()):
        source = os.path.join(os.getcwd(), o)
        # Make sure we only get the output folders
        if not os.path.isdir(source) or "_output" not in o:
            continue
        # Copy all the files we only need once
        if first_dir:
            shutil.copyfile(source + '/yolo-obj.cfg', output + '/yolo-obj.cfg')
            shutil.copyfile(source + '/data/obj.names', output + '/data/obj.names')
            shutil.copyfile(source + '/data/obj.data', output + '/data/obj.data')
            first_dir = False
        # Copy all files in data/obj/
        copy_tree(os.path.join(source, "data/obj/"), output_obj)
        # Merge test and train files
        with open(os.path.join(source, "data/train.txt")) as f:
            with open(output_data + '/train.txt', "a+") as f1:
                for line in f:
                    f1.write(line) 
                f1.write('\n')
        with open(os.path.join(source, "data/test.txt")) as f:
            with open(output_data + '/test.txt', "a+") as f1:
                for line in f:
                    f1.write(line) 
                f1.write('\n')

    # Generate labels using script in darknet
    os.mkdir(output_data + 'labels/')
    os.chdir(output_data + 'labels/')
    runpy.run_path(base_directory + '/darknet/data/labels/make_labels.py')

if __name__ == '__main__':
    merge()

