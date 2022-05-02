import os.path
from examples.pytorch_lightning_cifar10 import THIS_DIR
from examples.utils import get_client, create_experiment_and_upload_pipeline

EXPERIMENT_NAME = 'test experiment'
EXPERIMENT_DESCRIPTION = "Experiment for examples"
JOB_NAME = 'PL pipeline job example'
JOB_DESCRIPTION = "Pytorch lightning pipeline example"
PIPELINE_NAME = "PL pipeline example"
COMPILED_PIPELINE_NAME = 'pl_train_pipeline.py.tar.gz'
USER_NAMESPACE = 'admin'


if __name__ == '__main__':

    client = get_client()

    pipeline, experiment = create_experiment_and_upload_pipeline(
        client,
        PIPELINE_NAME,
        os.path.join(THIS_DIR, COMPILED_PIPELINE_NAME),
        JOB_DESCRIPTION,
        EXPERIMENT_NAME,
        EXPERIMENT_DESCRIPTION,
        USER_NAMESPACE
    )

    # Run a pipeline
    pipeline_run = client.run_pipeline(
        experiment_id=experiment.id,
        job_name=JOB_NAME,
        pipeline_id=pipeline.id,
        params={
            "lr": 0.05,
            "momentum": 0.9,
            "wd": 5e-4,
            "max_lr": 0.1,
            "batch_size": 32,
            "num_workers": 4,
            "max_epochs": 1,
        },
    )

    # Wait for the run to complete
    run_resp = client.wait_for_run_completion(pipeline_run.id, timeout=600)
    print(run_resp)
