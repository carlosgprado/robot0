# ----------------------------------------
# Motor(s) controller
#
# L298N Pinout
# ------------
# 
# - In1 Blue GPIO 23
# - In2 Yellow GPIO 24
# - In3 Green GPIO 22
# - In4 White GPIO 27
# ----------------------------------------

import time
import RPi.GPIO as gpio


class MotorController:
	def __init__(self):
		self.right_in = 23  # In1
		self.right_out = 24 # In2
		self.left_in = 22	# In3
		self.left_out = 27	# In4

		self._setup_pins()

		self.stop()

	def _setup_pins(self):
		gpio.setmode(gpio.BCM)

		gpio.setup(self.right_in, gpio.OUT)				
		gpio.setup(self.right_out, gpio.OUT)				
		gpio.setup(self.left_in, gpio.OUT)				
		gpio.setup(self.left_out, gpio.OUT)

	def stop(self):
		"""Collaborate and ilsten"""
		gpio.output(self.left_in, False)
		gpio.output(self.left_out, False)
		gpio.output(self.right_in, False)
		gpio.output(self.right_out, False)

	# ------------------------------------------------
	# Elementary movements (independent sides)
	# ------------------------------------------------
	def _left_forward(self, timeout=0):
		gpio.output(self.left_in, False)
		gpio.output(self.left_out, True)

	def _right_forward(self, timeout=0):
		gpio.output(self.right_in, False)
		gpio.output(self.right_out, True)

	def _left_backward(self, timeout=0):
		gpio.output(self.left_in, True)
		gpio.output(self.left_out, False)

	def _right_backward(self, timeout=0):
		gpio.output(self.right_in, True)
		gpio.output(self.right_out, False)
	
	# ------------------------------------------------
	# Basics movements (forward, backward, etc.)
	# These are combinations of elementary movements
	# ------------------------------------------------
	def forward(self, timeout=0):
		self._setup_pins()

		# The combination defines the motor polarity
		# May need tweaking due to wrong cabling assumptions
		self._right_forward()
		self._left_forward()

		time.sleep(timeout)
		gpio.cleanup()

	def backward(self, timeout=0):
		self._setup_pins()

		self._right_backward()
		self._left_backward()

		time.sleep(timeout)
		gpio.cleanup()

	def turn_right(self, timeout=0):
		self._setup_pins()

		self._left_forward()

		time.sleep(timeout)
		gpio.cleanup()
	
