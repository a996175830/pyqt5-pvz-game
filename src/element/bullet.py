import math
import sys
import traceback

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication

from src.my_util.utils import check_coordinate_in_range
from .base import Bullet
from src.config import normal_conf
from PyQt5.QtCore import QTimer, QPoint, QRect


class LineBullet(Bullet):
	"""
	直线子弹
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), direction=QPoint(1, 0), line_index=-1):
		super(LineBullet, self).__init__(p)
		self.direction = direction  # 方向
		self.row_index = line_index  # 子弹所在行索引
		self.slot_init()
		self.setObjectName("lineBullet")
		self.setStyleSheet("#lineBullet{background-color: transparent;}")
		self.setGeometry(QRect(start_pos.x(), start_pos.y(), self.width(), self.height()))
		self.setMaximumSize(QSize(self.width_, self.height_))

	def param_init(self):
		super(LineBullet, self).param_init()
		self.shoted_zombie_id_set = set()  # 被击中过的僵尸id列表
		self.across_plant_id_set = set()  # 经过的植物id列表

	def slot_init(self):
		self.timer.timeout.connect(self.move_bullet)

	def move_bullet(self):
		# 更新子弹的位置
		current_pos = self.pos()
		new_x = current_pos.x() + self.direction.x() * self.speed
		new_y = current_pos.y() + self.direction.y() * self.speed
		self.setGeometry(QRect(new_x, new_y, self.width(), self.height()))
		zombie_set = self.parent().zombie_set if hasattr(self.parent(), 'zombie_set') else []
		if self.check_zombie_collisions(list(zombie_set)):
			self.set_hit_state_image()
		plant_set = self.parent().plant_set if hasattr(self.parent(), 'plant_set') else []
		self.col_index = math.floor((new_x + 30) / self.parent().grass_width) - 1  # 更新当前所在列索引
		self.check_plant_collisions(list(plant_set))

	def check_zombie_collisions(self, zombie_list):
		"""
		子弹碰撞僵尸检测
		:param items:
		:return:
		"""
		bullet_rect = QRect(self.pos(), self.size())
		for zombie in zombie_list:
			zombie_rect = QRect(zombie.pos(), zombie.size())
			if bullet_rect.intersects(zombie_rect) and zombie.row_index == self.row_index:
				if bullet_rect.right() - zombie_rect.width() / 2 > zombie_rect.left():  # 校正 让子弹打中僵尸
					if id(zombie) in self.shoted_zombie_id_set:  # 直线打中过的僵尸不再击中
						return False
					if zombie.is_hypno is True: continue
					if self.bullet_id in [5, 6] and zombie.zombie_id == 22:  # 仙人掌针刺或者香蒲针刺 打破气球僵尸的气球
						zombie.set_balloon_boom()
					else:
						if zombie.zombie_level != 1: continue  # 僵尸的层级
					zombie.take_damage(self.damage, self)
					if self.bullet_id == 2:  # 冰豌豆
						zombie_id = zombie.zombie_id
						if zombie_id in (6, 7, 18):  # 铁门僵尸、看报纸僵尸、梯子僵尸
							if zombie.zombie_id == 7:
								if zombie.news_paper_is_dropped is True:
									zombie.set_moderate(self.moderate, self.moderate_duration)
						else:
							if zombie.is_car_zombie is False:  # 车类型不受减速效果影响
								zombie.set_moderate(self.moderate, self.moderate_duration)
					self.shoted_zombie_id_set.add(id(zombie))
					return True
		return False

	def check_plant_collisions(self, plant_list):
		"""
		子弹碰撞植物检测
		:param plant_list: 植物列表
		:return: 如果发生碰撞返回 True，否则返回 False
		"""
		for plant in plant_list:
			plant_id = id(plant)
			# 判断是否发生碰撞，并且在同一行和同一列
			if plant_id in self.across_plant_id_set:
				continue  # 已经处理过的植物，不再处理
			if self.col_index == plant.col_index and self.row_index == plant.row_index:
				if plant.plant_id == 26:  # 处理火炬树桩逻辑
					if self.bullet_id in [1, 2]:  # 普通豌豆、冰豌豆处理逻辑
						self.change_pea_bullet()
						self.across_plant_id_set.add(plant_id)  # 添加到已处理列表
						return True  # 碰撞发生，返回 True
		return False  # 没有碰撞，返回 False


class BiasBullet(Bullet):
	"""
	斜线子弹
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), direction=QPoint(1, 0)):
		super(BiasBullet, self).__init__(p)
		self.direction = direction  # 方向
		self.slot_init()
		self.setObjectName("lineBullet")
		self.setStyleSheet("#lineBullet{background-color: transparent;}")
		self.setGeometry(QRect(start_pos.x(), start_pos.y(), self.width(), self.height()))
		self.setMaximumSize(QSize(self.width_, self.height_))

	def param_init(self):
		super(BiasBullet, self).param_init()
		self.width_ = 30  # 子弹方格大小
		self.height_ = 30  # 子弹方格大小
		self.setFixedSize(QSize(self.width_, self.height_))
		self.row_index = -1  # 子弹所在行索引
		self.col_index = -1  # 子弹所在列索引
		self.shoted_zombie_id_set = set()  # 被击中过的僵尸id列表

	def slot_init(self):
		self.timer.timeout.connect(self.move_bullet)

	def move_bullet(self):
		# 更新子弹的位置
		current_pos = self.pos()
		new_x = current_pos.x() + self.direction.x() * self.speed
		new_y = current_pos.y() + self.direction.y() * self.speed
		self.row_index = math.floor((new_y - 160) / normal_conf.noswimming_grass_height) - 1  # 更新当前所在列索引
		self.col_index = math.floor((new_x + 60) / self.parent().grass_width) - 1  # 更新当前所在列索引
		self.setGeometry(QRect(new_x, new_y, self.width(), self.height()))
		if self.row_index > 15 or self.row_index < -5 or self.col_index < -5 or self.col_index > 10: self.deleteLater()
		zombie_set = self.parent().zombie_set if hasattr(self.parent(), 'zombie_set') else []
		if self.check_zombie_collisions(list(zombie_set)):
			self.set_hit_state_image()

	def check_zombie_collisions(self, zombie_list):
		"""
		子弹碰撞僵尸检测
		:param items:
		:return:
		"""
		bullet_rect = QRect(self.pos(), self.size())
		for zombie in zombie_list:
			zombie_rect = QRect(zombie.pos(), zombie.size())
			if bullet_rect.intersects(zombie_rect):
				if id(zombie) in self.shoted_zombie_id_set:  # 直线打中过的僵尸不再击中
					return False
				if zombie.is_hypno is True: continue
				zombie.take_damage(self.damage, self)
				self.shoted_zombie_id_set.add(id(zombie))
				return True
		return False


class StarBullet(BiasBullet):
	"""
	杨桃子弹
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), direction=QPoint(1, 0)):
		super(StarBullet, self).__init__(p, start_pos=start_pos, direction=direction)
		self.set_property(normal_conf.plant_bullet_data['star'])


class FumeBulletBase(Bullet):
	"""
	烟雾穿透子弹
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), line_index=-1, col_index=-1):
		super(FumeBulletBase, self).__init__(p)
		self.line_index = line_index  # 子弹所在行索引
		self.col_index = col_index  # 子弹所在行索引
		self.bullet_pos_tuple = (self.line_index, self.col_index)
		self.setObjectName("fumeBulletBase")
		self.setStyleSheet("#fumeBulletBase{background-color: transparent;}")
		self.width_ = 520  # 子弹方格大小
		self.height_ = 60  # 子弹方格大小
		self.has_attacked = False
		self.setGeometry(QRect(start_pos.x(), start_pos.y(), self.width(), self.height()))
		self.setFixedSize(QSize(self.width_, self.height_))

	def start_bullet(self):
		self.timer.setInterval(self.attack_gap * 1000)
		self.timer.start()
		self.timer.timeout.connect(self.move_bullet)

	def move_bullet(self):
		"""
		展示烟雾 造成伤害
		"""
		if self.has_attacked is False:
			self.take_damage()
		QTimer.singleShot(1200, self.hide)

	def take_damage(self):
		"""
		对所在行附近4格的僵尸造成伤害
		"""
		items = list(self.parent().zombie_set) if hasattr(self.parent(), 'zombie_set') else []
		for each_zombie in items:
			if each_zombie.is_hypno: continue  # 被魅惑的不被算在里面
			if self.bullet_pos_tuple[0] == each_zombie.row_index and 0 < each_zombie.col_index - self.bullet_pos_tuple[
				1] <= 4:
				each_zombie.set_moderate(self.moderate, self.moderate_duration)  # 减速效果
				each_zombie.take_damage(self.damage, self)
		self.has_attacked = True


class PeaBulletBase(LineBullet):
	"""
	豌豆子弹基类
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), direction=QPoint(1, 0), line_index=-1):
		super(PeaBulletBase, self).__init__(p, start_pos=start_pos, direction=direction, line_index=line_index)
		self.param_re_init()

	def param_re_init(self):
		self.is_transformed_once = False  # 标记是否从冰豌豆变为普通豌豆过

	def change_pea_bullet(self):
		"""
		普通豌豆-火豌豆
		冰豌豆-普通豌豆-火豌豆
		"""
		if self.bullet_id == 1:  # 当前是普通豌豆
			self.change_to_fire_pea()
		elif self.bullet_id == 2:  # 当前是冰豌豆
			if self.is_transformed_once is False:  # 如果是第一次调用
				self.change_to_normal_pea()
				self.is_transformed_once = True  # 标记已转换为普通豌豆
			else:  # 第二次调用，转换为火豌豆
				self.change_to_fire_pea()

	def change_to_fire_pea(self):
		"""
		经过了火炬树桩 威力增强
		"""
		self.damage = FirePeaBullet().damage  # 威力翻倍
		self.bullet_hit = FirePeaBullet().bullet_hit  # 更改被打中贴图
		self.effect_key = FirePeaBullet().effect_key  # 更改音效
		self.set_movie(FirePeaBullet().bullet)  # 更改贴图

	def change_to_normal_pea(self):
		"""
		经过了火炬树桩 变成普通豌豆
		"""
		self.damage = PeaBullet().damage
		self.bullet_hit = PeaBullet().bullet_hit  # 更改被打中贴图
		self.effect_key = PeaBullet().effect_key  # 更改音效
		self.moderate = PeaBullet().moderate  # 更改减速
		self.moderate_duration = PeaBullet().moderate_duration  # 更改减速时间
		self.set_movie(PeaBullet().bullet)  # 更改贴图


class PeaBullet(PeaBulletBase):
	"""
	豌豆子弹
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), direction=QPoint(1, 0), line_index=-1):
		super(PeaBullet, self).__init__(p, start_pos=start_pos, direction=direction, line_index=line_index)
		self.set_property(normal_conf.plant_bullet_data['pea'])


class IcePeaBullet(PeaBulletBase):
	"""
	冰豌豆子弹
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), direction=QPoint(1, 0), line_index=-1):
		super(IcePeaBullet, self).__init__(p, start_pos=start_pos, direction=direction, line_index=line_index)
		self.set_property(normal_conf.plant_bullet_data['ice_pea'])


class FirePeaBullet(PeaBulletBase):
	"""
	火焰豌豆子弹
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), direction=QPoint(1, 0), line_index=-1):
		super(FirePeaBullet, self).__init__(p, start_pos=start_pos, direction=direction, line_index=line_index)
		self.set_property(normal_conf.plant_bullet_data['fire_pea'])


class SproutMushroomBullet(LineBullet):
	"""
	小喷菇子弹
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), direction=QPoint(1, 0), line_index=-1):
		super(SproutMushroomBullet, self).__init__(p, start_pos=start_pos, direction=direction,
												   line_index=line_index)
		self.set_property(normal_conf.plant_bullet_data['lsm'])


class SeaMushroomBullet(LineBullet):
	"""
	海蘑菇子弹
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), direction=QPoint(1, 0), line_index=-1):
		super(SeaMushroomBullet, self).__init__(p, start_pos=start_pos, direction=direction,
												line_index=line_index)
		self.set_property(normal_conf.plant_bullet_data['sea_shroom_fume'])


class FumeMushroomBullet(FumeBulletBase):
	"""
	大喷菇子弹
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), line_index=-1, col_index=-1):
		super(FumeMushroomBullet, self).__init__(p, start_pos=start_pos,
												 line_index=line_index, col_index=col_index)
		self.set_property(normal_conf.plant_bullet_data['fume'])
		self.start_bullet()


class ThornBullet(LineBullet):
	"""
	仙人掌针刺
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), direction=QPoint(1, 0), line_index=-1):
		super(ThornBullet, self).__init__(p, start_pos=start_pos, direction=direction, line_index=line_index)
		self.set_property(normal_conf.plant_bullet_data['cactus_thorn'])


class CatTailBullet(LineBullet):
	"""
	香蒲针刺
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), direction=QPoint(1, 0), line_index=-1):
		super(CatTailBullet, self).__init__(p, start_pos=start_pos, direction=direction, line_index=line_index)
		self.set_property(normal_conf.plant_bullet_data['cactus_thorn'])


class ArcBullet(Bullet):
	"""
	抛物线子弹
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), line_index=-1):
		super(ArcBullet, self).__init__(p)
		self.start_pos = QPoint(start_pos.x() - self.width_ * 0.3, start_pos.y())
		self.row_index = line_index  # 子弹所在行索引
		self.param_reinit()
		self.timer_re_init()

	def param_reinit(self):
		self.is_attacking = False  # 正在攻击
		self.attack_for_type = 2  # 攻击植物or僵尸 # 元素类型1植物 2僵尸
		self.gravity = 0.5  # 模拟重力加速度
		self.time_elapsed = 0  # 经过的时间
		self.vx = 5  # 水平速度，根据需求调节
		self.vy = -15  # 初始垂直速度，向上
		self.width_ = 45  # 子弹方格大小
		self.height_ = 45  # 子弹方格大小
		self.setStyleSheet("#arcBullet{background-color: transparent;}")
		self.setGeometry(QRect(self.start_pos.x(), self.start_pos.y(), self.width_, self.height_))
		self.setFixedSize(QSize(self.width_, self.height_))
		self.current_pos = self.start_pos

	def timer_re_init(self):
		self.timer.timeout.connect(self.animate_bullet)
		self.timer.start()

	def get_aim_zombie(self):
		"""
		获取目标僵尸
		"""
		items = list(self.parent().zombie_set) if hasattr(self.parent(), 'zombie_set') else []
		aim_zombie_item = None
		aim_zombie_col = float('inf')  # 使用无穷大作为初始比较值
		for each_zombie in items:
			if each_zombie.is_hypno: continue  # 被魅惑的不被算在里面
			if each_zombie.row_index == self.row_index and each_zombie.col_index < aim_zombie_col and each_zombie.zombie_level == 1:
				if each_zombie.col_index < self.col_index: continue  # 在子弹后方的 不攻击
				aim_zombie_item = each_zombie
				aim_zombie_col = each_zombie.col_index
		return aim_zombie_item

	def get_aim_plant(self):
		"""
		获取目标植物
		"""
		items = list(self.parent().plant_set) if hasattr(self.parent(), 'plant_set') else []
		aim_plant_item = None
		aim_zombie_col = float('inf')  # 使用无穷大作为初始比较值
		for each_plant in items:
			if each_plant.row_index == self.row_index and each_plant.col_index < aim_zombie_col:
				aim_plant_item = each_plant
				aim_zombie_col = each_plant.col_index
		return aim_plant_item

	def animate_bullet(self):
		if self.attack_for_type == 1:  # 攻击植物
			aim_item = self.get_aim_plant()
		else:  # 攻击僵尸
			aim_item = self.get_aim_zombie()
		if aim_item is not None and not self.is_attacking:
			self.is_attacking = True

			# 获取目标僵尸的头部中心位置
			zombie_rect = aim_item.rect()
			zombie_head_center = QPoint(zombie_rect.left(), zombie_rect.top())
			aim_item_global_pos = aim_item.mapToGlobal(zombie_head_center)
			aim_item_local_pos = self.parent().mapFromGlobal(aim_item_global_pos)

			# 设置初始速度和目标位置
			self.target_pos = aim_item_local_pos
			self.dx = self.target_pos.x() - self.start_pos.x()
			self.dy = self.target_pos.y() - self.start_pos.y()

			# 计算与僵尸的距离
			distance = ((self.dx) ** 2 + (self.dy) ** 2) ** 0.5

			# 根据距离动态调整 total_time
			min_time = 15  # 最小飞行时间（帧数）
			max_time = 45  # 最大飞行时间（帧数）
			base_distance = 200  # 基准距离，200像素
			total_time = min(max_time, max(min_time, int(distance / base_distance * min_time)))

			# 水平速度
			self.vx = self.dx / total_time

			# 初始垂直速度
			self.gravity = 0.5  # 重力加速度
			self.vy = (self.dy - 0.5 * self.gravity * total_time ** 2) / total_time

			self.time_elapsed = 0  # 重置时间计数器

		if self.is_attacking:
			# 更新时间
			self.time_elapsed += 1

			# 更新水平位置 (线性)
			x_new = self.start_pos.x() + self.vx * self.time_elapsed

			# 更新垂直位置 (抛物线)
			y_new = self.start_pos.y() + (self.vy * self.time_elapsed) + (0.5 * self.gravity * (self.time_elapsed ** 2))

			# 更新子弹位置
			self.current_pos = QPoint(x_new, y_new)
			self.move(self.current_pos)

			# 碰撞检测，判断西瓜是否到达僵尸头部位置
			distance_to_target = ((self.current_pos.x() - self.target_pos.x()) ** 2 +
								  (self.current_pos.y() - self.target_pos.y()) ** 2) ** 0.5

			# 设置一个小的容差值，确保西瓜足够接近目标位置时才停止
			if distance_to_target < 2:  # 容差值5可以根据需要调整
				self.timer.stop()
				self.handle_animation_finished(aim_item)

	def set_range_splash_damage(self, base_zombie):
		"""
		根据溅射范围计算溅射伤害
		"""
		splash_zombie_id_set = set()
		base_zombie_pos_tuple = (base_zombie.row_index, base_zombie.col_index)
		items = list(self.parent().zombie_set) if hasattr(self.parent(), 'zombie_set') else []
		splash_zombie_list = []
		for each_zombie in items:
			if each_zombie.is_hypno: continue  # 被魅惑的不被算在里面
			if id(each_zombie) in splash_zombie_id_set: continue  # 目标僵尸不在溅射范围之内
			zombie_pos_tuple = (each_zombie.row_index, each_zombie.col_index)
			splash_zombie_id_set.add(id(each_zombie))
			if not self.effect_range: continue
			if check_coordinate_in_range(base_zombie_pos_tuple, self.effect_range, zombie_pos_tuple):
				splash_zombie_list.append(each_zombie)
		# 根据僵尸数量计算溅射伤害
		if len(splash_zombie_list) == 0: return
		effect_damage = int(574 / len(splash_zombie_list))
		if effect_damage >= 26:
			effect_damage = 26
		for splash_zombie in splash_zombie_list:
			splash_zombie.set_moderate(self.moderate, self.moderate_duration)  # 减速效果
			splash_zombie.take_damage(effect_damage, self)

	def handle_animation_finished(self, aim_item):
		"""
		处理投手砸中后效果
		"""
		try:
			if aim_item is None: return
			aim_item.take_damage(self.damage, self)
			if aim_item.item_type == 2:  # 处理僵尸
				self.set_hit_state_image()
				aim_item.set_moderate(self.moderate, self.moderate_duration)  # 减速效果
				self.is_attacking = False
				self.set_range_splash_damage(aim_item)
				if hasattr(self, "pause_duration"):
					aim_item.set_pause_status(self.pause_duration)
		except:
			pass
		try:
			self.deleteLater()  # 子弹消失
		except RuntimeError:
			pass


class MelonBullet(ArcBullet):
	"""
	西瓜投手子弹
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), line_index=-1):
		super(MelonBullet, self).__init__(p, start_pos=start_pos, line_index=line_index)
		self.set_property(normal_conf.plant_bullet_data['melon'])
		self.set_custom_size(100, 80)


class BasketballBullet(ArcBullet):
	"""
	篮球车子弹
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), line_index=-1):
		super(BasketballBullet, self).__init__(p, start_pos=start_pos, line_index=line_index)
		self.set_property(normal_conf.plant_bullet_data['basketball'])
		self.set_custom_size(80, 80)
		self.attack_for_type = 1  # 攻击植物


class IceMelonBullet(ArcBullet):
	"""
	冰西瓜投手子弹
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), line_index=-1):
		super(IceMelonBullet, self).__init__(p, start_pos=start_pos, line_index=line_index)
		self.set_property(normal_conf.plant_bullet_data['ice_melon'])
		self.set_custom_size(100, 80)


class ButterDotBullet(ArcBullet):
	"""
	玉米粒
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), line_index=-1):
		super(ButterDotBullet, self).__init__(p, start_pos=start_pos, line_index=line_index)
		self.set_property(normal_conf.plant_bullet_data['butter_dot'])


class ButterBullet(ArcBullet):
	"""
	玉米黄油
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), line_index=-1):
		super(ButterBullet, self).__init__(p, start_pos=start_pos, line_index=line_index)
		self.set_property(normal_conf.plant_bullet_data['butter'])
		self.pause_duration = self._data_item['pause_duration']  # 暂停僵尸 时间间隔


class CabbageBullet(ArcBullet):
	"""
	卷心菜投手子弹
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), line_index=-1):
		super(CabbageBullet, self).__init__(p, start_pos=start_pos, line_index=line_index)
		self.set_property(normal_conf.plant_bullet_data['cabbage'])


class TrackingBullet(Bullet):
	"""
	追踪子弹，始终指向目标僵尸
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), line_index=-1):
		super(TrackingBullet, self).__init__(p)
		self.start_pos = start_pos
		self.row_index = line_index
		self.current_pos = start_pos
		self.is_attacking = False
		self.target_pos = QPoint()
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.animate_bullet)
		self.timer.start(40)  # 每40ms更新一次，即每秒25帧

	def get_aim_zombie(self):
		"""
		获取目标僵尸：
		1. 优先选择当前行的僵尸。
		2. 在所有僵尸中选择 `col_index` 最小的僵尸。
		"""
		items = list(self.parent().zombie_set) if hasattr(self.parent(), 'zombie_set') else []
		aim_zombie_item = None
		aim_zombie_col = float('inf')  # 使用无穷大作为初始比较值

		# 优先选择当前行的僵尸，并在当前行中选择 `col_index` 最小的僵尸
		for each_zombie in items:
			if each_zombie.is_hypno: continue
			if each_zombie.row_index == self.row_index and each_zombie.col_index < aim_zombie_col and each_zombie.col_index != -1 and each_zombie.zombie_level == 1:
				aim_zombie_item = each_zombie
				aim_zombie_col = each_zombie.col_index

		# 如果当前行没有僵尸，则选择所有行中 `col_index` 最小的僵尸
		if aim_zombie_item is None:
			for each_zombie in items:
				if each_zombie.is_hypno: continue
				if each_zombie.col_index < aim_zombie_col and each_zombie.col_index != -1 and each_zombie.zombie_level == 1:
					aim_zombie_item = each_zombie
					aim_zombie_col = each_zombie.col_index
		return aim_zombie_item

	def animate_bullet(self):
		aim_zombie = self.get_aim_zombie()
		self.setVisible(aim_zombie is not None)
		if aim_zombie is not None:
			# 如果找到目标僵尸，更新子弹状态
			if not self.is_attacking:
				self.is_attacking = True
				zombie_rect = aim_zombie.rect()
				zombie_head_center = QPoint(zombie_rect.center().x(), zombie_rect.top())
				aim_zombie_global_pos = aim_zombie.mapToGlobal(zombie_head_center)
				self.target_pos = self.parent().mapFromGlobal(aim_zombie_global_pos)

				# 调整目标位置的 y 坐标
				self.target_pos.setY(int(self.target_pos.y() * 1.2))

			# 计算移动矢量
			dx = self.target_pos.x() - self.current_pos.x()
			dy = self.target_pos.y() - self.current_pos.y()
			distance = math.hypot(dx, dy)

			if distance > 0:
				# 设置子弹的速度
				speed = 15
				vx = speed * (dx / distance)
				vy = speed * (dy / distance)

				# 更新子弹位置
				self.current_pos += QPoint(int(vx), int(vy))
				self.move(self.current_pos)

				# 碰撞检测
				distance_to_target = math.hypot(self.target_pos.x() - self.current_pos.x(),
												self.target_pos.y() - self.current_pos.y())
				if distance_to_target < 8:  # 当距离目标僵尸足够近时，视为命中
					self.timer.stop()
					self.handle_animation_finished(aim_zombie)
		else:
			# 如果找不到目标僵尸并且子弹已经开始攻击，则销毁子弹
			if self.is_attacking:
				self.timer.stop()  # 停止计时器
				try:
					self.deleteLater()  # 子弹消失
				except RuntimeError:
					pass

	def handle_animation_finished(self, zombie):
		"""
		处理子弹命中僵尸后的效果
		"""
		try:
			zombie.take_damage(self.damage, self)
			self.set_hit_state_image()  # 处理子弹命中效果的图像更新
		except:
			pass
		self.is_attacking = False
		try:
			self.deleteLater()  # 子弹消失
		except RuntimeError:
			pass


class CatTailThornBullet(TrackingBullet):
	"""
	香蒲针刺
	"""

	def __init__(self, p=None, start_pos=QPoint(0, 0), line_index=-1):
		super(CatTailThornBullet, self).__init__(p, start_pos=start_pos, line_index=line_index)
		self.set_property(normal_conf.plant_bullet_data['cat_tail_thorn'])


if __name__ == '__main__':
	app = QApplication(sys.argv)
	win = ArcBullet()
	win.show()
	sys.exit(app.exec_())
