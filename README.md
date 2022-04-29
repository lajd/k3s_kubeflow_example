# Installing full Kubeflow (or Kubeflow pipelines)

See the `installations/` directory for instructions to install either Kubeflow (using microk8s) or a simplified
installation of Kubeflow pipelines (using k3s) that supports GPUs.

# Setting up examples

Note: The below assumes Conda (e.g. Anaconda or MiniConda) is installed. See https://docs.conda.io/en/latest/miniconda.html for details.

```commandline
conda create -n local_kubeflow python=3.9
conda activate local_kubeflow
```

Install PyPi dependencies:
```commandline
pip install -r requirements.txt
```
