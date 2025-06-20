grass_singular = ":grass/grass0.png"
grass_even_numbers = ":grass/grass1.png"
game_lose_x_offset = -40
max_grass_col = 9  # 最多9列
noswimming_grass_width = 103
noswimming_grass_height = 113
swimming_grass_width = 113
plant_param_dict = {
	"sun_flower": {
		"id": 1,
		"name": "sun_flower",
		"cn_name": "向日葵",
		"card_pix": ":images/cards/card_sf.png",
		"put_pix": ":images/plants/SunFlower/SunFlower1.gif",
		"cursor_pix": ":images/plants/SunFlower/SunFlower1_static.png",
		"cost": 50,
		"damage": 0,
		"hp": 150,
		"cooling": 1,
		"gap": 8,
		"sun_production": 25,
		"map_id": 1,  # 所在地图id
		"desc": "产生阳光，经济实惠"
	},
	"pea": {
		"id": 2,
		"name": "pea",
		"cn_name": "豌豆射手",
		"card_pix": ":images/cards/card_pea.png",
		"put_pix": ":images/plants/Peashooter/Peashooter.gif",
		"cursor_pix": ":images/plants/Peashooter/Peashooter_static.png",
		"cost": 100,
		"damage": 20,
		"moderate": 0.0,
		"hp": 300,
		"attack_gap": 1.75,
		"cooling": 7.5,
		"map_id": 1,  # 所在地图id
		"desc": "发射豌豆，击退敌人"
	},
	"nut": {
		"id": 3,
		"name": "nut",
		"cn_name": "坚果墙",
		"card_pix": ":images/cards/card_wallnut.png",
		"put_pix": ":images/plants/WallNut/WallNut.gif",
		"put_pix2": ":images/plants/WallNut/Wallnut_cracked1.gif",
		"put_pix3": ":images/plants/WallNut/Wallnut_cracked2.gif",
		"cursor_pix": ":images/plants/WallNut/WallNut_static.png",
		"cost": 50,
		"damage": 0,
		"moderate": 0.0,
		"hp": 4000,
		"cooling": 30,
		"map_id": 1,  # 所在地图id
		"desc": "高耐久墙壁，抵挡敌人"
	},
	"ice_pea": {
		"id": 4,
		"name": "ice_pea",
		"cn_name": "寒冰豌豆射手",
		"card_pix": ":images/cards/card_snowpea.png",
		"put_pix": ":images/plants/SnowPea/SnowPea.gif",
		"cursor_pix": ":images/plants/SnowPea/SnowPea_static.png",
		"cost": 175,
		"damage": 20,
		"moderate": 0.3,
		"hp": 250,
		"cooling": 7.5,
		"attack_gap": 1.75,
		"map_id": 1,  # 所在地图id
		"desc": "发射冰冻豌豆，减速敌人"
	},
	"cherry_boom": {
		"id": 5,
		"name": "cherry_boom",
		"cn_name": "樱桃炸弹",
		"card_pix": ":images/cards/card_cherry.png",
		"put_pix": ":images/plants/CherryBomb/CherryBomb.gif",
		"cursor_pix": ":images/plants/CherryBomb/CherryBomb_static.png",
		"cost": 150,
		"damage": 1800,
		"moderate": 0.0,
		"hp": 300,
		"cooling": 50,
		"attack_gap": 0,
		"map_id": 1,  # 所在地图id
		"range_effect": (1, 1, 1, 1),
		"desc": "爆炸范围伤害，毁灭敌人"
	},
	"repeater_pea": {
		"id": 6,
		"name": "repeater_pea",
		"cn_name": "双发豌豆射手",
		"card_pix": ":images/cards/card_repeaterpea.png",
		"put_pix": ":images/plants/Repeater/Repeater.gif",
		"cursor_pix": ":images/plants/Repeater/Repeater_static.png",
		"cost": 200,
		"damage": 20,
		"moderate": 0.0,
		"hp": 250,
		"attack_gap": 1.75,
		"cooling": 7.5,
		"map_id": 1,  # 所在地图id
		"desc": "双发射击，攻击更强"
	},
	"jalapeno": {
		"id": 7,
		"name": "jalapeno",
		"cn_name": "火爆辣椒",
		"card_pix": ":images/cards/card_jalapeno.png",
		"put_pix": ":images/plants/Jalapeno/Jalapeno.gif",
		"cursor_pix": ":images/plants/Jalapeno/Jalapeno_static.png",
		"cost": 125,
		"damage": 1800,
		"moderate": 0.0,
		"hp": 200,
		"cooling": 50,
		"attack_gap": 0,
		"map_id": 1,  # 所在地图id
		"range_effect": (20, 0, 20, 1),
		"desc": "强力爆炸，清理路径"
	},
	"pumpkin": {
		"id": 8,
		"name": "pumpkin",
		"cn_name": "倭瓜",
		"card_pix": ":images/cards/card_pumpkin.png",
		"put_pix": ":images/plants/Squash/Squash_static.png",
		"cursor_pix": ":images/plants/Squash/Squash_static.png",
		"cost": 50,
		"damage": 1800,
		"moderate": 0.0,
		"hp": 200,
		"cooling": 30,
		"attack_gap": 0,
		"map_id": 1,  # 所在地图id
		"range_effect": (1, 0, 0, 0),
		"desc": "强力防御，耐打击"
	},
	"little_sprout_mushroom": {
		"id": 9,
		"name": "little_sprout_mushroom",
		"cn_name": "小喷菇",
		"card_pix": ":images/cards/card_puffshroom.png",
		"put_pix": ":images/plants/PuffShroom/PuffShroom.gif",
		"sleep_pix": ":images/plants/PuffShroom/PuffShroomSleep.gif",
		"cursor_pix": ":images/plants/PuffShroom/PuffShroom_static.png",
		"cost": 0,
		"damage": 20,
		"moderate": 0.0,
		"hp": 300,
		"cooling": 7.5,
		"map_id": 2,  # 所在地图id
		"attack_gap": 2.0,
		"desc": "低成本，持续喷射"
	},
	"macadamia_nut": {
		"id": 10,
		"name": "macadamia_nut",
		"cn_name": "高坚果",
		"card_pix": ":images/cards/card_macadamia_nut.png",
		"put_pix": ":images/plants/TallNut/TallNut.gif",
		"put_pix2": ":images/plants/TallNut/TallnutCracked1.gif",
		"put_pix3": ":images/plants/TallNut/TallnutCracked2.gif",
		"cursor_pix": ":images/plants/TallNut/TallnutCracked_static.png",
		"cost": 125,
		"damage": 0,
		"moderate": 0.0,
		"hp": 8000,
		"cooling": 30,
		"map_id": 1,  # 所在地图id
		"desc": "超级坚固防御"
	},
	"sun_mushroom": {
		"id": 11,
		"name": "sun_mushroom",
		"cn_name": "阳光菇",
		"card_pix": ":images/cards/card_sun_mushroom.png",
		"put_pix": ":images/plants/SunShroom/SunShroom2.gif",
		"pro_pix": ":images/plants/SunShroom/SunShroom.gif",
		"cursor_pix": ":images/plants/SunShroom/SunShroom_static.png",
		"sleep_pix": ":images/plants/SunShroom/SunShroomSleep.gif",
		"cost": 25,
		"damage": 0,
		"hp": 150,
		"cooling": 7.5,
		"gap": 8,
		"sun_production": 15,
		"sun_production_grow": 25,
		"grow_gap": 30,
		"map_id": 2,  # 所在地图id
		"desc": "逐步产生阳光"
	},
	"potato_mine": {
		"id": 12,
		"name": "potato_mine",
		"cn_name": "土豆地雷",
		"card_pix": ":images/cards/card_potato_mine.png",
		"put_pix": ":images/plants/PotatoMine/PotatoMineNotReady.gif",
		"cursor_pix": ":images/plants/PotatoMine/PotatoMine_static.png",
		"cost": 25,
		"damage": 9999,
		"moderate": 0.0,
		"hp": 200,
		"cooling": 30,
		"attack_gap": 0,
		"map_id": 1,  # 所在地图id
		"range_effect": (0, 0, 0, 0),
		"arming_time": 5,
		"desc": "地雷引爆，重创敌人"
	},
	"fear_mushroom": {
		"id": 13,
		"name": "fear_mushroom",
		"cn_name": "胆小菇",
		"card_pix": ":images/cards/card_fear_mushroom.png",
		"put_pix": ":images/plants/ScaredyShroom/ScaredyShroom.gif",
		"sleep_pix": ":images/plants/ScaredyShroom/ScaredyShroomSleep.gif",
		"cursor_pix": ":images/plants/ScaredyShroom/ScaredyShroom_static.png",
		"cost": 25,
		"damage": 20,
		"moderate": 0.0,
		"hp": 300,
		"cooling": 7.5,
		"attack_gap": 2.0,
		"map_id": 2,  # 所在地图id
		"desc": "范围小，吓退敌人"
	},
	"chomper": {
		"id": 14,  # 食人花
		"name": "chomper",
		"cn_name": "食人花",
		"card_pix": ":images/cards/card_chomper.png",
		"put_pix": ":images/plants/Chomper/Chomper.gif",
		"cursor_pix": ":images/plants/Chomper/Chomper_static.png",
		"cost": 125,
		"damage": 2000,
		"moderate": 0.0,
		"hp": 300,
		"cooling": 7.5,
		"attack_gap": 0,
		"map_id": 1,  # 所在地图id
		"range_effect": (0, 0, 1, 0),
		"digestion_time": 42,  # 消化时间
		"desc": "吞噬敌人，强力进攻",
	}, "lurker": {
		"id": 15,  # 地刺
		"name": "lurker",
		"cn_name": "地刺",
		"card_pix": ":images/cards/card_lurker.png",
		"put_pix": ":images/plants/Spikeweed/Spikeweed.gif",
		"cursor_pix": ":images/plants/Spikeweed/Spikeweed_static.png",
		"cost": 100,
		"damage": 25,
		"moderate": 0.0,
		"hp": 300,
		"cooling": 7.5,
		"map_id": 1,  # 所在地图id
		"attack_gap": 1.0,  # 攻击间隔
		"range_effect": (0, 0, 0, 0),
		"desc": "荆棘防御，穿透杀伤",

	}, "frost_mushroom": {
		"id": 16,  # 冰霜蘑菇
		"name": "frost_mushroom",
		"cn_name": "冰霜蘑菇",
		"card_pix": ":images/cards/card_frost_mushroom.png",
		"put_pix": ":images/plants/IceShroom/IceShroom.gif",
		"cursor_pix": ":images/plants/IceShroom/IceShroom_static.png",
		"sleep_pix": ":images/plants/IceShroom/IceShroomSleep.gif",
		"cost": 75,
		"damage": 20,
		"moderate": 0.3,  # 减速
		"moderate_duration": 15,  # 减速
		"hp": 300,
		"cooling": 50,  # 7.5
		"attack_gap": 0,  # 攻击间隔
		"range_effect": (99, 99, 99, 99),  # 全屏攻击
		"prepare_time": 1,  # 准备时间
		"pause_duration": 5,  # 暂停僵尸持续时间
		"map_id": 2,  # 所在地图id
		"desc": "全屏冰冻",
	}, "cactus": {
		"id": 18,  # 仙人掌
		"name": "cactus",
		"cn_name": "仙人掌",
		"card_pix": ":images/cards/card_cactus.png",
		"put_pix": ":images/plants/Cactus/Cactus.gif",
		"cursor_pix": ":images/plants/Cactus/Cactus_static.png",
		"cost": 125,
		"damage": 20,
		"moderate": 0.3,  # 减速
		"moderate_duration": 15,  # 减速
		"hp": 550,
		"cooling": 7.5,  # 7.5
		"attack_gap": 1.75,  # 攻击间隔
		"map_id": 1,  # 所在地图id
		"desc": "中等伤害防御。",
	},
	"watermelon": {
		"id": 19,  # 西瓜投手
		"name": "watermelon",
		"cn_name": "西瓜投手",
		"card_pix": ":images/cards/card_watermelon.png",
		"put_pix": ":images/plants/WaterMelon/watermelon1.gif",
		"cursor_pix": ":images/plants/WaterMelon/watermelon_static.png",
		"cost": 300,
		"damage": 80,
		"moderate": 0.0,  # 减速
		"moderate_duration": 0,  # 减速时长
		"hp": 300,
		"cooling": 7.5,
		"effect_key": "melon_pact",
		"attack_gap": 2.9,  # 攻击间隔
		"desc": "投掷西瓜造成高伤害",
		"map_id": 1,  # 所在地图id
	}, "sea_shroom": {
		"id": 20,
		"name": "sea_shroom",
		"cn_name": "海蘑菇",
		"card_pix": ":images/cards/card_seaShroom.png",
		"put_pix": ":images/plants/SeaShroom/SeaShroom.gif",
		"cursor_pix": ":images/plants/SeaShroom/SeaShroom_static.png",
		"sleep_pix": ":images/plants/SeaShroom/SeaShroomSleep.gif",
		"cost": 0,
		"damage": 20,
		"moderate": 0.0,
		"hp": 300,
		"cooling": 30,
		"attack_gap": 2.0,
		"map_id": 3,  # 所在地图id
		"desc": "零成本的近战攻击植物，适合夜间作战"
	}, "tangle_kelp": {
		"id": 21,
		"name": "tangle_kelp",
		"cn_name": "缠绕水藻",
		"card_pix": ":images/cards/card_tangleklep.png",
		"put_pix": ":images/plants/TangleKlep/Float.gif",
		"cursor_pix": ":images/plants/TangleKlep/TangleKlep_static.png",
		"cost": 25,
		"damage": 99999,
		"moderate": 0.0,
		"hp": 300,
		"cooling": 30,
		"map_id": 3,  # 所在地图id
		"attack_gap": 2.0,
		"range_effect": (0, 0, 1, 0),
		"desc": "一击必杀的水生植物，能立即拖走一个敌人"
	}, "doom_shroom": {
		"id": 22,
		"name": "doom_shroom",
		"cn_name": "毁灭菇",
		"card_pix": ":images/cards/card_doomshroom.png",
		"put_pix": ":images/plants/DoomShroom/BeginBoom.gif",
		"cursor_pix": ":images/plants/DoomShroom/BeginBoom_static.png",
		"sleep_pix": ":images/plants/DoomShroom/Sleep.gif",
		"cost": 125,
		"map_id": 2,  # 所在地图id
		"damage": 99999,
		"moderate": 0.0,
		"hp": 300,
		"cooling": 50,
		"attack_gap": 2.0,
		"range_effect": (2, 3, 2, 3),
		"desc": "大范围的毁灭性爆炸，但会留下不宜种植的区域"
	},
	"cron_pult": {
		"id": 23,  # 玉米投手
		"name": "cron_pult",
		"cn_name": "玉米投手",
		"card_pix": ":images/cards/card_cron_pult.png",
		"put_pix": ":images/plants/Cornpult/full_idle.gif",
		"cursor_pix": ":images/plants/Cornpult/full_idle_static.png",
		"cost": 100,
		"damage": 20,
		"moderate": 0.0,  # 减速
		"moderate_duration": 0,  # 减速时长
		"hp": 300,
		"cooling": 7.5,
		"map_id": 1,  # 所在地图id
		"effect_key": "hit",
		"attack_gap": 1.9,  # 攻击间隔
		"desc": "投掷玉米或黄油",
	},
	"cabbage": {
		"id": 24,  # 卷心菜投手
		"name": "cabbage",
		"cn_name": "卷心菜投手",
		"card_pix": ":images/cards/card_cabbage.png",
		"put_pix": ":images/plants/Cabbagepult/idle.gif",
		"cursor_pix": ":images/plants/Cabbagepult/cabbage_static.png",
		"cost": 100,
		"damage": 60,
		"moderate": 0.0,  # 减速
		"moderate_duration": 0,  # 减速时长
		"hp": 300,
		"cooling": 7.5,
		"effect_key": "hit",
		"map_id": 1,  # 所在地图id
		"attack_gap": 1.9,  # 攻击间隔
		"desc": "投掷卷心菜",
	},
	"cat_tail": {
		"id": 25,  # 香蒲
		"name": "cat_tail",
		"cn_name": "香蒲",
		"card_pix": ":images/cards/card_cattail_grass.png",
		"put_pix": ":images/plants/Cattail/idle.gif",
		"cursor_pix": ":images/plants/Cattail/CatTail_static.png",
		"cost": 225,
		"damage": 20,
		"moderate": 0.0,  # 减速
		"map_id": 3,  # 所在地图id
		"moderate_duration": 0,  # 减速时长
		"hp": 300,
		"cooling": 1,
		"effect_key": "hit",
		"attack_gap": 1.7,  # 攻击间隔
		"desc": "发射追踪香蒲，优先攻击当前行",
	},
	"torchwood": {
		"id": 26,  # 火炬树桩
		"name": "torchwood",
		"cn_name": "火炬树桩",
		"card_pix": ":images/cards/card_torchwood.png",
		"put_pix": ":images/plants/Torchwood/Torchwood.gif",
		"cursor_pix": ":images/plants/Torchwood/Torchwood_static.png",
		"cost": 175,
		"damage": 0,
		"moderate": 0.0,  # 减速
		"moderate_duration": 0,  # 减速时长
		"hp": 300,
		"cooling": 7.5,
		"map_id": 1,  # 所在地图id
		"effect_key": "fire_pea",
		"attack_gap": 0,  # 攻击间隔
		"desc": "增强豌豆火力，遇寒冰失效",
	}, "three_pea": {
		"id": 27,
		"name": "three_pea",
		"cn_name": "三线射手",
		"card_pix": ":images/cards/card_threepeashooter.png",
		"put_pix": ":images/plants/Threepeater/Threepeater.gif",
		"cursor_pix": ":images/plants/Threepeater/three_pea_static.png",
		"cost": 325,
		"damage": 20,
		"moderate": 0.0,
		"hp": 300,
		"map_id": 1,  # 所在地图id
		"attack_gap": 1.75,
		"cooling": 7.5,
		"desc": "发射豌豆，击退敌人"
	}, "hypno_shroom": {
		"id": 28,
		"name": "hypno_shroom",
		"cn_name": "魅惑蘑菇",
		"card_pix": ":images/cards/card_hypnoshroom.png",
		"put_pix": ":images/plants/HypnoShroom/HypnoShroom.gif",
		"cursor_pix": ":images/plants/HypnoShroom/HypnoShroom_static.png",
		"sleep_pix": ":images/plants/HypnoShroom/HypnoShroomSleep.gif",
		"cost": 75,
		"damage": 0,
		"moderate": 0.0,
		"hp": 300,
		"map_id": 2,  # 所在地图id
		"attack_gap": 0,
		"cooling": 7.5,
		"desc": "发射豌豆，击退敌人"
	}, "magnet_shroom": {
		"id": 29,
		"name": "magnet_shroom",
		"cn_name": "磁力菇",
		"card_pix": ":images/cards/card_magnet_shroom.png",
		"put_pix": ":images/plants/MagnetShroom/idle.gif",
		"cursor_pix": ":images/plants/MagnetShroom/MagnetShroom_static.png",
		"cost": 100,
		"damage": 0,
		"hp": 300,
		"map_id": 1,  # 所在地图id
		"cooling": 7.5,
		"range_effect": (2, 2, 2, 2),
		"gap": 15,
		"desc": "吸取单体僵尸铁制饰物"
	}, "split_pea": {
		"id": 30,
		"name": "pea",
		"cn_name": "裂荚射手",
		"map_id": 1,  # 所在地图id
		"card_pix": ":images/cards/card_SplitPea.png",
		"put_pix": ":images/plants/SplitPea/SplitPea.gif",
		"cursor_pix": ":images/plants/SplitPea/SplitPea_static.png",
		"cost": 125,
		"damage": 20,
		"moderate": 0.0,
		"hp": 300,
		"attack_gap": 1.75,
		"cooling": 7.5,
		"desc": "同时向两个方向发射豌豆"
	}, "marigold": {
		"id": 31,
		"name": "marigold",
		"cn_name": "金盏花",
		"map_id": 1,  # 所在地图id
		"card_pix": ":images/cards/card_marigold.png",
		"put_pix": ":images/plants/Marigold/idle.gif",
		"cursor_pix": ":images/plants/Marigold/idle_static.png",
		"cost": 100,
		"damage": 0,
		"hp": 300,
		"cooling": 30,
		"gap": 3,
		"desc": "产生金币或银币"
	}, "twin_sun_flower": {
		"id": 32,
		"name": "twin_sun_flower",
		"cn_name": "双子向日葵",
		"map_id": 1,  # 所在地图id
		"card_pix": ":images/cards/card_twine_sf.png",
		"put_pix": ":images/plants/TwinSunflower/TwinSunflower1.gif",
		"cursor_pix": ":images/plants/TwinSunflower/TwinSunflower_static.png",
		"cost": 150,
		"damage": 0,
		"hp": 300,
		"cooling": 50,
		"gap": 8,
		"sun_production": 100,
		"desc": "产生阳光，经济实惠"
	}, "garlic": {
		"id": 33,
		"name": "garlic",
		"cn_name": "大蒜",
		"map_id": 1,  # 所在地图id
		"card_pix": ":images/cards/card_garlic.png",
		"put_pix": ":images/plants/Garlic/Garlic.gif",
		"put_pix2": ":images/plants/Garlic/Garlic_body2.gif",
		"put_pix3": ":images/plants/Garlic/Garlic_body3.gif",
		"cursor_pix": ":images/plants/Garlic/Garlic_static.png",
		"cost": 50,
		"damage": 0,
		"moderate": 0.0,
		"hp": 400,
		"cooling": 7.5,
		"desc": "高耐久墙壁，抵挡敌人"
	}, "gatling_pea": {
		"id": 34,
		"name": "gatling_pea",
		"cn_name": "机枪射手",
		"map_id": 1,  # 所在地图id
		"card_pix": ":images/cards/card_gatling_pea.png",
		"put_pix": ":images/plants/GatlingPea/GatlingPea.gif",
		"cursor_pix": ":images/plants/GatlingPea/idle_static.png",
		"cost": 250,
		"damage": 20,
		"moderate": 0.0,
		"hp": 300,
		"attack_gap": 1.75,
		"cooling": 50,
		"for_upgrade": True,  # 用作给其他植物提升
		"for_upgrade_id": 6,  # 用作提升的植物id
		"desc": "配合双发射手，每次发射四发豌豆"
	}, "winter_melon": {
		"id": 35,  # 冰西瓜投手
		"name": "winter_melon",
		"cn_name": "冰西瓜投手",
		"map_id": 1,  # 所在地图id
		"card_pix": ":images/cards/card_winter_melon.png",
		"put_pix": ":images/plants/WinterMelon/idle.gif",
		"cursor_pix": ":images/plants/WinterMelon/idle_static.png",
		"cost": 300,
		"damage": 80,
		"for_upgrade": True,  # 用作给其他植物提升
		"for_upgrade_id": 19,  # 用作提升的植物id
		"hp": 300,
		"cooling": 50,
		"effect_key": "melon_pact",
		"attack_gap": 2.9,  # 攻击间隔
		"desc": "投掷冰西瓜造成高伤害附带减速",
	}, "spiker_rock":
		{
			"id": 36,  # 地刺王
			"name": "spiker_rock",
			"cn_name": "地刺王",
			"map_id": 1,  # 所在地图id
			"card_pix": ":images/cards/card_spikerock.png",
			"put_pix": ":images/plants/Spikerock/Spikerock.gif",
			"cursor_pix": ":images/plants/Spikerock/idle_static.png",
			"cost": 125,
			"damage": 25,
			"moderate": 0.0,
			"hp": 450,
			"cooling": 50,
			"for_upgrade": True,  # 用作给其他植物提升
			"for_upgrade_id": 15,  # 用作给其他植物提升id
			"attack_gap": 1.0,  # 攻击间隔
			"range_effect": (0, 0, 0, 0),
			"desc": "荆棘防御，穿透杀伤",
		}, "coffee_bean": {
		"id": 37,  # 咖啡豆
		"name": "coffee_bean",
		"cn_name": "咖啡豆",
		"map_id": 1,  # 所在地图id
		"card_pix": ":images/cards/card_coffeebean.png",
		"put_pix": ":images/plants/CoffeeBean/CoffeeBeanEat.gif",
		"cursor_pix": ":images/plants/CoffeeBean/CoffeeBean_static.png",
		"cost": 75,
		"damage": 0,
		"moderate": 0.0,  # 减速
		"moderate_duration": 0,  # 减速时长
		"wake_up_duration": 1.7,  # 减速时长
		"hp": 300,
		"cooling": 7.5,
		"effect_key": "fire_pea",
		"attack_gap": 0,  # 攻击间隔
		"desc": "唤醒一株睡觉的植物",
	}, "fume_shroom": {
		"id": 38,
		"name": "fume_shroom",
		"cn_name": "大喷菇",
		"map_id": 2,  # 所在地图id
		"card_pix": ":images/cards/card_fumeshroom.png",
		"put_pix": ":images/plants/FumeShroom/FumeShroom.gif",
		"cursor_pix": ":images/plants/FumeShroom/FumeShroom_static.png",
		"sleep_pix": ":images/plants/FumeShroom/FumeShroomSleep.gif",  # 白天睡觉
		"cost": 75,
		"damage": 20,
		"moderate": 0.0,
		"hp": 300,
		"cooling": 7.5,
		"attack_gap": 2.0,
		"desc": "持续喷射"
	}, "grave_buster": {
		"id": 39,  # 墓碑吞噬者
		"name": "grave_buster",
		"cn_name": "墓碑吞噬者",
		"map_id": 2,  # 所在地图id
		"card_pix": ":images/cards/card_gravebuster.png",
		"put_pix": ":images/plants/GraveBuster/GraveBuster.gif",
		"cursor_pix": ":images/plants/GraveBuster/idle_static.png",
		"cost": 75,
		"damage": 0,
		"moderate": 0.0,  # 减速
		"moderate_duration": 0,  # 减速时长
		"buster_duration": 4.5,  # 吞噬时长
		"hp": 300,
		"cooling": 7.5,
		"effect_key": "",
		"attack_gap": 0,  # 攻击间隔
		"desc": "移除墓碑",
	}, "gold_magnet": {
		"id": 40,
		"name": "gold_magnet",
		"cn_name": "吸金磁",
		"card_pix": ":images/cards/card_gold_magnet.png",
		"put_pix": ":images/plants/GoldMagnet/idle.gif",
		"cursor_pix": ":images/plants/GoldMagnet/idle_static.png",
		"cost": 50,
		"damage": 0,
		"hp": 300,
		"cooling": 50,
		"map_id": 1,  # 所在地图id
		"for_upgrade": True,  # 用作给其他植物提升
		"for_upgrade_id": 29,  # 用作提升的id
		"gap": 6,
		"desc": "吸取全屏幕的钱币"
	}, "flower_pot": {
		"id": 41,
		"name": "flower_pot",
		"cn_name": "花盆",
		"map_id": 5,  # 所在地图id
		"card_pix": ":images/cards/card_flower_pot.png",
		"put_pix": ":images/plants/FlowerPot/idle.gif",
		"cursor_pix": ":images/plants/FlowerPot/FlowerPot_static.png",
		"cost": 25,
		"damage": 0,
		"hp": 300,
		"cooling": 7.5,
		"desc": "吸取全屏幕的钱币"
	}, "lily_pad": {
		"id": 42,
		"name": "lily_pad",
		"cn_name": "荷叶",
		"map_id": 3,  # 所在地图id
		"card_pix": ":images/cards/card_lilypad.png",
		"put_pix": ":images/plants/LilyPad/idle.gif",
		"cursor_pix": ":images/plants/LilyPad/LilyPad_static.png",
		"cost": 25,
		"damage": 0,
		"hp": 300,
		"cooling": 7.5,
		"desc": "栽种在水面上，可种其他植物"
	}, "blover": {
		"id": 43,
		"name": "blover",
		"cn_name": "三叶草",
		"card_pix": ":images/cards/card_clover.png",
		"put_pix": ":images/plants/Blover/Blover.gif",
		"cursor_pix": ":images/plants/Blover/Blover_static.png",
		"cost": 25,
		"map_id": 1,  # 所在地图id
		"damage": 0,
		"hp": 300,
		"cooling": 7.5,
		"desc": "栽种在水面上，可种其他植物"
	},
	"gloom_shroom": {
		"id": 44,
		"name": "gloom_shroom",
		"cn_name": "忧郁喷菇",
		"card_pix": ":images/cards/card_gloom_shroom.png",
		"put_pix": ":images/plants/GloomShroom/GloomShroom.gif",
		"cursor_pix": ":images/plants/GloomShroom/idle_static.png",
		"sleep_pix": ":images/plants/GloomShroom/GloomShroomSleep.gif",  # 白天睡觉
		"cost": 150,
		"map_id": 2,  # 所在地图id
		"damage": 20,
		"moderate": 0.0,
		"hp": 300,
		"cooling": 50,
		"attack_gap": 1.9,
		"for_upgrade": True,  # 用作给其他植物提升
		"for_upgrade_id": 38,  # 用作给其他植物提升
		"desc": "全方位喷射4次烟雾"
	},
	"star_fruit": {
		"id": 45,
		"name": "star_fruit",
		"cn_name": "杨桃",
		"map_id": 1,  # 所在地图id
		"card_pix": ":images/cards/card_starfruit.png",
		"put_pix": ":images/plants/Starfruit/Starfruit.gif",
		"cursor_pix": ":images/plants/Starfruit/Starfruit_static.png",
		"cost": 150,
		"damage": 20,
		"moderate": 0.0,
		"hp": 300,
		"cooling": 7.5,
		"attack_gap": 1.4,
		"desc": "向五个方向发射杨桃星星"
	}, "umbrella_leaf": {
		"id": 46,
		"name": "umbrella_leaf",
		"cn_name": "莴苣",
		"map_id": 1,  # 所在地图id
		"card_pix": ":images/cards/card_umbrella_leaf.png",
		"put_pix": ":images/plants/Umbrellaleaf/idle_static.png",
		"cursor_pix": ":images/plants/Umbrellaleaf/idle_static.png",
		"cost": 100,
		"damage": 0,
		"hp": 300,
		"cooling": 7.5,
		"desc": "防御蹦极僵尸以及篮球僵尸"
	},

}

plant_card_list = plant_param_dict.values()
placeholder_item_param_dict = {
	"tomb_stone": {
		"id": 100,
		"name": "tomb_stone",
		"cn_name": "墓碑",
		"cost": 0,
		"desc": ""
	}, "bury_item": {
		"id": 101,
		"name": "bury_item",
		"cn_name": "土坑",
		"cost": 0,
		"desc": ""
	}, "ice_item": {
		"id": 102,
		"name": "ice_item",
		"cn_name": "冰",
		"cost": 0,
		"desc": ""
	},
}

# 植物子弹类
plant_bullet_data = {
	"pea": {
		"id": 1,  # 豌豆子弹
		"name": "pea",
		"damage": 20,  # 子弹伤害
		"moderate": 0.0,  # 减速 (百分比，浮点数)
		"moderate_duration": 0.0,  # 减速 持续时间
		"attack_gap": 1.75,  # 攻击速度 单位秒
		"bullet": ":images/bullet/bullet.gif",  # 子弹图片
		"bullet_hit": ":images/bullet/PeaBulletHit.gif",  # 子弹打中效果
		"effect_key": "hit",  # 子弹打中效音效
		"knock_back": 0.0,  # 击退参数
		"penetrable": False,  # 是否能穿透
	},
	"ice_pea": {
		"id": 2,  # 冰霜豌豆子弹
		"name": "ice_pea",
		"damage": 20,
		"moderate": 0.15,
		"moderate_duration": 2.0,
		"attack_gap": 1.75,
		"bullet": ":images/bullet/ip_bullet.gif",
		"bullet_hit": ":images/bullet/ip_bullet.gif",
		"effect_key": "frozen",
		"knock_back": 0.0,
		"penetrable": False,
	}, "lsm": {
		"id": 3,  # 小喷菇子弹
		"name": "lsm",
		"damage": 20,
		"moderate": 0.0,
		"moderate_duration": 0.0,
		"attack_gap": 2.0,
		"bullet": ":images/bullet/ShroomBullet.gif",
		"bullet_hit": ":images/bullet/ShroomBulletHit.gif",
		"effect_key": "shoop",
		"knock_back": 0.0,
		"penetrable": False,
	}, "melon": {
		"id": 4,  # 西瓜
		"name": "melon",
		"damage": 80,
		"moderate": 0.0,
		"moderate_duration": 0.0,
		"attack_gap": 2.4,
		"bullet": ":images/bullet/melon.png",
		"bullet_hit": ":images/bullet/MelonBulletHit.gif",
		"effect_key": "melon_pact",
		"knock_back": 0.0,
		"penetrable": False,
		"effect_range": (1, 0, 1, 0),  # 溅射伤害范围
		"effect_damage": 26,  # 溅射伤害 动态 不确定
	}, "cactus_thorn": {
		"id": 5,  # 仙人掌针刺
		"name": "cactus_thorn",
		"damage": 20,  # 子弹伤害
		"moderate": 0.0,  # 减速 (百分比，浮点数)
		"moderate_duration": 0.0,  # 减速 持续时间
		"attack_gap": 1.75,  # 攻击速度 单位秒
		"bullet": ":images/bullet/ProjectileCactus.png",  # 子弹图片
		"bullet_hit": ":images/bullet/ProjectileCactus.png",  # 子弹打中图片
		"effect_key": "hit",  # 子弹打中效音效
		"knock_back": 0.0,  # 击退参数
		"penetrable": True,  # 是否能穿透
	}, "cat_tail_thorn": {
		"id": 6,  # 香蒲针刺
		"name": "cat_tail_thorn",
		"damage": 20,  # 子弹伤害
		"moderate": 0.0,  # 减速 (百分比，浮点数)
		"moderate_duration": 0.0,  # 减速 持续时间
		"attack_gap": 2.4,  # 攻击速度 单位秒
		"bullet": ":images/bullet/mine_red_spot.png",  # 子弹图片
		"bullet_hit": "",  # 子弹打中图片
		"effect_key": "hit",  # 子弹打中效音效
		"knock_back": 0.0,  # 击退参数
		"penetrable": False,  # 是否能穿透
	}, "butter_dot": {
		"id": 7,  # 黄油点
		"name": "butter_dot",
		"damage": 40,
		"moderate": 0.0,
		"moderate_duration": 0.0,
		"attack_gap": 1.9,
		"bullet": ":images/bullet/butter_dot.png",
		"bullet_hit": "",
		"effect_key": "hit",
		"knock_back": 0.0,
		"penetrable": False,
	}, "butter": {
		"id": 8,  # 黄油
		"name": "butter",
		"damage": 40,
		"moderate": 0.0,
		"moderate_duration": 0.0,
		"attack_gap": 1.9,
		"pause_duration": 4,  # 定身4秒
		"bullet": ":images/bullet/butter.png",
		"bullet_hit": "",
		"effect_key": "butter",
		"knock_back": 0.0,
		"penetrable": False,
	}, "cabbage": {
		"id": 9,  # 卷心菜
		"name": "cabbage",
		"damage": 60,
		"moderate": 0.0,
		"moderate_duration": 0.0,
		"attack_gap": 1.9,
		"bullet": ":images/bullet/cabbage.png",
		"bullet_hit": "",
		"effect_key": "hit",
		"knock_back": 0.0,
		"penetrable": False,
	}, "basketball": {
		"id": 10,  # 篮球
		"name": "basketball",
		"damage": 75,
		"moderate": 0.0,
		"moderate_duration": 0.0,
		"attack_gap": 2.4,
		"bullet": ":images/bullet/basketball.png",
		"bullet_hit": "",
		"effect_key": "basketball",
		"knock_back": 0.0,
		"penetrable": False,
	}, "fire_pea": {
		"id": 11,  # 火豌豆子弹
		"name": "fire_pea",
		"damage": 40,  # 子弹伤害
		"moderate": 0.0,  # 减速 (百分比，浮点数)
		"moderate_duration": 0.0,  # 减速 持续时间
		"attack_gap": 1.75,  # 攻击速度 单位秒
		"bullet": ":images/bullet/fire_pea1.gif",  # 子弹图片
		"bullet_hit": ":images/bullet/SputteringFire.gif",  # 子弹打中效果
		"effect_key": "fire_pea",  # 子弹打中效音效
		"knock_back": 0.0,  # 击退参数
		"penetrable": False,  # 是否能穿透
	}, "fume": {
		"id": 12,  # 大喷菇烟雾
		"name": "fume",
		"damage": 20,
		"moderate": 0.0,
		"moderate_duration": 0.0,
		"attack_gap": 1.8,
		"effect_range": (0, 0, 4, 0),
		"bullet": ":images/bullet/fume.gif",
		"bullet_hit": ":images/bullet/ShroomBulletHit.gif",
		"effect_key": "fume",
		"knock_back": 0.0,
		"penetrable": True,  # 穿透攻击
	}, "gloom_fume": {
		"id": 13,  # 忧郁喷菇烟雾
		"name": "gloom_fume",
		"damage": 20,
		"moderate": 0.0,
		"moderate_duration": 0.0,
		"attack_gap": 2.0,
		"bullet": ":images/bullet/surround_fume.gif",
		"bullet_hit": ":images/bullet/ShroomBulletHit.gif",
		"effect_key": "shoop",
		"knock_back": 0.0,
		"penetrable": False,
	}, "ice_melon": {
		"id": 14,  # 冰西瓜
		"name": "melon",
		"damage": 80,
		"moderate": 0.5,
		"moderate_duration": 10.0,
		"effect_range": (1, 0, 1, 0),  # 溅射伤害范围
		"effect_damage": 26,  # 溅射伤害 动态 不确定
		"attack_gap": 2.4,
		"bullet": ":images/bullet/ice_melon.png",
		"bullet_hit": ":images/bullet/IceMelonBulletHit.gif",
		"effect_key": "melon_pact",
		"knock_back": 0.0,
		"penetrable": False,
	}, "star": {
		"id": 15,  # 杨桃星星
		"name": "star",
		"damage": 20,
		"moderate": 0.0,
		"moderate_duration": 0.0,
		"attack_gap": 1.4,
		"bullet": ":images/bullet/Star.gif",
		"bullet_hit": ":images/bullet/StarBulletExplode.png",
		"effect_key": "hit",
		"knock_back": 0.0,
		"penetrable": False,
	}, "sea_shroom_fume": {
		"id": 16,  # 海蘑菇子弹
		"name": "sea_shroom_fume",
		"damage": 20,
		"moderate": 0.0,
		"moderate_duration": 0.0,
		"attack_gap": 2.0,
		"bullet": ":images/bullet/SeaShroomBullet.gif",
		"bullet_hit": ":images/bullet/SeaShroomBulletHit.gif",
		"effect_key": "shoop",
		"knock_back": 0.0,
		"penetrable": False,
	}
}

# 僵尸数据
zombie_param_dict = {
	"regular": {
		"id": 1,  # 普通僵尸
		"name": "regular",
		"put_pix": ":images/zombies/Zombie/Zombie.gif",  # 僵尸图像
		"attack_pix": ":images/zombies/Zombie/ZombieAttack.gif",  # 行走动画
		"idle_pix": ":images/zombies/Zombie/1.gif",  # 空闲动画
		"armor_health": 0,  # 防具耐久 (整数)
		"base_health": 270,  # 基础体力 (整数)
		"speed": 1.0,  # 移动速度（浮点数）
		"attack_frequency": 1.0,  # 攻击频率（秒，浮点数）
		"sound_effect": "hit",  # 被击中音效
	},
	"conehead": {
		"id": 2,  # 路障僵尸
		"name": "conehead",
		"put_pix": ":images/zombies/ConeheadZombie/ConeheadZombie.gif",
		"attack_pix": ":images/zombies/ConeheadZombie/ConeheadZombieAttack.gif",
		"idle_pix": ":images/zombies/ConeheadZombie/1.gif",
		"armor_health": 370,
		"base_health": 270,
		"speed": 0.8,
		"attack_frequency": 1.0,
		"sound_effect": "plastic_hit",
	},
	"buckethead": {
		"id": 3,  # 铁桶僵尸
		"name": "buckethead",
		"put_pix": ":images/zombies/BucketheadZombie/BucketheadZombie.gif",
		"attack_pix": ":images/zombies/BucketheadZombie/BucketheadZombieAttack.gif",
		"idle_pix": ":images/zombies/BucketheadZombie/1.gif",
		"no_icon_gif": ":images/zombies/Zombie/Zombie2.gif",
		"armor_health": 1100,
		"base_health": 270,
		"speed": 0.8,
		"attack_frequency": 1.0,
		"sound_effect": "shieldhit",
	},
	"flag": {
		"id": 4,  # 旗帜僵尸
		"name": "flag",
		"put_pix": ":images/zombies/FlagZombie/FlagZombie.gif",  # 僵尸图像
		"attack_pix": ":images/zombies/FlagZombie/FlagZombieAttack.gif",  # 行走动画
		"idle_pix": ":images/zombies/FlagZombie/1.gif",
		"armor_health": 0,
		"base_health": 270,
		"speed": 2.3,  # 移动速度（浮点数）
		"attack_frequency": 1.0,  # 攻击频率（秒，浮点数）
		"sound_effect": "hit",  # 被击中音效
		"damage_pix": ":images/zombies/FlagZombie/1.gif",
		"dying_pix": ":images/zombies/FlagZombie/FlagZombieLostHead.gif",
	},
	"rugby": {
		"id": 5,  # 橄榄球僵尸
		"name": "football",
		"put_pix": ":images/zombies/FootballZombie/FootballZombie.gif",
		"attack_pix": ":images/zombies/FootballZombie/FootballZombieAttack.gif",
		"idle_pix": ":images/zombies/FootballZombie/1.gif",
		"ash_pix": ":images/zombies/FootballZombie/BoomDie.gif",
		"no_icon_gif": ":images/zombies/FootballZombie/FootballZombieOrnLost.gif",
		"armor_health": 1400,
		"base_health": 270,
		"speed": 1.2,
		"attack_frequency": 1.0,
		"sound_effect": "hit",  # 被击中音效
		"damage_pix": ":images/zombies/FootballZombie/FootballZombieOrnLost.gif",
		"dying_pix": ":images/zombies/FootballZombie/Die.gif",
		"attack_damage_pix": ":images/zombies/FootballZombie/FootballZombieOrnLostAttack.gif",
		"attack_dying_pix": ":images/zombies/FootballZombie/Die.gif",
	},
	"iron_gate": {
		"id": 6,  # 铁门僵尸
		"name": "iron_gate",
		"put_pix": ":images/zombies/ScreenDoorZombie/HeadWalk1.gif",
		"attack_pix": ":images/zombies/ScreenDoorZombie/HeadAttack1.gif",
		"idle_pix": ":images/zombies/ScreenDoorZombie/1.gif",
		"no_icon_gif": ":images/zombies/Zombie/Zombie.gif",
		"armor_health": 800,
		"base_health": 270,
		"speed": 1.0,
		"attack_frequency": 1.0,
		"sound_effect": "shieldhit",
		"damage_pix": ":images/zombies/ScreenDoorZombie/HeadWalk1.gif",
		"dying_pix": ":images/zombies/ScreenDoorZombie/LostHeadWalk1.gif",
		"attack_damage_pix": ":images/zombies/ScreenDoorZombie/HeadAttack1.gif",
		"attack_dying_pix": ":images/zombies/FootballZombie/LostHeadAttack1.gif",
	},
	"news_paper": {
		"id": 7,  # 看报纸僵尸
		"name": "iron_gate",
		"put_pix": ":images/zombies/NewspaperZombie/HeadWalk1.gif",
		"attack_pix": ":images/zombies/NewspaperZombie/HeadAttack1.gif",
		"idle_pix": ":images/zombies/NewspaperZombie/1.gif",
		"ash_pix": ":images/zombies/NewspaperZombie/BoomDie.gif",
		"head_pix": ":images/zombies/NewspaperZombie/Head.gif",
		"armor_health": 150,
		"base_health": 270,
		"speed": 1.0,
		"attack_frequency": 1.0,
		"damage_pix": ":images/zombies/NewspaperZombie/HeadWalk0.gif",
		"dying_pix": ":images/zombies/NewspaperZombie/HeadWalk0.gif",
		"attack_damage_pix": ":images/zombies/NewspaperZombie/HeadAttack0.gif",
		"attack_dying_pix": ":images/zombies/NewspaperZombie/Die.gif",
	},
	"pole_vault": {
		"id": 8,  # 撑杆跳僵尸
		"name": "pole_vault",
		"put_pix": ":images/zombies/PoleVaultingZombie/PoleVaultingZombie.gif",
		"attack_pix": ":images/zombies/PoleVaultingZombie/PoleVaultingZombieAttack.gif",
		"idle_pix": ":images/zombies/PoleVaultingZombie/1.gif",
		"ash_pix": ":images/zombies/PoleVaultingZombieHead/BoomDie.gif",
		"head_pix": ":images/zombies/PoleVaultingZombie/PoleVaultingZombieHead.gif",
		"armor_health": 0,
		"base_health": 500,
		"speed": 2.0,
		"attack_frequency": 1.0,
		"damage_pix": ":images/zombies/PoleVaultingZombie/PoleVaultingZombieWalk.gif",
		"dying_pix": ":images/zombies/PoleVaultingZombie/PoleVaultingZombieLostHead.gif",
		"attack_damage_pix": ":images/zombies/PoleVaultingZombie/PoleVaultingZombieAttack.gif",
		"attack_dying_pix": ":images/zombies/PoleVaultingZombie/PoleVaultingZombieDie.gif",
	}, "swimming": {
		"id": 9,  # 普通游泳僵尸
		"name": "swimming",
		"put_pix": ":images/zombies/DuckyTubeZombie1/Walk1.gif",  # 僵尸图像
		"attack_pix": ":images/zombies/DuckyTubeZombie1/Attack.gif",  # 行走动画
		"idle_pix": ":images/zombies/DuckyTubeZombie1/1.gif",
		"swimming_walk_pix": ":images/zombies/DuckyTubeZombie1/Walk2.gif",
		"swimming_attack_pix": ":images/zombies/DuckyTubeZombie1/Attack.gif",
		"armor_health": 0,
		"base_health": 270,
		"speed": 1.0,  # 移动速度（浮点数）
		"attack_frequency": 1.0,  # 攻击频率（秒，浮点数）
		"sound_effect": "hit",  # 被击中音效
		"is_swimming_zombie": True,  # 是否为泳池僵尸
		"water_walk_pix": ":images/zombies/DuckyTubeZombie1/Walk2.gif",
		"damage_pix": ":images/zombies/DuckyTubeZombie1/Attack.gif",
		"dying_pix": ":images/zombies/DuckyTubeZombie1/Attack.gif",
		"attack_damage_pix": ":images/zombies/DuckyTubeZombie1/Attack.gif",
		"attack_dying_pix": ":images/zombies/DuckyTubeZombie1/Die.gif",
	}, "swimming_buckethead": {
		"id": 10,  # 游泳铁桶僵尸
		"name": "buckethead",
		"put_pix": ":images/zombies/DuckyTubeZombie3/Walk2.gif",
		"attack_pix": ":images/zombies/DuckyTubeZombie3/Attack.gif",
		"idle_pix": ":images/zombies/DuckyTubeZombie3/1.gif",
		"no_icon_gif": ":images/zombies/DuckyTubeZombie1/Walk2.gif",
		"swimming_walk_pix": ":images/zombies/DuckyTubeZombie3/Walk2.gif",
		"swimming_attack_pix": ":images/zombies/DuckyTubeZombie3/Attack.gif",
		"armor_health": 1100,
		"base_health": 270,
		"speed": 0.8,
		"attack_frequency": 1.0,
		"sound_effect": "shieldhit",
		"is_swimming_zombie": True,  # 是否为泳池僵尸
		"water_walk_pix": ":images/zombies/DuckyTubeZombie3/Walk2.gif",
		"damage_pix": ":images/zombies/DuckyTubeZombie3/Attack.gif",
		"dying_pix": ":images/zombies/DuckyTubeZombie3/Attack.gif",
		"attack_damage_pix": ":images/zombies/DuckyTubeZombie3/Attack.gif",
		"attack_dying_pix": ":images/zombies/DuckyTubeZombie3/Die.gif",

	}, "dive": {
		"id": 11,  # 潜水僵尸
		"name": "dive",
		"put_pix": ":images/zombies/SnorkelZombie/Walk1.gif",
		"attack_pix": ":images/zombies/SnorkelZombie/Attack.gif",
		"idle_pix": ":images/zombies/SnorkelZombie/1.gif",
		"swimming_walk_pix": ":images/zombies/SnorkelZombie/Walk2.gif",
		"swimming_attack_pix": ":images/zombies/SnorkelZombie/Attack.gif",
		"armor_health": 0,
		"base_health": 270,
		"speed": 0.8,
		"attack_frequency": 1.0,
		"is_swimming_zombie": True,  # 是否为泳池僵尸
		"water_walk_pix": ":images/zombies/SnorkelZombie/Walk2.gif",
		"damage_pix": ":images/zombies/SnorkelZombie/Attack.gif",
		"dying_pix": ":images/zombies/SnorkelZombie/Attack.gif",
		"attack_damage_pix": ":images/zombies/SnorkelZombie/Attack.gif",
		"attack_dying_pix": ":images/zombies/SnorkelZombie/Die.gif",
	}, "conehead_swimming": {
		"id": 12,  # 游泳路障僵尸
		"name": "dive",
		"put_pix": ":images/zombies/DuckyTubeZombie2/Walk1.gif",
		"attack_pix": ":images/zombies/DuckyTubeZombie2/Attack.gif",
		"idle_pix": ":images/zombies/DuckyTubeZombie2/1.gif",
		"swimming_walk_pix": ":images/zombies/DuckyTubeZombie2/Walk2.gif",
		"swimming_attack_pix": ":images/zombies/DuckyTubeZombie2/Attack.gif",
		"armor_health": 370,
		"base_health": 270,
		"speed": 0.8,
		"attack_frequency": 1.0,
		"is_swimming_zombie": True,  # 是否为泳池僵尸
		"sound_effect": "plastic_hit",
		"water_walk_pix": ":images/zombies/DuckyTubeZombie2/Walk2.gif",
		"damage_pix": ":images/zombies/DuckyTubeZombie2/Walk2.gif",
		"dying_pix": ":images/zombies/DuckyTubeZombie2/Walk2.gif",
		"attack_damage_pix": ":images/zombies/DuckyTubeZombie2/Attack.gif",
		"attack_dying_pix": ":images/zombies/DuckyTubeZombie2/Die.gif",
	}, "zomboni": {
		"id": 13,  # 雪橇车僵尸
		"name": "zomboni",
		"put_pix": ":images/zombies/Zomboni/drive.gif",
		"attack_pix": ":images/zombies/Zomboni/drive.gif",
		"idle_pix": ":images/zombies/Zomboni/drive.gif",
		"ash_pix": ":images/zombies/Zomboni/BoomDie.gif",
		"armor_health": 0,
		"base_health": 1350,
		"speed": 1.6,
		"damage": 9999,  # 直接秒杀
		"attack_frequency": 1.0,
		"is_swimming_zombie": False,  # 是否为泳池僵尸
		"sound_effect": "shieldhit",
		"damage_pix": ":images/zombies/Zomboni/drive.gif",
		"dying_pix": ":images/zombies/Zomboni/3.gif",
		"attack_damage_pix": ":images/zombies/Zomboni/drive.gif",
		"attack_dying_pix": ":images/zombies/Zomboni/3.gif",
	}, "imp": {
		"id": 14,  # 小鬼僵尸
		"name": "imp",
		"put_pix": ":images/zombies/Imp/1.gif",
		"attack_pix": ":images/zombies/Imp/Attack.gif",
		"idle_pix": ":images/zombies/Imp/0.gif",
		"ash_pix": ":images/zombies/Imp/1.gif",
		"head_pix": ":images/zombies/Imp/Die.gif",
		"armor_health": 0,
		"base_health": 270,
		"speed": 1.2,
		"damage": 30,
		"attack_frequency": 1.0,
		"is_swimming_zombie": False,  # 是否为泳池僵尸
		"damage_pix": ":images/zombies/Imp/1.gif",
		"dying_pix": ":images/zombies/Imp/Die.gif",
		"attack_damage_pix": ":images/zombies/Imp/Attack.gif",
		"attack_dying_pix": ":images/zombies/Imp/Attack.gif",
	}, "catapult": {
		"id": 15,  # 投石车僵尸
		"name": "catapult",
		"put_pix": ":images/zombies/CataPult/walk.gif",
		"attack_pix": ":images/zombies/CataPult/shoot.gif",
		"idle_pix": ":images/zombies/CataPult/idle.gif",
		"ash_pix": ":images/zombies/CataPult/BoomDie.gif",
		"armor_health": 0,
		"basketball_count": 20,
		"base_health": 850,
		"speed": 1.2,
		"damage": 9999,  # 直接秒杀
		"attack_frequency": 1.0,
		"gap": 2.0,
		"is_swimming_zombie": False,  # 是否为泳池僵尸
		"damage_pix": ":images/zombies/CataPult/walk.gif",
		"dying_pix": ":images/zombies/CataPult/walk.gif",
		"attack_damage_pix": ":images/zombies/CataPult/shoot.gif",
		"attack_dying_pix": ":images/zombies/CataPult/shoot.gif",
	}, "dancer": {
		"id": 16,  # 舞王僵尸
		"name": "dancer",
		"put_pix": ":images/zombies/DancingZombie/SlidingStep.gif",
		"attack_pix": ":images/zombies/DancingZombie/Attack.gif",
		"idle_pix": ":images/zombies/DancingZombie/0.gif",
		"ash_pix": ":images/zombies/DancingZombie/BoomDie.gif",
		"head_pix": ":images/zombies/DancingZombie/Head.gif",
		"dancing_pix": ":images/zombies/DancingZombie/Dancing.gif",
		"call_partner_pix": ":images/zombies/DancingZombie/Summon.gif",
		"armor_health": 0,
		"base_health": 500,
		"speed": 2.6,
		"attack_frequency": 1.0,
		"is_swimming_zombie": False,  # 是否为泳池僵尸
		"damage_pix": ":images/zombies/DancingZombie/Dancing.gif",
		"dying_pix": ":images/zombies/DancingZombie/LostHead.gif",
		"attack_damage_pix": ":images/zombies/DancingZombie/LostHeadAttack.gif",
		"attack_dying_pix": ":images/zombies/DancingZombie/Die.gif",
		"dance_gap": 7.75,
	}, "dancer_partner": {
		"id": 17,  # 伴舞僵尸
		"name": "dancer_partner",
		"put_pix": ":images/zombies/BackupDancer/Dancing.gif",
		"attack_pix": ":images/zombies/BackupDancer/Attack.gif",
		"idle_pix": ":images/zombies/BackupDancer/0.gif",
		"ash_pix": ":images/zombies/BackupDancer/BoomDie.gif",
		"head_pix": ":images/zombies/BackupDancer/Head.gif",
		"armor_health": 0,
		"base_health": 270,
		"speed": 0.8,
		"attack_frequency": 1.0,
		"is_swimming_zombie": False,  # 是否为泳池僵尸
		"damage_pix": ":images/zombies/BackupDancer/Dancing.gif",
		"dying_pix": ":images/zombies/BackupDancer/LostHead.gif",
		"attack_damage_pix": ":images/zombies/BackupDancer/LostHeadAttack.gif",
		"attack_dying_pix": ":images/zombies/BackupDancer/Die.gif",
	},
	"ladder_zombie": {
		"id": 18,  # 梯子僵尸
		"name": "ladder_zombie",
		"put_pix": ":images/zombies/ZombieLadder/ladderwalk.gif",
		"attack_pix": ":images/zombies/ZombieLadder/laddereat.gif",
		"idle_pix": ":images/zombies/ZombieLadder/idle.gif",
		"armor_health": 500,
		"base_health": 500,
		"speed": 1.5,
		"damage": 25,
		"attack_frequency": 1.0,
		"sound_effect": "shieldhit",
		"damage_pix": ":images/zombies/ZombieLadder/ladderwalk.gif",
		"dying_pix": ":images/zombies/ZombieLadder/ladderwalk.gif",
		"attack_damage_pix": ":images/zombies/ZombieLadder/laddereat.gif",
		"no_icon_gif": ":images/zombies/ZombieLadder/walk.gif",
	}, "disco_zombie": {
		"id": 19,  # disco僵尸
		"name": "disco_zombie",
		"put_pix": ":images/zombies/Zombie_disco/walk.gif",
		"attack_pix": ":images/zombies/Zombie_disco/eat.gif",
		"idle_pix": ":images/zombies/Zombie_disco/walk.gif",
		"dancing_pix": ":images/zombies/Zombie_disco/point.gif",
		"call_partner_pix": ":images/zombies/Zombie_disco/armraise.gif",
		"armor_health": 0,
		"base_health": 500,
		"speed": 2.6,
		"attack_frequency": 1.0,
		"is_swimming_zombie": False,  # 是否为泳池僵尸
		"damage_pix": ":images/zombies/Zombie_disco/moonwalk.gif",
		"dying_pix": ":images/zombies/Zombie_disco/moonwalk.gif",
		"attack_damage_pix": ":images/zombies/Zombie_disco/eat.gif",
		"attack_dying_pix": ":images/zombies/Zombie_disco/death.gif",
		"dance_gap": 7.75,
	}, "disco_partner": {
		"id": 20,  # disco的伴舞僵尸
		"name": "disco_partner",
		"put_pix": ":images/zombies/Zombie_backup/walk.gif",
		"attack_pix": ":images/zombies/Zombie_backup/eat.gif",
		"idle_pix": ":images/zombies/Zombie_backup/walk.gif",
		"armor_health": 0,
		"base_health": 270,
		"speed": 0.8,
		"attack_frequency": 1.0,
		"is_swimming_zombie": False,  # 是否为泳池僵尸
		"damage_pix": ":images/zombies/Zombie_backup/walk.gif",
		"dying_pix": ":images/zombies/Zombie_backup/walk.gif",
		"attack_damage_pix": ":images/zombies/Zombie_backup/eat.gif",
		"attack_dying_pix": ":images/zombies/Zombie_backup/death.gif",
	}, "pogo_zombie": {
		"id": 21,  # 跳跳僵尸
		"name": "pogo_zombie",
		"put_pix": ":images/zombies/ZombiePogo/pogo.gif",
		"attack_pix": ":images/zombies/ZombiePogo/eat.gif",
		"idle_pix": ":images/zombies/ZombiePogo/idle.gif",
		"no_icon_gif": ":images/zombies/ZombiePogo/walk.gif",
		"armor_health": 0,
		"base_health": 500,
		"speed": 2.4,
		"attack_frequency": 1.0,
		"is_swimming_zombie": False,  # 是否为泳池僵尸
		"damage_pix": ":images/zombies/ZombiePogo/walk.gif",
		"dying_pix": ":images/zombies/ZombiePogo/walk.gif",
		"attack_damage_pix": ":images/zombies/ZombiePogo/eat.gif",
		"attack_dying_pix": ":images/zombies/ZombiePogo/death.gif",
	}, "balloon_zombie": {
		"id": 22,  # 气球僵尸
		"name": "balloon_zombie",
		"put_pix": ":images/zombies/Zombie_balloon/swing.gif",
		"attack_pix": ":images/zombies/Zombie_balloon/eat.gif",
		"idle_pix": ":images/zombies/Zombie_balloon/idle.gif",
		"armor_health": 20,
		"base_health": 270,
		"speed": 1.8,
		"attack_frequency": 1.0,
		"is_swimming_zombie": False,  # 是否为泳池僵尸
		"damage_pix": ":images/zombies/Zombie_balloon/walk.gif",
		"dying_pix": ":images/zombies/Zombie_balloon/death.gif",
		"attack_damage_pix": ":images/zombies/Zombie_balloon/eat.gif",
		"attack_dying_pix": ":images/zombies/Zombie_balloon/death.gif",
	}, "digger_zombie": {
		"id": 23,  # 矿工僵尸
		"name": "digger_zombie",
		"put_pix": ":images/zombies/Zombie_digger/dig.gif",
		"attack_pix": ":images/zombies/Zombie_digger/eat.gif",
		"idle_pix": ":images/zombies/Zombie_digger/idle.gif",
		"no_icon_gif": ":images/zombies/Zombie_digger/Walk.gif",
		"armor_health": 100,
		"base_health": 270,
		"speed": 4.8,
		"attack_frequency": 1.0,
		"is_swimming_zombie": False,  # 是否为泳池僵尸
		"damage_pix": ":images/zombies/Zombie_digger/walk_nopickaxe.gif",
		"dying_pix": ":images/zombies/Zombie_digger/death.gif",
		"attack_damage_pix": ":images/zombies/Zombie_digger/eat.gif",
		"attack_dying_pix": ":images/zombies/Zombie_digger/walk_nopickaxe.gif",
	}, "joker_zombie": {
		"id": 24,  # 小丑僵尸
		"name": "joker_zombie",
		"put_pix": ":images/zombies/JackinTheBoxZombie/Walk.gif",
		"attack_pix": ":images/zombies/JackinTheBoxZombie/Attack.gif",
		"idle_pix": ":images/zombies/JackinTheBoxZombie/idle.gif",
		"no_icon_gif": ":images/zombies/JackinTheBoxZombie/Walk.gif",
		"armor_health": 0,
		"base_health": 500,
		"speed": 1.8,
		"attack_frequency": 1.0,
		"is_swimming_zombie": False,  # 是否为泳池僵尸
		"damage_pix": ":images/zombies/JackinTheBoxZombie/LostHead.gif",
		"dying_pix": ":images/zombies/JackinTheBoxZombie/LostHead.gif",
		"attack_damage_pix": ":images/zombies/JackinTheBoxZombie/LostHeadAttack.gif",
		"attack_dying_pix": ":images/zombies/JackinTheBoxZombie/Die.gif",
	}, "zombie_yeti": {
		"id": 28,  # 雪人僵尸
		"name": "zombie_yeti",
		"put_pix": ":images/zombies/Zombie_yeti/walk.gif",
		"attack_pix": ":images/zombies/Zombie_yeti/Attack.gif",
		"idle_pix": ":images/zombies/Zombie_yeti/idle.gif",
		"armor_health": 0,
		"base_health": 1350,
		"speed": 2.4,
		"attack_frequency": 1.0,
		"is_swimming_zombie": False,  # 是否为泳池僵尸
		"damage_pix": ":images/zombies/Zombie_yeti/LostHead.gif",
		"dying_pix": ":images/zombies/Zombie_yeti/LostHead.gif",
		"attack_damage_pix": ":images/zombies/Zombie_yeti/LostHeadAttack.gif",
		"attack_dying_pix": ":images/zombies/Zombie_yeti/death.gif",
	}, "red_gargantuar": {
		"id": 25,  # 红眼伽刚特尔
		"name": "red_gargantuar",
		"put_pix": ":images/zombies/Red_Gargantuar/walk.gif",
		"attack_pix": ":images/zombies/Red_Gargantuar/smash.gif",
		"idle_pix": ":images/zombies/Red_Gargantuar/idle.gif",
		"armor_health": 0,
		"base_health": 6000,
		"damage": 2000,
		"speed": 1.5,
		"attack_frequency": 1.0,
		"is_swimming_zombie": False,  # 是否为泳池僵尸
		"damage_pix": ":images/zombies/Red_Gargantuar/walk.gif",
		"dying_pix": ":images/zombies/Red_Gargantuar/walk.gif",
		"attack_damage_pix": ":images/zombies/Red_Gargantuar/smash.gif",
		"attack_dying_pix": ":images/zombies/Red_Gargantuar/death.gif",
	}, "white_gargantuar": {
		"id": 26,  # 白眼伽刚特尔
		"name": "zombie_yeti",
		"put_pix": ":images/zombies/White_Gargantuar/walk.gif",
		"attack_pix": ":images/zombies/White_Gargantuar/smash.gif",
		"idle_pix": ":images/zombies/White_Gargantuar/idle.gif",
		"armor_health": 0,
		"base_health": 3000,
		"damage": 2000,
		"speed": 1.5,
		"attack_frequency": 1.0,
		"is_swimming_zombie": False,  # 是否为泳池僵尸
		"damage_pix": ":images/zombies/White_Gargantuar/walk.gif",
		"dying_pix": ":images/zombies/White_Gargantuar/walk.gif",
		"attack_damage_pix": ":images/zombies/White_Gargantuar/smash.gif",
		"attack_dying_pix": ":images/zombies/White_Gargantuar/death.gif",
	}, "dolphin_rider": {
		"id": 27,  # 海豚骑士
		"name": "dolphin_rider",
		"put_pix": ":images/zombies/DolphinRiderZombie/Walk1.gif",
		"attack_pix": ":images/zombies/DolphinRiderZombie/Attack.gif",
		"idle_pix": ":images/zombies/DolphinRiderZombie/1.gif",
		"swimming_walk_pix": ":images/zombies/DolphinRiderZombie/Walk2.gif",
		"swimming_attack_pix": ":images/zombies/DolphinRiderZombie/Attack.gif",
		"armor_health": 0,
		"base_health": 500,
		"speed": 3.0,
		"attack_frequency": 1.0,
		"is_swimming_zombie": True,  # 是否为泳池僵尸
		"water_walk_pix": ":images/zombies/DolphinRiderZombie/Walk2.gif",
		"damage_pix": ":images/zombies/DolphinRiderZombie/Attack.gif",
		"dying_pix": ":images/zombies/DolphinRiderZombie/Attack.gif",
		"attack_damage_pix": ":images/zombies/DolphinRiderZombie/Attack.gif",
		"attack_dying_pix": ":images/zombies/DolphinRiderZombie/Die.gif",
	}
}
zombie_card_list = list(zombie_param_dict.values())
# 背景音乐对应关系
index_bgm_dict = {
	0: "qrc:music/bgm/start.mp3",  # 游戏首屏
	1: "qrc:music/bgm/start.mp3",  # 选择模式
	2: "qrc:music/bgm/start.mp3",  # 选择关卡
	3: "qrc:music/bgm/prepare.wav",  # 选择卡片
	7: "qrc:music/bgm/prepare.wav",  # 选择卡片
}

# 音效对应关系
sound_effect_dict = {
	"collect_sf": "qrc:music/effect/collectSunshine.wav",
	"lose": "qrc:music/effect/scream.wav",
	"win": "qrc:music/effect/gameWin.wav",
	"shovel": "qrc:music/effect/shovel.wav",
	"plant_raise": "qrc:music/effect/plantRaised.wav",
	"use_shovel": "qrc:music/effect/shovel.wav",
	"start_laugh": "qrc:music/effect/zombieLaugh.wav",
	"card_lift": "qrc:music/effect/cardLift.wav",
	"buzzer": "qrc:music/effect/buzzer.wav",
	"zombie_appear": "qrc:music/effect/zombieAppearGroan3.wav",
	"snow_pea_sparkles": "qrc:music/effect/snow_pea_sparkles.wav",
	"frozen": "qrc:music/effect/frozen.wav",
	"huge_wave": "qrc:music/effect/huge_wave.wav",
	"cherry_boom": "qrc:music/effect/cherry_boom.wav",
	"i_am_coming": "qrc:music/effect/i_am_coming.wav",
	"jalapeno": "qrc:music/effect/jalapeno.wav",
	"shoop": "qrc:music/effect/shoop.wav",
	"Shop": "qrc:music/effect/Shop.wav",
	"potato_mine": "qrc:music/effect/potato_mine.wav",
	"bigchomp": "qrc:music/effect/bigchomp.wav",
	"papaer_drop": "qrc:music/effect/papaer_drop.wav",
	"jumping": "qrc:music/effect/jumping.wav",
	"melon_pact": "qrc:music/effect/melon_pact.wav",
	"plant_grow": "qrc:music/effect/plantgrow.wav",
	"game_ready": "qrc:music/effect/readySetPlant.wav",
	"loadingbar_flower": "qrc:music/effect/loadingbar_flower.wav",
	"buttonclick": "qrc:music/effect/buttonclick.wav",
	"zamboni": "qrc:music/effect/zamboni.wav",
	"doomshroom": "qrc:music/effect/doomshroom.wav",
	"dave00": "qrc:music/effect/crazydaveshort1.wav",
	"dave01": "qrc:music/effect/crazydavelong1.wav",
	"dave02": "qrc:music/effect/crazydavelong2.wav",
	"dave03": "qrc:music/effect/crazydavelong3.wav",
	"dave04": "qrc:music/effect/crazydavecrazy.wav",
	"explosion": "qrc:music/effect/explosion.wav",
	"dancing": "qrc:music/effect/dancer.wav",
	"lawnmower": "qrc:music/effect/lawnmower.wav",
	"pool_cleaner": "qrc:music/effect/pool_cleaner.wav",
	"butter": "qrc:music/effect/butter.wav",
	"floop": "qrc:music/effect/floop.wav",
	"pause": "qrc:music/effect/pause.wav",
	"balloon_pop": "qrc:music/effect/balloon_pop.wav",
	"ballooninflate": "qrc:music/effect/ballooninflate.wav",
	"gravebusterchomp": "qrc:music/effect/gravebusterchomp.wav",
	"wakeup": "qrc:music/effect/wakeup.wav",
	"puff": "qrc:music/effect/puff.wav",
	"blover": "qrc:music/effect/blover.wav",
	"fume": "qrc:music/effect/fume.wav",
	"coin": "qrc:music/effect/coin.wav",
	"diamond": "qrc:music/effect/diamond.wav",
	"jackinthebox": "qrc:music/effect/jackinthebox.wav",
	"digger_zombie": "qrc:music/effect/digger_zombie.wav",
	"gargantudeath": "qrc:music/effect/gargantudeath.wav",
	"gargantuar_thump": "qrc:music/effect/gargantuar_thump.wav",
	"basketball": "qrc:music/effect/basketball.wav",
	"jump_into_water": "qrc:music/effect/jump_into_water.wav",
	"dolphin_appears": "qrc:music/effect/dolphin_appears.wav",
	"dolphin_before_jumping": "qrc:music/effect/dolphin_before_jumping.wav",
}
muti_effect_dict = {
	"shieldhit": [
		"qrc:music/effect/shield_hit.wav",
		"qrc:music/effect/shield_hit2.wav"
	],
	"groan": [
		"qrc:music/effect/groan.wav",
		"qrc:music/effect/groan2.wav",
		"qrc:music/effect/groan3.wav",
		"qrc:music/effect/groan4.wav",
		"qrc:music/effect/groan5.wav",
		"qrc:music/effect/groan6.wav",
	],
	"eaten": [
		"qrc:music/effect/gulp.wav",
	],
	"zombie_eating": [
		"qrc:music/effect/chomp.wav",
		"qrc:music/effect/chomp2.wav",
		"qrc:music/effect/chompsoft.wav",
	],
	"hit": [
		"qrc:music/effect/hit1.wav",
		"qrc:music/effect/hit2.wav",
		"qrc:music/effect/hit3.wav",
	],
	"plant": [
		"qrc:music/effect/plant.wav",
		"qrc:music/effect/plant2.wav",
	],
	"plastic_hit": [
		"qrc:music/effect/plastic_hit.wav",
		"qrc:music/effect/plastic_hit2.wav",
	],
	"squash_hmm": [
		"qrc:music/effect/squash_hmm.wav",
		"qrc:music/effect/squash_hmm2.wav",
	],
	"tap": [
		"qrc:music/effect/tap.wav",
		"qrc:music/effect/tap2.wav",
	],
	"fire_pea": [
		"qrc:music/effect/ignite.wav",
		"qrc:music/effect/ignite2.wav",
	],
	"newspaper_rarrgh": [
		"qrc:music/effect/newspaper_rarrgh.wav",
		"qrc:music/effect/newspaper_rarrgh2.wav",
		"qrc:music/effect/newspaper_rip.wav",
	],
	"throw": [
		"qrc:music/effect/throw.wav",
		"qrc:music/effect/throw2.wav",
	],
	"yuck": [
		"qrc:music/effect/yuck.wav",
		"qrc:music/effect/yuck2.wav",
	],
	"jack_surprise": [
		"qrc:music/effect/jack_surprise.wav",
		"qrc:music/effect/jack_surprise2.wav",
	],
}

# 僵尸体力 贴图对应关系
zombie_hp_gif_dict = {
	"normal": {
		100: ":images/zombies/normal.gif",
		20: ":images/zombies/normal2.gif",
		10: ":images/zombies/normal3.gif",
	},
	"rugby": {
		100: ":images/zombies/ruby00.gif",
		20: ":images/zombies/ruby000.gif",
		10: ":images/zombies/rugby0.gif",
	}

}
map_dict = {
	"day_time": {
		"id": 1,
		"bgm": "qrc:music/bgm/daytime.m4s",
		"bg_pic": ":images/map/gaming/daytime.png",
		"prepare_bg_pic": ":images/map/prepare/daytime.png",
		"name": "白天",
		"is_swimming_map": False,
		"is_daytime": True,  # 是否为白天
		"line_count": 5,
		"zombie_id_list": [2, 3, 4]
	},
	"night": {
		"id": 2,
		"bgm": "qrc:music/bgm/night.m4s",
		"bg_pic": ":images/map/gaming/night.png",
		"prepare_bg_pic": ":images/map/prepare/night.png",
		"name": "夜晚",
		"line_count": 5,
		"is_swimming_map": False,
		"is_daytime": False,  # 是否为白天
		# "zombie_id_list": [5, 6, 7, 8]
		"zombie_id_list": [5, 6, 16, 19, 24]
	},
	"swimming": {
		"id": 3,
		"bgm": "qrc:music/bgm/swimming.m4s",
		"bg_pic": ":images/map/gaming/swimming_pool.png",
		"prepare_bg_pic": ":images/map/prepare/swimming_pool.png",
		"name": "泳池",
		"line_count": 6,
		"is_swimming_map": True,
		"is_daytime": True,  # 是否为白天
		"zombie_id_list": [9, 10, 11, 12, 24, 27]
	},
	"night_swimming": {
		"id": 4,
		"bgm": "qrc:music/bgm/night_swimming.m4s",
		"bg_pic": ":images/map/gaming/night_swimming.png",
		"prepare_bg_pic": ":images/map/prepare/night_swimming.png",
		"name": "夜晚泳池",
		"line_count": 6,
		"is_swimming_map": True,
		"is_daytime": False,  # 是否为白天
		"zombie_id_list": [9, 10, 11, 12, 19, 22]
	}
}
dave_dialog_list = [
	{
		"content": "嘿，邻居！你今天感觉怎么样？",
		"pix": ":images/others/CrazyDave/blahblah.gif",
		"audio": "dave01"
	},
	{
		"content": "我是戴夫，但大家都叫我疯狂戴夫。",
		"pix": ":images/others/CrazyDave/mediumtalk.gif",
		"audio": "dave02"
	},
	{
		"content": "你一定在想：为什么叫我疯狂戴夫呢？",
		"pix": ":images/others/CrazyDave/mediumtalk.gif",
		"audio": "dave03"
	},
	{
		"content": "哈哈哈，没错，我~~~疯~~~了！！！！",
		"pix": ":images/others/CrazyDave/crazy.gif",
		"audio": "dave04"
	}
]
