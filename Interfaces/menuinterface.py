from abc import ABC, abstractmethod

class ButtonInterface(ABC):
	@abstractmethod
	def update(self, screen) -> None:
		pass	
	@abstractmethod
	def change_color(self, position) -> bool:
		pass	
	@abstractmethod
	def check_for_input(self, position) -> None:
		pass