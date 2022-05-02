# Pytorch Lightning Cifar10 Example

Based on https://pytorch-lightning.readthedocs.io/en/stable/notebooks/lightning_examples/cifar10-baseline.html

# Overview
The container image has already been built and pushed to the repository `lajd94/kubeflow_examples:pytorch_lightning_example`.

To build your own custom image, modify the `IMAGE_NAME` variable in the `container/Makefile` and rebuild/push the image.

# Instructions

1. Compile the pipeline
Compile the simple_pipeline by running:
```commandline
python run_pipeline.py
```
and note that the `simple_pipeline.py.tar.gz` is created

2. Run the steps in `run_pipeline.py`

```commandline
python run_pipeline.py
```

Navigate to the UI and observe the newly created pipeline run:

http://10.64.140.43.nip.io/_/pipeline/?ns=admin#/runs
