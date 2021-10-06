from abc import ABC, abstractclassmethod

class AbstractView(ABC):
    @abstractclassmethod
    def render(self):
        pass