from src.my_util.map_utils import get_random_line_index, add_map_details


def generate_map(zombie_id_list, game_all_time=300, is_swimming_map=False):
	"""
	生成地图
	:param game_all_time: 输入的整数
	:return: 生成的地图字典
	# 0一般进度 1开始出现僵尸 2中间结点 3最后一波（这里假设您只是想要表示游戏状态，而不是实际僵尸索引）
	"""
	map_data = {}
	map_data[10] = [1, 4, get_random_line_index()]
	half_value = game_all_time // 2
	detail1 = add_map_details(11, half_value, zombie_id_list=zombie_id_list, is_swimming_map=is_swimming_map)
	map_data.update(detail1)
	map_data[half_value - 1] = [2, 4, get_random_line_index()]
	detail2 = add_map_details(half_value + 2, game_all_time, zombie_id_list=zombie_id_list,
							  is_swimming_map=is_swimming_map)
	map_data.update(detail2)
	map_data[game_all_time + 1] = [3, 4, get_random_line_index()]
	return map_data


def pre_generate_map(zombie_id_list, game_all_time=300, is_swimming_map=False):
	return generate_map(zombie_id_list, game_all_time=game_all_time, is_swimming_map=is_swimming_map)


if __name__ == '__main__':
	print(pre_generate_map([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], ))
