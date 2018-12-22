train-yolo:
	wget -nc https://pjreddie.com/media/files/yolov3.weights
	docker build --network host --ulimit nofile=1024 -t yolo .
	docker run --runtime=nvidia --volume=$(shell pwd):/code yolo
