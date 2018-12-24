import click
import os
import shutil
from distutils.dir_util import copy_tree

@click.command()
def merge():
    os.chdir('data/')
    # Create output directory structure
    output = os.getcwd() + '/yolo_input/'
    output_data = output + '/data/'
    output_obj = output_data + 'obj/'
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
                f1.write('\n')
                for line in f:
                    f1.write(line) 
        with open(os.path.join(source, "data/test.txt")) as f:
            with open(output_data + '/test.txt', "a+") as f1:
                f1.write('\n')
                for line in f:
                    f1.write(line) 

if __name__ == '__main__':
    merge()
