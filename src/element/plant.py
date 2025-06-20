import random
import sys
import traceback

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication

from src.my_util.utils import check_coordinate_in_range
from .base import Plant, Element
from src.config import normal_conf

from PyQt5.QtCore import pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QPoint, pyqtProperty, QRect, QObject
from PyQt5.QtCore import Qt, QSize
from src.resources import resource_rc


class ShooterBase(Plant):
	"""
	射手基类
	:param Plant:
	:return:
	"""
	new_bullet_created = pyqtSignal(QPoint)

	def __init__(self, parent=None):
		super(ShooterBase, self).__init__(parent)

	def timer_init(self):
		self.attack_timer = QTimer(self)
		self.attack_timer.setInterval(int(self.attack_gap * 1000))  # 每 attack_gap 秒攻击一次
		self.attack_timer.timeout.connect(self.attack)

	def attack_timer_start(self):
		"""
		启动攻击定时器
		"""
		self.attack_timer.start()

	def attack(self):
		"""
		发射子弹攻击敌人
		"""
		self.new_bullet_created.emit(QPoint(1, 0))

	def set_pause_status(self):
		"""
		设置暂停状态
		"""
		if self.attack_timer.isActive():
			self.attack_timer.stop()
		self.pause_status = False
		self.movie.setPaused(True)

	def set_unpause_status(self):
		"""
		解除暂停状态
		"""
		if not self.attack_timer.isActive():
			self.attack_timer.start()
		self.pause_status = True
		self.movie.setPaused(False)


class AutoSunflower(Element):
	"""
	向日葵生成的阳光类
	"""
	auto_sun_flower_clicked = pyqtSignal()
	auto_sun_flower_hidden = pyqtSignal()

	def __init__(self, parent=None, size=QSize(85, 85)):
		super(AutoSunflower, self).__init__(parent)
		self.width_ = size.width()
		self.height_ = size.height()
		self.setCursor(Qt.PointingHandCursor)
		self.ui_re_init()
		self.setup_timer()

	def ui_re_init(self):
		self.setObjectName("autoSunflower")
		self.setFixedSize(QSize(self.width_, self.height_))
		self.setStyleSheet("#autoSunflower{background-color: transparent;}")
		self.set_movie(":images/others/roll_sf.gif")  # 设置阳光 GIF
		self.mousePressEvent = self.on_click

	def setup_timer(self):
		self.timer = QTimer(self)
		self.timer.setInterval(3000)  # 设置定时器为2秒
		self.timer.timeout.connect(self.on_timeout)

	def show(self) -> None:
		super(AutoSunflower, self).show()
		self.reset_timer()  # 重置定时器

	def on_click(self, event):
		if event.button() == Qt.LeftButton:
			self.hide()
			self.auto_sun_flower_clicked.emit()
			self.parent().resume_sunshine_timer()
			self.timer.stop()  # 停止定时器

	def reset_timer(self):
		self.timer.start()  # 重置定时器

	def on_timeout(self):
		self.hide()  # 隐藏阳光
		self.auto_sun_flower_hidden.emit()  # 发射隐藏信号

	def auto_hide(self):
		QTimer.singleShot(3000, self.hide)  # 停留一秒后自动隐藏

	@pyqtProperty(int)
	def height_animated(self):
		return self.height()

	@height_animated.setter
	def height_animated(self, value):
		self.setGeometry(self.geometry().x(), self.geometry().y(), self.width(), value)


class SunFlowerBase(Plant):
	"""
	向日葵类
	"""
	new_sunshine_produced = pyqtSignal(int)

	def __init__(self, parent=None):
		super(SunFlowerBase, self).__init__(parent)

	def param_re_init(self):
		self.timer_init()
		self.has_sunshine = False  # 当前是否有阳光
		self.auto_sunshine_size = QSize(85, 85)

	def timer_init(self):
		self.sunshine_timer = QTimer(self)
		self.sunshine_timer.timeout.connect(self.create_sunshine)
		self.set_random_interval()
		self.sunshine_timer.start()  # 启动定时器

	def set_random_interval(self):
		# 设定一个基于 self.sun_gap 的随机时间间隔（秒）
		min_interval = max(0, self.sun_gap - 2)  # 确保最小间隔时间不为负数
		max_interval = self.sun_gap + 2
		random_interval = random.uniform(min_interval, max_interval)  # 生成随机时间间隔
		self.sunshine_timer.setInterval(int(random_interval * 1000))  # 转换为毫秒

	def set_property(self, data_item):
		super(SunFlowerBase, self).set_property(data_item)
		# 向日葵特有属性
		self.sun_production = data_item.get('sun_production', 0)
		self.sun_gap = data_item['gap']

	def create_sunshine(self):
		# 检查是否有未处理的阳光
		if self.has_sunshine:
			return

		self.set_random_interval()  # 重新设置随机时间间隔
		self.sunshine = AutoSunflower(self, self.auto_sunshine_size)
		self.sunshine.auto_sun_flower_clicked.connect(lambda: self.new_sunshine_produced.emit(self.sun_production))
		self.sunshine.auto_sun_flower_hidden.connect(self.on_sunshine_hidden)  # 连接隐藏信号
		self.sunshine.show()

		sunshine_width = self.sunshine.width()
		sunshine_height = self.sunshine.height()
		self.sunshine.move(int(self.width() / 2 - sunshine_width / 2), int(self.height() / 2 - sunshine_height / 2))

		self.sunshine_timer.stop()  # 停止定时器，等待阳光被处理
		self.has_sunshine = True

	def on_sunshine_hidden(self):
		self.resume_sunshine_timer()

	def resume_sunshine_timer(self):
		# 重新启动定时器
		if not self.sunshine_timer.isActive():
			self.sunshine_timer.start()
		self.has_sunshine = False


class SunFlower(SunFlowerBase):
	"""
	向日葵类
	"""

	def __init__(self, parent=None):
		super(SunFlower, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["sun_flower"])
		self.param_re_init()


class TwinSunFlower(SunFlowerBase):
	"""
	双子向日葵类
	"""

	def __init__(self, parent=None):
		super(TwinSunFlower, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["twin_sun_flower"])
		self.param_re_init()
		self.auto_sunshine_size = QSize(120, 120)


class SunMushroom(SunFlowerBase):
	"""
	阳光菇
	"""
	grow_finished = pyqtSignal()  # 长大了 信号

	def __init__(self, parent=None):
		super(SunMushroom, self).__init__(parent)
		data_item = normal_conf.plant_param_dict["sun_mushroom"]
		self.set_property(data_item)
		self.param_re_init()
		self.pro_timer_init()

	def param_re_init(self):
		self.auto_sunshine_size = QSize(45, 45)
		self.sun_production_grow = self._data_item.get('sun_production_grow', "")
		self.grow_gap = self._data_item.get('grow_gap', 0)
		self.pro_pix = self._data_item.get('pro_pix', "")
		self.is_shroom = True  # 是否为蘑菇

	def pro_timer_init(self):
		self.pro_timer = QTimer(self)
		self.pro_timer.setInterval(self.grow_gap * 1000)
		self.pro_timer.timeout.connect(self.do_grow)
		self.pro_timer.start()

	def do_grow(self):
		"""
		长大
		:return:
		"""
		self.sun_production = self.sun_production_grow
		self.auto_sunshine_size = QSize(85, 85)
		self.set_movie(self.pro_pix)
		self.pro_timer.stop()
		self.grow_finished.emit()


class PeaShooter(ShooterBase):
	"""
	豌豆射手
	"""

	def __init__(self, parent=None):
		super(PeaShooter, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["pea"])
		self.timer_init()
		self.attack_timer_start()


class StarFruit(ShooterBase):
	"""
	杨桃
	"""

	def __init__(self, parent=None):
		super(StarFruit, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["star_fruit"])
		self.timer_init()
		self.attack_timer_start()

	def attack(self):
		"""
		发射三粒豌豆攻击敌人
		正面一粒 背面两粒
		"""
		self.new_bullet_created.emit(QPoint(-1, 0))
		self.new_bullet_created.emit(QPoint(0, -1))
		self.new_bullet_created.emit(QPoint(0, 1))
		self.new_bullet_created.emit(QPoint(1, -1))
		self.new_bullet_created.emit(QPoint(1, 1))


class ThreeShooter(ShooterBase):
	"""
	三线豌豆射手
	"""

	def __init__(self, parent=None):
		super(ThreeShooter, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["three_pea"])
		self.timer_init()
		self.attack_timer_start()


class NutBase(Plant):
	"""
	坚果类
	"""

	def __init__(self, parent=None):
		super(NutBase, self).__init__(parent)

	def take_damage(self, damage, attacker):
		super(NutBase, self).take_damage(damage, attacker)
		self.update_health()

	def set_property(self, _data_item):
		"""
		设置特有的属性
		"""
		super(NutBase, self).set_property(_data_item)
		self.put_pix2 = _data_item.get('put_pix2', "")
		self.put_pix3 = _data_item.get('put_pix3', "")

	def update_health(self):
		"""
		更新坚果墙的耐久度
		"""
		if self.hp <= 0:
			self.destroy()
		else:
			self.update_image()

	def update_image(self):
		"""根据当前血量更新坚果墙的显示图片"""
		health_percentage = self.hp / self.hp_all  # 总血量为4000
		if health_percentage <= 0.2:
			self.set_movie(self.put_pix3)  # 低于20%时的图片
		elif health_percentage <= 0.6:
			self.set_movie(self.put_pix2)  # 低于60%时的图片
		else:
			self.set_movie(self.put_pix)  # 恢复到正常状态的图片


class WallNut(NutBase):
	"""
	坚果
	"""

	def __init__(self, parent=None):
		super(WallNut, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["nut"])
		self.set_movie(self.put_pix)  # 设置初始动画


class MacadamiaNut(NutBase):
	"""
	高坚果
	"""

	def __init__(self, parent=None):
		super(MacadamiaNut, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["macadamia_nut"])
		self.set_movie(self.put_pix)  # 设置初始动画


class IcePea(ShooterBase):
	"""
	寒冰射手类
	"""

	def __init__(self, parent=None):
		super(IcePea, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["ice_pea"])
		self.timer_init()
		self.attack_timer_start()


class RepeaterPeaShooter(ShooterBase):
	"""
	双发豌豆射手
	"""

	def __init__(self, parent=None):
		super(RepeaterPeaShooter, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["repeater_pea"])
		self.timer_init()
		self.timer_re_init()
		self.attack_timer_start()

	def timer_re_init(self):
		self.attack_timer.disconnect()
		self.attack_timer.setInterval(self.attack_gap * 1000)  # 每 attack_gap 秒攻击一次
		self.attack_timer.timeout.connect(self.attack)

	def attack(self):
		"""
		发射两颗豌豆攻击敌人
		"""

		# 创建子弹对象
		def create_second_bullet():
			try:
				self.new_bullet_created.emit(QPoint(1, 0))
			except RuntimeError:
				pass

		try:
			self.new_bullet_created.emit(QPoint(1, 0))
			QTimer.singleShot(125, create_second_bullet)  # 停留一秒后自动隐藏
		except RuntimeError:
			pass


class LittleSproutMushroomShooter(ShooterBase):
	"""
	小喷菇
	"""

	def __init__(self, parent=None):
		super(LittleSproutMushroomShooter, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["little_sprout_mushroom"])
		self.set_custom_size(70, 70)
		self.timer_init()
		self.can_attack_flag = False
		self.is_shroom = True  # 是否为蘑菇
		self.attack_timer_start()

	def get_aim_zombie(self, zombie_set):
		"""
		获取目标僵尸
		"""
		items = list(zombie_set)
		aim_zombie_item = None
		aim_zombie_col = float('inf')  # 使用无穷大作为初始比较值
		for each_zombie in items:
			if each_zombie.row_index == self.row_index and each_zombie.col_index < aim_zombie_col:
				aim_zombie_item = each_zombie
				aim_zombie_col = each_zombie.col_index
		return aim_zombie_item

	def check_shroom_attack(self, zombie_set):
		"""
		检测距离是否够用
		"""
		aim_zombie_item = self.get_aim_zombie(zombie_set)
		if aim_zombie_item is None: return
		x1, y1 = self.row_index, self.col_index
		x2, y2 = aim_zombie_item.row_index, aim_zombie_item.col_index
		if x1 == x2 and y1 <= y2 <= y1 + 3:
			flag = True
		else:
			flag = False
		self.change_mushroom_status(flag)

	def change_mushroom_status(self, status):
		"""
		更改小喷菇状态
		:param fear_status:
		:return:
		"""
		try:
			if status is True:
				if not self.attack_timer.isActive():
					self.attack_timer.start()
			else:
				if self.attack_timer.isActive():
					self.attack_timer.stop()
		except:
			traceback.print_exc()


class PitcherBase(ShooterBase):
	"""
	投手植物基类
	"""

	def __init__(self, parent=None):
		super(PitcherBase, self).__init__(parent)


class TrackingPlantBase(ShooterBase):
	"""
	追踪子弹植物基类
	"""

	def __init__(self, parent=None):
		super(TrackingPlantBase, self).__init__(parent)


class CatTail(ShooterBase):
	"""
	香蒲
	"""

	def __init__(self, parent=None):
		super(CatTail, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["cat_tail"])
		self.timer_init()
		self.attack_timer_start()

	def attack(self):
		"""
		发射两枚香蒲针刺
		"""

		def create_other_thorn():
			try:
				self.new_bullet_created.emit(QPoint(1, 0))
			except RuntimeError:
				pass

		self.new_bullet_created.emit(QPoint(1, 0))
		QTimer.singleShot(200, create_other_thorn)


class Watermelon(PitcherBase):
	"""
	西瓜投手
	"""

	def __init__(self, parent=None):
		super(Watermelon, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["watermelon"])
		self.timer_init()
		self.set_custom_size(115, 115)
		self.attack_timer_start()


class WinterMelon(PitcherBase):
	"""
	冰西瓜投手
	"""

	def __init__(self, parent=None):
		super(WinterMelon, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["winter_melon"])
		self.timer_init()
		self.set_custom_size(115, 115)
		self.attack_timer_start()


class CobCannon(PitcherBase):
	"""
	玉米投手
	"""
	cob_bullet_created = pyqtSignal(QPoint, int)

	def __init__(self, parent=None):
		super(CobCannon, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["cron_pult"])
		self.timer_init()
		self.set_custom_size(115, 115)
		self.attack_timer_start()

	def attack(self):
		"""
		创建子弹对象，并更换贴图
		"""
		if random.random() < 0.25:
			bullet_id = 8  # 投射黄油
			cob_pix = ":images/plants/Cornpult/shooting1.gif"
		else:  # 发射玉米粒
			bullet_id = 7
			cob_pix = ":images/plants/Cornpult/shooting2.gif"

		# self.set_movie(cob_pix)  # 切换到攻击动画
		self.cob_bullet_created.emit(QPoint(1, 0), bullet_id)  # 发射子弹

		# 攻击完成后，延时恢复到待机动画
		QTimer.singleShot(1500, self.reset_to_idle)

	def reset_to_idle(self):
		"""
		恢复到待机状态
		"""
		self.set_movie(":images/plants/Cornpult/full_idle.gif")
		self.can_attacking = True  # 恢复可以攻击状态


class Cabbage(PitcherBase):
	"""
	西瓜投手
	"""

	def __init__(self, parent=None):
		super(Cabbage, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["cabbage"])
		self.timer_init()
		self.set_custom_size(115, 115)
		self.attack_timer_start()


class FearMushroom(ShooterBase):
	"""
	胆小菇
	"""

	def __init__(self, parent=None):
		super(FearMushroom, self).__init__(parent)
		self.is_fear = False  # 默认不害怕
		self.set_property(normal_conf.plant_param_dict["fear_mushroom"])
		self.is_shroom = True  # 是否为蘑菇
		self.timer_init()
		self.attack_timer_start()

	def change_mushroom_status(self, fear_status):
		"""
		更改胆小菇状态
		:param fear_status:
		:return:
		"""
		try:
			if self.is_fear == fear_status: return
			if fear_status is True:
				new_gif = ":images/plants/ScaredyShroom/ScaredyShroomCry.gif"
				if self.attack_timer.isActive():
					self.attack_timer.stop()
			else:
				new_gif = self.put_pix
				if not self.attack_timer.isActive():
					self.attack_timer.start()
			self.set_movie(new_gif)
			self.is_fear = fear_status
		except:
			pass

	def check_self_in_danger_zone(self, zombie_set):
		"""
		检测是否胆小
		"""
		flag = False
		zombie_list = list(zombie_set)
		for each_zombie in zombie_list:
			aim_zombie_item = each_zombie
			x1, y1 = self.row_index, self.col_index
			x2, y2 = aim_zombie_item.row_index, aim_zombie_item.col_index
			if (abs(x1 - x2) <= 3 and y1 == y2) or (abs(y1 - y2) <= 1 and x1 == x2) or (x1 == x2 and y1 == y2):
				flag = True
				break
		self.change_mushroom_status(flag)


class RangePlantBase(Plant):
	"""
	范围伤害的植物
	"""
	boom_finished = pyqtSignal(tuple)

	def __init__(self, p=None):
		super(RangePlantBase, self).__init__(p)
		self.boom_timer_init()

	def boom_timer_init(self):
		self.boom_timer = QTimer(self)
		self.boom_timer.setInterval(400)
		self.boom_timer.timeout.connect(self.set_boom)

	def set_boom(self):
		pass

	def emit_plant_died(self):
		try:
			self.plant_died.emit(self)
		except RuntimeError:
			pass


class SingleFlashPlantBase(Plant):
	"""
	单体秒杀僵尸
	"""
	flash_finished = pyqtSignal()

	def __init__(self, p=None):
		super(SingleFlashPlantBase, self).__init__(p)
		self.param_re_init()

	def param_re_init(self):
		self.hash_flashed = False

	def set_flash(self, zombie_item):
		"""
		秒杀僵尸
		"""
		if self.hash_flashed is True: return
		zombie_item.take_damage(self.damage)
		self.flash_finished.emit()
		self.hash_flashed = True
		try:
			QTimer.singleShot(400, lambda: self.plant_died.emit(self))
		except RuntimeError:
			pass


class CherryBoom(RangePlantBase):
	"""
	樱桃炸弹
	"""

	def __init__(self, parent=None):
		super(CherryBoom, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["cherry_boom"])

	def set_boom(self):
		"""
		爆炸 造成伤害 销毁
		:return:
		"""
		self.set_movie(":images/plants/CherryBomb/Boom.gif")
		self.boom_timer.stop()
		self.boom_finished.emit(self.range_effect)
		QTimer.singleShot(700, self.emit_plant_died)  # 停留后自动隐藏


class Jalapeno(RangePlantBase):
	"""
	火爆辣椒
	"""

	def __init__(self, parent=None):
		super(Jalapeno, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["jalapeno"])

	def set_boom(self):
		"""
		爆炸 造成伤害 销毁
		:return:
		"""

		self.boom_timer.stop()
		self.boom_finished.emit(self.range_effect)
		QTimer.singleShot(200, self.emit_plant_died)  # 停留后自动隐藏


class Pumpkin(RangePlantBase):
	"""
	倭瓜
	"""

	def __init__(self, parent=None):
		super(Pumpkin, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["pumpkin"])

	def scan_zombies(self, zombie_set):
		"""
		扫描附近的僵尸
		"""

		def set_damage():
			self.set_movie(":images/plants/Squash/SquashAttack.gif")
			try:
				for each_zombie_ in aim_zombie_list:
					each_zombie_.take_damage(self.damage, self)
			except RuntimeError:  # 可能攻击僵尸的时候 僵尸已经死了
				pass
			try:
				QTimer.singleShot(800, self.emit_plant_died)  # 停留后自动隐藏
			except RuntimeError:
				pass

		aim_zombie_list = []
		for each_zombie in list(zombie_set):
			if check_coordinate_in_range((self.row_index, self.col_index), self.range_effect,
										 (each_zombie.row_index, each_zombie.col_index)):
				aim_zombie_list.append(each_zombie)
		if len(aim_zombie_list) > 0:
			self.boom_finished.emit(self.range_effect)
			QTimer.singleShot(800, set_damage)


class PotatoMine(RangePlantBase):
	"""
	土豆地雷
	"""

	def __init__(self, parent=None):
		super(PotatoMine, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["potato_mine"])
		self.arming_time = self._data_item.get("arming_time", 0)
		self.mine_timer_init()

	def param_init(self):
		super(PotatoMine, self).param_init()
		self.mine_finished = False  # 炸弹是否可以爆炸

	def mine_timer_init(self):
		self.mine_timer = QTimer(self)
		self.mine_timer.setInterval(self.arming_time * 1000)
		self.mine_timer.timeout.connect(self.set_arming_status)
		self.mine_timer.start()

	def set_arming_status(self):
		self.set_movie(":images/plants/PotatoMine/PotatoMine.gif")  # 等待引爆状态
		self.mine_timer.stop()
		self.mine_finished = True

	def show_shipu(self):
		self.shipu_label = Element(self)
		self.shipu_label.set_movie(":images/plants/PotatoMine/ExplosionSpudow.gif")
		self.shipu_label.setFixedWidth(self.width_)
		self.shipu_label.setFixedHeight(55)
		self.shipu_label.raise_()
		self.shipu_label.show()

	def set_boom(self):
		"""
		爆炸 造成伤害 销毁
		:return:
		"""
		if self.mine_finished is False: return
		self.set_movie(":images/plants/PotatoMine/PotatoMine_mashed.gif")  # 已经引爆状态
		self.show_shipu()
		self.mine_timer.stop()
		self.boom_finished.emit(self.range_effect)
		QTimer.singleShot(400, self.emit_plant_died)  # 停留后自动隐藏


class Chomper(RangePlantBase):
	"""
	食人花
	"""

	def __init__(self, parent=None):
		super(Chomper, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["chomper"])
		self.digestion_time = self._data_item['digestion_time']  # 消化时间
		self.chomper_init()
		self.set_custom_size(120)

	def chomper_init(self):
		self.is_digesting = False  # 默认没有开始消化
		self.chomper_digesting_timer = QTimer(self)
		self.chomper_digesting_timer.setInterval(self.digestion_time * 1000)
		self.chomper_digesting_timer.timeout.connect(self.change_chomp_status)

	def change_chomp_status(self):
		"""
		消化完成
		:return:
		"""
		self.set_movie(self.put_pix)  # 默认状态
		self.chomper_digesting_timer.stop()
		self.is_digesting = False

	def set_chomp(self):
		"""
		食人
		:return:
		"""

		def set_chomp_status():
			if not self.chomper_digesting_timer.isActive():
				self.chomper_digesting_timer.start()
			self.set_movie(":images/plants/Chomper/ChomperDigest.gif")  # 正在消化

		if self.is_digesting is True: return
		self.is_digesting = True
		self.set_movie(":images/plants/Chomper/ChomperAttack.gif")  # 开始食人
		QTimer.singleShot(500, set_chomp_status)  # 停留后自动隐藏
		self.boom_finished.emit(self.range_effect)


class Lurker(RangePlantBase):
	"""
	地刺
	"""

	def __init__(self, p=None):
		super(Lurker, self).__init__(p)
		self.set_property(normal_conf.plant_param_dict["lurker"])
		self.lurker_timer_init()

	def lurker_timer_init(self):
		self.can_attack = True
		self.lurker_timer = QTimer(self)
		self.lurker_timer.setInterval(self.attack_gap * 1000)
		self.lurker_timer.timeout.connect(self.set_attack_state)

	def set_attack_state(self):
		self.can_attack = True

	def set_boom(self):
		if self.can_attack is False: return
		self.change_effect("hit", 500)
		self.boom_finished.emit(self.range_effect)
		self.can_attack = False


class SpikerRock(RangePlantBase):
	"""
	地刺王
	"""

	def __init__(self, p=None):
		super(SpikerRock, self).__init__(p)
		self.set_property(normal_conf.plant_param_dict["spiker_rock"])
		self.lurker_timer_init()

	def lurker_timer_init(self):
		self.can_attack = True
		self.current_level = 3
		self.lurker_timer = QTimer(self)
		self.lurker_timer.setInterval(self.attack_gap * 1000)
		self.lurker_timer.timeout.connect(self.set_attack_state)

	def set_property(self, _data_item):
		"""
		设置特有的属性
		"""
		super(SpikerRock, self).set_property(_data_item)
		self.put_pix2 = _data_item.get('put_pix2', "")
		self.put_pix3 = _data_item.get('put_pix3', "")

	def update_spikerRock_state(self):
		"""
		更新地磁王耐久度
		"""
		if self.hp <= 0:
			self.destroy()
		else:
			self.current_level -= 1
			if self.current_level == 2:
				self.set_movie(self.put_pix2)
			elif self.current_level == 3:
				self.set_movie(self.put_pix3)

	def set_attack_state(self):
		self.can_attack = True

	def set_boom(self):
		if self.can_attack is False: return
		self.change_effect("hit", 500)
		self.boom_finished.emit(self.range_effect)
		self.can_attack = False


class FrostMushroom(RangePlantBase):
	"""
	冰霜蘑菇
	"""

	def __init__(self, p=None):
		super(FrostMushroom, self).__init__(p)
		self.set_property(normal_conf.plant_param_dict["frost_mushroom"])
		self.prepare_time = self._data_item['prepare_time']  # 准备时间
		self.pause_duration = self._data_item['pause_duration']  # 僵尸暂停时间
		self.boom_timer.setInterval(self.prepare_time * 1000)
		self.is_shroom = True  # 是否为蘑菇

	def set_boom(self):
		try:
			self.boom_timer.stop()
			self.boom_finished.emit(self.range_effect)
			QTimer.singleShot(600, self.emit_plant_died)  # 停留后自动隐藏
		except RuntimeError:  # 1秒钟可能被僵尸吃掉
			pass


class Cactus(ShooterBase):
	"""
	仙人掌
	"""

	def __init__(self, parent=None):
		super(Cactus, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["cactus"])
		self.timer_init()
		self.attack_timer_start()


class SeaShroomShooter(ShooterBase):
	"""
	水兵菇
	"""

	def __init__(self, parent=None):
		super(SeaShroomShooter, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["sea_shroom"])
		self.is_shroom = True  # 是否为蘑菇
		self.timer_init()
		self.set_custom_size(80)
		self.attack_timer_start()


class TangleKelp(SingleFlashPlantBase):
	"""
	缠绕水藻 秒杀一个距离最近额僵尸
	"""

	def __init__(self, parent=None):
		super(TangleKelp, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["tangle_kelp"])


class DoomShroom(RangePlantBase):
	"""
	毁灭菇
	"""
	bury_gen_signal = pyqtSignal(tuple)

	def __init__(self, parent=None):
		super(DoomShroom, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["doom_shroom"])
		self.is_shroom = True  # 是否为蘑菇

	def set_boom(self):
		"""
		爆炸 造成伤害 销毁
		:return:
		"""
		QTimer.singleShot(450, self.before_boom)  # 停留后自动隐藏

	def before_boom(self):
		try:
			self.boom_timer.stop()
			self.boom_finished.emit(self.range_effect)
			self.set_movie(":images/plants/DoomShroom/Boom.png")
			QTimer.singleShot(450, self.after_boom)  # 停留后自动隐藏
		except RuntimeError:
			pass

	def after_boom(self):
		"""
		爆炸之后产生坑洞
		"""
		try:
			self.emit_plant_died()
			self.bury_gen_signal.emit((self.row_index, self.col_index))
		except RuntimeError:
			pass


class PlaceholderPlantBase(Plant):
	"""
	占位植物
	"""

	def __init__(self, p=None):
		super(PlaceholderPlantBase, self).__init__(p)
		self.hp_line.setVisible(False)  # 隐藏体力值
		self.plant_type = 1

	def set_base_infos(self, data_item):
		self._data_item = data_item
		self.plant_id = data_item['id']
		self.cost = data_item['cost']

	def paintEvent(self, event):
		super(Element, self).paintEvent(event)


class IceItem(PlaceholderPlantBase):
	"""
	冰
	"""

	def __init__(self, p=None):
		super(IceItem, self).__init__(p)
		self.set_base_infos(normal_conf.placeholder_item_param_dict['ice_item'])
		self.set_movie(":images/others/ice.png")
		self.ice_timer_init()

	def ice_timer_init(self):
		self.ice_timer = QTimer()
		self.ice_timer.setInterval(30000)
		self.ice_timer.timeout.connect(self.ice_clear)
		self.ice_timer.start()

	def ice_clear(self):
		try:
			self.plant_died.emit(self)
			self.ice_timer.stop()
		except RuntimeError:
			pass


class TombStoneItem(PlaceholderPlantBase):
	"""
	墓碑
	"""

	def __init__(self, p=None):
		super(TombStoneItem, self).__init__(p)
		self.set_base_infos(normal_conf.placeholder_item_param_dict['tomb_stone'])
		self.ui_reinit()

	def ui_reinit(self):
		super(TombStoneItem, self).ui_reinit()
		self.set_movie(":images/others/tomb/{}.png".format(random.randint(1, 5)))
		self.add_random_soil()

	def add_random_soil(self):
		"""
		添加土壤
		"""
		self.bury_soil = Element(self)
		self.bury_soil.set_movie(":images/others/soil/{}.png".format(random.randint(1, 5)))
		self.bury_soil.setFixedSize(QSize(75, 35))
		self.bury_soil.move(12, self.height_ - self.bury_soil.height())
		self.bury_soil.lower()


class BuryItem(PlaceholderPlantBase):
	"""
	土坑
	"""

	def __init__(self, p=None):
		super(BuryItem, self).__init__(p)
		self.set_base_infos(normal_conf.placeholder_item_param_dict['bury_item'])
		self.bury_param_init()
		self.bury_timer_init()
		if 0:
			self.set_bury_item(2, 3)

	def bury_param_init(self):
		self.passed_time = 0  # 过去了多久
		self.bury_timer_sec = 10  # 50秒修复一个坑

	def bury_timer_init(self):
		"""
		土坑状态更新定时器
		"""
		self.bury_timer = QTimer(self)
		self.bury_timer.setInterval(50000)  # 坑洞50秒修复好
		self.bury_timer.timeout.connect(self.update_bury_status)

	def set_bury_item(self, map_id, line_index):
		"""
		根据地图id 选择土坑样式
		"""
		if line_index in [2, 3]:
			if map_id == 3:  # 白天泳池
				self.bury_pix = ":images/others/crater/crater21.png"
			elif map_id == 4:  # 夜晚泳池
				self.bury_pix = ":images/others/crater/crater20.png"
			elif map_id == 2:
				self.bury_pix = ":images/others/crater/crater10.png"
			elif map_id == 1:
				self.bury_pix = ":images/others/crater/crater11.png"
		else:
			if map_id in [1, 3]:  # 白天
				self.bury_pix = ":images/others/crater/crater11.png"
			elif map_id in [2, 4]:  # 夜晚
				self.bury_pix = ":images/others/crater/crater10.png"
		pixmap = QPixmap(self.bury_pix)  # 替换为你的QRC资源路径
		half_width = pixmap.width() // 2
		half_height = pixmap.height()
		self.bury_full = pixmap.copy(QRect(0, 0, half_width, half_height))
		self.bury_part = pixmap.copy(QRect(half_width, 0, half_width, half_height))
		self.set_bury_status(1)
		self.bury_timer.start()

	def update_bury_status(self):
		"""
		更新土坑状态
		"""
		self.passed_time += 1
		if self.passed_time > self.bury_timer_sec:
			self.set_bury_status(3)
			self.plant_died.emit(self)
			self.bury_timer.stop()
			return
		if self.passed_time <= self.bury_timer_sec * 0.6:
			self.set_bury_status(1)
		else:
			self.set_bury_status(2)

	def set_bury_status(self, status):
		"""
		更新土坑状态
		1 完整土坑
		2 快修复了的土坑
		3 没有土坑
		"""
		status_pix_dict = {
			1: self.bury_full,
			2: self.bury_part,
			3: QPixmap(""),
		}
		if status not in status_pix_dict: return
		self.set_movie(status_pix_dict[status])


class Torchwood(Plant):
	"""
	火炬树桩
	"""

	def __init__(self, p=None):
		super(Torchwood, self).__init__(p)
		self.set_property(normal_conf.plant_param_dict['torchwood'])


class GraveBuster(Plant):
	"""
	墓碑吞噬者
	"""
	buster_finished = pyqtSignal(QObject)

	def __init__(self, p=None):
		super(GraveBuster, self).__init__(p)
		self.set_property(normal_conf.plant_param_dict['grave_buster'])
		self.buster_duration = self._data_item['buster_duration']  # 吞噬时长

	def start_buster(self, tomb_item):
		"""
		开始吞噬墓碑
		"""

		def buster_finish():
			try:
				self.buster_finished.emit(tomb_item)
			except:
				traceback.print_exc()

		try:
			QTimer.singleShot(self.buster_duration * 1000, buster_finish)
			self.plant_died.emit(self)
		except:
			traceback.print_exc()


class CoffeeBean(Plant):
	"""
	咖啡豆
	"""
	wake_up_finished = pyqtSignal(QObject)

	def __init__(self, p=None):
		super(CoffeeBean, self).__init__(p)
		self.set_property(normal_conf.plant_param_dict['coffee_bean'])
		self.wake_up_duration = self._data_item['wake_up_duration']  # 唤醒时长

	def start_wake_up(self, shroom_plant_item):
		"""
		开始唤醒蘑菇
		"""

		def wake_up_finish():
			try:
				self.wake_up_finished.emit(shroom_plant_item)
			except:
				traceback.print_exc()

		try:
			QTimer.singleShot(self.wake_up_duration * 1000, wake_up_finish)
			self.plant_died.emit(self)
		except:
			traceback.print_exc()


class HypnoShroom(Plant):
	"""
	魅惑蘑菇
	"""
	charm_created = pyqtSignal()

	def __init__(self, p=None):
		super(HypnoShroom, self).__init__(p)
		self.set_property(normal_conf.plant_param_dict['hypno_shroom'])
		self.is_shroom = True  # 是否为蘑菇

	def create_charm(self):
		"""
		创建了魅惑状态
		"""
		self.charm_created.emit()
		self.plant_died.emit(self)


class MagnetShroom(Plant):
	"""
	磁力蘑菇
	"""

	def __init__(self, p=None):
		super(MagnetShroom, self).__init__(p)
		self.set_property(normal_conf.plant_param_dict['magnet_shroom'])
		self.gap = self._data_item['gap']
		self.magnet_init()

	def magnet_init(self):
		self.is_shroom = True  # 是否为蘑菇
		self.is_magnet = False  # 是否吸取到了铁质武器
		self.magnet_timer = QTimer(self)
		self.magnet_timer.setInterval(self.gap * 1000)

	def change_magent_shroom_status(self):
		"""
		改变磁力菇状态
		"""
		try:
			self.is_magnet = not self.is_magnet
			if self.is_magnet:  # 吸取到了铁质武器
				pix = ":images/plants/MagnetShroom/nonactive_idle.gif"
			else:
				pix = ":images/plants/MagnetShroom/idle.gif"
			self.set_movie(pix)
		except RuntimeError:
			pass

	def scan_range_zombies(self, zombie_set):
		"""
		扫描范围内僵尸
		"""
		if self.is_magnet is True: return
		for each_zombie in list(zombie_set):
			if check_coordinate_in_range((self.row_index, self.col_index), self.range_effect,
										 (each_zombie.row_index, each_zombie.col_index)):
				each_zombie.lose_iron_weapons()
				# 根据僵尸计算铁质武器
				self.is_magnet = True
				self.set_movie(":images/plants/MagnetShroom/shooting.gif")
				QTimer.singleShot(800, self.change_magent_shroom_status)
				return


class SplitPeaShooter(ShooterBase):
	"""
	裂荚射手
	"""

	def __init__(self, parent=None):
		super(SplitPeaShooter, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["split_pea"])
		self.timer_init()
		self.attack_timer_start()

	def attack(self):
		"""
		发射三粒豌豆攻击敌人
		正面一粒 背面两粒
		"""
		self.new_bullet_created.emit(QPoint(1, 0))
		self.new_bullet_created.emit(QPoint(-1, 0))
		QTimer.singleShot(200, lambda: self.new_bullet_created.emit(QPoint(-1, 0)))


class GatlingPeaShooter(ShooterBase):
	"""
	机枪射手
	"""

	def __init__(self, parent=None):
		super(GatlingPeaShooter, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["gatling_pea"])
		self.timer_init()
		self.attack_timer_start()

	def attack(self):
		"""
		发射四粒豌豆攻击敌人
		"""
		self.new_bullet_created.emit(QPoint(1, 0))
		QTimer.singleShot(100, lambda: self.new_bullet_created.emit(QPoint(1, 0)))
		QTimer.singleShot(200, lambda: self.new_bullet_created.emit(QPoint(1, 0)))
		QTimer.singleShot(300, lambda: self.new_bullet_created.emit(QPoint(1, 0)))


class Marigold(Plant):
	"""
	金盏花
	"""
	new_coin_gen = pyqtSignal()

	def __init__(self, p=None):
		super(Marigold, self).__init__(p)
		self.set_property(normal_conf.plant_param_dict['marigold'])
		self.gap = self._data_item['gap']
		self.marigold_init()

	def marigold_init(self):
		"""
		金盏花定时器初始化
		"""
		self.marigold_timer = QTimer(self)
		self.marigold_timer.setInterval(self.gap * 1000)
		self.marigold_timer.start()
		self.marigold_timer.timeout.connect(self.new_coin_gen.emit)


class GoldMagnet(Plant):
	"""
	吸金磁
	"""

	def __init__(self, p=None):
		super(GoldMagnet, self).__init__(p)
		self.set_property(normal_conf.plant_param_dict['gold_magnet'])


class UmbrellaLeaf(Plant):
	"""
	莴苣
	"""

	def __init__(self, p=None):
		super(UmbrellaLeaf, self).__init__(p)
		self.set_property(normal_conf.plant_param_dict['umbrella_leaf'])


class Blover(Plant):
	"""
	三叶草
	"""
	blow_finished = pyqtSignal()  # 吹走完成

	def __init__(self, p=None):
		super(Blover, self).__init__(p)
		self.set_property(normal_conf.plant_param_dict['blover'])

	def prepare_blow(self):
		"""
		吹走迷雾 以及跳跳、气球僵尸
		"""

		def set_blow():
			try:
				zombie_set = self.parent().zombie_set if hasattr(self.parent(), 'zombie_set') else []
				for each_zombie in list(zombie_set):
					if each_zombie.zombie_id in [21, 22]:
						each_zombie.take_damage(9999)
				self.plant_died.emit(self)
			except RuntimeError:
				pass

		QTimer.singleShot(1500, set_blow)


class GloomShroom(ShooterBase):
	"""
	忧郁喷菇
	"""

	def __init__(self, parent=None):
		super(GloomShroom, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["gloom_shroom"])
		self.timer_init()
		self.attack_timer_start()
		self.is_shroom = True  # 是否为蘑菇


class FumeMushroomShooter(ShooterBase):
	"""
	大喷菇
	"""

	def __init__(self, parent=None):
		super(FumeMushroomShooter, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["fume_shroom"])
		self.timer_init()
		self.attack_timer_start()
		self.is_shroom = True  # 是否为蘑菇


class Garlic(NutBase):
	"""
	大蒜
	"""
	on_zombie_sick = pyqtSignal()

	def __init__(self, parent=None):
		super(Garlic, self).__init__(parent)
		self.set_property(normal_conf.plant_param_dict["garlic"])
		self.set_movie(self.put_pix)  # 设置初始动画
		self.set_custom_size(80)
	def take_damage(self, damage, attacker):
		super(Garlic, self).take_damage(damage, attacker)
		attacker.set_pause_status(0.5)  # 攻击者暂停
		attacker.change_random_line()  # 攻击者换路线
		self.on_zombie_sick.emit()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	win = FumeMushroomShooter()
	# win = Torchwood()
	# win = Watermelon()
	# win = TombStoneItem()
	# win = BuryItem()
	# win = IceItem()
	# win = PotatoMine()
	# win = CherryBoom()
	# win = IcePea()
	# win = WallNut()
	# win = Peashooter()
	# win = SunFlower()
	win.show()
	sys.exit(app.exec_())
