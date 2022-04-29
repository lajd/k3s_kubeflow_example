# Installing full Kubeflow (or Kubeflow pipelines)

See `installations/` directory

# Setting up examples

Note: The below assumes Conda (e.g. Anaconda or MiniConda) is installed. See https://docs.conda.io/en/latest/miniconda.html for details.

```commandline
conda create -n k3s_kubeflow_example python=3.9
conda activate k3s_kubeflow_example
```

Install PyPi dependencies:
```commandline
pip install -r requirements.txt
```
