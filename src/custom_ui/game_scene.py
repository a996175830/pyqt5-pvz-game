import random
import sys
import traceback

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QPoint, QRect, \
	QEasingCurve, QUrl, QTime, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QPainter, QPalette, QCursor, QKeySequence, QMovie
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QDialog, QMainWindow, QHBoxLayout, \
	QShortcut, QLabel, QStackedLayout, QGridLayout, QSizePolicy, QSpacerItem

from src.map import game_level
from src.my_util.utils import read_saved_file, save_to_saved_file
from src.signal_bus import bus
from .widgets import PlantCardBasket, Lawn, SlidingStackedWidget, NormalStyleButton, NormalStyleLabel, \
	AutoSunflower, GameProgressWidget, PlantToolTip, PlantSelectWidget, ZombiePrepareArea, ImageLabel, SurfaceWidget, \
	HelpPage, MainSetDialog, UnLockDialog, QuitGameDialog, NormalLevelCard, NormalWoodButton, DaveWidget, CurrencyWidget
from src.resources import resource_rc
from src.config import game_conf


class GameScene(QWidget):
	"""
	游戏场景
	"""

	def __init__(self, p=None, map_id=True):
		super(GameScene, self).__init__(p)
		self.map_id = map_id
		self.param_init()
		self.ui_init()

	def param_init(self):
		self.left_margin = 0
		self.top_margin = 0
		self.right_margin = 0
		self.bottom_margin = 25
		self.bg_pic = QPixmap()  # 背景图片

	def ui_init(self):
		self.resize(1380, 760)
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(self.left_margin, self.top_margin, self.right_margin, self.bottom_margin)
		self.plantCardBasket = PlantCardBasket(self)
		self.plantCardBasket.setMinimumWidth(880)
		self.top_layout = QHBoxLayout()
		self.top_layout.setContentsMargins(150, 5, 5, 5)
		self.top_layout.addWidget(self.plantCardBasket)
		self.top_layout.setAlignment(self.plantCardBasket, Qt.AlignLeft)
		self.menu_btn = NormalStyleButton(self, "菜单", ":images/others/prepare/button.png")
		self.lawn = Lawn(self)
		self.gameProgressWidget = GameProgressWidget(self)
		self.layout.addLayout(self.top_layout)
		self.layout.addWidget(self.lawn)
		self.setLayout(self.layout)

		# 游戏货币
		self.currencyWidget = CurrencyWidget(self)
		self.currencyWidget.move(QPoint(0, int(self.height() - 5)))
		self.currencyWidget.hide()

	def set_bg_pic(self, bg_pic):
		self.bg_pic = bg_pic
		self.repaint()
		self.update()

	def paintEvent(self, event):
		super(GameScene, self).paintEvent(event)
		if not self.bg_pic: return
		painter = QPainter(self)
		pixmap = QPixmap(self.bg_pic)
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()

	def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
		self.menu_btn.move(self.width() - self.menu_btn.width() - 3, 3)
		self.gameProgressWidget.move(self.width() - self.gameProgressWidget.width(),
									 self.height() - self.gameProgressWidget.height() + 5)
		super(GameScene, self).resizeEvent(a0)


class GamePrepareScene(QWidget):
	"""
	游戏开场准备场景
	"""

	def __init__(self, p=None):
		super(GamePrepareScene, self).__init__(p)
		self.param_init()
		self.ui_init()

	def param_init(self):
		self.prepare_bg_pic = ""

	def set_map_bg(self, map_bg):
		"""
		等待 地图背景
		"""
		self.prepare_bg_pic = map_bg
		self.repaint()
		self.update()

	def ui_init(self):
		self.setAttribute(Qt.WA_TranslucentBackground, True)
		self.layout = QHBoxLayout()
		self.plantSelectWidget = PlantSelectWidget(self)
		self.zombiePrepareArea = ZombiePrepareArea(self)
		self.layout.addWidget(self.plantSelectWidget)
		self.layout.addWidget(self.zombiePrepareArea)
		self.layout.setStretch(0, 4)
		self.layout.setStretch(1, 1)
		self.setLayout(self.layout)

	def set_prepare_scene(self, bg_pix):
		"""
		根据id计算背景图片
		"""
		self.bg_pix = bg_pix
		self.repaint()
		self.update()

	def paintEvent(self, event):
		super(GamePrepareScene, self).paintEvent(event)
		if self.prepare_bg_pic:
			painter = QPainter(self)
			pixmap = QPixmap(self.prepare_bg_pic)  # : 是 qrc 文件的标识符
			painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
			painter.end()


class GameLoadingScene(QWidget):
	"""
	游戏场景加载 首屏背景
	"""

	def __init__(self, p=None):
		super(GameLoadingScene, self).__init__(p)
		self.ui_init()
		self.set_up_ui()
		self.slot_init()

	def ui_init(self):
		self.start_btn = ImageLabel(self)
		self.start_btn.setCursor(Qt.PointingHandCursor)
		self.start_btn.setFixedWidth(350)
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(0, 0, 0, 30)
		self.layout.addWidget(self.start_btn)
		self.layout.setAlignment(self.start_btn, Qt.AlignBottom | Qt.AlignHCenter)
		self.setLayout(self.layout)

	def set_up_ui(self):
		pix = QPixmap(":images/others/prepare/click_to_start.jpeg")
		self.start_btn.set_pix(pix.scaled(self.start_btn.width(), 80))

	def slot_init(self):
		self.start_btn.hovered.connect(lambda: bus.effect_changed.emit("loadingbar_flower")
									   )

	def paintEvent(self, event):
		super(GameLoadingScene, self).paintEvent(event)
		painter = QPainter(self)
		pixmap = QPixmap(':images/others/prepare/start_bg.jpeg')  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()


class GameStartScene(QWidget):
	"""
	游戏开始背景
	"""
	style = """#word_tip{color:rgb(254,244,199);font-weight:600 pt;font-size:12pt;}"""
	game_mode_selected = pyqtSignal(int)  # 选了游戏模式

	def __init__(self, p=None):
		super(GameStartScene, self).__init__(p)
		self.param_init()
		self.ui_init()
		self.timer_init()
		self.slot_init()
		self.setStyleSheet(self.style)

	def param_init(self):
		self.can_click = True  # 是否能点击

	def ui_init(self):
		self.setMinimumWidth(1230)
		self.layout = QStackedLayout()
		self.surfaceWidget = SurfaceWidget(self)
		self.helpPage = HelpPage(self)
		self.layout.addWidget(self.surfaceWidget)
		self.layout.addWidget(self.helpPage)
		self.setLayout(self.layout)
		self.mainSetDialog = MainSetDialog(self)  # 设置对话框
		self.mainSetDialog.hide()

		self.unLockDialog = UnLockDialog(self)  # 未解锁 对话框
		self.unLockDialog.hide()

		self.quitGameDialog = QuitGameDialog(self)  # 退出游戏
		self.quitGameDialog.hide()

		# 背景遮罩
		self.overlay = QWidget(self)
		self.setObjectName("overlay")
		self.overlay.setAutoFillBackground(True)
		palette = self.overlay.palette()
		palette.setColor(QPalette.Window, QColor(70, 70, 70, 100))  # Adjust alpha for transparency
		self.overlay.setPalette(palette)
		self.overlay.hide()  # 默认隐藏 只有弹消息才会展示

	def slot_init(self):
		self.surfaceWidget.prepareButtonGroup.btn_clicked.connect(lambda index: self.process_game_mode(index))
		self.surfaceWidget.transBgButtonGroup.btn_clicked.connect(lambda index: self.process_game_set(index))
		self.helpPage.back_btn.clicked.connect(lambda: self.layout.setCurrentIndex(0))
		self.mainSetDialog.confirm_btn.clicked.connect(self.close_menu)

	def show_menu(self):
		self.mainSetDialog.show()
		self.overlay.show()

	def close_menu(self):
		self.mainSetDialog.hide()
		self.overlay.hide()

	def timer_init(self):
		self.twinkle_timer = QTimer()
		self.twinkle_timer.setInterval(100)
		self.twinkle_timer.timeout.connect(self.set_twinkle_effect)

	def set_twinkle_effect(self):
		"""
		设置第一个按钮一闪一闪
		"""
		self.surfaceWidget.prepareButtonGroup.StartAdventureButton.change_status_pix(
			not self.surfaceWidget.prepareButtonGroup.StartAdventureButton.is_hovered)

	def process_game_mode(self, index):
		"""
		处理游戏设置
		"""
		if not self.can_click:
			return  # 如果不能点击，直接返回
		if index == 1:
			self.surfaceWidget.show_hand_animation()  # 展示僵尸大手
			bus.effect_changed.emit("start_laugh")
			# 延迟处理
			self.can_click = False
			self.twinkle_timer.start()
			QTimer.singleShot(4500, lambda: self.enable_click(index))  # 处理结束后再允许点击
			return
		else:
			self.unLockDialog.show()

	def process_game_set(self, index):
		"""
		处理游戏模式
		"""
		if index == 1:
			self.show_menu()
		elif index == 2:
			self.layout.setCurrentIndex(1)
		elif index == 3:
			self.quitGameDialog.show()

	def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
		if self.can_click is False: return
		super(GameStartScene, self).mouseReleaseEvent(a0)

	def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
		self.overlay.setGeometry(self.rect())
		super(GameStartScene, self).resizeEvent(a0)

	def enable_click(self, index):
		"""
		重新允许点击
		"""
		self.can_click = True
		self.game_mode_selected.emit(index)


class GameLevelSelectScene(QWidget):
	"""
	游戏关卡选择
	"""

	def __init__(self, p=None):
		super(GameLevelSelectScene, self).__init__(p)
		self.param_init()
		self.ui_init()

	def param_init(self):
		self.row_num = 4
		self.col_num = 5
		self.max_level_id = -1  # 最大关卡id
		self.level_item_dict = {}

	def ui_init(self):
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(10, 10, 10, 0)
		self.top_widget = QWidget(self)
		self.top_widget.setFixedHeight(70)
		self.middle_grid = QGridLayout()
		self.btn_layout = QHBoxLayout()
		self.btn_layout.setContentsMargins(20, 10, 10, 5)
		self.back_menu_btn = NormalWoodButton(self)
		self.back_menu_btn.setFixedSize(QSize(100, 25))
		self.back_menu_btn.setText("返回菜单")
		self.btn_layout.addWidget(self.back_menu_btn)
		self.btn_layout.setAlignment(self.back_menu_btn, Qt.AlignLeft | Qt.AlignBottom)
		spacerItem = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.btn_layout.addItem(spacerItem)
		self.layout.addWidget(self.top_widget)
		self.layout.addLayout(self.middle_grid)
		self.layout.addLayout(self.btn_layout)
		self.setLayout(self.layout)

	def get_current_level(self):
		"""
		获取通关了的关卡
		"""
		current_level = 0
		try:
			current_level_list = read_saved_file(game_conf.level_saved_file)
			if len(current_level_list) != 0:
				current_level = int(current_level_list[0])
		except:
			traceback.print_exc()
		return current_level

	def save_current_levle(self, level):
		"""
		设置新的关卡记录
		"""
		save_to_saved_file(game_conf.level_saved_file, [level])

	def load_levels(self, level_list):
		"""
		加载关卡
		"""
		# 填充网格
		counter = 0
		for row in range(self.row_num):
			for col in range(self.col_num):
				level_item = NormalLevelCard(self)
				level_item.hovered.connect(lambda: bus.effect_changed.emit("tap"))
				level_item.set_level_item(level_list[counter])
				self.middle_grid.addWidget(level_item, row, col)
				counter += 1
				self.level_item_dict[counter] = level_item

	def update_game_level(self):
		"""
		更新关卡状态
		"""
		current_level = self.get_current_level()
		if 0:
			current_level = 5
		for each_level in self.level_item_dict.keys():
			is_passed = each_level <= current_level
			can_clicked = each_level <= current_level + 1  # 之前通过的关卡和最近未通过的关卡均可点击
			self.level_item_dict[each_level].change_clearance_status(is_passed, can_clicked)

	def paintEvent(self, event):
		super(GameLevelSelectScene, self).paintEvent(event)
		painter = QPainter(self)
		pixmap = QPixmap(':images/others/prepare/level_select_bg.png')  # : 是 qrc 文件的标识符
		painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
		painter.end()


class CrazyDaveScene(QWidget):
	"""
	展示疯狂戴夫
	"""

	def __init__(self, p=None):
		super(CrazyDaveScene, self).__init__(p)
		self.ui_init()

	def set_map_bg(self, map_bg):
		self.prepare_bg_pic = map_bg
		self.repaint()
		self.update()

	def ui_init(self):
		self.layout = QHBoxLayout()
		self.setContentsMargins(0, 0, 0, 0)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.daveWidget = DaveWidget(self)
		self.layout.addWidget(self.daveWidget)
		spacerItem = QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.layout.addItem(spacerItem)
		self.setLayout(self.layout)

	def paintEvent(self, event):
		super(CrazyDaveScene, self).paintEvent(event)
		if self.prepare_bg_pic:
			painter = QPainter(self)
			pixmap = QPixmap(self.prepare_bg_pic)  # : 是 qrc 文件的标识符
			painter.drawPixmap(QRect(0, 0, self.width(), self.height()), pixmap)
			painter.end()


if __name__ == '__main__':
	QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
	QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
	QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
	app = QApplication(sys.argv)
	app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
	# win = CrazyDaveScene()
	win = GameLevelSelectScene()
	# win = GameLoadingScene()
	# win = GameStartScene()
	# win = GamePrepareScene()
	win.show()
	sys.exit(app.exec_())
