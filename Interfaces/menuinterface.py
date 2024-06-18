from abc import ABC, abstractmethod

class ButtonInterface(ABC):
	@abstractmethod
	def update(self, screen) -> None:
		pass	
	@abstractmethod
	def checkForInput(self, position) -> bool:
		pass	
	@abstractmethod
	def changeColor(self, position) -> None:
		pass