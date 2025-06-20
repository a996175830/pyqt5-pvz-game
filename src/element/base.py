from PyQt5.QtCore import Qt, QSize, pyqtSignal, QTimer, QObject, QPoint, QRect
from PyQt5.QtGui import QPixmap, QMovie, QColor, QPainter
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QProgressBar, \
	QGraphicsColorizeEffect

from src.my_util.utils import get_random_line
from src.signal_bus import bus


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


class Element(QLabel):
	"""
	植物、僵尸、其他基础元素
	"""

	def __init__(self, p=None):
		super(Element, self).__init__(p)
		self.param_init()

	def param_init(self):
		self.width_ = 110
		self.height_ = 110

	def ui_init(self):
		self.setContentsMargins(0, 0, 0, 0)
		self.setObjectName("element")
		self.setStyleSheet("#element{background: transparent;}")  # Set transparent background
		self.setMouseTracking(True)  # 可以鼠标穿透
		self.setContentsMargins(5, 5, 5, 5)

	def set_movie(self, gif_qrc):
		try:
			is_gif = True
			if isinstance(gif_qrc, QMovie):
				self.movie = gif_qrc  # 使用 QRC 文件中的 GIF

			elif isinstance(gif_qrc, QPixmap):
				self.setPixmap(gif_qrc)
				is_gif = False
			elif ".gif" in gif_qrc:
				self.movie = QMovie(gif_qrc)  # 使用 QRC 文件中的 GIF
			else:
				self.setPixmap(QPixmap(gif_qrc))
				is_gif = False
			if is_gif is True:
				self.movie.frameChanged.connect(self.update_frame)  # 连接到帧更新槽
				self.setMovie(self.movie)
				self.movie.start()
		except RuntimeError:
			pass

	def update_frame(self, ):
		"""
		更新当前帧，缩放图像
		:param frame_number: 当前帧编号
		"""
		try:
			frame = self.movie.currentPixmap()
			scaled_frame = frame.scaled(self.width_, self.height_, Qt.KeepAspectRatio, Qt.SmoothTransformation)
			self.setPixmap(scaled_frame)
		except RuntimeError:
			pass

	def set_custom_size(self, width, height=100):
		"""
		自定义尺寸
		:return:
		"""
		self.width_ = width
		self.height_ = height
		self.setFixedSize(QSize(self.width_, self.height_))


class PZBase(Element):
	"""
	植物和僵尸的基类
	"""

	def __init__(self, parent=None):
		super().__init__(parent)
		self.param_init()
		self.ui_reinit()
		self.initialize_effects()

	def param_init(self):
		self.width_ = 100
		self.height_ = 100
		self.hp = 0
		self.hp_all = 0
		self.is_slow_down = False
		self.is_hypno = False  # 是否被催眠
		self.is_reversed = False  # 是否为反向
		self.shadow_is_on = False  # 是否展示阴影
		self.base_move_step = 0.0
		_data_item = dict()  # 私有属性存储数据项

	def ui_reinit(self):
		self.setFixedSize(QSize(self.width_, self.height_))
		self.setMouseTracking(True)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.layout = QVBoxLayout()
		self.layout.setSpacing(0)
		self.layout.setContentsMargins(0, 0, 0, 0)
		self.setContentsMargins(0, 0, 0, 0)
		self.hp_line = HPLine(self)
		self.layout.addWidget(self.hp_line)
		self.layout.setAlignment(self.hp_line, Qt.AlignTop | Qt.AlignHCenter | Qt.AlignCenter)
		self.setLayout(self.layout)

	def set_hp_value(self, value):
		"""
		设置体力条值
		:param value:
		:return:
		"""
		try:
			self.hp_line.hp_value.setText(f"HP:{self.hp}")
			self.hp_line.setValue(int(value / self.hp_all * 100))
		except:
			pass

	def die(self):
		try:
			self.deleteLater()
		except RuntimeError:
			pass

	def take_damage(self, damage, attacker):
		if self.is_hypno: return
		self.change_effect("hit", 500)

	def initialize_effects(self):
		"""
		初始化效果，包括高亮和减速效果
		"""
		self.colorize_effect = QGraphicsColorizeEffect(self)
		self.setGraphicsEffect(self.colorize_effect)
		self.colorize_effect.setColor(Qt.white)  # 默认颜色为白色（高亮效果）
		self.colorize_effect.setStrength(0)  # 默认强度为0

	def change_effect(self, effect, duration=0):
		"""
		更改效果
		"""

		def remove_effect():
			"""
			移除效果
			"""
			try:
				self.colorize_effect.setStrength(0)
			except RuntimeError:
				pass

		if self.is_hypno is True: return  # 被魅惑 不改变
		if effect == "hit":
			if self.is_slow_down is True: return  # 被减速 不改变
			effect_color = Qt.white
			strength = 0.2
			QTimer.singleShot(duration * 1000, remove_effect)
		elif effect == "slow_down":
			effect_color = Qt.blue  # 设置颜色为蓝色
			strength = 0.3
			self.is_slow_down = True
			QTimer.singleShot(duration * 1000, self.stop_slowdown_effect)
		elif effect == "hypno":
			effect_color = QColor(198, 54, 120)
			self.is_hypno = True
			strength = 0.6
		else:
			return
		self.colorize_effect.setColor(effect_color)  # 设置颜色为白色
		self.colorize_effect.setStrength(strength)  # 应用高亮效果

	def stop_slowdown_effect(self):
		"""
		应用减速效果
		"""
		self.colorize_effect.setStrength(0)  # 取消效果
		self.is_slow_down = False
		self.speed = self.base_move_step

	def paintEvent(self, event):
		# 调用父类的paintEvent方法绘制组件本身
		super(Element, self).paintEvent(event)
		if self.shadow_is_on:
			# 开始自定义绘制
			painter = QPainter(self)
			# 设置阴影颜色和透明度
			shadow_color = QColor(50, 50, 50, 180)  # 半透明黑色
			# 设置画刷颜色
			painter.setBrush(shadow_color)
			painter.setPen(Qt.NoPen)  # 无边框
			# 获取组件的宽度和高度
			width = self.width()
			height = self.height()
			# 阴影的宽度为组件宽度的0.8，位置在组件底部，离底部一定的距离
			shadow_width = width * 0.3
			shadow_height = height * 0.13  # 阴影高度相对较小，扁平化的效果
			# 计算阴影位置：居中显示，靠近底部
			shadow_rect = QRect(
				(width - shadow_width) / 1.83,  # 阴影居中
				height - shadow_height * 2,  # 阴影位置稍微离底部有点距离
				shadow_width,
				shadow_height
			)
			# 绘制椭圆形阴影
			painter.drawEllipse(shadow_rect)


class Plant(PZBase):
	"""
	植物基类
	"""
	plant_died = pyqtSignal(QObject)
	plant_hp_changed = pyqtSignal(int)

	def __init__(self, p=None):
		super(Plant, self).__init__(p)
		self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		self.slot_init()
		self.raise_()
		if 0:
			self.setStyleSheet("""background-color:blue""")

	def ui_init(self):
		super(Plant, self).ui_init()

	def take_damage(self, damage, attacker):
		super(Plant, self).take_damage(damage, attacker)
		self.hp -= damage
		self.plant_hp_changed.emit(self.hp)
		if self.hp <= 0:
			self.die()

	def die(self):
		self.plant_died.emit(self)
		super(Plant, self).die()

	def set_property(self, _data_item):
		self._data_item = _data_item
		self.plant_type = 0  # 植物类型  0 一般植物 1中立占位植物
		self.plant_id = _data_item['id']
		self.plant_name = _data_item['name']
		self.cost = _data_item['cost']
		self.put_pix = _data_item['put_pix']
		self.cursor_pix = _data_item['cursor_pix']
		self.damage = _data_item.get('damage', "")
		self.sleep_pix = _data_item.get('sleep_pix', "")  # 白天睡觉贴图
		self.for_upgrade = _data_item.get('for_upgrade', False)  # 用作给其他植物提升
		self.for_upgrade_id = _data_item.get('for_upgrade_id', 0)  # 提升的目标植物id
		self.hp = _data_item['hp']
		self.hp_all = _data_item['hp']
		self.cooling = _data_item['cooling']
		self.attack_gap = _data_item.get('attack_gap', 0.0)
		self.range_effect = _data_item.get("range_effect", tuple())  # 影响范围
		self.moderate = _data_item.get('moderate', 0.0)
		self.moderate_duration = _data_item.get('moderate_duration', 0.0)
		self.set_movie(self.put_pix)
		self.set_hp_value(self.hp)
		self.row_index = -1  # 植物所在行
		self.col_index = -1  # 植物所在列
		self.item_type = 1  # 元素类型1植物 2僵尸 3子弹
		self.is_shroom = False  # 是否为蘑菇
		self.plant_level = 1  # 0地底水底、1默认地面上、3周围

	def slot_init(self):
		self.plant_hp_changed.connect(lambda value: self.set_hp_value(value))


class Zombie(PZBase):
	"""
	僵尸基类
	"""
	zombie_died = pyqtSignal(QObject)
	zombie_hp_changed = pyqtSignal(int)
	sound_effect_changed = pyqtSignal(str)
	zombie_coord_changed = pyqtSignal(int, int)  # 僵尸格数位置发生了变化

	def __init__(self, p=None):
		super(Zombie, self).__init__(p)
		self.param_init()
		self.timer_init()
		self.slot_init()
		self.ice_label_init()
		if 0:
			self.setStyleSheet("""background-color:red""")

	def param_init(self):
		super(Zombie, self).param_init()
		self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
		self.setAttribute(Qt.WA_TransparentForMouseEvents)
		self.head_pix = ":images/zombies/Zombie/ZombieHead.gif"  # 头部
		self.damage_pix = ":images/zombies/Zombie/ZombieLostHead.gif"  # 损伤点 定义为装备掉落
		self.dying_pix = ":images/zombies/Zombie/ZombieDie.gif"  # 死亡pix 定义为死亡
		self.normal_gif = ""  # 初始样式
		self.no_icon_gif = ""  # 无护具
		self.attack_damage_pix = ":images/zombies/Zombie/ZombieAttack.gif"  # 损伤点 攻击图像
		self.attack_dying_pix = ":images/zombies/Zombie/ZombieLostHeadAttack.gif"  # 死亡点 攻击图像
		self.attack_pix = ":images/zombies/Zombie/ZombieAttack.gif"  # 一般攻击样式
		self.ash_pix = ":images/zombies/Zombie/BoomDie.gif"  # 灰烬
		self.sound_effect = "hit"  # 被打中后音效
		self.dying_status = False  # 是否濒死状态
		self.is_attacking = False  # 是否正在攻击
		self.is_car_zombie = False  # 是否正在攻击
		self.head_flew = False  # 头部是否飞出
		self.pause_status = False  # 是否暂停
		self.is_hypno = False  # 是否被魅惑
		self.moderate = 0.0  # 减速百分比
		self.damage = 100  # 每秒伤害
		self.moderate_duration = 0  # 减速持续时间
		self.attack_frequency = 1.0  # 攻击频率（攻速）
		self.row_index = -1  # 僵尸所在行号
		self.col_index = -1  # 僵尸所在列
		self.item_type = 2  # 元素类型1植物 2僵尸 3子弹
		self.zombie_level = 1  # 0地底水底、1默认地面上、2天空
		self.current_gif = ""  # 当前状态的gif 可能是walk 也可能是attack

	def timer_init(self):
		self.attack_timer = QTimer(self)
		self.pause_timer = QTimer(self)  # 暂停状态定时器
		self.dying_timer = QTimer(self)  # 濒死状态定时器
		self.dying_timer.setInterval(1000)
		self.dying_timer.timeout.connect(self.update_dying_status)
		self.pause_timer.timeout.connect(self.set_freeze_status_stop)

	def slot_init(self):
		self.zombie_hp_changed.connect(lambda value: self.change_zombie_gif(value))
		self.zombie_hp_changed.connect(lambda value: self.set_hp_value(value))

	def set_property(self, data_item):
		self.zombie_item = data_item
		self.zombie_id = self.zombie_item.get("id", "")
		self.armor_health = self.zombie_item.get("armor_health", 0)
		self.base_health = self.zombie_item.get("base_health", 0)
		self.zombie_name = self.zombie_item.get("name", "")
		self.normal_gif = self.zombie_item.get("put_pix", "")
		self.attack_pix = self.zombie_item.get("attack_pix", self.attack_pix)
		self.no_icon_gif = self.zombie_item.get('no_icon_gif', self.no_icon_gif)
		self.ash_pix = self.zombie_item.get("ash_pix", self.ash_pix)
		self.speed = self.zombie_item.get("speed", 1.0)  # 默认移动速度为1.0
		self.base_move_step = self.zombie_item.get("speed", 1.0)  # 默认速度为1.0
		self.attack_frequency = self.zombie_item.get('attack_frequency', 1.0)
		self.head_pix = self.zombie_item.get('head_pix', self.head_pix)
		self.damage_pix = self.zombie_item.get('damage_pix', self.damage_pix)
		self.dying_pix = self.zombie_item.get('dying_pix', self.dying_pix)
		self.sound_effect = self.zombie_item.get('sound_effect', self.sound_effect)
		self.is_swimming_zombie = self.zombie_item.get('is_swimming_zombie', False)
		self.attack_damage_pix = self.zombie_item.get('attack_damage_pix', self.attack_damage_pix)
		self.attack_dying_pix = self.zombie_item.get('attack_dying_pix', self.attack_dying_pix)
		hp_all = self.armor_health + self.base_health  # 体力值=防具+基础
		self.hp = hp_all
		self.hp_all = hp_all
		self.damage_point = self.base_health  # 计算损伤点
		self.death_point = 89  # 计算死亡点
		self.set_movie(self.normal_gif)
		self.set_hp_value(self.hp)

	def ice_label_init(self):
		self.ice_label = Element(self)
		self.ice_label.width_ = 95
		self.ice_label.height_ = 32
		self.ice_label.setFixedSize(QSize(self.ice_label.width_, self.ice_label.height_))
		self.ice_label.set_movie(":images/others/ice.gif")
		self.ice_label.move(int(self.width_ - self.ice_label.width_), int(self.height_ - self.ice_label.height_))
		self.ice_label.hide()

	def set_ash_state(self, boom_damage, real_ash=True):
		"""
		灰烬状态
		:return:
		"""

		def set_ash():
			try:
				self.hp -= boom_damage
				self.zombie_hp_changed.emit(self.hp)
			except RuntimeError:
				pass

		try:
			if real_ash is True:
				self.set_movie(self.ash_pix)
				delay_time = 1700  # 灰烬状态持续时间
			else:
				delay_time = 400  # 延迟吃掉僵尸
			QTimer.singleShot(delay_time, set_ash)  # 停留一秒后自动隐藏
		except:
			pass

	def set_crushed_state(self):
		"""
		被灰烬状态
		:return:
		"""

		def set_crushed():
			try:
				self.hp -= self.hp
				self.zombie_hp_changed.emit(self.hp)
			except RuntimeError:
				pass

		try:
			self.set_movie(self.head_pix)
			delay_time = 1200  # 灰烬状态持续时间
			QTimer.singleShot(delay_time, set_crushed)  # 停留后自动死亡
		except:
			pass

	def take_damage(self, damage, attacker):
		"""
		hp减少后 根据hp切换gif贴图
		:param hp:
		:return:
		"""
		super(Zombie, self).take_damage(damage, attacker)
		self.hp -= damage
		self.zombie_hp_changed.emit(self.hp)
		if self.is_slow_down is False or self.pause_status is False:
			self.sound_effect_changed.emit(self.sound_effect)
		if self.hp <= 40 and self.head_flew is False:
			self.show_head_drop()
		attacker_type = attacker.item_type if hasattr(attacker, "item_type") else -1
		if attacker_type == 2:  # 如果僵尸被僵尸杀死了
			self.sound_effect_changed.emit("zombie_eating")

	def show_head_drop(self):
		"""
		僵尸头部掉落
		:return:
		"""
		bus.effect_changed.emit("shoop")
		self.head_drop_label = Element(self)
		self.head_drop_label.setFixedHeight(self.height())
		self.head_drop_label.setFixedWidth(180)
		self.head_drop_label.set_movie(self.head_pix)
		self.head_drop_label.show()
		self.head_drop_label.raise_()
		self.head_drop_label.move(QPoint(int(self.width() / 3), 0))
		if isinstance(self.head_drop_label.movie, QMovie):
			self.head_drop_label.movie.finished.connect(self.head_drop_label.hide)
		self.head_flew = True

	def set_moderate(self, moderate, duration):
		"""
		僵尸被减速
		:param moderate:
		:return:
		"""
		# 降低移动速度
		if float(moderate) == 0.0 or self.zombie_id == 23: return  # 无需减速
		self.speed = self.base_move_step - moderate
		self.change_effect("slow_down", duration=duration * 1000)

	#
	# # 降低攻击速度
	# self.attack_frequency = 1.0
	# self.attack_timer_interval = (1 / self.attack_frequency) * 1000
	# print("attack_timer_interval==", self.attack_timer_interval)
	# if self.attack_timer.isActive():
	# 	self.attack_timer.start(self.attack_timer_interval)

	def die(self):
		# 执行僵尸死亡的逻辑
		try:
			self.hp = 0
			self.zombie_died.emit(self)
			super(Zombie, self).die()
		except RuntimeError:
			pass

	def lose_iron_weapons(self):
		"""
		失去铁质武器
		"""
		try:
			if self.hp - self.base_health > 0:  # 间接判断是否有防具
				self.take_damage(self.hp - self.base_health, Plant())  # 造成一个当前体力-基础体力的差值
				self.normal_gif = self.no_icon_gif
				self.set_movie(self.normal_gif)
		except RuntimeError:
			pass

	def change_zombie_gif(self, value):
		"""
		更改僵尸贴图
		:param value:
		:return:
		"""
		if value <= 0:  # 僵尸死亡
			self.die()
			return
		else:
			if self.is_attacking is True:
				if value <= self.death_point:
					new_gif = self.attack_dying_pix
				elif value <= self.damage_point:
					new_gif = self.attack_damage_pix
				else:
					new_gif = self.attack_pix
			else:
				if value <= self.death_point:
					new_gif = self.dying_pix
				elif value < self.damage_point:
					new_gif = self.damage_pix
				else:
					new_gif = self.normal_gif
		if self.current_gif != new_gif:  # 只有变化的时候更新
			self.current_gif = new_gif
			self.set_movie(self.current_gif)
		if value <= self.death_point:
			self.set_dying_status()

	def set_dying_status(self):
		"""
		设置濒死状态
		"""
		if self.dying_timer is True: return
		self.dying_timer.start()
		self.dying_status = True

	def update_dying_status(self):
		"""
		更新濒死流血状态
		"""
		if self.hp >= 0:
			self.hp -= 60

	def set_freeze_status_stop(self):
		"""
		设置暂停状态
		:return:
		"""
		self.pause_timer.stop()
		self.pause_status = False
		if self.ice_label.isVisible():
			self.ice_label.hide()
		self.movie.setPaused(False)

	def set_freeze_status(self, pause_duration):
		"""
		设置暂停状态样式
		:return:
		"""
		self.set_pause_status(pause_duration)
		self.ice_label.show()
		self.ice_label.raise_()

	def set_pause_status(self, pause_duration):
		"""
		设置暂停状态
		"""
		self.pause_timer.setInterval(pause_duration * 1000)
		if not self.pause_timer.isActive():
			self.pause_timer.start()
		self.pause_status = True
		self.movie.setPaused(True)

	def set_unpause_status(self):
		"""
		解除暂停状态
		"""
		if self.pause_timer.isActive():
			self.pause_timer.stop()
		self.pause_status = False
		self.movie.setPaused(False)

	def update_frame(self, ):
		"""
		更新当前帧，缩放图像
		:param frame_number: 当前帧编号
		"""
		try:
			if self.is_hypno is True or self.is_reversed is True:
				current_frame = self.movie.currentPixmap().toImage()
				scaled_frame = current_frame.scaled(self.width_, self.height_, Qt.KeepAspectRatio,
													Qt.SmoothTransformation)
				mirrored_frame = scaled_frame.mirrored(True, False)
				self.setPixmap(QPixmap.fromImage(mirrored_frame))
			else:
				frame = self.movie.currentPixmap()
				scaled_frame = frame.scaled(self.width_, self.height_, Qt.KeepAspectRatio, Qt.SmoothTransformation)
				self.setPixmap(scaled_frame)
		except RuntimeError:
			pass

	def change_random_line(self):
		"""
		更改线路
		随机一条相邻的线路
		"""
		new_line = get_random_line(self.row_index, self.parent().is_swimming_map)
		self.row_index = new_line


class Bullet(Element):
	"""
	子弹类
	"""
	bullet_hit_signal = pyqtSignal(str)  # 子弹打中了

	def __init__(self, parent=None):
		super(Bullet, self).__init__(parent)
		self.setParent(parent)
		self.param_init()
		self.timer_init()

	def param_init(self):
		super(Bullet, self).param_init()
		self.speed = 10  # 默认速度
		self.width_ = 65  # 子弹方格大小
		self.height_ = 65  # 子弹方格大小

	def timer_init(self):
		self.timer = QTimer(self)
		self.timer.start(20)  # 每20毫秒更新位置
		# 添加一个定时器，5秒后自动销毁子弹
		self.self_destroy_timer = QTimer(self)
		self.self_destroy_timer.timeout.connect(self.auto_destroy_bullet)
		self.self_destroy_timer.setSingleShot(True)  # 定时器只触发一次
		self.self_destroy_timer.start(5000)  # 5秒后自动回收

	def set_property(self, _data_item):
		self.bullet_id = _data_item['id']
		self.plant_name = _data_item['name']
		self.damage = _data_item['damage']
		self.bullet = _data_item['bullet']
		self.attack_gap = _data_item['attack_gap']
		self.moderate = _data_item['moderate']
		self.bullet_hit = _data_item['bullet_hit']
		self.moderate_duration = _data_item['moderate_duration']
		self.effect_key = _data_item['effect_key']
		self.penetrable = _data_item['penetrable']  # 是否能穿透
		self.effect_damage = _data_item.get("effect_damage", 0)  # 溅射伤害
		self.effect_range = _data_item.get("effect_range", tuple())  # 影响范围
		self._data_item = _data_item
		self.col_index = -1
		self.item_type = 3  # 元素类型3子弹
		self.set_movie(self.bullet)

	def move_bullet(self):
		pass

	def set_hit_state_image(self):
		"""
		设置子弹打中状态图像
		:return:
		"""
		self.bullet_hit_signal.emit(self.effect_key)
		if self.penetrable is False:
			self.set_movie(self.bullet_hit)
			QTimer.singleShot(150, self.self_destroy)  # 动画播放完成后执行清理操作
		else:
			self.move_bullet()  # 继续移动

	def self_destroy(self):
		"""
		销毁自己 内存回收
		:return:
		"""
		self.hide()
		self.timer.stop()
		try:
			self.deleteLater()
		except RuntimeError:
			pass

	def auto_destroy_bullet(self):
		"""
		销毁子弹，停止计时器并从场景中移除
		"""
		self.timer.stop()  # 停止移动子弹的计时器
		self.self_destroy_timer.stop()  # 停止5秒销毁定时器
		try:
			self.deleteLater()  # 从场景中移除子弹
		except RuntimeError:
			pass
