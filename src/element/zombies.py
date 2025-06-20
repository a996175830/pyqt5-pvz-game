import math
import random
import sys
import traceback
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QTimer, QObject, QPoint
from PyQt5.QtWidgets import QApplication

from src.config import normal_conf
from src.element.others import DancerLightItem
from src.my_util.utils import check_coordinate_in_range

from .base import Zombie, Element


class PrepareZombie(Element):
	"""
	准备状态的僵尸
	"""

	def __init__(self, p=None):
		super(PrepareZombie, self).__init__(p)
		if 0:
			self.set_zombie_item({"idle_pix": ":images/zombies/normal_idle.gif"})

	def set_zombie_item(self, zombie_item):
		"""
		设置僵尸空闲状态贴图
		"""
		if zombie_item['id'] in [7, 8, 13, 25, 26]:  # 读报僵尸、撑杆跳、伽刚特尔、雪橇车
			self.set_custom_size(250, 250)
		else:
			self.set_custom_size(180, 180)
		self.set_movie(zombie_item.get("idle_pix"))


class LineZombieBase(Zombie):
	"""
	走直线的僵尸
	"""
	enter_danger_zone = pyqtSignal(int)  # 僵尸labe_x坐标为负数

	def __init__(self, p=None):
		super().__init__(p)
		self.attack_timer.timeout.connect(self.attack_animation)
		if 0:
			self.setStyleSheet("""background-color:blue;""")

	def param_init(self):
		super(LineZombieBase, self).param_init()
		self.zombie_item = dict()
		self.width_ = 180
		self.height_ = 180
		self.timer_interval = 60  # 更新间隔（毫秒）
		self.label_x = 0  # 初始 X 坐标
		self.label_y = 0  # 初始 Y 坐标
		self.timer = QTimer(self)  # 永远不会暂停的timer
		self.timer.timeout.connect(self.zombie_move)
		self.setFixedSize(self.width_, self.height_)

	def set_zombie_pos(self, label_x, label_y):
		"""
		设置僵尸数据
		:param label_x: X 坐标
		:param label_y: Y 坐标
		"""
		self.label_x = label_x
		self.label_y = label_y
		self.start_moving()

	def set_line(self, line_index):
		"""
		更改行号
		:param line_index:
		:return:
		"""
		self.row_index = line_index

	def set_hp_flag(self, hp_flag):
		"""
		更改是否显示体力
		:param line_index:
		:return:
		"""
		self.hp_line.setVisible(hp_flag)

	def start_moving(self):
		"""
		启动移动功能
		"""
		self.timer.start(self.timer_interval)

	def stop_moving(self):
		"""
		停止移动功能
		"""
		self.timer.stop()

	def set_zombie_move(self):
		"""
		僵尸行走
		"""
		if self.pause_status is True: return
		if self.is_hypno is True or self.is_reversed is True:  # 被魅惑了
			self.label_x += self.speed
		else:
			self.label_x -= self.speed
		if self.label_x < normal_conf.game_lose_x_offset:
			self.enter_danger_zone.emit(self.row_index)
		self.move(self.label_x, self.label_y)
		new_col_index = math.floor((self.label_x + 60) / self.parent().grass_width) - 1  # 更新当前所在列索引
		if new_col_index != self.col_index:
			self.col_index = new_col_index
			self.zombie_coord_changed.emit(self.row_index, self.col_index)  # 僵尸格数发生了变化

	def change_random_line(self):
		"""
		随机换条线路
		"""
		old_line = self.row_index
		super(LineZombieBase, self).change_random_line()
		new_line = self.row_index
		self.label_y += (new_line - old_line) * normal_conf.noswimming_grass_height

	def get_aim_zombie(self, is_hypno=False):
		"""
		获取目标僵尸
		距离当前僵尸最近的僵尸
		is_hypno目标僵尸是否被魅惑
		"""
		items = list(self.parent().zombie_set) if hasattr(self.parent(), 'zombie_set') else []
		for each_zombie in items:
			if id(self) == id(each_zombie): continue  # 不攻击自己
			if is_hypno is False:
				if each_zombie.row_index == self.row_index and each_zombie.col_index == self.col_index:
					return each_zombie
			else:
				if each_zombie.row_index == self.row_index and each_zombie.col_index == self.col_index and each_zombie.is_hypno is True:
					return each_zombie

	def zombie_move(self):
		"""
		更新僵尸位置
		"""
		if self.is_attacking:
			return  # 僵尸处于攻击状态，不移动
		try:
			if self.is_hypno is False:
				if (self.zombie_id == 23 and self.is_dig_out is False):
					pass
				elif (self.zombie_id == 22 and self.balloon_boom is False):
					pass
				else:
					grass_widget_items = self.parent().grass_widget_items
					for coordinate, plant in grass_widget_items.items():  # plants 是一个包含所有植物的列表
						line_index = coordinate[0]
						if self.check_collision(plant, line_index):  # 僵尸将要吃植物
							if plant.plant_type == 1: continue
							if self.zombie_id == 8 and self.is_skipped is False and self.is_skipping is False:  # 撑杆跳僵尸
								self.set_pole_vault_state()  # 设置撑杆跳状态
								return
							if self.zombie_id == 27 and self.is_skipped is False and self.is_skipping is False:  # 撑杆跳僵尸
								self.set_pole_vault_state()  # 设置撑杆跳状态
								return
							if plant.plant_id == 12:  # 土豆地雷
								plant.set_boom()
								return
							if plant.plant_id in [15, 36]:  # 地刺
								if self.zombie_id in [13, 15]:  # 车类型僵尸
									plant.take_damage(self.damage, self)
									self.set_tire_explosion_status()
								else:
									self.set_zombie_move()
									plant.set_boom()
								return
							elif plant.plant_id == 14:  # 食人花
								if plant.is_digesting is False:
									plant.set_chomp()
									self.take_damage(plant.damage, self)
									return
							elif plant.plant_id == 21:  # 缠绕水藻
								plant.set_flash(self)
								return
							elif plant.plant_id == 28:  # 魅惑蘑菇
								self.change_effect("hypno")  # 僵尸设置为被迷惑状态
								plant.create_charm()
								return
							self.show_zombie_attack(plant)
							return
					aim_zombie = self.get_aim_zombie(True)  # 查找被魅惑了的僵尸
					if aim_zombie is not None:
						self.show_zombie_attack(aim_zombie)
						return
			else:
				# 处理攻击僵尸
				aim_zombie = self.get_aim_zombie(False)
				if aim_zombie is not None:
					self.show_zombie_attack(aim_zombie)
					return
			self.set_zombie_move()
			# 更改贴图
			if self.attack_timer.isActive():
				self.zombie_hp_changed.emit(self.hp)
				self.attack_timer.stop()
		except:
			pass

	def show_zombie_attack(self, aim_item):
		"""
		显示攻击植物的动画，并启动攻击定时器
		:param plant or zombie: 被攻击的植物或者僵尸
		"""
		try:
			self.stop_moving()  # 停止移动
			self.is_attacking = True
			aim_item.take_damage(self.damage, self)
			self.sound_effect_changed.emit("zombie_eating")
			attack_interval = 1000 / self.attack_frequency
			if not self.attack_timer.isActive():
				self.attack_timer.start(attack_interval)
				self.zombie_hp_changed.emit(self.hp)
		except:
			traceback.print_exc()

	def attack_animation(self):
		"""
		攻击动画定时器回调
		"""
		self.is_attacking = False
		self.start_moving()  # 恢复移动功能

	def check_collision(self, plant, line_index):
		"""
		检查僵尸是否与植物接触
		:param plant: Plant 对象
		:param line_index: 僵尸所在行索引
		:return: True 如果接触，否则 False
		"""
		# 确保只检查当前行
		try:
			return self.col_index == plant.col_index and self.row_index == line_index
		except RuntimeError:
			pass
		except Exception:
			traceback.print_exc()
		return False


class RegularZombie(LineZombieBase):
	"""
	普通僵尸
	"""

	def __init__(self, p=None):
		super(RegularZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['regular'])


class ConeheadZombie(LineZombieBase):
	"""
	路障僵尸
	"""

	def __init__(self, p=None):
		super(ConeheadZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['conehead'])


class BucketheadZombie(LineZombieBase):
	"""
	铁通僵尸
	"""

	def __init__(self, p=None):
		super(BucketheadZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['buckethead'])


class FlagZombie(LineZombieBase):
	"""
	旗帜僵尸
	"""

	def __init__(self, p=None):
		super(FlagZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['flag'])


class RubyZombie(LineZombieBase):
	"""
	橄榄球僵尸
	"""

	def __init__(self, p=None):
		super(RubyZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['rugby'])


class IronGateZombie(LineZombieBase):
	"""
	铁门僵尸
	"""

	def __init__(self, p=None):
		super(IronGateZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['iron_gate'])


class LadderZombie(LineZombieBase):
	"""
	梯子僵尸
	"""

	def __init__(self, p=None):
		super(LadderZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['ladder_zombie'])

	def lose_iron_weapons(self):
		super(LadderZombie, self).lose_iron_weapons()
		self.speed = 1.0


class NewsPaperZombie(LineZombieBase):
	"""
	看报纸僵尸（二爷）
	"""

	def __init__(self, p=None):
		super(NewsPaperZombie, self).__init__(p)
		self.param_reinit()
		self.set_property(normal_conf.zombie_param_dict['news_paper'])
		self.zombie_hp_changed.connect(lambda hp: self.change_erye_status_gif(hp))

	def param_reinit(self):
		self.news_paper_is_dropped = False  # 报纸是否掉落

	def change_erye_status_gif(self, hp):
		"""
		更改僵尸状态gif
		:param hp:
		:return:
		"""

		def set_paper_drop():
			try:
				self.news_paper_is_dropped = True
				self.speed += 1.0  # 提速
				self.attack_frequency += 0.5  # 提攻速
				self.sound_effect_changed.emit("papaer_drop")
				self.normal_gif = ":images/zombies/NewspaperZombie/HeadWalk0.gif"
				self.pause_status = False
			except RuntimeError:
				pass

		if hp <= self.armor_health and self.news_paper_is_dropped is False:
			if not self.is_attacking:
				self.set_movie(":images/zombies/NewspaperZombie/LostNewspaper.gif")
				self.sound_effect_changed.emit("newspaper_rarrgh")
				self.pause_status = True
				QTimer.singleShot(1600, set_paper_drop)


class PoleVaultZombie(LineZombieBase):
	"""
	撑杆跳僵尸
	"""

	def __init__(self, p=None):
		super(PoleVaultZombie, self).__init__(p)
		self.param_reinit()
		self.set_property(normal_conf.zombie_param_dict['pole_vault'])

	def param_reinit(self):
		self.is_skipped = False  # 默认没有跳过
		self.is_skipping = False  # 是否正在跳

	def set_pole_vault_state(self):
		"""
		设置撑杆跳状态
		:return:
		"""

		def set_normal_pix():
			"""
			落地后去掉撑杆
			"""
			self.normal_gif = ":images/zombies/PoleVaultingZombie/PoleVaultingZombieWalk.gif"
			self.set_movie(self.normal_gif)

		def set_land():
			"""
			设置落地状态
			:return:
			"""
			try:
				self.set_zombie_pos(self.label_x, self.label_y)
				self.set_movie(":images/zombies/PoleVaultingZombie/PoleVaultingZombieJump2.gif")
				self.speed = 1.0  # 降低移动速度
				self.is_skipped = True
				QTimer.singleShot(150, set_normal_pix)  # 停留一秒后自动隐藏
			except:
				pass

		if self.is_skipping is True: return
		# 设置撑杆跳状态
		self.is_skipping = True
		self.sound_effect_changed.emit("jumping")
		self.set_movie(":images/zombies/PoleVaultingZombieJump.gif")
		self.col_index -= 1
		self.label_x -= 140  # 左侧位移
		QTimer.singleShot(400, set_land)  # 停留一秒后自动隐藏

	def show_zombie_attack(self, aim_item):
		if self.is_skipping is True and self.is_skipped is False: return
		super(PoleVaultZombie, self).show_zombie_attack(aim_item)


class SwimmingLineZombieBase(LineZombieBase):
	"""
	游泳直线僵尸基类
	"""

	def __init__(self, p=None):
		super(SwimmingLineZombieBase, self).__init__(p)
		self.param_reinit()

	def param_reinit(self):
		self.is_in_pool = False  # 是否处于游泳池里

	def set_property(self, data_item):
		super(SwimmingLineZombieBase, self).set_property(data_item)
		self.swimming_walk_pix = self.zombie_item['swimming_walk_pix']
		self.swimming_attack_pix = self.zombie_item['swimming_attack_pix']

	def slot_init(self):
		super(SwimmingLineZombieBase, self).slot_init()
		self.zombie_coord_changed.connect(lambda row_index, col_index: self.check_move_to_swimming())

	def check_move_to_swimming(self):
		"""
		移动到水池边 下水
		"""
		if self.col_index < normal_conf.max_grass_col and self.is_in_pool is False:
			self.normal_gif = self.swimming_walk_pix
			self.attack_pix = self.swimming_attack_pix
			self.is_in_pool = True
			self.sound_effect_changed.emit("jump_into_water")  # 僵尸进入水中
			self.set_movie(self.normal_gif)


class ImpZombie(LineZombieBase):
	"""
	小鬼僵尸
	"""

	def __init__(self, p=None):
		super(ImpZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['imp'])
		self.set_custom_size(75)
		self.death_point = 70


class CarZombieBase(LineZombieBase):
	"""
	开车的直线僵尸
	"""

	def __init__(self, p=None):
		super(CarZombieBase, self).__init__(p)
		self.is_car_zombie = True
		self.tire_explosion_pix = ""
		self.damage = 99999

	def set_tire_explosion_status(self):
		"""
		设置被地刺扎爆炸
		:return:
		"""
		self.set_movie(self.tire_explosion_pix)
		QTimer.singleShot(1850, self.die)  # 指定时间之后死亡


class DancerZombieBase(LineZombieBase):
	"""
	舞王僵尸
	"""
	dancing_start = pyqtSignal()
	partner_gen = pyqtSignal(list)

	def __init__(self, p=None):
		super(DancerZombieBase, self).__init__(p)

	def set_property(self, data_item):
		super(DancerZombieBase, self).set_property(data_item)
		self.dance_gap = self.zombie_item['dance_gap']
		self.dancing_pix = self.zombie_item['dancing_pix']
		self.call_partner_pix = self.zombie_item['call_partner_pix']
		self.death_point = 165  # 死亡点
		self.dancer_param_init()
		self.dancer_ui_init()
		self.dance_timer_init()

	def dancer_param_init(self):
		self.is_dancing = False  # 是否正在跳舞
		self.partner_dict = {"left": None, "right": None, "top": None, "bottom": None}  # 伴舞僵尸字典

	def dancer_ui_init(self):
		self.dancerLightItem = DancerLightItem(self)
		self.dancerLightItem.setAlignment(Qt.AlignHCenter)
		self.dancerLightItem.setFixedSize(QSize(100, 220))
		self.dancerLightItem.move(QPoint(int((self.width_ - self.dancerLightItem.width()) / 2),
										 40))
		self.dancerLightItem.setVisible(False)

	def dance_timer_init(self):
		self.dance_timer = QTimer(self)
		self.dance_timer.setInterval(self.dance_gap * 1000)
		self.dance_timer.timeout.connect(self.take_dance)
		self.dance_timer.start()

	def take_dance(self):
		"""
		跳舞召唤同伴
		自己跳舞 根据当前位置召唤同伴出场
		"""
		try:
			if self.is_dancing is True or self.label_x > self.parent().width() - normal_conf.noswimming_grass_width * 2:
				return
		except:
			pass
		self.is_dancing = True

		def do_dancing():
			try:
				self.set_movie(self.dancing_pix)  # 进行跳舞
				self.gen_partner()
				self.speed = 0.8  # 跳舞结束把速度降下来
				self.is_dancing = False
				self.dance_timer.stop()  # 以后就不跳舞了
				try:
					QTimer.singleShot(2500, lambda: self.set_movie(self.normal_gif))
					self.dancerLightItem.setVisible(False)
				except RuntimeError:
					pass
			except RuntimeError:
				pass

		try:
			self.dancing_start.emit()
			self.set_movie(self.call_partner_pix)  # 召唤同伴
			self.dancerLightItem.setVisible(True)
			self.dancerLightItem.raise_()
			QTimer.singleShot(1200, do_dancing)
		except RuntimeError:
			pass

	def gen_partner(self):
		"""
		根据舞王所在的行数和位置生成上下左右的僵尸
		"""
		try:
			is_swimming = self.parent().is_swimming_map
			max_lines = 6 if is_swimming else 5  # 根据地图类型判断最大行数
			line = self.row_index
			position_x = self.label_x
			zombie_pos_list = []
			zombie_pos_list.append([position_x - self.width_, line])
			zombie_pos_list.append([position_x + self.width_, line])
			if line > 0:
				zombie_pos_list.append([position_x, line - 1])
			if line < max_lines - 1:
				zombie_pos_list.append([position_x, line + 1])
			self.partner_gen.emit(zombie_pos_list)
		except:
			pass

	def zombie_move(self):
		if self.is_dancing is True: return
		super(DancerZombieBase, self).zombie_move()


class DacnerPartnerZombie(LineZombieBase):
	"""
	舞王伴舞僵尸
	"""

	def __init__(self, p=None):
		super(DacnerPartnerZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['dancer_partner'])


class DiscoPartnerZombie(LineZombieBase):
	"""
	disco伴舞僵尸
	"""

	def __init__(self, p=None):
		super(DiscoPartnerZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['disco_partner'])


class PogoZombie(LineZombieBase):
	"""
	跳跳僵尸
	"""

	def __init__(self, p=None):
		super(PogoZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['pogo_zombie'])
		self.death_point = 165

	def lose_iron_weapons(self):
		super(PogoZombie, self).lose_iron_weapons()
		self.speed = 1.2


class BalloonZombie(LineZombieBase):
	"""
	气球僵尸
	"""

	def __init__(self, p=None):
		super(BalloonZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['balloon_zombie'])
		self.balloon_init()

	def balloon_init(self):
		self.zombie_level = 2  # 天空
		self.balloon_boom = False  # 气球是否爆炸了

	def set_balloon_boom(self):
		"""
		气球爆炸 变成普通僵尸
		"""
		if self.balloon_boom is True: return
		self.normal_gif = ":images/zombies/Zombie_balloon/walk.gif"
		self.set_movie(self.normal_gif)
		self.balloon_boom = True
		self.zombie_level = 1  # 地面
		self.set_property(normal_conf.zombie_param_dict['regular'])
		self.sound_effect_changed.emit("balloon_pop")  # 气球爆炸


class DiggerZombie(LineZombieBase):
	"""
	矿工僵尸
	"""

	def __init__(self, p=None):
		super(DiggerZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['digger_zombie'])
		self.digger_init()

	def digger_init(self):
		self.zombie_level = 0  # 地底
		self.is_dig_out = False

	def digger_out_ground(self, lose_icron=False):
		"""
		矿工僵尸从地底主动出来
		"""
		self.zombie_level = 1
		if lose_icron is True:
			self.set_movie(":images/zombies/Zombie_digger/drill_nopickaxe.gif")
		else:
			self.set_movie(":images/zombies/Zombie_digger/drill.gif")
		self.set_pause_status(3)  # 僵直3秒
		self.normal_gif = ":images/zombies/Zombie_digger/walk_nopickaxe.gif"
		self.set_movie(self.normal_gif)
		self.speed = 1.2  # 减速
		if lose_icron is False:
			self.is_reversed = True  # 设为反向
		self.is_dig_out = True

	def lose_iron_weapons(self):
		"""
		矿工僵尸失去镐头 从地面出来
		"""
		self.digger_out_ground(True)  # 主动出土
		super(DiggerZombie, self).lose_iron_weapons()

	def zombie_move(self):
		if self.col_index == 0 and self.is_dig_out is False:
			self.digger_out_ground()  # 主动出土
		super(DiggerZombie, self).zombie_move()


class JokerZombie(LineZombieBase):
	"""
	小丑僵尸
	"""

	def __init__(self, p=None):
		super(JokerZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['joker_zombie'])
		self.box_state_init()
		self.death_point = 165

	def box_state_init(self):
		self.box_is_open = False  # 盒子是否打开了
		self.effect_range = (2, 2, 2, 2)
		self.max_boom_probability = 10

	def boom_plants(self):
		"""
		消除指定范围的植物
		"""
		plant_set = self.parent().plant_set if hasattr(self.parent(), 'plant_set') else []
		plant_list = list(plant_set)
		zombie_coord = (self.row_index, self.col_index)
		for each_plant in plant_list:
			plant_coord = (each_plant.row_index, each_plant.col_index)
			if check_coordinate_in_range(zombie_coord, self.effect_range, plant_coord):
				each_plant.take_damage(9999, self)  # 清除范围内植物
		self.zombie_died.emit(self)

	def slot_init(self):
		super(JokerZombie, self).slot_init()
		self.zombie_coord_changed.connect(self.update_probability)

	def update_probability(self):
		"""
		更新爆炸概率

		"""
		if self.col_index > 8: return
		if random.randint(1, self.col_index) == 1:
			self.set_box_open()  # 打开盒子

	def set_box_open(self):
		"""
		盒子打开 造成伤害
		"""

		def set_boom():
			"""
			爆炸，造成伤害
			"""
			try:
				self.sound_effect_changed.emit("jack_surprise")
				self.set_movie(":images/zombies/JackinTheBoxZombie/Boom.gif")
				self.boom_plants()
				QTimer.singleShot(800, set_die)
			except RuntimeError:
				pass

		def set_die():
			"""
			小丑僵尸死亡
			"""
			self.die()

		if self.box_is_open is True: return
		self.box_is_open = True
		self.set_movie(":images/zombies/JackinTheBoxZombie/OpenBox.gif")
		QTimer.singleShot(500, set_boom)


class GargantuarBase(LineZombieBase):
	"""
	伽刚特尔基类
	"""

	def __init__(self, p=None):
		super(GargantuarBase, self).__init__(p)
		self.death_point = 0
		self.damage = 9999

	def show_zombie_attack(self, aim_item):
		super(GargantuarBase, self).show_zombie_attack(aim_item)
		self.sound_effect_changed.emit("gargantuar_thump")  # 打击音


class YetiZombie(LineZombieBase):
	"""
	雪人僵尸
	"""

	def __init__(self, p=None):
		super(YetiZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['zombie_yeti'])
		self.death_point = 449


class RegularSwimmingZombie(SwimmingLineZombieBase):
	"""
	普通游泳僵尸
	"""

	def __init__(self, p=None):
		super(RegularSwimmingZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['swimming'])


class DolphinRiderZombie(SwimmingLineZombieBase):
	"""
	海豚骑士
	"""

	def __init__(self, p=None):
		super(DolphinRiderZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['dolphin_rider'])
		self.death_point = 165
		self.set_custom_size(200, 200)

	def param_reinit(self):
		super(DolphinRiderZombie, self).param_reinit()
		self.is_skipped = False  # 默认没有跳过
		self.is_skipping = False  # 是否正在跳

	def set_pole_vault_state(self):
		"""
		设置撑杆跳状态
		:return:
		"""

		def set_normal_pix():
			"""
			落地后去掉海豚
			"""
			self.normal_gif = ":images/zombies/DolphinRiderZombie/Walk3.gif"
			self.set_movie(self.normal_gif)

		def set_land():
			"""
			设置落地状态
			:return:
			"""
			try:
				self.set_zombie_pos(self.label_x, self.label_y)
				self.set_movie(":images/zombies/DolphinRiderZombie/Jump2.gif")
				self.speed = 1.4  # 降低移动速度
				self.is_skipped = True
				QTimer.singleShot(150, set_normal_pix)  # 停留一秒后自动隐藏
			except:
				pass

		if self.is_skipping is True: return
		# 设置跳跃状态
		self.is_skipping = True
		self.sound_effect_changed.emit("dolphin_before_jumping")
		self.set_movie(":images/zombies/DolphinRiderZombie/Jump.gif")
		self.col_index -= 1
		self.label_x -= 140  # 左侧位移
		QTimer.singleShot(400, set_land)  # 停留一秒后自动隐藏

	def show_zombie_attack(self, aim_item):
		if self.is_skipping is True and self.is_skipped is False: return
		super(DolphinRiderZombie, self).show_zombie_attack(aim_item)


class BucketheadSwimmingZombie(SwimmingLineZombieBase):
	"""
	铁桶游泳僵尸
	"""

	def __init__(self, p=None):
		super(BucketheadSwimmingZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['swimming_buckethead'])

	def lose_iron_weapons(self):
		self.set_property(normal_conf.zombie_param_dict['swimming'])


class ConeheadSwimmingZombie(SwimmingLineZombieBase):
	"""
	路障游泳僵尸
	"""

	def __init__(self, p=None):
		super(ConeheadSwimmingZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['conehead_swimming'])


class DiveZombieBase(SwimmingLineZombieBase):
	"""
	直线潜水僵尸基类
	"""

	def __init__(self, p=None):
		super(DiveZombieBase, self).__init__(p)


class DiveZombie(DiveZombieBase):
	"""
	直线潜水僵尸基类
	"""

	def __init__(self, p=None):
		super(DiveZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['dive'])

	def check_move_to_swimming(self):
		super(DiveZombie, self).check_move_to_swimming()
		if self.is_in_pool:
			self.zombie_level = 0


class ZomboniZombie(CarZombieBase):
	"""
	雪橇车僵尸
	"""
	ice_gen_signal = pyqtSignal(tuple)  # 产生了冰

	def __init__(self, p=None):
		super(ZomboniZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['zomboni'])
		self.tire_explosion_pix = ":images/zombies/Zomboni/5.gif"
		self.death_point = 199

	def slot_init(self):
		super(ZomboniZombie, self).slot_init()
		self.zombie_coord_changed.connect(lambda row, col: self.change_zombie_speed())

	def set_tire_explosion_status(self):
		self.set_movie(":images/zombies/Zomboni/4.gif")
		QTimer.singleShot(1350, lambda: super(ZomboniZombie, self).set_tire_explosion_status())

	def zombie_move(self):
		super(ZomboniZombie, self).zombie_move()
		if self.col_index < 0: return
		if self.col_index < normal_conf.max_grass_col:
			self.ice_gen_signal.emit((self.row_index, self.col_index))

	def change_zombie_speed(self):
		"""
		当前列越小速度越慢
		"""
		self.speed -= 0.03


class CataPultZombie(CarZombieBase):
	"""
	投篮车僵尸
	"""
	basketball_gen = pyqtSignal()  # 开始攻击植物

	def __init__(self, p=None):
		super(CataPultZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['catapult'])
		self.gap = self.zombie_item['gap']
		self.basketball_count = self.zombie_item['basketball_count']  # 有20个篮球
		self.tire_explosion_pix = ":images/zombies/CataPult/bounce.gif"
		self.basketball_init()
		self.death_point = 199

	def basketball_init(self):
		self.basketball_timer = QTimer(self)
		self.basketball_timer.setInterval(self.gap * 1000)
		self.basketball_timer.timeout.connect(self.check_attack)
		self.can_move = True

	def slot_init(self):
		super(CataPultZombie, self).slot_init()
		self.zombie_coord_changed.connect(lambda row, col: self.check_zombie_move(col))

	def check_zombie_move(self, col):
		"""
		走到第一格判断一下
		"""
		aim_col = normal_conf.max_grass_col - 1
		if col == aim_col:
			self.basketball_timer.start()
			self.can_move = False
		elif col < aim_col:
			self.can_move = True
			self.basketball_timer.stop()

	def check_attack(self):
		"""
		检测目标植物
		"""
		plant_set = self.parent().plant_set if hasattr(self.parent(), 'plant_set') else []
		plant_list = list(plant_set)
		aim_plant = None
		for each_plant in plant_list:
			if each_plant.row_index == self.row_index and each_plant.plant_type == 0:  # 攻击植物
				aim_plant = each_plant
				break
		if aim_plant is None or self.basketball_count <= 0:  # 向前开动 进行碾压
			self.damage = 9999
			self.can_move = True
		else:  # 进行篮球攻击
			self.damage = 75
			self.basketball_gen.emit()
			self.basketball_count -= 1
			self.can_move = False

	def zombie_move(self):
		"""
		移动之后
		"""
		if self.can_move:
			super(CataPultZombie, self).zombie_move()


class DancerZombie(DancerZombieBase):
	"""
	舞王僵尸
	"""

	def __init__(self, p=None):
		super(DancerZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['dancer'])


class DiscoZombie(DancerZombieBase):
	"""
	disco僵尸
	"""

	def __init__(self, p=None):
		super(DiscoZombie, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['disco_zombie'])


class RedGargantuar(GargantuarBase):
	"""
	红眼伽刚特尔
	"""

	def __init__(self, p=None):
		super(RedGargantuar, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['red_gargantuar'])


class WhiteGargantuar(GargantuarBase):
	"""
	白眼伽刚特尔
	"""

	def __init__(self, p=None):
		super(WhiteGargantuar, self).__init__(p)
		self.set_property(normal_conf.zombie_param_dict['white_gargantuar'])


if __name__ == '__main__':
	QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
	QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
	QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
	app = QApplication(sys.argv)
	app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
	win = DancerZombie()
	win.show()
	sys.exit(app.exec_())
