import os.path
import requests

import kfp

from examples.simple_pipeline import THIS_DIR

HOST = 'http://10.64.140.43.nip.io'
USERNAME = "admin"
PASSWORD = "admin"
KUBEFLOW_DEPLOYMENT_NAMESPACE = "kubeflow"
USER_NAMESPACE = 'admin'
EXPERIMENT_NAME = 'test experiment'
JOB_NAME = 'simple pipeline job example'
PIPELINE_NAME = f"simple pipeline"


def get_client():
    # Method to connect to kubeflow pipelines when using Multi-User configuration
    session = requests.Session()
    response = session.get(HOST)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"login": USERNAME, "password": PASSWORD}
    session.post(response.url, headers=headers, data=data)
    session_cookie = session.cookies.get_dict()["authservice_session"]

    client = kfp.Client(
        host=f"{HOST}/pipeline",
        cookies=f"authservice_session={session_cookie}",
        namespace=KUBEFLOW_DEPLOYMENT_NAMESPACE,
    )
    client.list_experiments(namespace='kubeflow')
    return client


if __name__ == '__main__':

    client = get_client()

    # List pipelines
    client.list_pipelines()

    # Upload the pipeline
    simple_pipeline_id = client.get_pipeline_id(PIPELINE_NAME)

    if simple_pipeline_id:
        print(f"Pipeline with name {PIPELINE_NAME} already exists")
        simple_pipeline = client.get_pipeline(simple_pipeline_id)
    else:
        simple_pipeline = client.upload_pipeline(
            os.path.join(THIS_DIR, "simple_pipeline.py.tar.gz"),
            PIPELINE_NAME,
            "A simple pipeline for testing"
        )

    print(f"Pipeline ID: {simple_pipeline.id}")

    # Get the pipeline
    client.get_pipeline(simple_pipeline.id)

    # Create an experiment if not exists
    try:
        test_experiment = client.get_experiment(experiment_name=EXPERIMENT_NAME, namespace=USER_NAMESPACE)
        print(f"Experiment {EXPERIMENT_NAME} already exists in namespace {USER_NAMESPACE}")
    except ValueError:
        test_experiment = client.create_experiment(
            name=EXPERIMENT_NAME,
            description='An experiment for testing',
            namespace=USER_NAMESPACE
        )

    print(f"Test experiment ID: {test_experiment.id}")


    # Run a pipeline
    pipeline_run = client.run_pipeline(
        experiment_id=test_experiment.id,
        job_name=JOB_NAME,
        pipeline_id=simple_pipeline.id,
        params={
            "learning_rate": 0.1,
            "num_layers": 2,
            "optimizer": 'ftrl'
        },
    )

    # Wait for the run to complete
    run_resp = client.wait_for_run_completion(pipeline_run.id, timeout=300)
    print(run_resp)
