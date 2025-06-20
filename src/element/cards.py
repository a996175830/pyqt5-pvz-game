import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QRect, QEasingCurve, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QImage, QMovie
from PyQt5.QtWidgets import QApplication, QLabel, QSizePolicy, QFrame, QVBoxLayout


class Element(QLabel):
	"""
	植物、僵尸、其他基础元素
	"""

	def __init__(self, p=None):
		super(Element, self).__init__(p)

	def param_init(self):
		self.height_ = 120

	def ui_init(self):
		pass

	def set_movie(self, gif_qrc):
		if ".gif" in gif_qrc:
			self.movie = QMovie(gif_qrc)  # 使用 QRC 文件中的 GIF
			self.movie.frameChanged.connect(self.update_frame)  # 连接到帧更新槽
			self.setMovie(self.movie)
			self.movie.start()
		else:
			self.setPixmap(QPixmap(gif_qrc))

	def update_frame(self, frame_number):
		"""
		更新当前帧，缩放图像
		:param frame_number: 当前帧编号
		"""
		frame = self.movie.currentPixmap()
		scaled_frame = frame.scaled(self.height_, self.height_, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		self.setPixmap(scaled_frame)


class BaseCard(Element):
	"""
	卡片基类
	"""
	style = """#cooling_mask{background-color:rgba(70,70,70,0.8);}"""
	card_clicked = pyqtSignal(str)
	card_hovered = pyqtSignal(bool)
	card_item_clicked = pyqtSignal(QObject, dict)

	def __init__(self, p=None):
		super(BaseCard, self).__init__(p)
		self.param_init()
		self.ui_re_init()
		self.setStyleSheet(self.style)

	def param_init(self):
		super(BaseCard, self).param_init()
		self.grayscale_pixmap = QPixmap()  # 不可种植状态
		self.original_pixmap = QPixmap()  # 可种植状态
		self.cursor_pixmap_str = ""  # 鼠标样式
		self.cooling = 0  # 冷却时间(秒)

	def ui_re_init(self):
		self.setFixedSize(QSize(65, 92))

	def set_card_item(self, card_item):
		"""
		设置卡片数据
		:param card_item:
		:return:
		"""
		card_pix = card_item['card_pix']
		self.cost = card_item['cost']
		self.cn_name = card_item['cn_name']
		self.set_movie(card_pix)
		self.cooling = card_item['cooling']  # 冷却时间
		self.original_pixmap = QPixmap(card_pix).scaled(65, 92)  # 确保路径正确
		self.cursor_pixmap_str = card_item['cursor_pix']  # 鼠标样式
		self.setPixmap(self.original_pixmap)  # 默认不可放置
		self.card_item = card_item


class CardItem(BaseCard):
	"""
	卡片基类
	"""
	style = """#cooling_mask{background-color:rgba(70,70,70,0.8);}"""
	cooling_is_finished = pyqtSignal()

	def __init__(self, p=None):
		super(BaseCard, self).__init__(p)
		self.ui_re_init()
		self.setStyleSheet(self.style)

	def ui_re_init(self):
		super(CardItem, self).ui_re_init()
		self.layout = QVBoxLayout()

		self.cooling_mask = QLabel(self)  # 冷却遮罩
		self.cooling_mask.setObjectName("cooling_mask")
		self.cooling_mask.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.cooling_mask.resize(self.size())

	def set_card_item(self, card_item):
		"""
		设置卡片数据
		:param card_item:
		:return:
		"""
		super(CardItem, self).set_card_item(card_item)
		self.grayscale_pixmap = self.to_grayscale(self.original_pixmap)
		self.setPixmap(self.grayscale_pixmap)  # 默认不可放置
		self.cooling_start()

	def cooling_start(self, ):
		"""
		冷却开始
		:param cooling_time: 冷却时间（秒）
		"""
		self.cooling_finished = False  # 是否能够种植
		self.can_cost_flag = False  # 是否买得起
		self.cooling_mask.setVisible(True)  # 显示遮罩
		self.animation = QPropertyAnimation(self.cooling_mask, b"geometry")
		self.animation.setDuration(self.cooling * 1000)  # 动画持续时间（毫秒）
		self.animation.setStartValue(QRect(0, 0, self.width(), self.height()))  # 从下往上开始
		self.animation.setEndValue(QRect(0, -self.height(), self.width(), self.height()))  # 最终隐藏在上面
		self.animation.setEasingCurve(QEasingCurve.Linear)
		self.animation.finished.connect(self.on_animation_finished)  # 连接信号到槽函数
		self.animation.start()

	def to_grayscale(self, pixmap):
		"""
		将图片转成灰色
		:param pixmap:
		:return:
		"""
		image = pixmap.toImage()
		image = image.convertToFormat(QImage.Format_Grayscale8)
		return QPixmap.fromImage(image)

	def change_card_status(self, can_cost_flag=False):
		"""
		设置当前卡片是否可用
		:param status: 卡片是否可用的标志
		"""
		self.can_cost_flag = can_cost_flag
		status = all([self.cooling_finished, self.can_cost_flag])
		if status:
			self.setPixmap(self.original_pixmap)
		else:
			self.setPixmap(self.grayscale_pixmap)
		cursor = Qt.PointingHandCursor if status else Qt.ArrowCursor
		self.setCursor(cursor)

	def on_animation_finished(self):
		"""
		动画结束时执行的操作
		"""
		self.cooling_finished = True
		self.change_card_status()  # 更新卡片状态为可用
		self.cooling_is_finished.emit()

	def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
		self.cooling_mask.resize(self.size())
		super(BaseCard, self).resizeEvent(a0)

	def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
		if ev.button() == Qt.LeftButton:
			if all([self.cooling_finished, self.can_cost_flag]):
				self.card_clicked.emit(self.cursor_pixmap_str)
			else:
				self.card_clicked.emit("")
		super(BaseCard, self).mouseReleaseEvent(ev)


class PlantCard(CardItem):
	"""
	植物卡片
	"""

	def __init__(self, p=None):
		super(PlantCard, self).__init__(p)
		if 0:
			self.set_card_item({
				"id": 1,
				"name": "sun_flower",
				"cn_name": "向日葵",
				"pix": ":images/cards/card_sf.png",
				"put_pix": ":images/plants/sun_flower.gif",
				"cursor_pix": ":images/plants/sf_static.png",
				"cost": 50,
				"damage": 0,
				"hp": 150,
				"cooling": 1,
				"gap": 8,
				"sun_production": 25,
				"desc": "产生阳光，经济实惠"
			})

	def enterEvent(self, a0: QtCore.QEvent) -> None:
		self.card_hovered.emit(True)
		super(PlantCard, self).enterEvent(a0)

	def leaveEvent(self, a0: QtCore.QEvent) -> None:
		self.card_hovered.emit(False)
		super(PlantCard, self).leaveEvent(a0)


class SimpleCard(BaseCard):
	"""
	一般卡片
	"""

	def __init__(self, p=None):
		super(SimpleCard, self).__init__(p)
		self.param_re_init()
		self.layer_init()

	def param_re_init(self):
		self.is_selected = False  # 默认没被选择
		self.card_item = dict()

	def layer_init(self):
		self.layer_label = QLabel(self)
		self.layer_label.setObjectName("layer_label")
		self.layer_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.layer_label.resize(self.size())

	def change_card_selected_status(self):
		"""
		更改被选择状态
		:param status:
		:return:
		"""
		self.is_selected = not self.is_selected
		style = """""" if self.is_selected is False else """#layer_label{background-color:rgba(10,10,10,0.6);border-radius:4px;}"""
		self.setStyleSheet(style)

	def enterEvent(self, a0: QtCore.QEvent) -> None:
		self.card_hovered.emit(True)
		super(SimpleCard, self).enterEvent(a0)

	def leaveEvent(self, a0: QtCore.QEvent) -> None:
		self.card_hovered.emit(False)
		super(SimpleCard, self).leaveEvent(a0)

	def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
		if ev.button() == Qt.LeftButton:
			self.card_item_clicked.emit(self, self.card_item)
			if self.is_selected: return
		super(SimpleCard, self).mouseReleaseEvent(ev)

	def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
		self.layer_label.resize(self.size())


class ZombieCard(SimpleCard):
	"""
	僵尸卡片
	"""
	style = """#zombieCard{border:4px solid rgb(90,87,134);border-radius:6px;background-color:rgb(67,65,86)}"""

	def __init__(self, p=None):
		super(ZombieCard, self).__init__(p)
		self.setStyleSheet(self.style)

	def ui_re_init(self):
		super(ZombieCard, self).ui_re_init()
		self.setObjectName("zombieCard")

	def set_card_item(self, card_item):
		self.set_movie(card_item.get("idle_pix", ""))
		self.card_item = card_item


class EmptyCard(QFrame):
	"""
	空卡片
	"""
	style = """#emptyCard{background-color:rgb(95,48,20);border-radius:4px; }#emptyCard:hover{background-color:rgb(110,59,30)}"""

	def __init__(self, p=None):
		super(EmptyCard, self).__init__(p)
		self.ui_init()

	def ui_init(self):
		self.setFixedSize(QSize(65, 92))
		self.setObjectName("emptyCard")
		self.setStyleSheet(self.style)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	win = PlantCard()
	win.show()
	sys.exit(app.exec_())
