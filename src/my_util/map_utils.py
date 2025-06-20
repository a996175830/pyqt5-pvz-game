import random



def get_random_zombie_id(zombie_id_list):
	"""
	获取随机僵尸索引
	:return: 僵尸索引
	"""
	return random.choice(zombie_id_list)


def get_random_line_index(from_index=0, to_index=4):
	"""
	获取随机一条线路
	:return: 线路索引
	"""
	return random.randint(from_index, to_index)


def get_random_swimming_line_index():
	"""
	获取随机一条线路
	:return: 线路索引
	"""
	return random.choice([2, 3])


def add_map_details(from_sec, to_sec, step=5, zombie_id_list=[], is_swimming_map=False):
	"""
	添加地图细节
	:param from_sec: 开始秒数
	:param to_sec: 结束秒数
	:return: 地图细节字典
	"""
	swimming_zombie_list = [9, 10, 11, 12, 27]  # 游泳僵尸列表
	detail_map = {}
	for i in range(from_sec, to_sec + 1, step):  # 注意这里使用 to_sec + 1 来确保包含 to_sec
		if is_swimming_map is True and random.randint(1,4)==1:
			if random.choice([1, 2]) == 1:  # 产生泳池僵尸
				detail_map[i] = [0, get_random_zombie_id([each_zombie_id for each_zombie_id in zombie_id_list if
														  each_zombie_id in set(swimming_zombie_list)]),
								 get_random_swimming_line_index()]
			else:
				detail_map[i] = [0, get_random_zombie_id([each_zombie_id for each_zombie_id in zombie_id_list if
														  each_zombie_id not in set(swimming_zombie_list)]), get_random_line_index()]
		else:
			detail_map[i] = [0, get_random_zombie_id(zombie_id_list), get_random_line_index()]
	return detail_map
