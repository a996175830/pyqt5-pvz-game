from copy import deepcopy
from src.config import normal_conf
from .game_map import pre_generate_map

base_plant_id_list = [1, 2, 3, 4, 5, 6]


class MapBase:

	def __init__(self):
		self.param_init()

	def param_init(self):
		self.can_selected_plant_id_list = base_plant_id_list  # 支持选择的植物
		self.zombie_id_list = []  # 会出现的僵尸
		self.map_dict = dict()  # 地图内容
		self.game_time = 260  # 游戏时长
		self.base_sunshine = 100  # 游戏初始阳光值
		self.game_mode = "正常模式"  # 游戏模式

	def set_property(self, map_item):
		self.map_id = map_item['id']
		self.bgm = map_item['bgm']
		self.bg_pic = map_item['bg_pic']
		self.name = map_item['name']
		self.zombie_id_list = map_item['zombie_id_list']
		self.is_swimming_map = map_item['is_swimming_map']
		self.prepare_bg_pic = map_item['prepare_bg_pic']
		self.line_count = map_item['line_count']
		self.get_map_dict()

	def get_map_dict(self):
		"""
		生成随机地图，确保5和6在pre_zombie_id_list中移除，但6在final_zombie_id_list中保留且final_zombie_id_list只移除5。
		:return: None，但会更新self.map_dict
		"""
		self.map_dict = pre_generate_map(self.zombie_id_list, is_swimming_map=self.is_swimming_map)


class DayTimeMap(MapBase):
	"""
	白天地图
	"""

	def __init__(self):
		super(DayTimeMap, self).__init__()
		self.set_property(normal_conf.map_dict['day_time'])


class NightMap(MapBase):
	"""
	夜晚地图
	"""

	def __init__(self):
		super(NightMap, self).__init__()
		self.set_property(normal_conf.map_dict['night'])


class SwimmingMap(MapBase):
	"""
	泳池地图
	"""

	def __init__(self):
		super(SwimmingMap, self).__init__()
		self.set_property(normal_conf.map_dict['swimming'])


class NightSwimmingMap(MapBase):
	"""
	夜晚泳池
	"""

	def __init__(self):
		super(NightSwimmingMap, self).__init__()
		self.set_property(normal_conf.map_dict['night_swimming'])
