# Running the spark operator in Kubeflow

This example is significantly based on the work of Sadik Bakiu found here: https://github.com/sbakiu/kubeflow-spark


## Setup the Spark kubernetes operator
```commandline
bash ./setup_spark.sh
```

## Run the pipeline

```commandline
python run_pipeline.py
```

Example output:

```bash
Pipeline with name spark pipeline already exists -- replacing
Pipeline ID: 21d70853-dfba-470e-919b-a956294a8507
Experiment test experiment already exists in namespace admin
Test experiment ID: 9c880fe9-84f8-42a9-a67f-4343ec66a188
{'pipeline_runtime': {'pipeline_manifest': None,
                      'workflow_manifest': '{"metadata":{"name":"spark-operator-job-pipeline-nbgzs","generateName":"spark-operator-job-pipeline-","namespace":"admin","selfLink":"/apis/argoproj.io/v1alpha1/namespaces/admin/workflows/spark-operator-job-pipeline-nbgzs","uid":"33b9c929-8afb-466a-b92a-c701b324985b","resourceVersion":"2349983","generation":6,"creationTimestamp":"2022-06-05T05:57:14Z","labels":{"pipeline/runid":"372f4409-85cf-47ad-8d2c-1fd4b75fe2aa","pipelines.kubeflow.org/kfp_sdk_version":"1.8.12","workflows.argoproj.io/completed":"true","workflows.argoproj.io/phase":"Succeeded"},"annotations":{"pipelines.kubeflow.org/kfp_sdk_version":"1.8.12","pipelines.kubeflow.org/pipeline_compilation_time":"2022-05-07T15:00:02.864662","pipelines.kubeflow.org/pipeline_spec":"{\\"description\\": '
...
```
