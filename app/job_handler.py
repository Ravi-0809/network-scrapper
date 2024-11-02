import uuid
from k8s_utils import Kubernetes

kube_namespace = "scrapper"

def create_jobs(processed_data):
    k8s = Kubernetes()

    for idx, data in enumerate(processed_data):
        job_id = str(uuid.uuid4())
        job_arguments = [data["url"], "--username", data["username"], "--password", data["password"]]

        print(f"Starting job number {idx+1} - {job_id}")
        print(f"args - {job_arguments}")

        job = k8s.create_job(job_id=job_id, job_arguments=job_arguments)
        k8s.batch_api.create_namespaced_job(kube_namespace, job)
        print(f"Started")
        print()
        print("-----")
        print()
