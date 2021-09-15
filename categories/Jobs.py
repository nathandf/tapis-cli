from core.TapipyCategory import TapipyCategory
from tapipy.errors import InvalidInputError
from datetime import datetime

class Jobs(TapipyCategory):
    def __init__(self):
        TapipyCategory.__init__(self)

    def download(self, uuid, output_path) -> None:
        try:
            self.client.jobs.getJobOutputDownload(jobUuid=uuid, outputPath=output_path)
            self.logger.complete(f"Download complete for job {uuid}")
            return
        except InvalidInputError as e:
            self.logger.error(f"{e.message}")

    def get(self, uuid) -> None:
        try:
            job = self.client.jobs.getJob(jobUuid=uuid)
            self.logger.log(job)
            return
        except InvalidInputError:
            self.logger.error(f"Job not found with uuid '{uuid}'")

    def history(self, uuid) -> None:
        try:
            status = self.client.jobs.getJobHistory(jobUuid=uuid)
            self.logger.log(status)

            return
        except InvalidInputError:
            self.logger.error(f"Job not found with uuid '{uuid}'")
            self.exit(1)

    def status(self, uuid) -> None:
        try:
            status = self.client.jobs.getJobStatus(jobUuid=uuid)
            self.logger.log(status)

            return
        except InvalidInputError:
            self.logger.error(f"Job not found with uuid '{uuid}'")
            self.exit(1)

    def list(self) -> None:
        jobs = self.client.jobs.getJobList()
        self.logger.log(jobs)

    def submit(self, app_id, app_version, *args) -> None:
        # Set the name and description to datetime-appid-username
        name = f"{datetime.now()}-{app_id}-{self.client.username}"
        description = name
        # If the user specified args after the appid and appversion, we assume they
        # are passing name in the first arg and description in the second
        name = args[0] if len(args) >= 1 else name
        description = args[0] if len(args) > 1 else description

        try:
            job = self.client.jobs.submitJob(name=name, appId=app_id, appVersion=app_version, description=description)
            self.logger.info(f"Job submitted. Uuid: {job.uuid}")
            return
        except InvalidInputError as e:
            self.logger.error(e.message)
            self.exit(1)

    # TODO Some error
    def resubmit(self, uuid) -> None:
        try:
            self.client.jobs.resubmitJob(jobuuid=uuid)
            self.logger.info(f"Job resubmitted. Uuid: {uuid}")
            return
        except InvalidInputError as e:
            self.logger.error(e.message)
            self.exit(1)