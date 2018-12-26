import click
import os, tempfile
import cv2 as cv
import numpy as np
from runpy import run_path

# Have to import from darknet directory
os.chdir('darknet')
darknet = run_path('darknet.py')
os.chdir('..')

os.chdir('data/yolo_input/')
config_path = 'yolo-obj.cfg'
meta_path = 'data/obj.data'
weight_path = '../../models/yolo-obj.backup'

# Load yolo 
performDetect = darknet['performDetect']
performDetect(configPath=config_path, metaPath=meta_path, weightPath=weight_path, showImage=False, initOnly=True)

def printCoordinates(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        print("X: " + str(x))
        print("Y: " + str(y))

def create_rect(tl, tr, br, bl):
	rect = np.zeros((4, 2), dtype = "float32")
	rect[0] = tl
	rect[1] = tr
	rect[2] = br
	rect[3] = bl
	return rect


def four_point_transform(image, tl, tr, br, bl):
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))

	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))

	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")

	# compute the perspective transform matrix and then apply it
	M = cv.getPerspectiveTransform(create_rect(tl,tr,br,bl), dst)
	warped = cv.warpPerspective(image, M, (maxWidth, maxHeight))

	# return the warped image
	return warped


@click.argument('inputfile', type=click.Path())
@click.command()
def project(inputfile):
    cv.namedWindow("image")
    cv.setMouseCallback("image", printCoordinates)
    # Paths suck because darknet has to be run in the yolo_input folder
    inputfile = os.path.join('../..', inputfile)
    cap = cv.VideoCapture(inputfile)
    if not cap.isOpened():
        print("Error")
        return
    count = 0

    # Initialize a temporary file because performDetect requires a file on disk
    frame_file = tempfile.NamedTemporaryFile(suffix='.png')

    while cap.isOpened():
        ret,frame = cap.read()
        cv.imshow('image',frame)
        cv.imwrite(frame_file.name, frame)

        # Run detection
        # detection = performDetect(imagePath=frame_file.name, configPath=config_path, metaPath=meta_path, weightPath=weight_path, showImage=False)
        # print(detection)

        warped = four_point_transform(frame, (276,360),(1015,381),(1274,603),(6,551))
        cv.imshow('warped',warped)

        count = count + 1
        if cv.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    project()
