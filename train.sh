#!/bin/sh
cd videos/6onyyYEM9ws_output/
/yolo/darknet/darknet detector train data/obj.data yolo-obj.cfg /code/yolov3.weights
/yolo/darknet/darknet detector detect backup/yolo-obj_final.weights ../6onyyYEM9ws.mp4
