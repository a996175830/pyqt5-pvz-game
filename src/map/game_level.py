"""
游戏关卡
"""

daytime = ":images/map/level/1.png"
night = ":images/map/level/2.png"
swimming_pool = ":images/map/level/3.png"
night_swimming = ":images/map/level/4.png"
daytime_list = [{"map_id": 1, "level": i, "pic": daytime, "text": "冒险模式第{}关".format(i)} for i in range(1, 6)]
night_list = [{"map_id": 2, "level": i, "pic": night, "text": "冒险模式第{}关".format(i)} for i in range(6, 11)]
swimming_pool_list = [{"map_id": 3, "level": i, "pic": swimming_pool, "text": "冒险模式第{}关".format(i)} for i in
					  range(11, 16)]
night_swimming_list = [{"map_id": 4, "level": i, "pic": night_swimming, "text": "冒险模式第{}关".format(i)} for i in
					   range(16, 21)]
level_list = daytime_list + night_list + swimming_pool_list + night_swimming_list
