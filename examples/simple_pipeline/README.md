# Simple pipeline example

Simple pipeline example based on https://github.com/kubeflow/examples/tree/master/demos/simple_pipeline

# Requirements: 
- Kubeflow installed in microk8s
- Kubeflow accessible via http://10.64.140.43.nip.io

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

