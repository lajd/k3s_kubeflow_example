import os.path

from examples.spark import THIS_DIR
from examples.utils import get_client, create_experiment_and_upload_pipeline

USER_NAMESPACE = "admin"
EXPERIMENT_NAME = 'test experiment'
EXPERIMENT_DESCRIPTION = "Experiment for examples"
JOB_NAME = 'spark pipeline job example'
PIPELINE_NAME = "spark pipeline"
PIPELINE_DESCRIPTION = "spark pipeline example"
COMPILED_PIPELINE_NAME = 'spark_job_pipeline.yaml'


if __name__ == '__main__':
    client = get_client()

    pipeline, experiment = create_experiment_and_upload_pipeline(
        client,
        PIPELINE_NAME,
        os.path.join(THIS_DIR, COMPILED_PIPELINE_NAME),
        pipeline_description=PIPELINE_DESCRIPTION,
        experiment_name=EXPERIMENT_NAME,
        experiment_description=EXPERIMENT_DESCRIPTION,
        user_namespace=USER_NAMESPACE
    )

    # Run a pipeline
    pipeline_run = client.run_pipeline(
        experiment_id=experiment.id,
        job_name=JOB_NAME,
        pipeline_id=pipeline.id,
        params={},
    )

    # Wait for the run to complete
    run_resp = client.wait_for_run_completion(pipeline_run.id, timeout=300)
    print(run_resp)
