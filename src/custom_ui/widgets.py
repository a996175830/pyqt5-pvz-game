import copy
import random
import sys
from functools import partial

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QTimer, QPropertyAnimation, QPoint, QRect, \
	QEasingCurve, QParallelAnimationGroup, QObject, QUrl, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QMovie, QFontDatabase, QFont, QFontMetrics, QTransform, QMatrix4x4, \
	QVector3D, QColor
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QSpacerItem, QSizePolicy, QLabel, QHBoxLayout, QVBoxLayout, QFrame, \
	QWidget, QGridLayout, \
	QStackedWidget, QSlider, QGraphicsDropShadowEffect, QPushButton, QDialog, QCheckBox, \
	QFormLayout, QGraphicsColorizeEffect, QProgressBar
from src.config import normal_conf, game_conf, item_desc
from src.element.cards import PlantCard, SimpleCard, EmptyCard, ZombieCard
from src.element.others import ZombieHandElement, DaveDialogElement, DaveElement
from src.element.zombies import PrepareZombie
from src.signal_bus import bus
from src.my_util.utils import clear_layout, read_saved_file, save_to_saved_file, query_item_infos, convert_cooling
from src.resources import resource_rc


class HPLine(QProgressBar):
	"""
	体力条
	"""

	def __init__(self, parent=None):
		super(HPLine, self).__init__(parent)
		self.init_ui()

	def init_ui(self):
		self.setFixedSize(QSize(95, 14))
		self.setMinimum(0)
		self.setMaximum(100)

		# 设置进度条的样式
		self.setStyleSheet("""
            QProgressBar {
                border: 1px solid #3C3C3C;
                border-radius: 3px;
                background-color: rgba(85, 49, 62,0.7); /* 背景颜色 */
                text-align: center; /* 文本水平居中 */
                padding: 0px; /* 去除内部填充 */
                color: transparent;
            }
            QProgressBar::chunk {
                background-color: red; /* 有值的部分颜色 */
            }
        """)

		self.layout = QHBoxLayout()
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.layout.setSpacing(0)
		self.hp_value = QLabel()
		self.hp_value.setStyleSheet("color: green;")  # 设置标签字体颜色
		self.hp_value.setAlignment(Qt.AlignCenter)  # 标签内容居中
		self.layout.addWidget(self.hp_value)  # 添加标签到布局
		self.layout.setAlignment(self.hp_value, Qt.AlignCenter)  # 标签内容居中
		self.setLayout(self.layout)


class NormalWordLabel(QLabel):
	"""
	通用文字组件
	"""
	clicked = pyqtSignal()

	def __init__(self, p=None, font_size="10", bold=False, color="black", hover_color="black", bg_color="white"):
		super(NormalWordLabel, self).__init__(p)
		self.font_size = font_size
		self.bold = bold
		self.color = color
		self.bg_color = bg_color
		self.hover_color = hover_color
		self.ui_init()

	def ui_init(self):
		self.setObjectName("normalWordLabel")
		font_weight = "600" if self.bold else "100"
		font_db = QFontDatabase()
		font_id = font_db.addApplicationFont(":font/petitesmile-51jrz.ttf")
		if font_id != -1:
			font_family = font_db.applicationFontFamilies(font_id)[0]
		else:
			font_family = "Arial"  # 使用默认字体作为备选
		self.setStyleSheet(
			"""#normalWordLabel{color:%s;background-color:%s;font-weight:%s;font-size:%spt;font-family:"%s"}#normalWordLabel:hover{color:%s}""" % (
				self.color, self.bg_color,
				font_weight,
				self.font_size, font_family, self.hover_color))

	def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
		self.clicked.emit()
		super(NormalWordLabel, self).mouseReleaseEvent(ev)


class ImageLabel(QLabel):
	clicked = pyqtSignal()
	hovered = pyqtSignal(bool)

	def __init__(self, p=None):
		super(ImageLabel, self).__init__(p)

	def ui_init(self):
		self.setScaledContents(True)

	def set_pix(self, pix_path):
		if isinstance(pix_path, QPixmap):
			self.setPixmap(pix_path)
		else:
			self.setPixmap(QPixmap(pix_path))

	def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
		self.clicked.emit()
		super(ImageLabel, self).mouseReleaseEvent(ev)

	def enterEvent(self, a0: QtCore.QEvent) -> None:
		self.hovered.emit(True)
		super(ImageLabel, self).enterEvent(a0)

	def leaveEvent(self, a0: QtCore.QEvent) -> None:
		self.hovered.emit(False)
		super(ImageLabel, self).leaveEvent(a0)


class GameDialogBase(QDialog):
	"""
	菜单对话框
	"""

	def __init__(self, p=None):
		super(GameDialogBase, self).__init__(p)
		self.ui_init()

	def ui_init(self):
		self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setFixedSize(QSize(350, 350))
		self.setModal(Qt.ApplicationModal)

	def paintEvent(self, event):
		super(GameDialogBase, self).paintEvent(event)
		painter = QPainter(self)
		pixmap = QPixmap(':images/others/prepare/menu.png')  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()

	# 无边框的拖动
	def mouseMoveEvent(self, e: QtGui.QMouseEvent):  # 重写移动事件
		try:
			self._endPos = e.pos() - self._startPos
			self.move(self.pos() + self._endPos)
		except (AttributeError, TypeError):
			pass

	def mousePressEvent(self, e: QtGui.QMouseEvent):
		if e.button() == QtCore.Qt.LeftButton:
			self._isTracking = True
			self._startPos = QtCore.QPoint(e.x(), e.y())

	def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
		if e.button() == QtCore.Qt.LeftButton:
			self._isTracking = False
			self._startPos = None
			self._endPos = None


class MenuDialog(GameDialogBase):
	"""
	菜单对话框
	"""

	def __init__(self, p=None):
		super(MenuDialog, self).__init__(p)
		self.ui_re_init()
		self.set_up_ui()
		self.slot_init()

	def ui_re_init(self):
		self.layout = QVBoxLayout()
		self.top_layout = QVBoxLayout()
		self.top_layout.setSpacing(5)
		self.top_layout.setContentsMargins(10, 50, 10, 30)
		self.layout.setContentsMargins(10, 10, 10, 30)
		self.cancel_btn = NormalStyleButton(self, "继续游戏", ":images/others/prepare/button.png")
		self.new_game_btn = NormalStyleButton(self, "新·游戏", ":images/others/prepare/button.png")
		self.back_btn = NormalStyleLabel(self, )
		self.top_layout.addWidget(self.cancel_btn)
		self.top_layout.addWidget(self.new_game_btn)
		self.top_layout.setAlignment(self.cancel_btn, Qt.AlignHCenter | Qt.AlignBottom)
		self.top_layout.setAlignment(self.new_game_btn, Qt.AlignHCenter | Qt.AlignBottom)
		self.layout.addLayout(self.top_layout)
		self.layout.addWidget(self.back_btn)
		self.layout.setStretch(0, 10)
		self.layout.setStretch(1, 1)
		self.layout.setAlignment(self.back_btn, Qt.AlignHCenter | Qt.AlignBottom)
		self.setLayout(self.layout)

	def set_up_ui(self):
		self.back_btn.setText("返回")

	def slot_init(self):
		self.back_btn.clicked.connect(self.close)

	def reject(self):
		pass

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			pass
		else:
			super(MenuDialog, self).keyPressEvent(event)


class CustomSlider(QSlider):
	def __init__(self, parent=None):
		super().__init__(Qt.Horizontal, parent)
		self.setMinimum(0)
		self.setMaximum(100)
		# 应用QSS样式表
		self.setStyleSheet("""
		            QSlider::groove:horizontal {
		                background: rgb(24, 25, 30);
		                height: 3px;
		                border-radius:2px;
		            }

		            QSlider::handle:horizontal {
		                image: url(:images/others/prepare/handle.png);
		                width: 20px;  /* 图片的宽度 */
		                height: 30px; /* 图片的高度 */
		                margin: -14px 0px;  /* 使图片居中于滑槽 */
		            }

		            QSlider::groove:horizontal:hover {
		                background: rgb(30, 32, 36);
		            }
		        """)


class NormalCheckBox(QCheckBox):
	color1 = "rgb(43,46,57)"
	style = """
	#normalCheckBox{
			color:%s;
			font-size:11pt;
			font-weight:520;
	}
	#normalCheckBox::indicator::unchecked{ 
			width: 12px;  
			height: 12px;  
			border:5px solid rgb(94,95,126);
			border-radius:4px;
			background-color:%s}
	#normalCheckBox::indicator::checked{ 
			width: 12px;  
			height: 12px;
			image:url(:images/others/prepare/tick.png);
			border:5px solid rgb(94,95,126);
			border-radius:4px;
			background-color:%s}
                """ % (color1, color1, color1)

	def __init__(self, p=None):
		super(NormalCheckBox, self).__init__(p)
		self.setObjectName("normalCheckBox")
		self.setCheckState(Qt.Unchecked)  # 初始化状态
		self.setContentsMargins(30, 20, 0, 0)
		self.setStyleSheet(self.style)
		self.setFixedSize(QSize(30, 30))


class MianSetItems(QWidget):
	"""
	菜单设置项目
	"""

	def __init__(self, p=None):
		super(MianSetItems, self).__init__(p)
		self.ui_init()
		self.set_up_ui()

	def ui_init(self):
		self.setObjectName("mianSetItems")
		self.layout = QFormLayout()
		self.layout.setSpacing(20)
		self.music_set_label = NormalWordLabel(self, color="rgb(131,133,176)", hover_color="rgb(131,133,176)",
											   bg_color="rgb(55,57,69)", font_size="15", bold=True)
		self.bg_music_slider = CustomSlider(self)

		self.effect_set_label = NormalWordLabel(self, color="rgb(131,133,176)", hover_color="rgb(131,133,176)",
												bg_color="rgb(55,57,69)", font_size="15", bold=True)
		self.effect_slider = CustomSlider(self)

		self.three_d_sepped = NormalWordLabel(self, color="rgb(131,133,176)", hover_color="rgb(131,133,176)",
											  bg_color="rgb(55,57,69)", font_size="15", bold=True)
		self.three_d_check_box = NormalCheckBox(self)

		self.show_hp_flag = NormalWordLabel(self, color="rgb(131,133,176)", hover_color="rgb(131,133,176)",
											bg_color="rgb(55,57,69)", font_size="15", bold=True)
		self.show_hp_check_box = NormalCheckBox(self)

		self.layout.addRow(self.music_set_label, self.bg_music_slider)
		self.layout.addRow(self.effect_set_label, self.effect_slider)
		self.layout.addRow(self.three_d_sepped, self.three_d_check_box)
		self.layout.addRow(self.show_hp_flag, self.show_hp_check_box)
		self.setLayout(self.layout)

	def set_up_ui(self):
		self.music_set_label.setText("音乐")
		self.effect_set_label.setText("音效")
		self.three_d_sepped.setText("2D 加速")
		self.show_hp_flag.setText("显示体力")
		self.bg_music_slider.setValue(50)
		self.effect_slider.setValue(100)
		self.three_d_check_box.setChecked(True)


class MainSetDialog(GameDialogBase):
	"""
	游戏设置
	"""
	style = """#confirm_btn{color:rgb(62,204,84);background-color:transparent;font-size:26pt;font-weight:800 pt;}"""

	def __init__(self, p=None):
		super(MainSetDialog, self).__init__(p)
		self.ui_re_init()
		self.slot_init()
		self.setStyleSheet(self.style)

	def ui_re_init(self):
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(70, 90, 60, 20)
		self.mianSetItems = MianSetItems(self)
		self.confirm_btn = ButtonBase(self)
		self.confirm_btn.setObjectName("confirm_btn")
		self.confirm_btn.setText("确定")
		self.layout.addWidget(self.mianSetItems)
		self.layout.addWidget(self.confirm_btn)
		self.layout.setAlignment(self.confirm_btn, Qt.AlignBottom)
		self.setLayout(self.layout)

	def slot_init(self):
		self.confirm_btn.clicked.connect(self.hide)


class NormalStyleLabel(NormalWordLabel):
	def __init__(self, p=None):
		super(NormalStyleLabel, self).__init__(p, font_size="13", color="rgb(0,194,0)", bg_color="transparent",
											   hover_color="white")

		self.setCursor(Qt.PointingHandCursor)


class NormalStyleButton(ImageLabel):
	"""
	个性化按钮
	"""

	def __init__(self, p=None, text="", pix=""):
		super(NormalStyleButton, self).__init__(p)
		self.ui_init()
		self.btn_label.setText(text)
		self.set_pix(pix)

	def ui_init(self):
		self.setCursor(Qt.PointingHandCursor)
		self.layout = QHBoxLayout()
		self.layout.setContentsMargins(3, 3, 3, 3)
		self.btn_label = NormalStyleLabel(self, )
		self.layout.addWidget(self.btn_label)
		self.layout.setAlignment(self.btn_label, Qt.AlignHCenter)
		self.setLayout(self.layout)


class NormaGrassItem(QFrame):
	"""
	单个草坪
	"""
	grass_clicked = pyqtSignal()

	def __init__(self, p=None):
		super(NormaGrassItem, self).__init__(p)
		self.param_init()
		self.ui_re_init()
		if 0:
			self.setStyleSheet("""background-color:lightblue;""")

	def param_init(self):
		self.width_ = normal_conf.noswimming_grass_width
		self.height_ = normal_conf.noswimming_grass_height
		self.has_plant = False  # 是否有植物

	def ui_re_init(self):
		self.setFixedSize(QSize(self.width_, self.height_))
		self.grass_layout = QVBoxLayout()
		self.grass_layout.setContentsMargins(3, 3, 3, 3)
		self.setLayout(self.grass_layout)

	def set_plant_item(self, plant_item, show_hp=True):
		"""
		:return:
		"""
		if plant_item.plant_type != 1:
			plant_item.hp_line.setVisible(show_hp)
		else:
			plant_item.hp_line.setVisible(False)
		self.grass_layout.insertWidget(0, plant_item)
		self.grass_layout.setAlignment(plant_item, Qt.AlignHCenter | Qt.AlignVCenter)
		bus.sunshine_cost.emit(plant_item.cost)
		self.has_plant = True

	def clear_plant(self):
		clear_layout(self.grass_layout)
		self.has_plant = False

	def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
		if a0.button() == Qt.LeftButton:
			self.grass_clicked.emit()


class SwimmingArea(QWidget):
	"""
	泳池区域
	"""

	def __init__(self, p=None, row_number=3, map_id=3):
		super(SwimmingArea, self).__init__(p)
		self.setParent(p)
		self.row_number = row_number
		self.map_id = map_id
		self.ui_init()

	def ui_init(self):
		self.setContentsMargins(0, 0, 0, 0)
		self.gif_label = QLabel(self)
		self.gif_label.setGeometry(self.rect())
		self.gif_label.setAlignment(Qt.AlignCenter)
		gif_path = ""
		if self.row_number in [2, 3]:
			if self.map_id == 3:
				gif_path = ":images/others/pool.gif"
			elif self.map_id == 4:
				gif_path = ":images/others/pool_night.gif"
		self.movie = QMovie(gif_path)
		self.gif_label.setMovie(self.movie)
		self.movie.start()
		self.gif_label.setScaledContents(True)

	def resizeEvent(self, event):
		super().resizeEvent(event)
		# 调整 QLabel 的大小以适应 QFrame
		self.gif_label.setGeometry(self.rect())


class Lawn(QWidget):
	"""
	场景
	"""

	def __init__(self, parent=None):
		super(Lawn, self).__init__(parent)
		self.param_init()
		self.ui_param_init()

	def param_init(self):
		self.row_y_list = [65, 197, 329, 461, 593]  # 每条路线y值
		self.grid_cols = normal_conf.max_grass_col

	def load_map_ui(self, map_id, is_first=False):
		self.map_id = map_id
		if is_first is False:
			self.scene_init()
		self.init_ui()
		self.load_grass()
		self.update_row_rects()

	def scene_init(self):
		"""
		重新初始化场景，删除所有子控件，清空布局，确保所有数据被重置。
		"""
		clear_layout(self.grass_layout)
		for frame in self.row_frames:
			try:
				frame.deleteLater()
			except:
				pass
		self.row_frames = []
		for grass_item in self.grass_items.values():
			try:
				grass_item.deleteLater()
			except:
				pass

		self.grass_items = {}
		clear_layout(self.layout)
		self.row_y_list = []  # 重置行的y坐标列表
		self.grid_cols = normal_conf.max_grass_col  # 重置列数
		try:
			self.lawn_left_widget.deleteLater()
		except:
			pass
		try:
			self.lawn_right_widget.deleteLater()
		except:
			pass

	def ui_param_init(self):
		self.layout = QHBoxLayout()
		self.layout.setSpacing(0)
		self.setLayout(self.layout)

	def init_ui(self):
		self.setMinimumHeight(655)
		self.lawn_left_widget = QWidget(self)
		self.lawn_right_widget = QWidget(self)
		self.lawn_left_widget.setFixedWidth(80)
		self.lawn_right_widget.setFixedWidth(80)
		if self.map_id in [3, 4]:
			self.grid_rows = 6
		else:
			self.grid_rows = 5
		self.setContentsMargins(-10, 0, 0, 10)
		if self.map_id in [3, 4]:
			self.layout.setContentsMargins(25, 45, 85, 0)
		else:
			self.layout.setContentsMargins(40, 0, 85, 0)
		self.load_frames()
		self.layout.addWidget(self.lawn_left_widget)
		self.layout.addLayout(self.grass_layout)
		self.layout.addWidget(self.lawn_right_widget)

	def load_frames(self):
		"""
		加载水平冰道
		"""
		self.row_frames = []
		self.grass_layout = QVBoxLayout()
		for row_number in range(self.grid_rows):
			row_frame = SwimmingArea(self, row_number, self.map_id)
			row_frame.setObjectName("row_frame")
			row_frame.setMinimumHeight(int(self.height() / self.grid_rows))
			row_layout = QHBoxLayout(row_frame)
			row_layout.setContentsMargins(0, 0, 0, 0)
			row_layout.setSpacing(0)
			self.row_frames.append(row_frame)
			self.grass_layout.addWidget(row_frame)
		self.grass_layout.setSpacing(3)
		self.update_row_rects()

	def load_grass(self):
		"""
		加载草坪
		"""
		self.grass_items = {}  # 用于存储所有草坪项的字典
		for row in range(self.grid_rows):
			row_frame = self.row_frames[row]
			row_layout = row_frame.layout()
			for col in range(self.grid_cols):
				coordinate = (row, col)
				item = NormaGrassItem(self)
				item.grass_clicked.connect(lambda coord=coordinate: bus.lawn_chunk_clicked.emit(coord))
				self.grass_items[coordinate] = item
				row_layout.addWidget(item)

	def update_row_rects(self):
		"""
		更新每行的矩形区域，并更新 row_y_list 以存储每行的中心位置
		"""
		self.row_y_list = []
		layout_rect = self.geometry()
		row_height = layout_rect.height() / self.grid_rows
		for row in range(self.grid_rows):
			y = row * row_height + row_height / 2
			self.row_y_list.append(int(y))

	def resizeEvent(self, event) -> None:
		"""
		窗口缩放，重新计算每行的矩形区域
		"""
		try:
			self.update_row_rects()
		except:
			pass
		super(Lawn, self).resizeEvent(event)  # 调用基类的方法以保持标准行为


class SunFlowerBasket(ImageLabel):
	"""
	收藏阳光的篮子
	"""

	def __init__(self, p=None):
		super(SunFlowerBasket, self).__init__(p)
		self.ui_init()
		if 0:
			self.change_current_sun_num(50)

	def ui_init(self):
		self.setObjectName("funFlowerBasket")
		self.layout = QVBoxLayout()
		self.setFixedSize(QSize(80, 100))
		self.layout.setContentsMargins(13, 10, 15, 10)
		self.current_sun_label = NormalWordLabel(self, font_size="14", color="black", bg_color="rgb(242,236,174)",
												 bold=False)
		self.current_sun_label.setFixedHeight(20)
		self.current_sun_label.setMinimumWidth(55)
		self.current_sun_label.setAlignment(Qt.AlignCenter)
		self.current_sun_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
		self.layout.addWidget(self.current_sun_label)
		self.layout.setAlignment(self.current_sun_label, Qt.AlignBottom | Qt.AlignCenter)
		self.setLayout(self.layout)

	def change_current_sun_num(self, sun_num):
		"""
		更改当前阳光数
		:return:
		"""
		self.current_sun_label.setText(str(sun_num))

	def paintEvent(self, event):
		super(SunFlowerBasket, self).paintEvent(event)
		painter = QPainter(self)
		pixmap = QPixmap(':/images/others/basket/sf_basket.png')  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()


class ShovelBasket(ImageLabel):
	"""
	铲子的篮子
	"""
	style = """#shovelBasket{background-color:rgb(238,236,177);}"""

	def __init__(self, p=None):
		super(ShovelBasket, self).__init__(p)
		self.param_init()
		self.ui_init()
		self.change_shovel_status(self.has_shovel)
		self.setStyleSheet(self.style)

	def param_init(self):
		self.has_shovel = True

	def ui_init(self):
		self.setObjectName("shovelBasket")
		self.layout = QVBoxLayout()
		self.setFixedSize(QSize(120, 60))
		self.layout.setContentsMargins(15, 10, 15, 5)
		self.shovel_label = ImageLabel(self)
		self.layout.addWidget(self.shovel_label)
		self.layout.setAlignment(self.shovel_label, Qt.AlignHCenter | Qt.AlignVCenter)
		self.setLayout(self.layout)

	def change_shovel_status(self, status):
		"""
		:param status: 是否有铲子
		:return:
		"""
		self.shovel_pix = ":images/others/basket/shovel.png" if status is True else ""
		self.shovel_label.set_pix(self.shovel_pix)

	def paintEvent(self, event):
		super(ShovelBasket, self).paintEvent(event)
		painter = QPainter(self)
		pixmap = QPixmap(':images/others/basket/shovel_groove.png')  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()

	def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
		if ev.button() == Qt.LeftButton:
			self.has_shovel = not self.has_shovel
		bus.cursor_changed.emit(self.shovel_pix)
		bus.effect_changed.emit("use_shovel")
		self.change_shovel_status(self.has_shovel)
		super(ShovelBasket, self).mouseReleaseEvent(ev)


class PlantCardBasket(QFrame):
	"""
	植物篮子
	"""
	style = """#plantCardBasket{background-color:rgb(114,49,19);border:5px solid rgb(141,67,30);border-radius:6px;}"""
	card_hovered = pyqtSignal(QObject)

	def __init__(self, p=None):
		super(PlantCardBasket, self).__init__(p)
		self.param_init()
		self.ui_init()
		self.setStyleSheet(self.style)
		if 0:
			self.load_cards([1, 2, 3, 4, 5, 6])

	def param_init(self):
		self.card_list = []
		self.card_dict = dict()  # 植物id:item

	def ui_init(self):
		self.setObjectName("plantCardBasket")
		self.setMaximumHeight(110)
		self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
		self.layout = QHBoxLayout()
		self.layout.setContentsMargins(5, 5, 5, 5)
		self.layout.setSpacing(8)
		self.setLayout(self.layout)

		self.sunFlowerBasket = SunFlowerBasket(self)  # 加入阳光计数
		self.shovelBasket = ShovelBasket(self)
		self.layout.addWidget(self.sunFlowerBasket)
		self.layout.setAlignment(self.sunFlowerBasket, Qt.AlignLeft)

		self.card_widget = QWidget(self)
		self.card_widget.setMinimumWidth(660)
		self.card_widget_layout = QHBoxLayout()
		self.card_widget_layout.setContentsMargins(0, 0, 0, 0)
		self.card_widget.setLayout(self.card_widget_layout)
		self.layout.addWidget(self.card_widget)
		self.layout.addWidget(self.shovelBasket)  # 加入铲子
		self.layout.setAlignment(self.shovelBasket, Qt.AlignRight)

	def clear_selected_cards(self):
		# 加载之前先清理
		clear_layout(self.card_widget_layout)
		self.card_list.clear()
		self.card_dict.clear()

	def load_cards(self, plant_id_list):
		"""
		加载植物卡片
		:return:
		"""
		selected_plant_dict = {v['id']: v for v in normal_conf.plant_param_dict.values()}
		for index, each_plant_id in enumerate(plant_id_list):
			each_card_item = selected_plant_dict[each_plant_id]
			card = PlantCard(self)
			card.set_card_item(each_card_item)
			card.card_clicked.connect(lambda pix, card=card: self.process_card_clicked(pix))
			card.cooling_is_finished.connect(bus.plant_cooling_finished.emit)
			card.card_hovered.connect(lambda status, card=card: bus.card_hovered.emit(card, status))
			self.card_widget_layout.addWidget(card)
			self.card_list.append(card)
			self.card_dict[each_card_item["id"]] = card

	# 添加铲子和间隔项到布局中

	def process_card_clicked(self, pix):
		"""
		处理卡片点击事件
		:param pix:
		:return:
		"""
		if pix:
			bus.cursor_changed.emit(pix)
		else:  # 卡片不可种植
			bus.effect_changed.emit("buzzer")

	def start_cooling(self):
		"""
		开始冷却
		:return:
		"""
		for each_item in self.card_list:
			self.start_each_cooling(each_item)

	def start_each_cooling(self, each_item):
		each_item.cooling_start()
		each_item.change_card_status()


class SlidingStackedWidget(QStackedWidget):
	LEFT2RIGHT, RIGHT2LEFT, TOP2BOTTOM, BOTTOM2TOP, AUTOMATIC = range(5)
	indexChanged_signal = pyqtSignal(int)

	def __init__(self, *args, **kwargs):
		super(SlidingStackedWidget, self).__init__(*args, **kwargs)
		self._pnow = QPoint(0, 0)
		# 动画速度
		self._speed = 500
		# 当前索引
		self._now = 0
		# 自动模式的当前索引
		self._current = 0
		# 下一个索引
		self._next = 0
		# 是否激活
		self._active = 0
		# 动画方向(默认是横向)
		self._orientation = Qt.Horizontal
		# 动画曲线类型
		self._easing = QEasingCurve.Linear
		# 初始化动画
		self._initAnimation()

	def slideInIdx(self, idx, direction=4):
		"""滑动到指定序号
		:param idx:               序号
		:type idx:                int
		:param direction:         方向,默认是自动AUTOMATIC=4
		:type direction:          int
		"""
		if idx > self.count() - 1:
			direction = self.TOP2BOTTOM if self._orientation == Qt.Vertical else self.RIGHT2LEFT
			idx = idx % self.count()
		elif idx < 0:
			direction = self.BOTTOM2TOP if self._orientation == Qt.Vertical else self.LEFT2RIGHT
			idx = (idx + self.count()) % self.count()
		self.slideInWgt(self.widget(idx), direction)

	def slideInWgt(self, widget, direction):
		"""滑动到指定的widget
		:param widget:        QWidget, QLabel, etc...
		:type widget:         QWidget Base Class
		:param direction:     方向
		:type direction:      int
		"""
		if self._active:
			return
		self._active = 1
		_now = self.currentIndex()
		if _now == self.count() - 1:
			pass
		else:
			_next = 0
		_next = self.indexOf(widget)
		if _now == _next:
			self._active = 0
			return

		w_now = self.widget(_now)
		w_next = self.widget(_next)

		# 自动判断方向
		# if _now < _next:
		directionhint = self.TOP2BOTTOM if self._orientation == Qt.Vertical else self.RIGHT2LEFT
		# else:
		# 	directionhint = self.BOTTOM2TOP if self._orientation == Qt.Vertical else self.LEFT2RIGHT
		if direction == self.AUTOMATIC:
			direction = directionhint

		# 计算偏移量
		offsetX = self.frameRect().width()
		offsetY = self.frameRect().height()
		w_next.setGeometry(0, 0, offsetX, offsetY)
		if direction == self.BOTTOM2TOP:
			offsetX = 0
			offsetY = -offsetY
		elif direction == self.TOP2BOTTOM:
			offsetX = 0
		elif direction == self.RIGHT2LEFT:
			offsetX = -offsetX
			offsetY = 0
		elif direction == self.LEFT2RIGHT:
			offsetY = 0

		# 重新定位显示区域外部/旁边的下一个窗口小部件
		pnext = w_next.pos()
		pnow = w_now.pos()
		self._pnow = pnow

		# 移动到指定位置并显示
		w_next.move(pnext.x() - offsetX, pnext.y() - offsetY)
		w_next.show()
		w_next.raise_()
		self._animnow.setTargetObject(w_now)
		self._animnow.setDuration(self._speed)
		self._animnow.setEasingCurve(self._easing)
		self._animnow.setStartValue(QPoint(pnow.x(), pnow.y()))
		self._animnow.setEndValue(QPoint(offsetX + pnow.x(), offsetY + pnow.y()))

		self._animnext.setTargetObject(w_next)
		self._animnext.setDuration(self._speed)
		self._animnext.setEasingCurve(self._easing)
		self._animnext.setStartValue(
			QPoint(-offsetX + pnext.x(), offsetY + pnext.y()))
		self._animnext.setEndValue(QPoint(pnext.x(), pnext.y()))

		self._next = _next
		self._now = _now
		self._active = 1
		self._animgroup.start()

	def _initAnimation(self):
		"""初始化当前页和下一页的动画变量"""
		# 当前页的动画
		self._animnow = QPropertyAnimation(
			self, propertyName=b'pos', duration=self._speed,
			easingCurve=self._easing)
		# 下一页的动画
		self._animnext = QPropertyAnimation(
			self, propertyName=b'pos', duration=self._speed,
			easingCurve=self._easing)
		# 并行动画组
		self._animgroup = QParallelAnimationGroup(
			self, finished=self.animationDoneSlot)
		self._animgroup.addAnimation(self._animnow)
		self._animgroup.addAnimation(self._animnext)

	def setCurrentIndex(self, index):
		# 覆盖该方法实现的动画切换
		# super(SlidingStackedWidget, self).setCurrentIndex(index)
		# 坚决不能调用上面的函数,否则动画失效
		self.slideInIdx(index)

	def setCurrentWidget(self, widget):
		# 覆盖该方法实现的动画切换
		super(SlidingStackedWidget, self).setCurrentWidget(widget)
		# 坚决不能调用上面的函数,否则动画失效
		self.setCurrentIndex(self.indexOf(widget))

	def animationDoneSlot(self):
		"""动画结束处理函数"""
		# 由于重写了setCurrentIndex方法所以这里要用父类本身的方法
		#         self.setCurrentIndex(self._next)
		QStackedWidget.setCurrentIndex(self, self._next)
		w = self.widget(self._now)
		w.hide()
		w.move(self._pnow)
		self._active = 0

	def autoStop(self):
		"""停止自动播放"""
		if hasattr(self, '_autoTimer'):
			self._autoTimer.stop()

	def autoStart(self, msec=3000):
		"""自动轮播
		:param time: 时间, 默认3000, 3秒
		"""
		if not hasattr(self, '_autoTimer'):
			self._autoTimer = QTimer(self, timeout=self._autoStart)
		self._autoTimer.stop()
		self._autoTimer.isActive()
		self._autoTimer.start(msec)

	def _autoStart(self):
		if self._current == self.count():
			self._current = 0
		self._current += 1
		self.setCurrentIndex(self._current)
		self.indexChanged_signal.emit(self._current)


class AutoSunflower(QLabel):
	def __init__(self, p=None, relative_pos=QPoint(0, 0)):
		super().__init__(p)
		self.relative_pos = relative_pos
		self.setParent(p)
		self.ui_init()

	def ui_init(self):
		self.setCursor(Qt.PointingHandCursor)
		self.height_ = 100
		self.is_clicked = False  # 避免重复点击
		self.setObjectName("autoSunflower")
		self.setFixedSize(QSize(self.height_, self.height_))
		self.setStyleSheet("#autoSunflower{background-color: transparent;}")
		self.setMovie(QMovie(":images/others/roll_sf.gif"))
		self.movie = self.movie()
		self.movie.start()
		self.movie.frameChanged.connect(self.update_frame)
		self.mousePressEvent = self.on_click

		# 初始化计时器
		self.hide_timer = QTimer()
		self.hide_timer.timeout.connect(self.auto_hide)

		# 开始动画
		self.start_x = random.randint(0, self.parent().width() - self.height_)
		self.start_y = -self.height_  # Start above the visible area
		self.end_x = self.start_x
		self.end_y = self.parent().height() - self.height()
		self.start_animation(self.start_x, self.start_y, self.end_x, self.end_y)

	def update_frame(self, frame_number):
		"""
		更新当前帧，缩放图像到 50x50
		"""
		frame = self.movie.currentPixmap()
		scaled_frame = frame.scaled(self.height_, self.height_, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		self.setPixmap(scaled_frame)

	def on_click(self, event):
		if event.button() == Qt.LeftButton:
			if self.is_clicked is True: return
			bus.sunshine_produced.emit(25)  # 发射信号增加阳光
			bus.effect_changed.emit("collect_sf")
			self.hide_timer.stop()  # 停止计时器
			self.animate_to_position(self.relative_pos)  # 开始向指定位置的动画
			self.is_clicked = True

	def start_animation(self, start_x, start_y, end_x, end_y):
		# 创建下落动画
		self.animation = QPropertyAnimation(self, b"pos")
		self.animation.setDuration(3000)  # 动画持续时间
		self.animation.setStartValue(QPoint(start_x, start_y))
		self.animation.setEndValue(QPoint(end_x, end_y))
		# 使用直线插值函数
		self.animation.setEasingCurve(QEasingCurve.Linear)
		self.animation.finished.connect(self.check_bottom_reached)
		self.animation.start()

	def check_bottom_reached(self):
		# 检查是否到达底部
		if self.pos().y() + self.height_ >= self.parent().height():
			self.hide_timer.start(3000)  # 启动计时器，三秒后隐藏

	def animate_to_position(self, end_pos):
		# 创建平滑曲线动画
		self.animation = QPropertyAnimation(self, b"pos")
		self.animation.setDuration(500)  # 动画持续时间
		start_pos = self.pos()

		self.animation.setStartValue(start_pos)
		self.animation.setEndValue(end_pos)
		self.animation.setEasingCurve(QEasingCurve.OutQuad)  # 使用平滑的曲线

		# 动画完成后隐藏组件
		self.animation.finished.connect(self.hide)
		self.animation.start()

	def auto_hide(self):
		self.hide()  # 自动隐藏
		self.hide_timer.stop()  # 停止计时器

	def hide(self) -> None:
		bus.sunshine_finished.emit()
		super(AutoSunflower, self).hide()


class FlagItem(ImageLabel):
	"""
	进度条上的旗子
	"""

	def __init__(self, p):
		super(FlagItem, self).__init__(p)
		self.ui_init()

	def ui_init(self):
		super(FlagItem, self).ui_init()
		self.set_pix(":images/others/FlagMeterParts2.png")
		self.setFixedSize(QSize(15, 15))


class ProgressSlider(QSlider):
	def __init__(self, parent=None):
		super().__init__(Qt.Horizontal, parent)
		self.init_ui()

	def init_ui(self):
		# 滑块样式表
		self.setMaximumWidth(200)
		self.setFixedHeight(30)
		self.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 8px solid rgb(79,79,117);
                border-radius: 8px;  /* 圆角边框 */
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                                            stop:0 rgb(255, 255, 131), 
                                            stop:1 rgb(57, 167, 16));
                height: 10px;  /* 滑块高度 */
            }
            QSlider::handle:horizontal {
                border-image: url(:images/others/FlagMeterParts1.png);
                width: 14px;
                height: 14px;
            }
            QSlider::sub-page:horizontal {
				border: 8px solid rgb(79,79,117);
                background: black;
                border-radius: 8px;  /* 圆角边框 */
            }
        """)
		self.setMinimum(0)
		self.setMaximum(100)
		self.setSingleStep(1)
		self.setValue(0)

	def setValue(self, value):
		super(ProgressSlider, self).setValue(100 - value)


class ProgressWidget(QWidget):
	def __init__(self, p=None):
		super(ProgressWidget, self).__init__(p)
		self.param_init()
		self.ui_init()

	def param_init(self):
		self.flag_dict = dict()  # key:进度百分比 value:flag_item
		self.current_node_index = -1  # 当前结点索引位置
		self.max_sec = -1  # 最大秒数

	def ui_init(self):
		self.setFixedWidth(180)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.layout = QVBoxLayout()
		self.inner_widget = QWidget(self)
		self.inner_widget_layout = QVBoxLayout()
		self.layout.setContentsMargins(0, 10, 0, 10)
		self.progressSlider = ProgressSlider(self)
		self.inner_widget_layout.addWidget(self.progressSlider)
		self.inner_widget.setLayout(self.inner_widget_layout)
		self.layout.addWidget(self.inner_widget)
		self.setLayout(self.layout)

		spacerItem = QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
		self.hover_layout = QVBoxLayout(self.progressSlider)
		self.hover_layout.setContentsMargins(0, 0, 0, 0)
		self.img_label = ImageLabel(self.inner_widget)  # 底部关卡进程
		self.img_label.set_pix(":images/others/FlagMeterLevelProgress.png")
		self.img_label.raise_()
		self.hover_layout.addItem(spacerItem)
		self.hover_layout.addWidget(self.img_label)
		self.hover_layout.setAlignment(self.img_label, Qt.AlignHCenter | Qt.AlignBottom)

	def clear_flags(self):
		for each_flag_item in self.flag_dict.values():
			try:
				each_flag_item.deleteLater()
			except RuntimeError:
				pass
		self.flag_dict.clear()

	def set_flags(self, map_dict):
		"""
		加载旗帜
		:param map_dict: 包含节点数据的字典
		:return: None
		"""
		self.clear_flags()
		process_widget_width = 100  # 获取进度条的宽度
		self.max_sec = max(map_dict.keys())  # 获取最后一个节点的时间
		process_list = [key for key, value in map_dict.items() if value[0] in [2, 3]]  # 筛选需要插入旗帜的节点
		num_flags = len(process_list)  # 计算需要插入的旗帜数量
		if num_flags == 0:  # 如果没有旗帜需要插入，直接返回
			return
		min_x, max_x = 15, process_widget_width  # 定义旗帜的最小和最大x坐标
		interval = (max_x - min_x) / (num_flags - 1) if num_flags > 1 else 0  # 计算旗帜之间的间隔
		for flag_counter, game_sec in enumerate(process_list[::-1]):  # 用枚举函数替代计数器
			progress_percent = int(game_sec / self.max_sec * 100)  # 计算节点所在进度百分比
			flag_item = FlagItem(self)  # 创建旗帜对象
			flag_x = int(min_x + interval * flag_counter)  # 计算x坐标
			# 如果是最后一个旗帜，x 坐标减去 15
			if flag_counter == num_flags - 1:
				flag_x -= 15
			flag_item.move(flag_x, 20)  # 将旗帜移动到相应位置
			flag_item.raise_()  # 将旗帜放置在最上层
			self.flag_dict[progress_percent] = flag_item  # 保存旗帜进度字典

	def set_flag_raise(self, game_progress):
		"""
		旗子升起
		:param game_progress: 当前游戏进度的百分比
		:return: None
		"""
		if game_progress in self.flag_dict:  # 直接检查键是否在字典中
			aim_flag_item = self.flag_dict[game_progress]
			aim_flag_item.move(aim_flag_item.x(), 10)  # 移动旗帜到新的位置


class GameProgressWidget(QWidget):
	"""
	游戏进度
	"""
	style = """#game_level,#game_level_mode{font-weight:bold;font-size:11pt;}#game_level{color:rgb(208,180,108);x}#game_level_mode{color:rgb(246,252,36);}"""

	def __init__(self, p=None):
		super(GameProgressWidget, self).__init__(p)
		self.param_init()
		self.ui_init()
		self.setStyleSheet(self.style)

	def param_init(self):
		self.game_max_sec = 1  # 游戏时长

	def ui_init(self):
		self.setFixedHeight(55)
		self.setFixedWidth(350)
		self.layout = QHBoxLayout()
		self.layout.setSpacing(3)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.game_level = QLabel(self)
		self.progressWidget = ProgressWidget(self)
		self.game_level_mode = QLabel(self)
		self.game_level.setObjectName("game_level")
		self.game_level_mode.setObjectName("game_level_mode")

		self.game_level.setFixedHeight(20)
		self.game_level_mode.setFixedHeight(20)
		shadow_effect1 = QGraphicsDropShadowEffect()
		shadow_effect1.setBlurRadius(5)  # 设置模糊半径
		shadow_effect1.setOffset(3, 3)  # 设置阴影偏移量
		shadow_effect1.setColor(Qt.black)  # 设置阴影颜色
		shadow_effect2 = QGraphicsDropShadowEffect()
		shadow_effect2.setBlurRadius(5)  # 设置模糊半径
		shadow_effect2.setOffset(3, 3)  # 设置阴影偏移量
		shadow_effect2.setColor(Qt.black)  # 设置阴影颜色
		self.game_level.setGraphicsEffect(shadow_effect1)
		self.game_level_mode.setGraphicsEffect(shadow_effect2)
		self.layout.addWidget(self.game_level)
		self.layout.addWidget(self.progressWidget)
		self.layout.addWidget(self.game_level_mode)
		self.layout.setStretch(0, 0)
		self.layout.setStretch(1, 3)
		self.layout.setStretch(2, 0)
		self.setLayout(self.layout)

	def update_game_process(self, game_sec, process_list):
		"""
		:param game_sec:
		:param process_list:
		:return:
		"""
		game_progress = int(game_sec / self.game_max_sec * 100)  # 游戏进度百分比
		self.progressWidget.progressSlider.setValue(game_progress)
		if len(process_list) == 0: return
		process_node_type = process_list[0]
		bus.game_node_changed.emit(process_node_type)
		if process_node_type in [2, 3]:
			self.progressWidget.set_flag_raise(game_progress)

	def set_flags(self, map_dict):
		self.game_max_sec = list(map_dict.keys())[-1]
		self.progressWidget.set_flags(map_dict)


class PlantToolTip(QFrame):
	"""
	植物提示组件
	"""
	style = """#inner_frame{background-color:rgb(255,255,200);border:1px solid black;border-radius:2px;}#load_label{color:red;}#name_label{color:black;}"""

	def __init__(self, p=None):
		super(PlantToolTip, self).__init__(p)
		self.ui_init()
		self.setStyleSheet(self.style)
		if 0:
			self.set_toolTip({"name": "向日葵"}, True)

	def ui_init(self):
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
		self.setObjectName("plantToolTip")
		self.setFixedWidth(92)
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(5, 0, 5, 0)
		self.layout.setSpacing(2)
		self.inner_frame = QFrame(self)
		self.inner_frame.setObjectName("inner_frame")
		self.frame_layout = QVBoxLayout()
		self.frame_layout.setContentsMargins(5, 0, 5, 0)
		self.frame_layout.setSpacing(2)
		self.inner_frame.setLayout(self.frame_layout)
		self.load_label = QLabel(self)
		self.name_label = QLabel(self)
		self.load_label.setObjectName("load_label")
		self.name_label.setObjectName("name_label")
		self.frame_layout.addWidget(self.load_label)
		self.frame_layout.addWidget(self.name_label)
		self.frame_layout.setAlignment(self.name_label, Qt.AlignHCenter)
		self.inner_frame.setLayout(self.frame_layout)
		self.layout.addWidget(self.inner_frame)
		self.setLayout(self.layout)

	def set_toolTip(self, card_obj):
		"""
		设置提示
		:param plant_item:植物数据
		:param state:是否装填
		:return:
		"""
		cooling_finished = card_obj.cooling_finished
		if cooling_finished is True:
			height = 22
			tip = ""
		else:
			height = 33
			tip = "重新装填中..."
		self.setFixedHeight(height)
		self.name_label.setText(card_obj.cn_name)
		self.load_label.setText(tip)
		self.load_label.setVisible(cooling_finished is False)


class PlantSelectToolTip(QFrame):
	"""
	植物提示组件
	"""
	style = """#inner_frame{background-color:rgb(255,255,200);border:1px solid black;border-radius:2px;}#desc_label{color:black;font-family:"Arial"}#name_label{color:black;font-weight:550 pt;font-family:"Arial"}"""

	def __init__(self, p=None):
		super(PlantSelectToolTip, self).__init__(p)
		self.ui_init()
		self.setStyleSheet(self.style)

	def ui_init(self):
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
		self.setObjectName("plantSelectToolTip")
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(5, 0, 5, 0)
		self.layout.setSpacing(2)
		self.inner_frame = QFrame(self)
		self.inner_frame.setObjectName("inner_frame")
		self.frame_layout = QVBoxLayout()
		self.frame_layout.setContentsMargins(5, 3, 5, 3)
		self.frame_layout.setSpacing(2)
		self.inner_frame.setLayout(self.frame_layout)
		self.desc_label = QLabel(self)
		self.name_label = QLabel(self)
		self.desc_label.setObjectName("desc_label")
		self.name_label.setObjectName("name_label")
		self.frame_layout.addWidget(self.name_label)
		self.frame_layout.addWidget(self.desc_label)
		self.frame_layout.setAlignment(self.name_label, Qt.AlignHCenter)
		self.frame_layout.setAlignment(self.desc_label, Qt.AlignHCenter)
		self.inner_frame.setLayout(self.frame_layout)
		self.layout.addWidget(self.inner_frame)
		self.setLayout(self.layout)

	def set_toolTip(self, card_item):
		"""
		设置提示
		:return:
		"""
		# 计算文字的宽度
		card_name = card_item['cn_name']
		card_desc = card_item['desc']
		font = QFont('Arial', 10)
		fm = QFontMetrics(font)
		text_width = fm.boundingRect(card_desc).width()
		self.desc_label.setFixedWidth(text_width)  # 加上20的边距
		self.name_label.setText(card_name)
		self.desc_label.setText(card_desc)
		self.desc_label.adjustSize()
		self.adjustSize()


class PlantSelectBasket(QFrame):
	"""
	开场植物选择篮子
	"""
	style = """#plantSelectBasket{background-color:rgb(81,35,12);border-radius:6px;}"""
	card_hovered = pyqtSignal(QObject, bool, dict)
	card_item_clicked = pyqtSignal(QObject, dict)

	def __init__(self, p=None):
		super(PlantSelectBasket, self).__init__(p)
		self.param_init()
		self.ui_init()
		self.set_up_ui()
		self.setStyleSheet(self.style)  # 确保在初始化后设置样式表
		self.set_plant_cards(normal_conf.plant_param_dict)

	def param_init(self):
		self.grid_row = 6  # 卡片行数
		self.grid_col = 10  # 卡片列数
		self.card_dict = dict()  # 卡片id:item对应关系

	def ui_init(self):
		self.setObjectName("plantSelectBasket")  # 设置对象名称
		self.layout = QVBoxLayout()
		self.grid_layout = QGridLayout()
		self.startRockBtn = StartRockBtn(self)
		self.selectLastBtn = StartRockBtn(self)
		self.showAlmanacBtn = StartRockBtn(self)
		self.startRockBtn.setEnabled(False)
		self.selectLastBtn.setMinimumWidth(205)
		self.layout.addLayout(self.grid_layout)
		self.btn_layout = QHBoxLayout()
		self.btn_layout.setSpacing(15)
		spacerItem1 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		spacerItem2 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.btn_layout.addItem(spacerItem1)
		self.btn_layout.addWidget(self.startRockBtn)
		self.btn_layout.addWidget(self.selectLastBtn)
		self.btn_layout.addWidget(self.showAlmanacBtn)
		self.btn_layout.addItem(spacerItem2)
		self.layout.addLayout(self.btn_layout)
		self.setLayout(self.layout)

	def set_up_ui(self):
		self.startRockBtn.setText("一起摇滚吧")
		self.selectLastBtn.setText("选择上次选择的植物")
		self.showAlmanacBtn.setText("查看图鉴")

	def set_plant_cards(self, plant_param_dict):
		"""
		设置植物
		:param plant_param_dict:
		:return:
		"""
		# 遍历字典值并放置植物卡片
		card_items = list(plant_param_dict.values())
		index = 0
		for row in range(self.grid_row):
			for col in range(self.grid_col):
				if index < len(card_items):
					plant_card = SimpleCard(self)
					card_item = card_items[index]
					plant_card.set_card_item(card_item)
					plant_card.card_hovered.connect(
						partial(self.handle_card_hovered, plant_card, plant_card.card_item))
					plant_card.card_item_clicked.connect(
						partial(self.handle_card_clicked, plant_card, plant_card.card_item))
					self.grid_layout.addWidget(plant_card, row, col)
					self.card_dict[card_item['id']] = plant_card
					index += 1
				else:
					empty_widget = EmptyCard(self)
					self.grid_layout.addWidget(empty_widget, row, col)

	def handle_card_hovered(self, plant_card, card_item, status):
		"""
		处理植物卡片被悬停事件
		:param plant_card: 植物卡片
		:param card_item: 植物卡片项
		:param status: 悬停状态
		"""
		self.card_hovered.emit(plant_card, status, card_item)

	def handle_card_clicked(self, plant_card, card_item):
		"""
		处理植物卡片被点击事件
		:param plant_card: 植物卡片
		:param card_item: 植物卡片项
		:param status: 悬停状态
		"""
		self.card_item_clicked.emit(plant_card, card_item)


class SelectedCardsBasket(QFrame):
	"""
	开场选择了植物的卡片篮子
	"""
	style = """#selectedCardsBasket{background-color:rgb(114,49,19);border:5px solid rgb(141,67,30);border-radius:6px;}"""
	on_card_remove = pyqtSignal(dict)  # 卡片被移除
	card_num_is_max = pyqtSignal(bool)  # 卡片是否达放满了

	def __init__(self, p=None):
		super(SelectedCardsBasket, self).__init__(p)
		self.param_init()
		self.ui_init()
		self.setStyleSheet(self.style)
		self.load_cards()  # 加载空卡片

	def param_init(self):
		self.max_cards = 9  # 最多能选卡片数量
		self.card_list = list()  # 卡片列表

	def ui_init(self):
		self.setFixedHeight(130)
		self.setObjectName("selectedCardsBasket")
		self.layout = QHBoxLayout()
		self.sunFlowerBasket = SunFlowerBasket(self)  # 加入阳光计数
		self.inner_basket = QWidget(self)
		self.inner_basket_layout = QHBoxLayout()
		self.inner_basket_layout.setContentsMargins(0, 0, 0, 0)
		self.inner_basket_layout.setSpacing(5)
		self.inner_basket.setLayout(self.inner_basket_layout)
		self.layout.addWidget(self.sunFlowerBasket)
		self.layout.addWidget(self.inner_basket)
		self.setLayout(self.layout)

	def add_card(self, card_item):
		if card_item in self.card_list: return
		self.card_list.append(card_item)
		bus.effect_changed.emit("tap")
		self.load_cards()

	def get_card_id_list(self):
		return [each['id'] for each in self.card_list]

	def remove_card(self, card_item):
		if card_item not in self.card_list: return
		self.card_list.remove(card_item)
		bus.effect_changed.emit("tap")
		self.load_cards()

	def clear_cards(self):
		self.card_list.clear()
		self.load_cards()

	def load_cards(self):
		"""
		加载卡片数据
		:return:
		"""
		clear_layout(self.inner_basket_layout)
		for i in range(0, self.max_cards):
			if i < len(self.card_list):
				card_item = self.card_list[i]
				card = SimpleCard(self)
				card.card_item_clicked.connect(
					partial(self.handle_card_clicked, card_item))
				card.set_card_item(card_item)
			else:
				card = EmptyCard(self)
			self.inner_basket_layout.addWidget(card)
		self.card_num_is_max.emit(len(self.card_list) == self.max_cards)

	def handle_card_clicked(self, card_item):
		"""
		处理植物卡片被点击事件
		"""
		self.on_card_remove.emit(card_item)


class ButtonBase(QPushButton):
	def __init__(self, p=None):
		super(ButtonBase, self).__init__(p)
		self.setCursor(Qt.PointingHandCursor)


class StartRockBtn(ButtonBase):
	"""
	一起摇滚吧
	"""
	style = """#startRockBtn{background-color:rgb(114,49,19);color:rgb(203,140,60);font-weight:800 pt;font-size:14pt;border-radius:4px;}#startRockBtn:hover{background-color:rgb(148,72,23)}#startRockBtn:disabled {
                background-color: rgb(96,45,18);  
                color: rgb(53,39,11);
                border-color:rgb(40,18,7);
            }"""

	def __init__(self, p=None):
		super(StartRockBtn, self).__init__(p)
		self.ui_init()

	def ui_init(self):
		self.setObjectName("startRockBtn")
		self.setFixedSize(QSize(140, 38))
		self.setStyleSheet(self.style)


class PlantSelectWidget(QWidget):
	"""
	开场植物选择组件
	"""
	style = """#plantSelectWidget{background-color:transparent;}"""
	card_opt_signal = pyqtSignal()  # 操作了卡片

	def __init__(self, p=None):
		super(PlantSelectWidget, self).__init__(p)
		self.param_init()
		self.ui_init()
		self.slot_init()
		self.setStyleSheet(self.style)

	def param_init(self):
		self.selected_card_list = []

	def ui_init(self):
		self.setObjectName("plantSelectWidget")
		self.layout = QVBoxLayout()
		self.layout.setSpacing(5)
		self.top_layout = QHBoxLayout()
		self.selectedCardsBasket = SelectedCardsBasket(self)
		self.middle_layout = QHBoxLayout()
		self.mid_right_widget = QWidget(self)
		self.plantSelectBasket = PlantSelectBasket(self)
		self.top_layout.addWidget(self.selectedCardsBasket)
		spacerItem = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.top_layout.addItem(spacerItem)
		self.middle_layout.addWidget(self.plantSelectBasket)
		self.middle_layout.addWidget(self.mid_right_widget)
		self.layout.addLayout(self.top_layout)
		self.layout.addLayout(self.middle_layout)
		self.layout.setStretch(0, 1)
		self.layout.setStretch(1, 6)
		self.setLayout(self.layout)

		self.plantSelectToolTip = PlantSelectToolTip(self)
		self.plantSelectToolTip.hide()

		self.selectedCardsBasket.setMinimumWidth(794)

	def clear_selected_cards(self):
		"""
		移除已选择的卡片
		"""
		for each_card in self.selected_card_list:
			self.process_card_removed(each_card)
		self.selected_card_list = []

	def slot_init(self):
		self.plantSelectBasket.card_hovered.connect(lambda obj, s, data: self.show_card_toolTip(obj, s, data))
		self.plantSelectBasket.card_item_clicked.connect(lambda obj, data: self.process_card_selected(obj, data))
		self.selectedCardsBasket.on_card_remove.connect(lambda card_item: self.process_card_removed(card_item))
		self.selectedCardsBasket.card_num_is_max.connect(lambda s: self.plantSelectBasket.startRockBtn.setEnabled(s))
		self.plantSelectBasket.startRockBtn.clicked.connect(self.do_save_selected_plants)
		self.plantSelectBasket.selectLastBtn.clicked.connect(self.do_select_last_plants)

	def do_save_selected_plants(self):
		"""
		保存本次的植物卡片id
		"""
		card_list = [str(each['id']) for each in self.selectedCardsBasket.card_list]
		save_to_saved_file(game_conf.last_saved_file, card_list)

	def do_select_last_plants(self):
		"""
		选择上次选择过的植物
		"""
		last_selected_plant_ids = read_saved_file(game_conf.last_saved_file)
		for each_plant_id in last_selected_plant_ids:
			plant_item = self.plantSelectBasket.card_dict[int(each_plant_id)]
			self.process_card_selected(plant_item, plant_item.card_item)
		self.card_opt_signal.emit()

	def show_card_toolTip(self, card_obj, status, data):
		"""
		展示卡片状态提示
		:param card_obj: 卡片对象
		:param status: 提示是否显示的状态
		:param data: 提示内容数据
		"""
		self.plantSelectToolTip.set_toolTip(data)
		card_pos = card_obj.mapToGlobal(QPoint(0, 0))
		tooltip_width = self.plantSelectToolTip.desc_label.width()
		tooltip_x = card_pos.x() + int((card_obj.width() - tooltip_width) / 2)
		tooltip_y = card_pos.y() + card_obj.height() - 3
		self.plantSelectToolTip.move(tooltip_x, tooltip_y)
		self.plantSelectToolTip.setVisible(status)

	def process_card_selected(self, card_obj, data):
		"""
		处理卡片被选择状态
		:param card_obj:
		:param status:
		:param data:
		:return:
		"""
		if card_obj.is_selected is False:
			if len(self.selectedCardsBasket.card_list) >= self.selectedCardsBasket.max_cards: return
			card_obj.change_card_selected_status()  # 改变选择状态
			self.selectedCardsBasket.add_card(data)
			self.card_opt_signal.emit()
			self.selected_card_list.append(data)

	def process_card_removed(self, card_item):
		"""
		卡片被移除了，待选卡片回复状态
		"""
		self.plantSelectBasket.card_dict[card_item['id']].change_card_selected_status()
		self.selectedCardsBasket.remove_card(card_item)
		self.card_opt_signal.emit()


class ZombiePrepareArea(QWidget):
	"""
	僵尸准备区域
	"""

	def __init__(self, p=None):
		super(ZombiePrepareArea, self).__init__(p)
		self.ui_init()
		if 0:
			self.load_zombies([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

	def ui_init(self):
		self.setMinimumSize(QSize(420, 600))
		self.zombie_item_list = []

	def load_zombies(self, zombie_id_list):
		"""
		加载准备状态的僵尸，并确保总高度不超过父窗口高度
		"""
		# 获取符合条件的僵尸列表
		for each_zombie_ in self.zombie_item_list:  # 清空之前的僵尸
			try:
				each_zombie_.deleteLater()
			except RuntimeError:
				pass
		map_zombie_list = [value for value in normal_conf.zombie_param_dict.values() if value["id"] in zombie_id_list]

		# 初始坐标和最大宽度限制
		start_x = 0
		start_y = int(self.height() * 0.11)  # 僵尸起始Y位置
		max_width = int(self.width())
		max_height = int(self.height())  # 父窗口的高度

		# 水平和垂直间距
		horizontal_spacing = 10
		vertical_spacing = 10

		# 计算僵尸的总高度
		total_zombie_height = 0

		# 临时保存僵尸项的宽度和高度，用于之后调整间距
		zombie_items = []

		# 遍历僵尸并计算所需总高度
		for map_zombie_item in map_zombie_list:
			try:
				zombie_item = PrepareZombie(self)
				zombie_item.set_zombie_item(map_zombie_item)
				zombie_width = zombie_item.width() - 60
				zombie_height = zombie_item.height() - 120
				zombie_items.append((zombie_item, zombie_width, zombie_height))
				total_zombie_height += zombie_height + vertical_spacing
				self.zombie_item_list.append(zombie_item)
			except RuntimeError:
				pass

		# 如果总高度超过父窗口高度，则重新计算垂直间距以适应窗口
		if total_zombie_height > max_height:
			# 减少垂直间距，确保僵尸不超出父窗口高度
			available_height = max_height - start_y
			num_zombies = len(zombie_items)
			max_rows = available_height // (zombie_items[0][2] + vertical_spacing)
			if max_rows == 0:
				max_rows = 1  # 确保至少有一行
			vertical_spacing = (available_height - (max_rows * zombie_items[0][2])) // (max_rows - 1)

		# 重新放置僵尸
		start_x = 0
		start_y = int(self.height() * 0.11)
		for zombie_item, zombie_width, zombie_height in zombie_items:
			# 检查是否超出右边界，如果超出则换行排列
			if start_x + zombie_width > max_width:
				start_x = 0  # 换行时X坐标重置
				start_y += zombie_height + vertical_spacing  # Y坐标增加

			# 放置僵尸
			zombie_item.move(start_x, start_y)
			zombie_item.show()

			# 更新X坐标，用于放置下一个僵尸
			start_x += zombie_width + horizontal_spacing


class NormalSelectButton(QLabel):
	"""
	开场选择按钮
	"""
	clicked = pyqtSignal()
	hovered = pyqtSignal(bool)

	def __init__(self, p=None, normal_pix_str="", hover_pix_str="", width=400, height=150, pix_width=120):
		super(NormalSelectButton, self).__init__(p)
		self.height = height
		self.normal_pix = QPixmap(normal_pix_str).scaled(width, pix_width)
		self.hover_pix = QPixmap(hover_pix_str).scaled(width, pix_width)
		self.width = width
		self.param_init()
		self.ui_init()

	def param_init(self):
		self.is_hovered = False

	def ui_init(self):
		self.setFixedSize(QSize(self.width, self.height))
		self.setPixmap(QPixmap(self.normal_pix))
		self.setCursor(Qt.PointingHandCursor)

	def change_status_pix(self, status):
		"""
		根据不同状态改变贴图
		"""
		self.is_hovered = status
		if status is True:
			self.setPixmap(QPixmap(self.hover_pix))
		else:
			self.setPixmap(QPixmap(self.normal_pix))

	def enterEvent(self, a0: QtCore.QEvent) -> None:
		self.hovered.emit(True)
		self.change_status_pix(True)
		super(NormalSelectButton, self).enterEvent(a0)

	def leaveEvent(self, a0: QtCore.QEvent) -> None:
		self.change_status_pix(False)
		self.hovered.emit(False)
		super(NormalSelectButton, self).leaveEvent(a0)

	def mouseReleaseEvent(self, ev: QtGui.QMouseEvent) -> None:
		self.clicked.emit()
		super(NormalSelectButton, self).mouseReleaseEvent(ev)


class PrepareButtonGroup(QWidget):
	"""
	开场准备按钮组
	"""
	btn_hovered = pyqtSignal()  # 鼠标移入
	btn_clicked = pyqtSignal(int)  # 点了哪个按钮

	def __init__(self, p=None):
		super(PrepareButtonGroup, self).__init__(p)
		self.ui_init()
		self.slot_init()

	def ui_init(self):
		self.setFixedHeight(450)
		self.setContentsMargins(0, 0, 0, 0)
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.StartAdventureButton = NormalSelectButton(self, ":images/others/prepare/StartAdventure.png",
													   ":images/others/prepare/StartAdventure1.png", )
		self.SelectorSmallGameButton = NormalSelectButton(self, ":images/others/prepare/SelectorSmallGame.png",
														  ":images/others/prepare/SelectorSmallGame1.png", 430)
		self.SelectorScreenChallengesButton = NormalSelectButton(self,
																 ":images/others/prepare/SelectorScreenChallenges.png",
																 ":images/others/prepare/SelectorScreenChallenges1.png",
																 400)
		self.SelectorScreenSurvivalButton = NormalSelectButton(self,
															   ":images/others/prepare/SelectorScreenSurvival.png",
															   ":images/others/prepare/SelectorScreenSurvival1.png",
															   370)

		self.StartAdventureButton.move(0, 30)
		self.SelectorSmallGameButton.move(0, 150)
		self.SelectorScreenChallengesButton.move(0, 230)
		self.SelectorScreenSurvivalButton.move(0, 310)

	def slot_init(self):
		self.StartAdventureButton.hovered.connect(self.btn_hovered.emit)
		self.StartAdventureButton.clicked.connect(lambda: self.btn_clicked.emit(1))

		self.SelectorSmallGameButton.hovered.connect(self.btn_hovered.emit)
		self.SelectorSmallGameButton.clicked.connect(lambda: self.btn_clicked.emit(2))

		self.SelectorScreenChallengesButton.hovered.connect(self.btn_hovered.emit)
		self.SelectorScreenChallengesButton.clicked.connect(lambda: self.btn_clicked.emit(3))

		self.SelectorScreenSurvivalButton.hovered.connect(self.btn_hovered.emit)
		self.SelectorScreenSurvivalButton.clicked.connect(lambda: self.btn_clicked.emit(4))


class NormalTransBGButton(ButtonBase):
	"""
	透明背景按钮
	"""
	style = """#normalTransBGButton{border:none;background-color:transparent;}"""

	def __init__(self, p=None):
		super(NormalTransBGButton, self).__init__(p)
		self.ui_init()
		self.setStyleSheet(self.style)

	def ui_init(self):
		self.setObjectName("normalTransBGButton")
		self.setFixedSize(QSize(110, 100))


class TransBgButtonGroup(QWidget):
	"""
	右下角透明背景按钮
	"""
	btn_clicked = pyqtSignal(int)

	def __init__(self, p=None):
		super(TransBgButtonGroup, self).__init__(p)
		self.ui_init()
		self.slot_init()

	def ui_init(self):
		self.layout = QHBoxLayout()
		self.btn1 = NormalTransBGButton(self)
		self.btn2 = NormalTransBGButton(self)
		self.btn3 = NormalTransBGButton(self)
		self.layout.addWidget(self.btn1)
		self.layout.addWidget(self.btn2)
		self.layout.addWidget(self.btn3)
		self.setLayout(self.layout)

	def slot_init(self):
		self.btn1.clicked.connect(lambda: self.btn_clicked.emit(1))
		self.btn2.clicked.connect(lambda: self.btn_clicked.emit(2))
		self.btn3.clicked.connect(lambda: self.btn_clicked.emit(3))


class SurfaceWidget(QWidget):
	"""

	"""

	def __init__(self, p=None):
		super(SurfaceWidget, self).__init__(p)
		self.param_init()
		self.ui_init()
		self.slot_init()

	def param_init(self):
		self.hand_is_shown = False  # 大手是否展示过
		self.can_click = True  # 是否能点击

	def paintEvent(self, event):
		super(SurfaceWidget, self).paintEvent(event)
		painter = QPainter(self)
		pixmap = QPixmap(':images/others/prepare/Surface.jpeg')  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()

	def ui_init(self):
		self.setMinimumWidth(1230)
		self.left_corner_tip = QLabel(self)
		tip_bg_pix = QPixmap(":images/others/prepare/wood_tip.png")
		self.left_corner_tip.setPixmap(tip_bg_pix)
		self.word_tip = QLabel(self.left_corner_tip)
		self.word_tip.setObjectName("word_tip")
		self.left_corner_tip.move(10, 0)
		self.word_tip.move(100, int(tip_bg_pix.size().height() * 0.66))
		self.word_tip.setText("亲爱的玩家")
		# 右边游戏模式选择
		self.prepareButtonGroup = PrepareButtonGroup(self)
		# 右下角选项按钮
		self.transBgButtonGroup = TransBgButtonGroup(self)
		self.transBgButtonGroup.raise_()
		self.prepareButtonGroup.raise_()

		# 开场僵尸大手
		self.zombieHandElement = ZombieHandElement(self)
		initial_pos = QPoint(int(self.width() * 0.25), self.height() + self.zombieHandElement.height() * 2.3)
		self.zombieHandElement.move(initial_pos)
		# 将元素层级降低
		self.zombieHandElement.lower()

	def slot_init(self):
		self.prepareButtonGroup.btn_hovered.connect(lambda: bus.effect_changed.emit("buttonclick"))

	def show_hand_animation(self):
		"""
		展示僵尸大手移动动画 自下而上
		"""
		if self.hand_is_shown is True: return
		start_pos = self.zombieHandElement.pos()
		end_pos = start_pos - QPoint(0, self.zombieHandElement.height())
		self.animation = QPropertyAnimation(self.zombieHandElement, b"pos")
		self.animation.setDuration(300)
		self.animation.setStartValue(start_pos)
		self.animation.setEndValue(end_pos)
		self.animation.start()
		self.hand_is_shown = True

	def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
		if self.can_click is False: return
		if a0.button() == Qt.LeftButton:
			# 点击右下角三项
			pass

	def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
		self.prepareButtonGroup.move(int(self.width() * 0.55), 60)
		self.transBgButtonGroup.move(int(self.width() * 0.695), int(self.height() * 0.78))
		super(SurfaceWidget, self).resizeEvent(a0)


class NormalWoodButton(ButtonBase):
	"""
	木质按钮
	"""
	style = """#normalWoodButton{background-color:rgb(143,67,27);font-size:11pt;border:1px solid black;border-radius:4px;color:rgb(213,159,43)}#normalWoodButton:hover{background-color:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.506, stop:0 rgba(255, 161, 83, 255), stop:1 rgba(157, 79, 34, 255));color:rgb(255,253,100);}"""

	def __init__(self, p=None):
		super(NormalWoodButton, self).__init__(p)
		self.ui_init()
		self.setStyleSheet(self.style)

	def ui_init(self):
		self.setObjectName("normalWoodButton")


class HelpPage(QWidget):
	"""
	帮助页面
	"""

	def __init__(self, p=None):
		super(HelpPage, self).__init__(p)
		self.ui_init()
		self.set_up_ui()

	def ui_init(self):
		self.layout = QVBoxLayout()
		self.help_tip = ImageLabel(self)
		self.back_btn = NormalWoodButton(self)
		self.back_btn.setFixedSize(QSize(155, 38))
		self.layout.addWidget(self.help_tip)
		self.layout.addWidget(self.back_btn)
		self.layout.setAlignment(self.help_tip, Qt.AlignHCenter)
		self.layout.setAlignment(self.back_btn, Qt.AlignHCenter)
		self.setLayout(self.layout)

	def set_up_ui(self):
		self.help_tip.set_pix(":images/others/prepare/help.png")
		self.back_btn.setText("主菜单")

	def paintEvent(self, event):
		super(HelpPage, self).paintEvent(event)
		painter = QPainter(self)
		pixmap = QPixmap(':images/others/prepare/help_bg.jpeg')  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()


class GameMoviePlayPage(QWidget):
	"""
	游戏通关 播放视频
	"""

	def __init__(self, p=None):
		super(GameMoviePlayPage, self).__init__(p)
		self.ui_init()
		self.load_res()
		if 0:
			self.start_play_moive()

	def ui_init(self):
		# 初始化窗口
		self.setGeometry(100, 100, 800, 600)
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)
		self.video_widget = QVideoWidget()
		self.layout.addWidget(self.video_widget)
		self.video_player = QMediaPlayer(self)
		self.audio_player = QMediaPlayer(self)
		self.video_player.setVideoOutput(self.video_widget)
		self.setLayout(self.layout)

	def load_res(self):
		video_res = QUrl("qrc:video/Zombies on Your Lawn video.mp4")
		audio_res = QUrl("qrc:video/Zombies on Your Lawn audio.m4s")
		self.video_player.setMedia(QMediaContent(video_res))
		self.audio_player.setMedia(QMediaContent(audio_res))

	def start_play_moive(self):
		"""
		开始播放 音视频
		"""
		self.play_video()
		self.play_audio()

	def play_video(self):
		# 播放视频
		self.video_player.play()

	def play_audio(self):
		# 播放音频
		self.audio_player.play()


class UnLockDialog(GameDialogBase):
	"""
	未解锁对话框
	"""

	def __init__(self, p=None):
		super(UnLockDialog, self).__init__(p)
		self.slot_init()

	def ui_init(self):
		super(UnLockDialog, self).ui_init()
		self.setFixedSize(QSize(400, 200))
		self.confirm_btn = NormalTransBGButton(self)
		self.confirm_btn.setFixedSize(QSize(300, 35))
		self.layout = QVBoxLayout()
		self.layout.addWidget(self.confirm_btn)
		self.layout.setAlignment(self.confirm_btn, Qt.AlignBottom | Qt.AlignHCenter)
		self.setLayout(self.layout)

	def slot_init(self):
		self.confirm_btn.clicked.connect(self.close)

	def paintEvent(self, event):
		super(GameDialogBase, self).paintEvent(event)
		painter = QPainter(self)
		pixmap = QPixmap(':images/others/prepare/unlock_dialog.png')  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()


class QuitGameDialog(GameDialogBase):
	"""
	未解锁对话框
	"""
	quite_game_signal = pyqtSignal()

	def __init__(self, p=None):
		super(QuitGameDialog, self).__init__(p)
		self.slot_init()

	def ui_init(self):
		super(QuitGameDialog, self).ui_init()
		self.setFixedSize(QSize(400, 200))
		self.confirm_btn = NormalTransBGButton(self)
		self.cancel_btn = NormalTransBGButton(self)
		self.confirm_btn.setFixedSize(QSize(158, 38))
		self.cancel_btn.setFixedSize(QSize(158, 38))
		self.layout = QVBoxLayout()
		button_layout = QHBoxLayout()
		button_layout.addWidget(self.confirm_btn)
		button_layout.addWidget(self.cancel_btn)
		spacerItem = QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
		self.layout.addItem(spacerItem)
		self.layout.addLayout(button_layout)
		self.setLayout(self.layout)

	def slot_init(self):
		self.confirm_btn.clicked.connect(self.quite_game_signal.emit)
		self.cancel_btn.clicked.connect(self.close)

	def paintEvent(self, event):
		super(GameDialogBase, self).paintEvent(event)
		painter = QPainter(self)
		pixmap = QPixmap(':images/others/prepare/quit_dialog.png')  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()


class NormalLevelCard(QWidget):
	"""
	关卡卡片
	"""
	hovered = pyqtSignal(bool)
	style = """#level_name{color:black;font-size:10pt;background-color:transparent;font-weight:600 pt;}"""

	def __init__(self, p=None):
		super(NormalLevelCard, self).__init__(p)
		self.param_init()
		self.ui_init()
		self.initialize_effects()
		self.slot_init()
		self.setStyleSheet(self.style)
		if 0:
			self.set_level_item({'pic': ':images/map/level/1.png', 'text': '冒险模式第1关'})

	def param_init(self):
		self.level_item = dict()
		self.can_clicked = False  # 关卡是否通过了

	def ui_init(self):
		self.setFixedSize(QSize(117, 117))
		self.setCursor(Qt.PointingHandCursor)
		self.layout = QVBoxLayout()
		self.game_passed_label = ImageLabel(self)
		self.game_passed_label.setFixedSize(QSize(72, 63))
		self.game_passed_label.set_pix(':images/others/game_passed.png')
		self.game_passed_label.move(0, 0)
		self.top_layout = QVBoxLayout()
		self.layout.setContentsMargins(10, 5, 10, 13)
		self.top_layout.setContentsMargins(5, 0, 10, 10)
		self.level_pic = ImageLabel(self)
		self.level_pic.setFixedSize(QSize(82, 62))
		self.level_name = QLabel(self)
		self.level_name.setObjectName("level_name")
		self.level_name.setFixedHeight(26)
		self.top_layout.addWidget(self.level_pic)
		self.layout.addLayout(self.top_layout)
		spacerItem = QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
		self.layout.addItem(spacerItem)
		self.layout.addWidget(self.level_name)
		self.setLayout(self.layout)
		self.game_passed_label.setVisible(False)
		self.game_passed_label.raise_()

	def slot_init(self):
		self.hovered.connect(lambda s: self.control_hovered_status(s))

	def control_hovered_status(self, s):
		level_name_style = """#level_name{color:%s;font-size:10pt;background-color:transparent;font-weight:600 pt;}"""
		if s is True:
			self.colorize_effect.setStrength(0.2)  # 应用高亮效果
			color = "red"
		else:
			self.colorize_effect.setStrength(0)
			color = "black"
		self.level_name.setStyleSheet(level_name_style % color)

	def set_level_item(self, level_item, ):
		"""
		关卡数据
		"""
		self.level_item = level_item
		level_pic = level_item.get("pic")
		level_word = level_item.get("text")
		self.level_pic.set_pix(level_pic)
		self.level_name.setText(level_word)

	def change_clearance_status(self, status, is_passed):
		"""
		改变关卡状态
		"""
		self.game_passed_label.setVisible(status)
		self.can_clicked = is_passed

	def initialize_effects(self):
		"""
		初始化效果，包括高亮和减速效果
		"""
		self.colorize_effect = QGraphicsColorizeEffect(self)
		self.setGraphicsEffect(self.colorize_effect)
		self.colorize_effect.setColor(Qt.white)  # 默认颜色为白色（高亮效果）
		self.colorize_effect.setStrength(0)  # 默认强度为0

	def enterEvent(self, a0: QtCore.QEvent) -> None:
		self.hovered.emit(True)
		super(NormalLevelCard, self).enterEvent(a0)

	def leaveEvent(self, a0: QtCore.QEvent) -> None:
		self.hovered.emit(False)
		super(NormalLevelCard, self).leaveEvent(a0)

	def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
		if a0.button() == Qt.LeftButton and self.can_clicked:
			bus.game_level_selected.emit(self.level_item)
		super(NormalLevelCard, self).mouseReleaseEvent(a0)

	def paintEvent(self, event):
		super(NormalLevelCard, self).paintEvent(event)
		painter = QPainter(self)
		pixmap = QPixmap(':images/others/level_card.png')  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()


class DaveWidget(QWidget):
	"""
	戴夫组件
	"""
	finished = pyqtSignal()  # 所有对话框都处理完了

	def __init__(self, p=None):
		super(DaveWidget, self).__init__(p)
		self.param_init()
		self.ui_init()
		self.slot_init()
		self.change_dave_data_item()
		if 0:
			self.set_dave_data_item(normal_conf.dave_dialog_list[0])

	def param_init(self):
		self.current_dave_pix_index = 0  # 当前是第几个画面
		self.current_dave_wave = ""  # 当前戴夫语音

	def ui_init(self):
		self.setMinimumWidth(350)
		self.layout = QHBoxLayout()
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.daveDialogElement = DaveDialogElement(self)
		self.daveDialogElement.continue_btn.setCursor(Qt.PointingHandCursor)
		self.daveElement = DaveElement(self)
		self.layout.addWidget(self.daveElement)
		self.setLayout(self.layout)
		self.daveDialogElement.raise_()

	def slot_init(self):
		self.daveDialogElement.continue_btn.clicked.connect(self.change_dave_data_item)

	def change_dave_data_item(self):
		"""
		发射戴夫当前语音内容
		:return:
		"""
		if self.current_dave_pix_index == len(normal_conf.dave_dialog_list):
			self.finished.emit()
		else:
			self.set_dave_data_item(normal_conf.dave_dialog_list[self.current_dave_pix_index])
			self.current_dave_pix_index += 1

	def set_dave_data_item(self, data_item):
		content = data_item.get("content", "")
		gif_pix = data_item.get("pix", "")
		audio = data_item.get("audio", "")
		self.daveDialogElement.set_dialog_content(content)
		self.daveElement.set_dave_movie(gif_pix)
		bus.effect_changed.emit(audio)

	def resizeEvent(self, a0: QtGui.QResizeEvent):
		self.daveDialogElement.move(int(self.width() / 1.7 - self.daveDialogElement.width() / 2), 60)
		super(DaveWidget, self).resizeEvent(a0)


class TipWidget(QFrame):
	"""
	游戏中提示组件
	"""
	style = """#tipWidget{background-color:rgba(0,0,0,0.5);}#tip_label{color:rgb(238,234,189);font-size:18pt;font-weight:600 pt;}"""

	def __init__(self, p=None):
		super(TipWidget, self).__init__(p)
		self.ui_init()
		self.setStyleSheet(self.style)
		if 0:
			self.set_tip_text("这是提示文字")

	def ui_init(self):
		self.setObjectName("tipWidget")
		self.setFixedHeight(65)
		self.layout = QHBoxLayout()
		self.tip_label = QLabel(self)
		self.tip_label.setObjectName("tip_label")
		spacerItem1 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		spacerItem2 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.layout.addItem(spacerItem1)
		self.layout.addWidget(self.tip_label)
		self.layout.addItem(spacerItem2)
		self.setLayout(self.layout)

	def set_tip_text(self, tip_text):
		"""
		设置提示文字
		"""
		self.show()
		self.raise_()
		self.tip_label.setText(tip_text)
		QTimer.singleShot(1500, self.hide)


class CurrencyWidget(QWidget):
	"""
	货币组件
	"""
	style = """QLabel{font-size:14pt;font-weight:600 pt;}#gold_dollar_label{color:rgb(247,188,6);}#silver_dollar_label{color:rgb(237,237,237);}#diamond_label{color:rgb(18,99,197);}"""

	def __init__(self, p=None):
		super(CurrencyWidget, self).__init__(p)
		self.param_init()
		self.ui_init()
		self.setStyleSheet(self.style)
		self.update_coin_count(1, 0)
		self.update_coin_count(2, 0)
		self.update_coin_count(3, 0)

	def param_init(self):
		self.silver_dollar_count = 999
		self.gold_dollar_count = 999
		self.diamond_count = 999

		self.label_height = 21

	def ui_init(self):
		self.setFixedSize(QSize(400, 45))
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.diamond_label = QLabel(self)
		self.gold_dollar_label = QLabel(self)
		self.silver_dollar_label = QLabel(self)
		self.diamond_label.setMinimumWidth(90)
		self.gold_dollar_label.setMinimumWidth(90)
		self.silver_dollar_label.setMinimumWidth(90)
		self.diamond_label.setObjectName("diamond_label")
		self.gold_dollar_label.setObjectName("gold_dollar_label")
		self.silver_dollar_label.setObjectName("silver_dollar_label")
		self.silver_dollar_label.move(53, self.label_height)
		self.gold_dollar_label.move(193, self.label_height)
		self.diamond_label.move(340, self.label_height)

	def update_coin_count(self, coin_type, count):
		"""
		更新金钱数量
		coin_type: 1: 钻石, 2: 金币, 3: 银币
		count: 变化数量, 可以传负数
		"""
		coin_type_label_dict = {
			1: [self.diamond_label, 'diamond_count'],
			2: [self.gold_dollar_label, 'gold_dollar_count'],
			3: [self.silver_dollar_label, 'silver_dollar_count'],
		}
		if coin_type not in coin_type_label_dict:
			return
		current_count = getattr(self, coin_type_label_dict[coin_type][1])
		new_count = current_count + count
		setattr(self, coin_type_label_dict[coin_type][1], new_count)
		coin_type_label_dict[coin_type][0].setText(str(new_count))

	def paintEvent(self, event):
		super(CurrencyWidget, self).paintEvent(event)
		painter = QPainter(self)
		pixmap = QPixmap(':images/others/currency/coinbank.png')  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()

	def show(self) -> None:
		QTimer.singleShot(3000, self.hide)
		super(CurrencyWidget, self).show()


class CurrencyItem(ImageLabel):
	"""
	货币组件
	"""
	currency_clicked = pyqtSignal(int)

	def __init__(self, p=None, currency_type=1):
		super(CurrencyItem, self).__init__(p)
		self.param_init()
		self.currency_type = currency_type
		self.set_currency_type(currency_type)

		self.angle = 0  # 初始角度
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.update_rotation)
		self.timer.start(50)  # 每50毫秒更新一次

	def param_init(self):
		self.diamod_side = 70
		self.dollar_side = 45
		self.setCursor(Qt.PointingHandCursor)
		self.setWindowFlag(Qt.WindowStaysOnTopHint)

	def set_currency_type(self, currency_type):
		"""
		设置货币类型
		"""
		currency_type_pix_dict = {
			1: ":images/others/currency/diamond.png",  # 钻石
			2: ":images/others/currency/gold_dollar.png",  # 金币
			3: ":images/others/currency/silver_dollar.png",  # 银币
		}
		if currency_type not in currency_type_pix_dict.keys():
			return
		if currency_type == 1:
			side_width = self.diamod_side
		else:
			side_width = self.dollar_side
		self.setFixedSize(QSize(side_width, side_width))
		self.set_pix(currency_type_pix_dict[currency_type])

	def mouseReleaseEvent(self, ev):
		if ev.button() == Qt.LeftButton:
			self.currency_clicked.emit(self.currency_type)
			try:
				self.deleteLater()
			except:
				pass
		super(CurrencyItem, self).mouseReleaseEvent(ev)

	def show(self):
		QTimer.singleShot(10000, self.hide)
		super(CurrencyItem, self).show()

	def update_rotation(self):
		# 每次增加5度旋转
		self.angle += 5
		if self.angle >= 360:
			self.angle = 0
		self.update()  # 重新绘制 QLabel

	def paintEvent(self, event):
		# 重写paintEvent进行自定义绘制
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)

		# 获取图片的中心点
		center = self.rect().center()

		# 创建旋转变换
		transform = QTransform()

		# 绕Y轴进行缩放模拟翻转效果
		scale_factor = abs(180 - self.angle % 360) / 90.0  # 从1.0到0再回到1.0的缩放值
		if scale_factor > 1.0:
			scale_factor = 2.0 - scale_factor  # 保证scale_factor在0-1之间变化

		transform.translate(center.x(), center.y())  # 将坐标系平移到中心
		transform.scale(scale_factor, 1)  # 缩放Y轴，X轴保持原样
		transform.translate(-center.x(), -center.y())  # 平移回去

		# 应用变换
		painter.setTransform(transform)

		# 先绘制阴影
		self.draw_shadow(painter)

		# 绘制图片
		painter.drawPixmap(self.rect(), self.pixmap())

	def draw_shadow(self, painter):
		"""
		绘制黑色阴影，随着图片旋转，边缘一圈阴影
		"""
		shadow_color = QColor(0, 0, 0, 80)  # 半透明黑色
		shrink_factor = 0.95  # 控制缩小比例，可以调整为更小的值
		# 创建缩小后的矩形
		shadow_rect = self.rect()
		# 缩小阴影矩形
		shadow_rect = shadow_rect.adjusted(
			int((1 - shrink_factor) * shadow_rect.width() / 2),
			int((1 - shrink_factor) * shadow_rect.height() / 2),
			-int((1 - shrink_factor) * shadow_rect.width() / 2),
			-int((1 - shrink_factor) * shadow_rect.height() / 2),
		)
		# 设置画笔和笔刷
		painter.setPen(Qt.NoPen)
		painter.setBrush(shadow_color)
		# 绘制阴影
		painter.drawEllipse(shadow_rect)


class AlmanacPicWidget(QWidget):
	"""
	图鉴图片
	"""

	def __init__(self, p=None):
		super(AlmanacPicWidget, self).__init__(p)
		self.param_init()
		self.ui_init()
		if 0:
			self.set_item_infos(
				{
					"item_level": 1,
					"cursor_pix": ":images/plants/CherryBomb/CherryBomb_static.png",
				}
			)

	def param_init(self):
		self.bg_pix = ""

	def ui_init(self):

		self.layout = QHBoxLayout()
		self.layout.setContentsMargins(10, 10, 10, 10)
		spacerItem1 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		spacerItem2 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.item_pic = ImageLabel(self)
		self.layout.addItem(spacerItem1)
		self.layout.addWidget(self.item_pic)
		self.layout.addItem(spacerItem2)
		self.setLayout(self.layout)

	def set_item_infos(self, item_infos, item_type="plant"):
		"""
		设置背景、图像
		"""

		item_level = item_infos.get("map_id", 1)  # 1白天	2黑夜	3泳池	4黑夜泳池
		level_bg_dict = {
			1: ":images/others/almanac/Almanac_GroundDay.jpg",
			2: ":images/others/almanac/Almanac_GroundNight.jpg",
			3: ":images/others/almanac/Almanac_GroundPool.jpg",
			4: ":images/others/almanac/Almanac_GroundNightPool.jpg",
			5: ":images/others/almanac/Almanac_GroundRoof.jpg",
		}
		if item_type == "zombie":
			self.setFixedSize(QSize(310, 270))
			self.bg_pix = level_bg_dict.get(1, "")
			move = QMovie(item_infos.get("idle_pix", ""))
			self.item_pic.setMovie(move)
			move.start()
		else:
			self.setFixedSize(QSize(296, 190))
			self.bg_pix = level_bg_dict.get(item_level, level_bg_dict[1])
			self.item_pic.set_pix(item_infos.get("cursor_pix", ""))
		self.repaint()
		self.update()

	def paintEvent(self, event):
		super(AlmanacPicWidget, self).paintEvent(event)
		if not self.bg_pix: return
		painter = QPainter(self)
		pixmap = QPixmap(self.bg_pix)  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()


class AlmanacDetail(QWidget):
	"""
	图鉴详情
	"""
	style = """QLabel{font-size:9pt;font-family:"微软雅黑";font-weight:550;}#damage_label,#range_label,#usage_label,#cost_label,#desc_info,#restore_label{color:rgb(69,47,26);}#item_name_label{font-size:17pt;font-weight:650;color:rgb(242,174,55);}#brief_intro{color:rgb(21,20,20);}#unique_label{color:rgb(149,61,105);}#damage_info_label,#range_info_label,#usage_info_label{color:rgb(247,94,75);}#desc_info{color:rgb(136,100,66);}"""

	def __init__(self, p=None, almanac_type="plant"):
		super(AlmanacDetail, self).__init__(p)
		self.alm_type = almanac_type
		self.param_init()
		self.ui_init()
		self.setStyleSheet(self.style)
		if 0:
			self.set_item_infos({
				"name": "樱桃炸弹",
				"description": "樱桃炸弹，能以炸掉一定区域内所有僵尸。他们一种下就会立刻引爆，所有请把他们种在僵尸们的身边。",
				"toughness": 300,
				"power": 1800,
				"range": "自身为中心周围1.5格的圆",
				"characteristics": "立即生效",
				"desc": "“我要‘爆’开了，”樱桃一号说。“不，我们是要‘炸’开了！”它哥哥樱桃二号说。经过激烈的商议之后，它们才统一达成“爆炸”这个说法。"
			})

	def param_init(self):
		self.bg_pix = ""

	def ui_init(self):
		self.setMaximumWidth(460)
		self.setContentsMargins(30, 20, 30, 20)
		self.bg_pix = ':images/others/almanac/Almanac_PlantCard.png' if self.alm_type == "plant" else ':images/others/almanac/Almanac_ZombieCard.png'
		self.repaint()
		self.update()
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(20, 10, 60, 20)
		self.top_layout = QHBoxLayout()
		self.top_layout.setContentsMargins(0, 0, 0, 0)
		self.almanacPicWidget = AlmanacPicWidget(self)
		spacerItem3 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		spacerItem4 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		spacerItem5 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		spacerItem6 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.top_layout.addItem(spacerItem3)
		self.top_layout.addWidget(self.almanacPicWidget)
		self.top_layout.addItem(spacerItem4)
		self.item_name_layout = QHBoxLayout()
		self.item_name_layout.setContentsMargins(0, 20, 0, 40)
		self.item_name_label = QLabel(self)
		self.item_name_layout.addItem(spacerItem5)
		self.item_name_layout.addWidget(self.item_name_label)
		self.item_name_layout.addItem(spacerItem6)
		self.info_layout = QVBoxLayout()
		self.brief_intro = QLabel(self)
		self.info_form = QFormLayout()
		# 信息表单
		self.damage_label = QLabel(self)
		self.damage_info_label = QLabel(self)
		self.range_label = QLabel(self)
		self.range_info_label = QLabel(self)
		self.usage_label = QLabel(self)
		self.usage_info_label = QLabel(self)
		self.item_name_label.setObjectName("item_name_label")
		self.brief_intro.setObjectName("brief_intro")
		self.damage_label.setObjectName("damage_label")
		self.damage_info_label.setObjectName("damage_info_label")
		self.range_label.setObjectName("range_label")
		self.range_info_label.setObjectName("range_info_label")

		self.damage_label.setText("伤害：")
		self.range_label.setText("范围：")

		self.info_form.addRow(self.damage_label, self.damage_info_label)
		self.info_form.addRow(self.range_label, self.range_info_label)

		self.info_bottom_layout = QHBoxLayout()
		self.cost_layout = QHBoxLayout()
		self.resote_layout = QHBoxLayout()
		self.cost_label = QLabel(self)
		self.cost_info = QLabel(self)
		self.resote_label = QLabel(self)
		self.resote_info = QLabel(self)
		self.cost_label.setFixedWidth(28)
		spacerItem1 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.cost_layout.addWidget(self.cost_label)
		self.cost_layout.addWidget(self.cost_info)
		self.cost_layout.setAlignment(self.cost_info, Qt.AlignLeft)
		self.resote_layout.addItem(spacerItem1)
		self.resote_layout.addWidget(self.resote_label)
		self.resote_layout.addWidget(self.resote_info)
		self.resote_layout.setAlignment(self.resote_label, Qt.AlignRight)
		self.resote_layout.setAlignment(self.resote_info, Qt.AlignRight)
		self.cost_label.setText("花费：")
		self.resote_label.setText("恢复时间：")
		self.resote_label.setFixedWidth(55)
		self.info_bottom_layout.addLayout(self.cost_layout)
		self.info_bottom_layout.addLayout(self.resote_layout)

		self.unique_label = QLabel(self)
		self.unique_label.setWordWrap(True)
		self.desc_info = QLabel(self)
		self.desc_info.setMinimumHeight(60)
		self.desc_info.setWordWrap(True)
		self.unique_label.setObjectName("unique_label")
		self.desc_info.setObjectName("desc_info")
		self.info_layout.addWidget(self.brief_intro)
		self.info_layout.addLayout(self.info_form)
		self.info_layout.addWidget(self.unique_label)
		self.info_layout.addWidget(self.desc_info)

		spacerItem = QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
		self.layout.addLayout(self.top_layout)
		self.layout.addLayout(self.item_name_layout)
		self.layout.addLayout(self.info_layout)
		self.layout.addItem(spacerItem)
		self.layout.addLayout(self.info_bottom_layout)
		self.setLayout(self.layout)

	def set_item_infos(self, item_infos):
		"""
		展示数据信息
		"""
		if self.alm_type == "zombie":
			self.damage_label.setText("速度：")
			self.range_label.setText("体力：")
			self.range_info_label.setText(str(item_infos.get("toughness", "")))
			self.layout.setContentsMargins(40, 30, 60, 20)
			self.damage_info_label.setText(str(item_infos.get("speed", "")))
		else:
			self.damage_info_label.setText(str(item_infos.get("power", "")))
			self.range_info_label.setText(str(item_infos.get("range", "")))
			self.cost_info.setText(str(item_infos.get("cost", "")))
			cooling_word = convert_cooling(item_infos.get("cooling", ""))
			self.resote_info.setText(cooling_word)
			self.cost_label.setText("花费：")
			self.resote_label.setText("恢复时间：")
			self.range_label.setText("范围：")
			self.layout.setContentsMargins(20, 10, 60, 20)
		self.cost_label.setVisible(self.alm_type != "zombie")
		self.resote_label.setVisible(self.alm_type != "zombie")
		self.item_name_label.setText(item_infos.get("name", ""))
		self.brief_intro.setText(item_infos.get("description", ""))
		self.unique_label.setText(item_infos.get("characteristics", ""))
		self.desc_info.setText(item_infos.get("desc", ""))
		self.almanacPicWidget.set_item_infos(item_infos, self.alm_type)

	def paintEvent(self, event):
		super(AlmanacDetail, self).paintEvent(event)
		if not self.bg_pix: return
		painter = QPainter(self)
		pixmap = QPixmap(self.bg_pix)  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()


class AlmanacDetailPage(QWidget):
	"""
	图鉴详情页背景
	"""
	style = """#top_label{color:rgb(249,175,47);font-size:18pt;font-weight:600 pt;}#close_label,#back_label{color:rgb(38,34,34);font-size:10pt;font-weight:600 pt;}"""

	def __init__(self, p=None, almanac_type="plant"):
		super(AlmanacDetailPage, self).__init__(p)
		self.alm_type = almanac_type
		self.param_init()
		self.ui_init()
		self.setStyleSheet(self.style)

	def param_init(self):
		self.bg_pix = ""
		self.grid_row = 6
		self.grid_col = 8

	def ui_init(self):
		self.bg_pix = ':images/others/almanac/Almanac_PlantBack.jpg' if self.alm_type == "plant" else ':images/others/almanac/Almanac_ZombieBack.jpg'
		self.alm_title = "图鉴——植物" if self.alm_type == "plant" else "图鉴——僵尸"
		self.layout = QVBoxLayout()
		self.top_widget = QWidget(self)
		self.top_widget_layout = QHBoxLayout()
		self.top_widget.setLayout(self.top_widget_layout)
		self.top_widget.setFixedHeight(100)
		self.top_label = QLabel(self)
		self.top_label.setObjectName("top_label")
		self.top_label.setText(self.alm_title)
		spacerItem1 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		spacerItem2 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.top_widget_layout.addItem(spacerItem1)
		self.top_widget_layout.addWidget(self.top_label)
		self.top_widget_layout.addItem(spacerItem2)
		self.middle_layout = QHBoxLayout()
		self.middle_layout.setContentsMargins(0, 0, 0, 0)
		self.middle_card_grid = QGridLayout()
		self.middle_card_grid.setContentsMargins(0, 0, 0, 0)
		self.middle_card_grid.setHorizontalSpacing(0)
		self.middle_card_grid.setVerticalSpacing(5)
		self.middle_layout.addLayout(self.middle_card_grid)
		self.almanacDetail = AlmanacDetail(self, almanac_type=self.alm_type)
		self.middle_layout.addWidget(self.almanacDetail)
		self.bottom_layout = QHBoxLayout()
		self.back_btn = NormalSelectButton(self,
										   ":images/others/almanac/Almanac_IndexButton.png",
										   ":images/others/almanac/Almanac_IndexButtonHighlight.png",
										   170, 25, 25)
		self.close_btn = NormalSelectButton(self,
											":images/others/almanac/Almanac_CloseButton.png",
											":images/others/almanac/Almanac_CloseButtonHighlight.png",
											95, 25, 25)
		self.bottom_layout.addWidget(self.back_btn)
		self.bottom_layout.setAlignment(self.back_btn, Qt.AlignBottom)
		spacerItem1 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.bottom_layout.addItem(spacerItem1)
		self.bottom_layout.addWidget(self.close_btn)
		self.bottom_layout.setAlignment(self.close_btn, Qt.AlignBottom)
		self.back_label = QLabel("图鉴索引")
		self.close_label = QLabel("关闭")
		self.back_label.setObjectName("back_label")
		self.close_label.setObjectName("close_label")
		self.back_btn_hover_layout = QHBoxLayout(self.back_btn)
		self.back_btn_hover_layout.addWidget(self.back_label)
		self.back_btn_hover_layout.setAlignment(self.back_label, Qt.AlignRight)
		self.close_btn_hover_layout = QHBoxLayout(self.close_btn)
		self.close_btn_hover_layout.addWidget(self.close_label)
		self.close_btn_hover_layout.setAlignment(self.close_label, Qt.AlignRight)
		self.back_btn_hover_layout.setContentsMargins(0, 0, 50, 0)
		self.close_btn_hover_layout.setContentsMargins(0, 0, 40, 0)
		self.layout.addWidget(self.top_widget)
		self.layout.addLayout(self.middle_layout)
		self.layout.addLayout(self.bottom_layout)
		self.setLayout(self.layout)

	def slot_init(self):
		self.close_btn.clicked.connect()

	import copy

	def load_alma_cards(self, plant_param_dict):
		"""
		加载卡片到网格布局
		:param plant_param_dict:
		:return:
		"""
		# 使用深拷贝创建 card_items，避免修改原始数据
		card_items = copy.deepcopy(list(plant_param_dict.values()))
		card_items.sort(key=lambda item: item.get('for_upgrade', False), reverse=False)
		index = 0
		for row in range(self.grid_row):
			for col in range(self.grid_col):
				if index < len(card_items):
					if self.alm_type == "plant":
						item_card = SimpleCard(self)
					else:
						item_card = ZombieCard(self)
					item_card.setFixedSize(QSize(77, 95))
					card_item = card_items[index]
					if self.alm_type == "plant":
						item_desc_infos = query_item_infos(card_item['id'], item_desc.plants)
					else:
						item_desc_infos = query_item_infos(card_item['id'], item_desc.zombies)
					# 更新 card_item 数据
					card_item.update(item_desc_infos)
					if index == 0:  # 展示默认
						self.handle_card_clicked(card_item)
					item_card.set_card_item(card_item)
					item_card.card_item_clicked.connect(
						partial(self.handle_card_clicked, card_item))
					self.middle_card_grid.addWidget(item_card, row, col)
					index += 1

	def handle_card_clicked(self, card_item):
		"""
		卡片被单击事件
		"""
		card_item['name'] = card_item.get("cn_name", "") if card_item.get("characteristics") is None else card_item.get(
			"name", "")
		bus.effect_changed.emit("buttonclick")
		self.almanacDetail.set_item_infos(card_item)

	def paintEvent(self, event):
		super(AlmanacDetailPage, self).paintEvent(event)
		if not self.bg_pix: return
		painter = QPainter(self)
		pixmap = QPixmap(self.bg_pix)  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()


class NormalAlmanacIndexItem(QWidget):
	"""
	图鉴类别选择基础item
	"""

	def __init__(self, p=None, item_type="plant"):
		super(NormalAlmanacIndexItem, self).__init__(p)
		self.item_type = item_type
		self.ui_init()
		self.set_item()

	def ui_init(self):
		self.setFixedSize(QSize(550, 192))
		self.layout = QVBoxLayout()
		self.top_img = ImageLabel(self)
		self.bottom_btn = ButtonBase(self)
		self.bottom_btn.setFixedSize(QSize(156, 36))
		self.bottom_btn.setObjectName("bottom_btn")
		self.layout.addWidget(self.top_img)
		self.layout.setAlignment(self.top_img, Qt.AlignHCenter)
		self.layout.addWidget(self.bottom_btn)
		self.layout.setAlignment(self.bottom_btn, Qt.AlignHCenter)
		self.setLayout(self.layout)

	def set_item(self):
		if self.item_type == "plant":
			img_pix = ":images/plants/SunFlower/SunFlower1.gif"
			style = """#bottom_btn{border:2px solid rgb(142,67,27);font-weight:600;background-color:rgb(143,67,27);font-size:13pt;color:rgb(203,146,41);border-radius:3px;}#bottom_btn:hover{background-color:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.506, stop:0 rgba(255, 161, 83, 255), stop:1 rgba(157, 79, 34, 255));color:rgb(255,253,100);}"""
			self.bottom_btn.setText("查看植物")
		else:
			img_pix = ":images/zombies/Zombie/1.gif"
			style = """#bottom_btn{border:5px solid rgb(87,88,118);font-weight:600;background-color:rgb(93,95,126);font-size:13pt;color:rgb(0,214,0);border-radius:3px;}#bottom_btn:hover{background-color:qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.506, stop:0 rgba(153,156,171, 255), stop:1 rgba(93,95,126, 255));color:rgb(255,253,100);}"""
			self.bottom_btn.setText("查看僵尸")
			self.top_img.setFixedSize(QSize(250, 140))
		movie = QMovie(img_pix)
		self.top_img.setMovie(movie)
		movie.start()
		self.bottom_btn.setStyleSheet(style)


class AlmanacIndexPage(QWidget):
	"""
	图鉴索引选择组件
	"""
	style = """#top_label{color:rgb(218,218,218);font-size:18pt;font-weight:600 pt;}#close_label,#back_label{color:rgb(38,34,34);font-size:10pt;font-weight:800;}"""

	def __init__(self, p=None):
		super(AlmanacIndexPage, self).__init__(p)
		self.ui_init()
		self.setStyleSheet(self.style)

	def ui_init(self):
		self.layout = QVBoxLayout()
		self.alm_title = "图鉴——索引"
		self.top_widget = QWidget(self)
		self.top_widget_layout = QHBoxLayout()
		self.top_widget.setLayout(self.top_widget_layout)
		self.top_widget.setFixedHeight(110)
		self.top_label = QLabel(self)
		self.top_label.setObjectName("top_label")
		self.top_label.setText(self.alm_title)
		spacerItem1 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		spacerItem2 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.top_widget_layout.addItem(spacerItem1)
		self.top_widget_layout.addWidget(self.top_label)
		self.top_widget_layout.addItem(spacerItem2)

		self.trans_widget = QWidget(self)
		self.trans_widget.setFixedHeight(170)

		self.middle_layout = QHBoxLayout()
		self.normalAlmanacIndexItemPlant = NormalAlmanacIndexItem(self)
		self.normalAlmanacIndexItemZombie = NormalAlmanacIndexItem(self, "zombie")
		self.middle_layout.addWidget(self.normalAlmanacIndexItemPlant)
		self.middle_layout.addWidget(self.normalAlmanacIndexItemZombie)
		self.close_btn = NormalSelectButton(self,
											":images/others/almanac/Almanac_CloseButton.png",
											":images/others/almanac/Almanac_CloseButtonHighlight.png",
											95, 25, 25)
		spacerItem0 = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.close_label = QLabel("关闭")
		self.close_label.setObjectName("close_label")
		self.bottom_layout = QHBoxLayout()
		self.bottom_layout.addItem(spacerItem0)
		self.bottom_layout.addWidget(self.close_btn)
		self.close_btn_hover_layout = QHBoxLayout(self.close_btn)
		self.close_btn_hover_layout.addWidget(self.close_label)
		self.close_btn_hover_layout.setAlignment(self.close_label, Qt.AlignRight)
		self.close_btn_hover_layout.setContentsMargins(0, 0, 40, 0)
		self.layout.addWidget(self.top_widget)
		self.layout.addWidget(self.trans_widget)

		self.layout.addLayout(self.middle_layout)
		spacerItem = QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
		self.layout.addItem(spacerItem)
		self.layout.addLayout(self.bottom_layout)
		self.setLayout(self.layout)

	def paintEvent(self, event):
		super(AlmanacIndexPage, self).paintEvent(event)
		painter = QPainter(self)
		pixmap = QPixmap(":images/others/almanac/Almanac_IndexBack.jpg")  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()


class AlmanacWidget(QWidget):
	"""
	图鉴组件 包含两个页面
	1.植物or僵尸选择页面
	2.植物or僵尸详情页面
	"""
	almanac_closed = pyqtSignal()  # 图鉴关闭

	def __init__(self, p=None):
		super(AlmanacWidget, self).__init__(p)
		self.ui_init()
		self.set_up_ui()
		self.slot_init()

	def ui_init(self):
		self.setFixedSize(QSize(1230, 800))
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.stacked_widget = QStackedWidget(self)
		self.layout.addWidget(self.stacked_widget)
		self.almanacIndexPage = AlmanacIndexPage(self)
		self.plantAlmanacDetailPage = AlmanacDetailPage(self, almanac_type="plant")
		self.zombieAlmanacDetailPage = AlmanacDetailPage(self, almanac_type="zombie")
		self.stacked_widget.addWidget(self.almanacIndexPage)
		self.stacked_widget.addWidget(self.plantAlmanacDetailPage)
		self.stacked_widget.addWidget(self.zombieAlmanacDetailPage)
		self.setLayout(self.layout)

	def set_up_ui(self):
		self.plantAlmanacDetailPage.load_alma_cards(normal_conf.plant_param_dict)
		self.zombieAlmanacDetailPage.load_alma_cards(normal_conf.zombie_param_dict)

	def slot_init(self):
		self.plantAlmanacDetailPage.close_btn.clicked.connect(self.almanac_closed.emit)
		self.zombieAlmanacDetailPage.close_btn.clicked.connect(self.almanac_closed.emit)
		self.plantAlmanacDetailPage.back_btn.clicked.connect(lambda: self.change_stacked_index(0))
		self.zombieAlmanacDetailPage.back_btn.clicked.connect(lambda: self.change_stacked_index(0))
		self.almanacIndexPage.normalAlmanacIndexItemPlant.bottom_btn.clicked.connect(
			lambda: self.change_stacked_index(1))
		self.almanacIndexPage.normalAlmanacIndexItemZombie.bottom_btn.clicked.connect(
			lambda: self.change_stacked_index(2))

	def change_stacked_index(self, aim_index):
		self.stacked_widget.setCurrentIndex(aim_index)


class GameOverDialog(QDialog):
	"""
	游戏失败对话框
	"""

	def __init__(self, p=None):
		super(GameOverDialog, self).__init__(p)
		self.ui_init()
		self.slot_init()

	def ui_init(self):
		self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setModal(Qt.ApplicationModal)
		self.setFixedSize(QSize(380, 220))
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(10, 10, 10, 22)
		self.confirm_btn = NormalTransBGButton(self)
		self.confirm_btn.setFixedSize(QSize(286, 31))
		spacerItem = QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
		self.layout.addItem(spacerItem)
		self.layout.addWidget(self.confirm_btn)
		self.setLayout(self.layout)

	def slot_init(self):
		self.confirm_btn.clicked.connect(self.hide)

	def paintEvent(self, event):
		super(GameOverDialog, self).paintEvent(event)
		painter = QPainter(self)
		pixmap = QPixmap(':images/others/game_over_dialog.png')  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()

	# 无边框的拖动
	def mouseMoveEvent(self, e: QtGui.QMouseEvent):  # 重写移动事件
		try:
			self._endPos = e.pos() - self._startPos
			self.move(self.pos() + self._endPos)
		except (AttributeError, TypeError):
			pass

	def mousePressEvent(self, e: QtGui.QMouseEvent):
		if e.button() == QtCore.Qt.LeftButton:
			self._isTracking = True
			self._startPos = QtCore.QPoint(e.x(), e.y())

	def mouseReleaseEvent(self, e: QtGui.QMouseEvent):
		if e.button() == QtCore.Qt.LeftButton:
			self._isTracking = False
			self._startPos = None
			self._endPos = None

	def reject(self):
		pass

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			pass
		else:
			super(GameOverDialog, self).keyPressEvent(event)


if __name__ == '__main__':
	QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
	QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
	QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
	app = QApplication(sys.argv)
	app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
	win = GameOverDialog()
	# win = AlmanacIndexPage()
	# win = NormalAlmanacIndexItem()
	# win = AlmanacWidget()
	# win = AlmanacPicWidget()
	# win = AlmanacDetail()
	# win = AlmanacDetailPage()
	# win = CurrencyItem(None, 3)
	# win = CurrencyWidget()
	# win = TipWidget()
	# win = DaveWidget()
	# win = GameDialogBase()
	# win = NormalLevelCard()
	# win = QuitGameDialog()
	# win = SurfaceWidget()
	# win = UnLockDialog()
	# win = GameMoviePlayPage()
	# win = GameLoadingBG()
	# win = HelpPage()
	# win = MainSetDialog()
	# win = MenuDialog()
	# win = MianSetItems()
	# win = PrepareButtonGroup()
	# win = ZombiePrepareArea()
	# win = StartRockBtn()
	# win = PlantSelectWidget()
	# win = PlantSelectBasket()
	# win = PlantToolTip()
	# win = GameProgressWidget()
	# win = ProgressWidget()
	# win = AutoSunflower()
	# win = NormalZombieItem()
	# win = ShovelBasket()
	# win = SunFlowerBasket()
	# win = PlantCardBasket()
	# win = Lawn(None, 3)
	# win = NormaGrassItem()
	win.show()
	sys.exit(app.exec_())
