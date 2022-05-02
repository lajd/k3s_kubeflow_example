import os.path
import requests

import kfp


def get_client(host: str = 'http://10.64.140.43.nip.io', username: str = 'admin', password: str = 'admin', kubeflow_deployment_ns: str = 'kubeflow'):
    # Method to connect to kubeflow pipelines when using Multi-User configuration
    session = requests.Session()
    response = session.get(host)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"login": username, "password": password}
    session.post(response.url, headers=headers, data=data)
    session_cookie = session.cookies.get_dict()["authservice_session"]

    client = kfp.Client(
        host=f"{host}/pipeline",
        cookies=f"authservice_session={session_cookie}",
        namespace=kubeflow_deployment_ns,
    )
    client.list_experiments(namespace='kubeflow')
    return client


##
def create_experiment_and_upload_pipeline(
        client: kfp.Client,
        pipeline_name: str,
        compiled_pipeline_path: str,
        pipeline_description: str,
        experiment_name: str,
        experiment_description: str,
        user_namespace: str = 'admin',
):

    client = get_client()

    # List pipelines
    client.list_pipelines()

    # Upload the pipeline
    pipeline_id = client.get_pipeline_id(pipeline_name)

    if pipeline_id:
        client.delete_pipeline(pipeline_id)

        print(f"Pipeline with name {pipeline_name} already exists -- replacing")
    pipeline = client.upload_pipeline(
        compiled_pipeline_path,
        pipeline_name,
        pipeline_description
    )

    print(f"Pipeline ID: {pipeline.id}")

    # Get the pipeline
    client.get_pipeline(pipeline.id)

    # Create an experiment if not exists
    try:
        experiment = client.get_experiment(experiment_name=experiment_name, namespace=user_namespace)
        print(f"Experiment {experiment_name} already exists in namespace {user_namespace}")
    except ValueError:
        experiment = client.create_experiment(
            name=experiment_name,
            description=experiment_description,
            namespace=user_namespace
        )

    print(f"Test experiment ID: {experiment.id}")
    return pipeline, experiment