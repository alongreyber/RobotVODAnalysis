FROM nvidia/cuda:9.1-devel-ubuntu16.04

# working directory
WORKDIR /yolo

# addons
RUN \
	apt-get update && \
	apt-get install -y \
	wget git build-essential

# build repo
RUN \
	git clone https://github.com/pjreddie/darknet && \
	cd darknet && \
	make

WORKDIR /code
ADD train.sh .
# defaults command
#ENTRYPOINT ["/bin/bash"]
