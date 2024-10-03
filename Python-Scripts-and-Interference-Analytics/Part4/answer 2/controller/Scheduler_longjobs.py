import docker
import subprocess
from Scheduler_logger import Job


class DockerController:
    '''CLass representing the controller for the parsec jobs

        :param logger: The (logger) of this class
        :type logger: SchedulerLogger
    '''

    def __init__(self, logger):
        self.client = docker.from_env()
        self.logger = logger
        self.jobs = dict()
        self.memcached_cores = 2
        blackscholes = self.create_parsec_job("2", "2", "blackscholes", "parsec", "anakli/cca:parsec_blackscholes")
        # dict {String: [number_of_threads, number_of_cores]}
        self.jobs[blackscholes] = ["2", "2", "short"]
        canneal = self.create_parsec_job("4", "2,3", "canneal", "parsec", "anakli/cca:parsec_canneal")
        self.jobs[canneal] = ["4", "2,3", "long"]
        dedup = self.create_parsec_job("1", "2", "dedup", "parsec", "anakli/cca:parsec_dedup")
        self.jobs[dedup] = ["1", "2", "short"]
        ferret = self.create_parsec_job("3", "2,3", "ferret", "parsec", "anakli/cca:parsec_ferret")
        self.jobs[ferret] = ["3", "2,3", "long"]
        freqmine = self.create_parsec_job("4", "2,3", "freqmine", "parsec", "anakli/cca:parsec_freqmine")
        self.jobs[freqmine] = ["4", "2,3", "long"]
        radix = self.create_parsec_job("1", "2", "radix", "splash2x", "anakli/cca:splash2x_radix")
        self.jobs[radix] = ["1", "2", "short"]
        vips = self.create_parsec_job("2", "2", "vips", "parsec", "anakli/cca:parsec_vips")
        self.jobs[vips] = ["2", "2", "short"]
        self.queue_short_jobs = [dedup, radix, blackscholes, vips]
        self.queue_long_jobs = [ferret, canneal, freqmine]
        self.running = []

    def create_parsec_job(self, number_of_threads, name_of_cores, name_of_container, parsec_or_splash, image):
        """Returns the parsec job container with the specified attributes

                :param number_of_threads: The number of threads of the container
                :type number_of_threads: str
                :param name_of_cores: The number of cores for the container
                :type name_of_cores: str
                :param name_of_container: The name of the container
                :type name_of_container: str
                :param parsec_or_splash: The type of the parsec benchmark
                :type parsec_or_splash: str
                :param image: The image of the container to be created
                :type image: str

                :returns: container
                :rtype: docker.Container
        """
        return self.client.containers.create(
            name=name_of_container,
            image=image,
            command=f"./run -a run -S {parsec_or_splash} -p {name_of_container} -i native -n {number_of_threads}",
            detach=True,
            auto_remove=False,
            cpuset_cpus=name_of_cores
        )

    def run_container(self, container):
        container.reload()
        if container.status == "paused":
            container.unpause()
            self.logger.job_unpause(container.name)
        elif container.status == "created":
            container.start()
            self.logger.job_start(container.name, self.jobs[container][1], self.jobs[container][0])

    def update_cores(self, container):
        container.reload()
        if container.status == "exited":
            return
        new_cores = ""
        if self.jobs[container][2] == "short":
            return
        if self.jobs[container][2] == "long" and self.memcached_cores == 1:
            new_cores = "1,2,3"
        elif self.jobs[container][2] == "long" and self.memcached_cores == 2:
            new_cores = "2,3"
        container.update(cpuset_cpus=new_cores)
        print("CHANGED CORES" + container.name + new_cores)
        self.logger.update_cores(container.name, new_cores)
        '''
        if cores == "2,3":
            container.pause()
            self.logger.job_pause(container.name)
        '''
        self.jobs[container][1] = new_cores

    def is_finished(self, container):
        container.reload()
        if container.status == "exited":
            print("REMOVED " + container.name)
            self.logger.job_end(container.name)
            container.remove()
            return True
        else:
            return False

    def add_job(self):
        run_short_job = True
        for job in self.queue_long_jobs:
            self.run_container(job)
            self.running.append(job)
            self.update_cores(job)
        self.queue_long_jobs = []
        for job in self.running:
            if self.jobs[job][2] == "short":
                run_short_job = False
        if len(self.running) < 4 and run_short_job and len(self.queue_short_jobs) != 0:
            new = self.queue_short_jobs[0]
            self.run_container(new)
            self.running.append(new)
            self.queue_short_jobs.remove(new)
            self.update_cores(new)

    def end_scheduler(self):
        self.logger.job_end("scheduler")


    def update(self, number_of_cores_memcached):
        cores_changed = False
        to_remove = []
        self.add_job()
        if number_of_cores_memcached != self.memcached_cores:
            cores_changed = True
            self.memcached_cores = number_of_cores_memcached
        for job in self.running:
            print(job.name)
            if self.is_finished(job):
                to_remove.append(job)
                continue
            if cores_changed:
                self.update_cores(job)

        for job in to_remove:
            self.running.remove(job)
            self.add_job()
        return len(self.running) + len(self.queue_short_jobs) + len(self.queue_long_jobs) == 0
