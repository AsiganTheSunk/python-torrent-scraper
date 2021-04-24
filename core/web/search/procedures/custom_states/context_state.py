from __future__ import annotations
from abc import ABC, abstractmethod


class Context(ABC):
    _state = None

    def __init__(self, state: State, job_name: str) -> None:
        self.job_name = job_name
        self.transition_to(state)

    def transition_to(self, state: State):
        self._state = state
        self._state.context = self

    def advance(self):
        self._state.next_state()
        # print(self._state.__class__.__name__)


class State(ABC):
    @property
    def context(self) -> Context:
        return self._context

    @context.getter
    def get_progress(self):
        pass

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def next_state(self) -> None:
        pass
