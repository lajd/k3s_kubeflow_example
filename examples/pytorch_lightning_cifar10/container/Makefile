IMAGE_NAME := "lajd94/kubeflow_examples:pytorch_lightning_example"

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -ti $(IMAGE_NAME) /bin/bash

push:
	docker push $(IMAGE_NAME)
