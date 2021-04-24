from core.web.search.procedures.custom_states.context_state import State


class TaskInitialized(State):
    def __init__(self):
        self.name = self.__class__.__name__
        self.task_state_progress = 10

    def get_progress(self):
        return self.task_state_progress

    def next_state(self) -> None:
        try:
            self.context.transition_to(TaskProcessing())
        except:
            self.context.transition_to(TaskFailed())


class TaskProcessing(State):
    def __init__(self):
        self.name = self.__class__.__name__
        self.task_state_progress = 20

    def get_progress(self):
        return self.task_state_progress

    def next_state(self) -> None:
        try:
            self.context.transition_to(TaskExecuted())
        except:
            self.context.transition_to(TaskFailed())


class TaskExecuted(State):
    def __init__(self):
        self.name = self.__class__.__name__
        self.task_state_progress = 33

    def get_progress(self):
        return self.task_state_progress

    def next_state(self) -> None:
        try:
            self.context.transition_to(TaskWaiting())
        except:
            self.context.transition_to(TaskFailed())


class TaskWaiting(State):
    def __init__(self):
        self.name = self.__class__.__name__
        self.task_state_progress = 40

    def get_progress(self):
        return self.task_state_progress

    def next_state(self) -> None:
        try:
            self.context.transition_to(TaskCompleted())
        except:
            self.context.transition_to(TaskFailed())


class TaskCompleted(State):
    def __init__(self):
        self.name = self.__class__.__name__
        self.task_state_progress = 100

    def get_progress(self):
        return self.task_state_progress

    def next_state(self) -> None:
        print('Job Completed')


class TaskFailed(State):
    def __init__(self):
        self.name = self.__class__.__name__
        self.task_state_progress = 100

    def get_progress(self):
        return self.task_state_progress

    def next_state(self) -> None:
        print('Job Completed')
