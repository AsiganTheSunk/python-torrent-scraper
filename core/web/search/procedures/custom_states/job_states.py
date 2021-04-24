from web.search.procedures.custom_states.context_state import State


class JobInitialized(State):
    def __init__(self):
        self.name = self.__class__.__name__
        self.job_state_progress = 10

    def get_progress(self):
        return self.job_state_progress

    def next_state(self) -> None:
        try:
            self.context.transition_to(JobRunning())
        except:
            self.context.transition_to(JobFailed())


class JobRunning(State):
    def __init__(self):
        self.name = self.__class__.__name__
        self.job_state_progress = 30

    def get_progress(self):
        return self.job_state_progress

    def next_state(self) -> None:
        try:
            self.context.transition_to(JobCompleted())
        except:
            self.context.transition_to(JobFailed())


class JobCompleted(State):
    def __init__(self):
        self.name = self.__class__.__name__
        self.job_state_progress = 100

    def get_progress(self):
        return self.job_state_progress

    def next_state(self) -> None:
        print('Job Completed')


class JobFailed(State):
    def __init__(self):
        self.name = self.__class__.__name__
        self.job_state_progress = 100

    def get_progress(self):
        return self.job_state_progress

    def next_state(self) -> None:
        print('Job Completed')
