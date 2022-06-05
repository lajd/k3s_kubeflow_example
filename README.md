# Installing full Kubeflow (or Kubeflow pipelines)

See the `installations/` directory for instructions to install either Kubeflow (using microk8s) or a simplified
installation of Kubeflow pipelines (using k3s) that supports GPUs.


## Installation options
### K3s Kubeflow Pipelines installation with GPU support
- [Installation instructions](installations/k3s_kfp_gpu/README.md)

### Micro k8s full Kubeflow installation (No GPU support)
- [Installation instructions](installations/microk8s_kf/README.md)

# Setting up examples

Note: The below assumes Conda (e.g. Anaconda or MiniConda) is installed. See https://docs.conda.io/en/latest/miniconda.html for details.

```commandline
conda create -n local_kubeflow python=3.9
conda activate local_kubeflow
```

Install package and PyPi dependencies:
```commandline
pip install -e .
```

## Simple pipeline
Try an example pipeline in `examples/simple_pipeline/README.md`

## Pytorch Lightning pipeline
Try an example pipeline in `examples/pytorch_lightning_cifar10/README.md`

## Spark submit example pipeline
Try an example pipeline in `examples/spark/README.md`

