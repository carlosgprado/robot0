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

		self.locked = False
		self._setup_pins()

		self.stop()

	def _setup_pins(self):
		gpio.setmode(gpio.BCM)

		gpio.setup(self.right_in, gpio.OUT)				
		gpio.setup(self.right_out, gpio.OUT)				
		gpio.setup(self.left_in, gpio.OUT)				
		gpio.setup(self.left_out, gpio.OUT)

	def check_lock(f):
		def wrapper(self, *args):
			if self.locked:
				print("[+] Motors are locked by software.")
			else:
				f(self, *args)
		return wrapper

	def stop(self):
		"""Collaborate and listen"""

		gpio.output(self.left_in, False)
		gpio.output(self.left_out, False)
		gpio.output(self.right_in, False)
		gpio.output(self.right_out, False)

	def lock(self):
		self.locked = True

	def unlock(self):
		self.locked = False

	def is_locked(self):
		return self.locked

	# ------------------------------------------------
	# Elementary movements (independent sides)
	# ------------------------------------------------
	@check_lock
	def _left_forward(self, timeout=0):
		gpio.output(self.left_in, False)
		gpio.output(self.left_out, True)

	@check_lock
	def _right_forward(self, timeout=0):
		gpio.output(self.right_in, False)
		gpio.output(self.right_out, True)

	@check_lock
	def _left_backward(self, timeout=0):
		gpio.output(self.left_in, True)
		gpio.output(self.left_out, False)

	@check_lock
	def _right_backward(self, timeout=0):
		gpio.output(self.right_in, True)
		gpio.output(self.right_out, False)
	
	# ------------------------------------------------
	# Basics movements (forward, backward, etc.)
	# These are combinations of elementary movements
	# ------------------------------------------------
	@check_lock
	def forward(self, timeout=0):
		"""Call without arguments to go forward forever"""

		# The combination defines the motor polarity
		# May need tweaking due to wrong cabling assumptions
		self._right_forward()
		self._left_forward()

		if timeout > 0:
			time.sleep(timeout)
			self.stop()

	@check_lock
	def backward(self, timeout=0):
		"""Call without arguments to go backwards forever"""

		self._right_backward()
		self._left_backward()

		if timeout > 0:
			time.sleep(timeout)
			self.stop()

	@check_lock
	def turn_right(self, timeout=0):
		"""Call without arguments to circle forever :)"""

		self._left_forward()

		if timeout > 0:
			time.sleep(timeout)
			self.stop()

	@check_lock
	def turn_left(self, timeout=0):
		"""Call without arguments to circle forever :)"""

		self._right_forward()

		if timeout > 0:
			time.sleep(timeout)
			self.stop()

	@check_lock
	def turn_right_backward(self, timeout=0):
		"""Call without arguments to circle forever"""

		self._left_backward()

		if timeout > 0:
			time.sleep(timeout)
			self.stop()

	@check_lock
	def turn_left_backward(self, timeout=0):
		"""Call without arguments to circle forever"""

		self._right_backward()

		if timeout > 0:
			time.sleep(timeout)
			self.stop()


