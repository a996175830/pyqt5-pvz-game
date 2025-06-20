import math
import random
import sys

from PyQt5.QtGui import QPixmap, QPainter

from .base import Element
from PyQt5.QtCore import QTimer, QPoint, Qt, QSize, QRect
from PyQt5.QtWidgets import QApplication, QFrame, QGraphicsColorizeEffect, QLabel, QVBoxLayout, QPushButton
from src.resources import resource_rc


class LawnMower(Element):
	"""
	除草机
	"""

	def __init__(self, p=None, is_swimming_pool=True, line_index=-1):
		super(LawnMower, self).__init__(p)
		self.is_swimming_pool = is_swimming_pool  # 是否为泳池
		self.row_index = line_index  # 所在行
		self.param_init()
		self.ui_reinit()
		if 0:
			self.setStyleSheet("background-color: red;")  # 测试背景色

	def param_init(self):
		super(LawnMower, self).param_init()
		self.width_ = 80
		self.height_ = 110
		self.setObjectName("lawnMower")
		self.setFixedSize(self.width_, self.height_)
		self.setStyleSheet("#lawnMower{background-color: transparent;}")  # Ensure visibility

		self.move_speed = 10  # 每次移动的像素
		self.timer_interval = 20  # 定时器触发的间隔（毫秒）
		self.target_x = None

		# 创建定时器
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.update_position)

	def ui_reinit(self):
		# 注意: set_movie 需要自定义方法来设置 GIF 动画
		if self.is_swimming_pool is False:
			self.set_movie(":images/others/mower/lawn_mower.gif")
		else:
			self.set_movie(":images/others/mower/PoolCleaner.png")

	def start_moving(self, line_index):
		try:
			self.current_pos = self.pos()
			screen_geometry = QApplication.primaryScreen().geometry()
			self.target_x = screen_geometry.width()
			self.timer.start(self.timer_interval)

		except RuntimeError:
			pass

	def update_position(self):
		"""
		更新除草机的位置
		"""
		current_x = self.pos().x()
		if current_x < self.target_x:
			zombie_set = self.parent().zombie_set if hasattr(self.parent(), 'zombie_set') else []
			zombie_list = list(zombie_set)
			new_x = min(current_x + self.move_speed, self.target_x)
			self.move(new_x, self.pos().y())
			mower_rect = QRect(self.pos(), self.size())
			for zombie in zombie_list:
				zombie_rect = QRect(zombie.pos(), zombie.size())
				if mower_rect.intersects(zombie_rect) and zombie.row_index == self.row_index:
					zombie.set_crushed_state()  # 被碾死 剩下头颅
		else:
			self.timer.stop()
			self.on_animation_finished()

	def on_animation_finished(self):
		"""
		动画结束后的处理，例如隐藏或删除除草机
		"""
		self.deleteLater()  # 或者使用 self.deleteLater() 以删除对象


class AshFire(Element):
	"""
	灰烬火焰
	"""

	def __init__(self, p=None):
		super(AshFire, self).__init__(p)
		self.param_init()

	def param_init(self):
		super(AshFire, self).param_init()

	def set_ash_data(self, ash_pix, relative_pos, size=QSize(99999, 150)):
		self.width_ = size.width()
		self.height_ = size.height()
		self.setFixedSize(QSize(self.width_, self.height_))
		self.set_movie(ash_pix)
		self.move(QPoint(0, relative_pos.y() - int(self.height_ / 2)))


class Snowflake:
	"""
	雪球基础组件
	"""

	def __init__(self, width):
		self.base_width = width
		self.image = QPixmap(":others/down_frost.png")
		self.rect = self.image.rect()
		self.x = random.randint(-250, width)
		self.y = -self.rect.height()  # 初始位置在屏幕顶部之上
		self.speed = random.randint(1, 5)  # 你可以根据需要调整速度范围
		self.dy = self.speed
		self.angle = math.radians(80)  # 15度转换为弧度
		self.dx = self.speed * math.cos(self.angle)

	def move(self, height):
		self.x += self.dx
		self.y += self.dy
		# 如果雪球超出窗口底部，重置位置
		if self.y > height:
			self.y = -self.rect.height()  # 重置到屏幕顶部之上
			self.x = random.randint(0, self.base_width - self.rect.width())

	def draw(self, painter):
		painter.drawPixmap(self.x, self.y, self.image)


class Frost(QFrame):
	"""
	下雪的背景
	"""
	style = """#frost{background-color:rgb(21, 135, 232);}"""

	def __init__(self, p=None):
		super().__init__(p)
		self.initUI()
		self.effect_init()
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.update)
		self.show_snow(self.width())
		self.setStyleSheet(self.style)

	def initUI(self):
		self.setObjectName("frost")
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setAutoFillBackground(True)

	def show_snow(self, base_width):
		# 创建足够多的雪球对象，让它们分布在屏幕顶部
		self.snowflakes = [Snowflake(base_width) for _ in range(40)]  # 你可以根据需要调整雪球的数量
		self.timer.start(10)

	def effect_init(self):
		self.colorize_effect = QGraphicsColorizeEffect(self)
		self.colorize_effect.setColor(Qt.blue)  # 默认颜色为白色（高亮效果）
		self.colorize_effect.setStrength(0.2)  # 默认强度为0
		self.setGraphicsEffect(self.colorize_effect)

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		# 绘制背景色（虽然已在initUI中设置，但可保留以确保）
		for snowflake in self.snowflakes:
			snowflake.move(self.height())  # 更新雪球的位置
			snowflake.draw(painter)  # 绘制雪球

	def resizeEvent(self, event):
		# 当窗口大小改变时，重新初始化雪球的位置
		self.timer.stop()
		self.snowflakes = [Snowflake(event.size().width()) for _ in self.snowflakes]
		self.timer.start(10)
		self.update()

	def show(self) -> None:
		QTimer.singleShot(1200, self.hide)  # 停留后自动隐藏
		super(Frost, self).show()


class ZombieHandElement(Element):
	"""
	开场僵尸大手
	"""

	def __init__(self, p=None):
		super(ZombieHandElement, self).__init__(p)
		self.ui_init()

	def ui_init(self):
		super(ZombieHandElement, self).ui_init()
		pix_map = QPixmap(":images/others/prepare/hand.png")
		self.set_movie(pix_map.scaled(265, 341))
		self.setFixedSize(QSize(285, 341))


class CountdownElement(Element):
	"""
	游戏开始前倒计时
	"""

	def __init__(self, p=None):
		super(CountdownElement, self).__init__(p)
		self.ui_init()

	def ui_init(self):
		super(CountdownElement, self).ui_init()
		self.width_ = 650
		self.height_ = 500
		self.setFixedSize(QSize(self.width_, self.height_))

	def show_count_down(self, count_down_type):
		"""
		展示场景内文字
		"""
		if count_down_type == "game_start":
			show_time = 3000
			gif_movie = ":images/others/prepare.gif"
		elif count_down_type == "big_wave":
			show_time = 2500
			gif_movie = ":images/others/big_wave.gif"

		elif count_down_type == "final_wave":
			show_time = 2500
			gif_movie = ":images/others/FinalWave.gif"
		elif count_down_type == "game_lose":
			show_time = 3000
			gif_movie = ":images/others/fail.png"
		else:
			return
		self.show()
		self.set_movie(gif_movie)
		QTimer.singleShot(show_time, self.hide)


class DaveDialogElement(Element):
	"""
	戴夫对话框
	"""
	style = """#dialog_content{color:black;font-size:12pt;font-weight:600;}#continue_btn{border:none;font-size:11pt;}"""

	def __init__(self, p=None):
		super(DaveDialogElement, self).__init__(p)
		self.ui_init()
		self.setStyleSheet(self.style)
		if 0:
			self.set_dialog_content("set_dialog_content set_dialog_content")

	def ui_init(self):
		self.width_ = 175
		self.height_ = 100
		self.setFixedSize(QSize(self.width_, self.height_))
		pix = QPixmap(":images/others/CrazyDave/ad_L_P1_S.png")
		self.set_movie(pix)
		self.dialog_content = QLabel(self)
		self.dialog_content.setWordWrap(True)
		self.dialog_content.setObjectName("dialog_content")
		self.continue_btn = QPushButton(self)
		self.continue_btn.setCursor(Qt.PointingHandCursor)
		self.continue_btn.setText("continue")
		self.continue_btn.setObjectName("continue_btn")
		self.layout = QVBoxLayout()
		self.layout.setContentsMargins(10, 10, 10, 10)
		self.layout.addWidget(self.dialog_content)
		self.layout.addWidget(self.continue_btn)
		self.layout.setAlignment(self.continue_btn, Qt.AlignCenter | Qt.AlignCenter)
		self.setLayout(self.layout)

	def set_dialog_content(self, content):
		self.dialog_content.setText(content)


class DaveElement(Element):
	"""
	戴夫
	"""

	def __init__(self, p=None):
		super(DaveElement, self).__init__(p)
		self.ui_init()
		if 0:
			self.set_dave_movie(":images/others/CrazyDave/blahblah.gif")

	def ui_init(self):
		self.width_ = 800
		self.height_ = 800
		self.setFixedSize(QSize(self.width_, self.height_))

	def set_dave_movie(self, gif_path):
		self.set_movie(gif_path)
		QTimer.singleShot(2000, self.set_idle)

	def set_idle(self):
		self.set_movie(":images/others/CrazyDave/idle.gif")


class DancerLightItem(Element):
	def __init__(self, p=None):
		super(DancerLightItem, self).__init__(p)
		self.param_init()

	def param_init(self):
		# 初始化定时器
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.show_next_light)
		self.current_index = 0  # 当前展示的切片索引
		# 加载并切分图片
		self.light_cut()

		# 开始定时器，间隔时间设置为500毫秒
		self.timer.start(500)
		self.setAlignment(Qt.AlignHCenter)
		self.setAttribute(Qt.WA_TranslucentBackground)

	def light_cut(self):
		# 加载灯光图像资源
		self.light_pix = ":images/zombies/DancingZombie/spotlight_8.png"
		pixmap = QPixmap(self.light_pix)  # 替换为你的QRC资源路径

		if pixmap.isNull():
			return

		self.slices = []  # 用来存储图像的每个切片

		# 等宽切分图像为5张
		slice_width = pixmap.width() // 5  # 切分成5个等宽部分
		height = pixmap.height()

		# 设定缩放后的大小
		target_width = 80
		target_height = 120

		for i in range(5):  # 切分成5张图
			# 切分并缩放
			slice_pixmap = pixmap.copy(QRect(i * slice_width, 0, slice_width, height))
			scaled_pixmap = slice_pixmap.scaled(target_width, target_height)  # 缩放到80x120
			self.slices.append(scaled_pixmap)

		# 初始显示第一张图
		self.setPixmap(self.slices[0])

	def show_next_light(self):
		# 显示下一个切片
		self.current_index = (self.current_index + 1) % len(self.slices)
		self.setPixmap(self.slices[self.current_index])


if __name__ == '__main__':
	app = QApplication(sys.argv)
	win = DancerLightItem()
	# win = DaveDialogElement()
	# win = DaveElement()
	# win = CountdownElement()
	# win = ZombieHandElement()
	# win = Frost()
	win.show()
	sys.exit(app.exec_())
