import logging
import argparse
import uuid

from kubernetes import client
from kubernetes import config

logging.basicConfig(level=logging.INFO)
config.load_incluster_config()

class Kubernetes:
    def __init__(self):

        # Init Kubernetes
        self.core_api = client.CoreV1Api()
        self.batch_api = client.BatchV1Api()

    @staticmethod
    def create_pod_template(pod_name, container):
        pod_template = client.V1PodTemplateSpec(
            spec=client.V1PodSpec(restart_policy="Never", containers=[container]),
            metadata=client.V1ObjectMeta(name=pod_name, labels={"pod_name": pod_name}),
        )

        return pod_template

    @staticmethod
    def create_job(job_id, job_arguments):
        container = client.V1Container(
            image="network-scapper-selenium-job:latest",
            name="selenium-job",
            image_pull_policy="Never",
            args=job_arguments,
            command=["python3", "-u", "job/selenium_job.py"],
        )

        logging.info(
            f"Created container with name: {container.name}, "
            f"image: {container.image} and args: {container.args}"
        )

        pod_name = f"selenium-job-pod-{job_id}"
        pod_template = client.V1PodTemplateSpec(
            spec=client.V1PodSpec(restart_policy="Never", containers=[container]),
            metadata=client.V1ObjectMeta(name=pod_name, labels={"pod_name": pod_name}),
        )


        job_name = f"selenium-job-{job_id}"
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=job_name, labels={"job_name": job_name}),
            spec=client.V1JobSpec(backoff_limit=0, template=pod_template),
        )

        logging.info(f"Created job with name: {job_name}")

        return job