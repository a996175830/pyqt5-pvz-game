
import math
import random
import sys

from PyQt5.QtGui import QPixmap, QPainter

from .base import Element
from PyQt5.QtCore import QTimer, QPoint, Qt, QSize, QRect
from PyQt5.QtWidgets import QApplication, QFrame, QGraphicsColorizeEffect, QLabel, QVBoxLayout, QPushButton




class CurrencyBase(Element):
	"""
	货币基类
	"""

	def __init__(self, p=None):
		super(CurrencyBase, self).__init__(p)
		self.param_init()

	def param_init(self):
		super(CurrencyBase, self).param_init()
		self.width_ = 20
		self.height_ = 20
		self.setFixedSize(QSize(self.width_, self.height_))

class CurrencyDiamond(CurrencyBase):
	"""
	钻石
	"""

	def __init__(self, p=None):
		super(CurrencyDiamond, self).__init__(p)


class CurrencyGoldDollar(CurrencyBase):
	"""
	金币
	"""

	def __init__(self, p=None):
		super(CurrencyGoldDollar, self).__init__(p)


class CurrencySilverDollar(CurrencyBase):
	"""
	银币
	"""

	def __init__(self, p=None):
		super(CurrencySilverDollar, self).__init__(p)
