import random
import sys
import traceback

from PyQt5.QtCore import Qt, QSize, QTimer, QPropertyAnimation, QPoint, QEasingCurve, QUrl, QCoreApplication
from PyQt5.QtGui import QPixmap, QColor, QPalette, QCursor, QKeySequence, QIcon
from PyQt5.QtMultimedia import QMediaPlaylist, QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, \
	QShortcut
from src.config import normal_conf, game_conf
from src.element.bullet import IcePeaBullet, PeaBullet, SproutMushroomBullet, MelonBullet, ThornBullet, ButterDotBullet, \
	ButterBullet, CabbageBullet, CatTailThornBullet, IceMelonBullet, FumeMushroomBullet, StarBullet, BasketballBullet
from src.element.others import AshFire, Frost, CountdownElement, LawnMower
from src.element.plant import SunFlower, PeaShooter, WallNut, IcePea, RepeaterPeaShooter, CherryBoom, Jalapeno, Pumpkin, \
	LittleSproutMushroomShooter, MacadamiaNut, SunMushroom, PotatoMine, FearMushroom, Chomper, Lurker, FrostMushroom, \
	Watermelon, Cactus, SeaShroomShooter, DoomShroom, TangleKelp, TombStoneItem, BuryItem, IceItem, CobCannon, Cabbage, \
	CatTail, Torchwood, ThreeShooter, HypnoShroom, SplitPeaShooter, MagnetShroom, Marigold, TwinSunFlower, GoldMagnet, \
	SpikerRock, GatlingPeaShooter, WinterMelon, CoffeeBean, GraveBuster, Blover, FumeMushroomShooter, GloomShroom, \
	StarFruit, Garlic, UmbrellaLeaf
from src.element.zombies import RegularZombie, ConeheadZombie, BucketheadZombie, FlagZombie, RubyZombie, IronGateZombie, \
	NewsPaperZombie, PoleVaultZombie, RegularSwimmingZombie, BucketheadSwimmingZombie, DiveZombie, \
	ConeheadSwimmingZombie, \
	ImpZombie, ZomboniZombie, CataPultZombie, DancerZombie, DacnerPartnerZombie, LadderZombie, DiscoZombie, \
	DiscoPartnerZombie, PogoZombie, BalloonZombie, DiggerZombie, JokerZombie, WhiteGargantuar, RedGargantuar, \
	DolphinRiderZombie
from src.custom_ui.game_scene import GameScene, GamePrepareScene, GameLoadingScene, GameStartScene, \
	GameLevelSelectScene, \
	CrazyDaveScene
from src.map.map_conf import DayTimeMap, SwimmingMap, NightMap, NightSwimmingMap
from .signal_bus import bus
from src.threads.audio_thread import AudioThread
from src.my_util.utils import remove_list_item, check_coordinate_in_range, get_aim_item_data
from src.custom_ui.widgets import SlidingStackedWidget, \
	AutoSunflower, PlantToolTip, MenuDialog, GameMoviePlayPage, TipWidget, AlmanacWidget, CurrencyItem, GameOverDialog
from src.map.game_level import level_list
import src.resources.resource_rc

QCoreApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)


class Window(QMainWindow):
	def __init__(self):
		super(Window, self).__init__()
		self.param_int()
		self.map_init()
		self.ui_init()
		self.slot_init()
		self.player_init()
		self.timer_init()
		self.register_shortcut()

	def param_int(self):
		self.game_ui_not_loaded = True  # 游戏ui是否加载过一次
		self.auto_sunshine_shown = False
		self.current_put_pix_str = ""
		self.game_seconds = 0  # 当前游戏秒数
		self.zombie_line_x = 0
		self.map_id = 1  # 当前地图id
		self.current_level = 1  # 当前是第几关
		self.bgm_volume = 50  # 背景音乐音量
		self.plant_set = set()  # 植物集合
		self.zombie_set = set()  # 僵尸集合
		self.bullet_set = set()  # 子弹集合
		self.grass_widget_items = dict()  # 记录植物
		self.map_dict = dict()  # 地图
		self.cursor_str_item_dict = {
			":images/plants/SunFlower/SunFlower1_static.png": SunFlower,
			":images/plants/SunShroom/SunShroom_static.png": SunMushroom,
			":images/plants/Peashooter/Peashooter_static.png": PeaShooter,
			":images/plants/WallNut/WallNut_static.png": WallNut,
			":images/plants/SnowPea/SnowPea_static.png": IcePea,
			":images/plants/CherryBomb/CherryBomb_static.png": CherryBoom,
			":images/plants/Repeater/Repeater_static.png": RepeaterPeaShooter,
			":images/plants/TallNut/TallnutCracked_static.png": MacadamiaNut,
			":images/plants/PuffShroom/PuffShroom_static.png": LittleSproutMushroomShooter,
			":images/plants/ScaredyShroom/ScaredyShroom_static.png": FearMushroom,
			":images/plants/Jalapeno/Jalapeno_static.png": Jalapeno,
			":images/plants/Squash/Squash_static.png": Pumpkin,
			":images/plants/PotatoMine/PotatoMine_static.png": PotatoMine,
			":images/plants/Chomper/Chomper_static.png": Chomper,
			":images/plants/Spikeweed/Spikeweed_static.png": Lurker,
			":images/plants/IceShroom/IceShroom_static.png": FrostMushroom,
			":images/plants/WaterMelon/watermelon_static.png": Watermelon,
			":images/plants/Cactus/Cactus_static.png": Cactus,
			":images/plants/SeaShroom/SeaShroom_static.png": SeaShroomShooter,
			":images/plants/DoomShroom/BeginBoom_static.png": DoomShroom,
			":images/plants/TangleKlep/TangleKlep_static.png": TangleKelp,
			":images/plants/Cornpult/full_idle_static.png": CobCannon,
			":images/plants/Cabbagepult/cabbage_static.png": Cabbage,
			":images/plants/Cattail/CatTail_static.png": CatTail,
			":images/plants/Torchwood/Torchwood_static.png": Torchwood,
			":images/plants/Threepeater/three_pea_static.png": ThreeShooter,
			":images/plants/HypnoShroom/HypnoShroom_static.png": HypnoShroom,
			":images/plants/MagnetShroom/MagnetShroom_static.png": MagnetShroom,
			":images/plants/SplitPea/SplitPea_static.png": SplitPeaShooter,
			":images/plants/Marigold/idle_static.png": Marigold,
			":images/plants/SunFlower/TwinSunflower_static.png": TwinSunFlower,
			":images/plants/GoldMagnet/idle_static.png": GoldMagnet,
			":images/plants/WinterMelon/idle_static.png": WinterMelon,
			":images/plants/Spikerock/idle_static.png": SpikerRock,
			":images/plants/GatlingPea/idle_static.png": GatlingPeaShooter,
			":images/plants/CoffeeBean/CoffeeBean_static.png": CoffeeBean,
			":images/plants/GraveBuster/idle_static.png": GraveBuster,
			":images/plants/Blover/Blover_static.png": Blover,
			":images/plants/FumeShroom/FumeShroom_static.png": FumeMushroomShooter,
			":images/plants/GloomShroom/idle_static.png": GloomShroom,
			":images/plants/Starfruit/Starfruit_static.png": StarFruit,
			":images/plants/Garlic/Garlic_static.png": Garlic,
			":images/plants/Umbrellaleaf/idle_static.png": UmbrellaLeaf,
		}  # 鼠标样式-植物实体对应关系
		self.placeholder_item_id_dict = {
			100: TombStoneItem,
			101: BuryItem,
			102: IceItem,
		}  # 占位植物id-实体对应关系
		self.zombie_id_item_dict = {
			1: RegularZombie,
			2: ConeheadZombie,
			3: BucketheadZombie,
			4: FlagZombie,
			5: RubyZombie,
			6: IronGateZombie,
			7: NewsPaperZombie,
			8: PoleVaultZombie,
			9: RegularSwimmingZombie,
			10: BucketheadSwimmingZombie,
			11: DiveZombie,
			12: ConeheadSwimmingZombie,
			13: ZomboniZombie,
			14: ImpZombie,
			15: CataPultZombie,
			16: DancerZombie,
			17: DacnerPartnerZombie,
			18: LadderZombie,
			19: DiscoZombie,
			20: DiscoPartnerZombie,
			21: PogoZombie,
			22: BalloonZombie,
			23: DiggerZombie,
			24: JokerZombie,
			25: RedGargantuar,
			26: WhiteGargantuar,
			27: DolphinRiderZombie,
		}  # 僵尸id-僵尸对应关系
		self.hp_visible_flag = False  # 是否显示体力
		self.index_map_dict = {
			1: DayTimeMap,
			2: NightMap,
			3: SwimmingMap,
			4: NightSwimmingMap,
		}

	def map_init(self):
		# 地图-地图实体对应关系
		self.map_item = self.index_map_dict[self.map_id]()
		self.map_id = self.map_item.map_id

	def ui_param_init(self):
		self.row_y_list = self.gameScene.lawn.row_y_list
		self.lawn_mower_line_dict = dict()
		self.zombie_line_x = self.gameScene.lawn.width()
		self.grass_items = self.gameScene.lawn.grass_items

	def timer_init(self):
		# 定时掉落阳光
		self.auto_sunshine_timer = QTimer(self)
		self.auto_sunshine_timer.setInterval(2000)
		self.auto_sunshine_timer.timeout.connect(self.create_auto_sunflower)

	def game_init(self):
		"""
		游戏初始化
		:return:
		"""
		self.game_seconds = 0  # 当前游戏秒数
		self.clear_game_scene()
		self.gameScene.set_bg_pic(self.map_item.bg_pic)
		base_sunshine = self.map_item.base_sunshine
		zombie_id_list = self.map_item.zombie_id_list  # 地图中会出现的僵尸id列表
		self.gameScene.gameProgressWidget.game_level.setText("冒险模式 " + self.map_item.name)
		self.gameScene.gameProgressWidget.game_level_mode.setText(self.map_item.game_mode)
		self.gamePrepareScene.plantSelectWidget.selectedCardsBasket.sunFlowerBasket.current_sun_label.setText(
			str(base_sunshine))  # 初始阳光值
		self.gamePrepareScene.zombiePrepareArea.load_zombies(zombie_id_list)
		self.is_swimming_map = self.map_item.is_swimming_map
		self.map_dict = self.map_item.map_dict
		self.grass_width = normal_conf.swimming_grass_width if self.is_swimming_map else normal_conf.noswimming_grass_width
		self.gameScene.gameProgressWidget.set_flags(self.map_dict)
		self.map_time_list = list(self.map_dict.keys())
		self.sunshine_value = base_sunshine  # 当前阳光数
		self.process_sunshine(0, "plus", "nature")  # 初始化阳光数
		self.map_timer = QTimer(self)  # 地图定时器
		self.map_timer.setInterval(1000)
		self.map_timer.timeout.connect(self.load_map)
		self.game_status = 0  # 游戏是否结束0未结束 1失败 2 通关
		self.pause_status = False  # 游戏是否暂停了
		self.dave_is_shown = False  # 疯狂戴夫场景是否展示过

	# 清理游戏场景内临时参数

	def ui_init(self):
		self.setFixedSize(QSize(1230, 800))
		self.setWindowIcon(QIcon(":images/others/icon.ico"))
		self.setWindowTitle(game_conf.game_name)
		self.stacked_widget = SlidingStackedWidget(self)
		self.gameLoadingBG = GameLoadingScene(self)  # 游戏加载界面
		self.gameStartBG = GameStartScene(self)  # 游戏模式选择界面
		self.crazyDaveScene = CrazyDaveScene(self)  # 疯狂戴夫场景
		self.gameLevelSelectScene = GameLevelSelectScene(self)  # 游戏关卡选择场景
		self.gamePrepareScene = GamePrepareScene(self)  # 游戏开始前等待场景
		self.gameScene = GameScene(self, self.map_id)  # 游戏场景
		self.gameMoviePlayPage = GameMoviePlayPage(self)  # 游戏结束场景
		self.almanacWidget = AlmanacWidget(self)  # 图鉴
		self.stacked_widget.addWidget(self.gameLoadingBG)  # 0
		self.stacked_widget.addWidget(self.gameStartBG)  # 1
		self.stacked_widget.addWidget(self.gameLevelSelectScene)  # 2
		self.stacked_widget.addWidget(self.gamePrepareScene)  # 3
		self.stacked_widget.addWidget(self.gameScene)  # 4
		self.stacked_widget.addWidget(self.gameMoviePlayPage)  # 5
		self.stacked_widget.addWidget(self.crazyDaveScene)  # 6
		self.stacked_widget.addWidget(self.almanacWidget)  # 7
		self.setCentralWidget(self.stacked_widget)
		self.menuDialog = MenuDialog(self)
		self.menuDialog.hide()
		# 消息背景蒙层
		self.overlay = QWidget(self)
		self.setObjectName("overlay")
		self.overlay.setAutoFillBackground(True)
		palette = self.overlay.palette()
		palette.setColor(QPalette.Window, QColor(70, 70, 70, 100))
		self.overlay.setPalette(palette)
		self.overlay.hide()  # 默认隐藏 只有弹消息才会展示
		sunflower_basket = self.gameScene.plantCardBasket.sunFlowerBasket
		global_pos = sunflower_basket.mapToGlobal(QPoint(sunflower_basket.pos().x() + 150,
														 sunflower_basket.pos().y() + 5))
		self.sunshine_basket_pos = self.mapFromGlobal(global_pos)
		# 植物提示组件
		self.plantToolTip = PlantToolTip(self)
		self.plantToolTip.hide()
		# 灰烬
		self.ashFire = AshFire(self)
		self.ashFire.hide()
		# 冰蘑菇特效
		self.frost = Frost(self)
		self.frost.hide()
		# 开场倒计时
		self.countdownElement = CountdownElement(self)
		self.countdownElement.move(QPoint(int(self.width() / 2 - self.countdownElement.width() / 2),
										  int(self.height() / 2 - self.countdownElement.height() / 2)))
		self.countdownElement.hide()
		# 加载关卡
		self.gameLevelSelectScene.load_levels(level_list)
		# 游戏内提示文字
		self.tipWidget = TipWidget(self)
		self.tipWidget.setFixedWidth(self.width())
		self.tipWidget.move(QPoint(0, int(self.height() - self.tipWidget.height() - 25)))
		self.tipWidget.hide()

		self.gameOverDialog = GameOverDialog(self)
		self.gameOverDialog.hide()

	def slot_init(self):
		bus.lawn_chunk_clicked.connect(lambda lawn_tuple: self.set_lawn_plant(lawn_tuple))
		bus.sunshine_produced.connect(lambda value: self.process_sunshine(value, "plus", "nature"))
		bus.sunshine_cost.connect(lambda value: self.process_sunshine(value, "min"))
		bus.sunshine_finished.connect(lambda: self.process_sunshine(0, "plus", "nature"))
		bus.effect_changed.connect(lambda effect_key: self.play_sound_effect(effect_key))
		bus.cursor_changed.connect(lambda static_pix: self.set_plant_cursor(static_pix))
		# bus.game_finished.connect(lambda game_status: self.set_game_status(game_status))
		bus.game_node_changed.connect(
			lambda node_type: self.change_node_sound_effect(node_type))
		bus.card_hovered.connect(
			lambda plant_obj, status: self.show_card_toolTip(plant_obj, status))
		bus.plant_cooling_finished.connect(self.refresh_plant_cards_status)
		bus.game_level_selected.connect(lambda level_dict: self.set_current_level(level_dict))
		self.gameScene.menu_btn.clicked.connect(self.show_menu)
		self.menuDialog.cancel_btn.clicked.connect(self.close_menu)
		self.menuDialog.back_btn.clicked.connect(self.close_menu)
		self.stacked_widget.currentChanged.connect(self.on_game_scene_changed)
		self.gameLoadingBG.start_btn.clicked.connect(lambda: self.change_stacked_index(1))
		self.gameStartBG.game_mode_selected.connect(lambda: self.change_stacked_index(2))
		self.gamePrepareScene.plantSelectWidget.plantSelectBasket.startRockBtn.clicked.connect(self.game_start)
		self.gamePrepareScene.plantSelectWidget.plantSelectBasket.showAlmanacBtn.clicked.connect(
			lambda: self.change_stacked_index(7))
		self.gameStartBG.mainSetDialog.mianSetItems.bg_music_slider.valueChanged.connect(
			lambda value: self.bgm_player.setVolume(value))
		self.gameStartBG.quitGameDialog.quite_game_signal.connect(self.close)  # 确认退出游戏
		self.gameLevelSelectScene.back_menu_btn.clicked.connect(lambda: self.change_stacked_index(1))
		self.crazyDaveScene.daveWidget.finished.connect(
			lambda: self.change_stacked_index(3))  # 跳转到选择卡片
		self.almanacWidget.almanac_closed.connect(lambda: self.almanacWidget.stacked_widget.setCurrentIndex(0))
		self.almanacWidget.zombieAlmanacDetailPage.close_btn.clicked.connect(lambda: self.change_stacked_index(7))
		self.almanacWidget.almanacIndexPage.close_btn.clicked.connect(lambda: self.change_stacked_index(3))
		self.gameOverDialog.confirm_btn.clicked.connect(self.confirm_game_lose)
		self.gameStartBG.mainSetDialog.mianSetItems.show_hp_check_box.stateChanged.connect(self.control_hp_flag)

	def control_hp_flag(self, state):
		"""
		控制是否显示体力
		"""
		if state != self.hp_visible_flag:
			self.hp_visible_flag = state
			self.normal_control("hp")

	def confirm_game_lose(self):
		"""
		确认游戏失败 返回关卡选择页面
		"""
		self.clear_game_scene()
		self.change_stacked_index(2)

	def clear_game_scene(self):
		"""
		每次游戏成功or失败 都清理一下游戏场景
		"""
		if self.auto_sunshine_timer.isActive():
			self.auto_sunshine_timer.stop()
		for each_zombie in list(self.zombie_set):
			try:
				each_zombie.deleteLater()
			except:
				pass
		for each_bullet in list(self.bullet_set):
			try:
				each_bullet.deleteLater()
			except:
				pass
		for each_mover_pack in self.lawn_mower_line_dict.values():
			try:
				each_mover_pack[0].deleteLater()
			except:
				pass
		self.gamePrepareScene.plantSelectWidget.selectedCardsBasket.clear_cards()
		self.gamePrepareScene.plantSelectWidget.clear_selected_cards()
		for each_plant in list(self.plant_set):
			self.clear_plant_item(each_plant, False, force=True)
		for grass_item in self.grass_items.values():
			grass_item.clear_plant()  # 清理掉植物
		self.lawn_mower_line_dict.clear()
		self.plant_set.clear()
		self.zombie_set.clear()
		self.bullet_set.clear()
		self.grass_widget_items.clear()
		self.gameScene.gameProgressWidget.progressWidget.clear_flags()

	def change_stacked_index(self, aim_index):
		"""
		更改堆栈组件索引
		"""
		self.stacked_widget.setCurrentIndex(aim_index)

	def game_start(self):
		self.stacked_widget.setCurrentIndex(4)
		QTimer.singleShot(300, self.load_lawn_mowers)

	def set_current_level(self, level_dict):
		"""
		设置地图关卡
		"""
		self.current_level = level_dict['level']
		self.map_id = level_dict['map_id']
		self.map_init()
		self.gamePrepareScene.set_prepare_scene(self.map_id)
		self.gameScene.lawn.load_map_ui(self.map_id, self.game_ui_not_loaded)
		self.grass_items = self.gameScene.lawn.grass_items
		self.crazyDaveScene.set_map_bg(self.map_item.prepare_bg_pic)
		self.gamePrepareScene.set_map_bg(self.map_item.prepare_bg_pic)
		self.ui_param_init()
		self.game_init()
		self.gen_random_tomb()
		self.change_stacked_index(6) if self.current_level == 1 else self.change_stacked_index(3)
		if 0:
			# self.normal_control("hp")  # 显示体力
			self.sunshine_value = 10000
		self.game_ui_not_loaded = False

	def on_game_scene_changed(self, index):
		"""
		切换了游戏页面
		"""
		if index in [1, 2, 3, 7]:  # 处理loading 和选择、图鉴页面bgm
			self.set_bgm(normal_conf.index_bgm_dict[index])
			if index == 2:  # 游戏场景
				self.gameLevelSelectScene.update_game_level()  # 更新关卡状态f
		elif index == 4:  # 游戏场景
			self.show_countdown()  # 展示游戏开始倒计时
		elif index == 6:  # 戴夫场景
			bus.effect_changed.emit("dave00")
			self.dave_is_shown = True  # 疯狂戴夫场景已经展示过
		if index != 1:
			if self.gameStartBG.twinkle_timer.isActive():
				self.gameStartBG.twinkle_timer.stop()

	def process_sunshine(self, value, op, from_=""):
		"""
		添加或者减少阳光数
		:return:
		"""
		if from_ == "nature":
			self.auto_sunshine_shown = False
		if op == "min":
			self.sunshine_value -= value
		elif op == "plus":
			self.sunshine_value += value
		else:
			return
		self.gameScene.plantCardBasket.sunFlowerBasket.change_current_sun_num(self.sunshine_value)  # 更新阳光数
		self.refresh_plant_cards_status()
		if from_ in ["sf_", "sm_"]:  # 向日葵或者阳光菇
			bus.effect_changed.emit("collect_sf")

	def check_bullet_lines(self, aim_line, bullet_id):
		"""
		检测目标行是否存在僵尸
		:return:
		"""
		try:
			zombie_list = self.zombie_set
			if bullet_id == 10 and len(zombie_list) > 0:
				return True
			else:
				for each_zombie in zombie_list:
					if each_zombie.row_index == aim_line and each_zombie.zombie_level == 1 and each_zombie.is_hypno is False:
						return True
		except:
			traceback.print_exc()
		return False

	def show_bullet(self, item_item, start_pos, direction, bullet_id, bullet_line):
		"""
		展示子弹
		:return:
		"""
		try:
			item_id = item_item.plant_id
		except AttributeError:
			item_id = item_item.zombie_id
		if item_id in [25, 45]:
			pass
		else:
			if self.check_bullet_lines(bullet_line, bullet_id) is False: return  # 所在行没有僵尸 不需要创建子弹
		if bullet_id == 1:
			if item_id == 30 and direction == QPoint(-1, 0):  # 如果是往左攻击 则修正初始x值
				bullet = PeaBullet(self, start_pos=QPoint(int(start_pos.x() - item_item.width()),
														  int(start_pos.y())), direction=direction,
								   line_index=bullet_line)
			else:
				if item_id == 34:  # 机枪射手
					y_offset = item_item.height() * 0.25
					bullet = PeaBullet(self, QPoint(start_pos.x(),
													int(start_pos.y() + y_offset)), direction=direction,
									   line_index=bullet_line)
				else:
					bullet = PeaBullet(self, start_pos=start_pos, direction=direction, line_index=bullet_line)
			self.play_sound_effect("throw")
		elif bullet_id == 2:
			bullet = IcePeaBullet(self, start_pos=start_pos, direction=direction, line_index=bullet_line)
		elif bullet_id == 3:
			if item_id == 13:  # 胆小菇
				y_offset = item_item.height() * 0.5  # 修改y偏移量
			else:
				y_offset = item_item.height() * 0.7
			bullet = SproutMushroomBullet(self, start_pos=QPoint(start_pos.x(),
																 int(start_pos.y() + y_offset)),
										  direction=direction, line_index=bullet_line)
			self.play_sound_effect("puff")
		elif bullet_id == 16:  # 海蘑菇子弹
			y_offset = item_item.height() * 0.7
			bullet = SproutMushroomBullet(self, start_pos=QPoint(start_pos.x(),
																 int(start_pos.y() + y_offset)),
										  direction=direction, line_index=bullet_line)
		elif bullet_id == 12:  # 大喷菇烟雾
			y_offset = item_item.height() * 0.1
			bullet = FumeMushroomBullet(self, start_pos=QPoint(start_pos.x(), int(start_pos.y() + y_offset)),
										line_index=bullet_line, col_index=item_item.col_index)
			self.play_sound_effect("fume")
		elif bullet_id == 4:  # 西瓜
			bullet = MelonBullet(self, start_pos=start_pos, line_index=bullet_line)
		elif bullet_id == 10:  # 僵尸篮球
			self.play_sound_effect("basketball")
			bullet = BasketballBullet(self, start_pos=start_pos, line_index=bullet_line)
		elif bullet_id == 14:  # 冰西瓜
			bullet = IceMelonBullet(self, start_pos=start_pos, line_index=bullet_line)
		elif bullet_id == 15:  # 杨桃星星
			x_offset = item_item.width() * 0.3  # 修改y偏移量
			y_offset = item_item.height() * 0.3  # 修改y偏移量
			bullet = StarBullet(self, start_pos=QPoint(start_pos.x() - x_offset,
													   int(start_pos.y() + y_offset)), direction=direction)
		elif bullet_id == 7:  # 玉米粒
			bullet = ButterDotBullet(self, start_pos=start_pos, line_index=bullet_line)
		elif bullet_id == 8:  # 黄油
			bullet = ButterBullet(self, start_pos=start_pos, line_index=bullet_line)
		elif bullet_id == 9:  # 卷心菜
			bullet = CabbageBullet(self, start_pos=start_pos, line_index=bullet_line)
		elif bullet_id == 6:  # 香蒲针刺
			bullet = CatTailThornBullet(self, start_pos=start_pos, line_index=bullet_line)
		elif bullet_id == 5:
			y_offset = item_item.height() * 0.34  # 修改y偏移量
			bullet = ThornBullet(self, start_pos=QPoint(start_pos.x(),
														int(start_pos.y() + y_offset)), direction=direction,
								 line_index=bullet_line)
		else:
			return
		bullet.bullet_hit_signal.connect(lambda effect_key: self.play_sound_effect(effect_key))
		if bullet_id != 6:
			bullet.show()
		if bullet_id == 2 and random.randint(1, 3) == 1:  # 冰霜豌豆播放冰霜声音
			self.play_sound_effect("snow_pea_sparkles")
		self.bullet_set.add(bullet)

	def refresh_plant_cards_status(self, index=-1):
		# 刷新卡槽
		card_list = self.gameScene.plantCardBasket.card_list
		if index == -1:
			for card in card_list:
				card.change_card_status(card.cost <= self.sunshine_value)
		else:
			card_list[index].cooling_start()

	def player_init(self):
		"""
		背景音乐
		使用QMediaPlayer播放背景音乐
		:return:
		"""
		self.bgm_player = QMediaPlayer(self)  # 背景音乐
		self.bgm_player.setVolume(self.bgm_volume)  # 设置背景音乐音量
		self.playlist = QMediaPlaylist(self)

	def set_bgm(self, bgm_qrc):
		"""
		更改背景音乐
		:param bgm_qrc:
		:return:
		"""
		self.playlist.clear()
		self.playlist.addMedia(QMediaContent(QUrl(bgm_qrc)))  # 这样使用qrc资源
		self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
		self.bgm_player.setPlaylist(self.playlist)
		self.bgm_player.play()

	def set_plant_cursor(self, put_pix):
		"""
		更改鼠标样式
		:param put_pix:
		:return:
		"""
		self.change_cursor_style(put_pix)

	def change_cursor_style(self, pix):
		"""
		更改鼠标样式
		:param pix:
		:return:
		"""
		self.current_put_pix_str = pix
		cursor = QCursor(QPixmap(pix))
		self.setCursor(cursor)

	def set_lawn_plant(self, lawn_tuple):
		"""
		在草坪上种植植物
		:param lawn_tuple:
		:return:
		"""
		if not self.current_put_pix_str: return
		# 处理铲子
		if "shovel" in self.current_put_pix_str:  # 如果放置的是铲子
			if lawn_tuple in self.grass_widget_items.keys():
				self.clear_plant_item(self.grass_widget_items[lawn_tuple], play_eaten_effect=False)
			self.gameScene.plantCardBasket.shovelBasket.change_shovel_status(True)  # 设置有铲子
			bus.effect_changed.emit("shovel")  # 种植植物音效
		else:
			# 种植植物逻辑
			if self.current_put_pix_str not in self.cursor_str_item_dict.keys(): return
			plant_item = self.cursor_str_item_dict[self.current_put_pix_str](self)
			plant_item.setParent(self)
			if self.plant_new_plant(plant_item, lawn_tuple) is False: return
			new_plant_id = plant_item.plant_id
			self.gameScene.plantCardBasket.card_dict[new_plant_id].cooling_start()
			# 刷新冷却
			plant_id_list = [plant_id_ for plant_id_ in self.gameScene.plantCardBasket.card_dict.keys()]
			self.gameScene.plantCardBasket.start_each_cooling(
				self.gameScene.plantCardBasket.card_list[plant_id_list.index(new_plant_id)])
			bus.effect_changed.emit("plant")  # 种植植物音效
		self.change_cursor_style("")
		self.current_put_pix_str = ""  # 放置成功后清空当前植物

	def plant_new_plant(self, plant_item, lawn_tuple, force_remove=False):
		"""
		在指定位置种植新的植物
		"""
		aim_grass_item = self.grass_items[lawn_tuple]
		plant_type = plant_item.plant_type
		if plant_type == 0:  # 植物类型
			for_upgrade_id = plant_item.for_upgrade_id
			if lawn_tuple in self.grass_widget_items.keys():
				exists_plant_item = self.grass_widget_items[lawn_tuple]
				if plant_item.for_upgrade is True and for_upgrade_id == exists_plant_item.plant_id:
					self.clear_plant_item(exists_plant_item, play_eaten_effect=False)  # 升级现有植物
				elif plant_item.plant_id == 39 and exists_plant_item.plant_id == 100:  # 处理墓碑吞噬者逻辑
					plant_item.start_buster(exists_plant_item)  # 开始吞噬墓碑
					self.gen_coins(plant_item, 1)
				elif exists_plant_item.plant_type == 1:  # 如果现存的是中立植物 比如：冰、坑 直接略过
					self.show_game_tip("你不能把植物种在这里！")
					return False
				else:
					self.show_game_tip("你不能把植物种在这里！")
					return False
			else:
				if plant_item.for_upgrade is True:
					aim_plant_name = get_aim_item_data(for_upgrade_id, normal_conf.plant_param_dict, "cn_name")
					self.show_game_tip("只能种在{}上".format(aim_plant_name))
					return False  # 不允许直接种紫卡
				if plant_item.plant_id == 39:
					return False  # 不允许直接种墓碑吞噬者
		aim_grass_item.set_plant_item(plant_item, self.hp_visible_flag)
		bullet_row_index = lawn_tuple[0]  # 子弹所在行数
		bullet_col_index = lawn_tuple[1]  # 子弹所在列数
		plant_item.row_index = bullet_row_index  # 设置植物所在行
		plant_item.col_index = bullet_col_index  # 设置植物所在列
		new_plant_pos = plant_item.pos()
		new_plant_pos_x = int(new_plant_pos.x() + aim_grass_item.width() * 0.7)
		bullet_base_pos = QPoint(new_plant_pos_x, new_plant_pos.y())
		new_plant_id = plant_item.plant_id
		if new_plant_id == 1:  # 向日葵
			plant_item.new_sunshine_produced.connect(lambda value: self.process_sunshine(value, "plus", "sf_"))
		elif new_plant_id in [2, 6, 30, 34]:  # 豌豆射手、双发射手、裂荚射手、机枪射手
			plant_item.new_bullet_created.connect(
				lambda direction: self.show_bullet(
					plant_item, plant_item.mapTo(self, bullet_base_pos),
					direction, 1, bullet_row_index))
		elif new_plant_id == 27:  # 三线射手
			top_pos = QPoint(bullet_base_pos.x(), bullet_base_pos.y() - normal_conf.noswimming_grass_height)
			bottom_pos = QPoint(bullet_base_pos.x(),
								bullet_base_pos.y() + normal_conf.noswimming_grass_height + plant_item.height_ / 2)
			# 创建三枚子弹
			if bullet_row_index - 1 >= 0:  # 如果植物放在了第一行 就不创建顶部的子弹了
				plant_item.new_bullet_created.connect(
					lambda direction: self.show_bullet(
						plant_item, plant_item.mapTo(self, top_pos),
						direction, 1, bullet_row_index - 1))
			plant_item.new_bullet_created.connect(
				lambda direction: self.show_bullet(
					plant_item, plant_item.mapTo(self, bullet_base_pos),
					direction, 1, bullet_row_index))
			plant_item.new_bullet_created.connect(
				lambda direction: self.show_bullet(
					plant_item, plant_item.mapTo(self, bottom_pos),
					direction, 1, bullet_row_index + 1))
		elif new_plant_id == 4:  # 寒冰豌豆射手
			plant_item.new_bullet_created.connect(
				lambda direction: self.show_bullet(
					plant_item, plant_item.mapTo(self, bullet_base_pos),
					direction, 2, bullet_row_index))
		elif new_plant_id == 45:  # 杨桃
			plant_item.new_bullet_created.connect(
				lambda direction: self.show_bullet(
					plant_item, plant_item.mapTo(self, bullet_base_pos),
					direction, 15, bullet_row_index))
		elif new_plant_id == 18:  # 仙人掌
			plant_item.new_bullet_created.connect(
				lambda direction: self.show_bullet(
					plant_item, plant_item.mapTo(self, bullet_base_pos),
					direction, 5, bullet_row_index))
		elif new_plant_id == 9:  # 小喷姑
			plant_item.new_bullet_created.connect(
				lambda direction: self.show_bullet(
					plant_item, plant_item.mapTo(self, bullet_base_pos),
					direction, 3, bullet_row_index))
		elif new_plant_id == 38:  # 大喷姑
			plant_item.new_bullet_created.connect(
				lambda direction: self.show_bullet(
					plant_item, plant_item.mapTo(self, bullet_base_pos),
					direction, 12, bullet_row_index))
		elif new_plant_id == 20:  # 海蘑菇
			plant_item.new_bullet_created.connect(
				lambda direction: self.show_bullet(
					plant_item, plant_item.mapTo(self, bullet_base_pos),
					direction, 16, bullet_row_index))
		elif new_plant_id == 13:  # 胆小菇
			plant_item.new_bullet_created.connect(
				lambda direction: self.show_bullet(
					plant_item, plant_item.mapTo(self, bullet_base_pos),
					direction, 3, bullet_row_index))
		elif new_plant_id == 31:  # 金盏花
			plant_item.new_coin_gen.connect(
				lambda: self.gen_coins(plant_item, 1))
		elif new_plant_id == 19:  # 西瓜投手
			plant_item.new_bullet_created.connect(
				lambda direction: self.show_bullet(
					plant_item, plant_item.mapTo(self, bullet_base_pos),
					direction, 4, bullet_row_index))
		elif new_plant_id == 35:  # 冰西瓜投手
			plant_item.new_bullet_created.connect(
				lambda direction: self.show_bullet(
					plant_item, plant_item.mapTo(self, bullet_base_pos),
					direction, 14, bullet_row_index))
		elif new_plant_id == 23:  # 玉米投手
			plant_item.cob_bullet_created.connect(
				lambda direction, bullet_id: self.show_bullet(
					plant_item, plant_item.mapTo(self, bullet_base_pos),
					direction, bullet_id, bullet_row_index))
		elif new_plant_id == 24:  # 卷心菜投手
			plant_item.new_bullet_created.connect(
				lambda direction: self.show_bullet(
					plant_item, plant_item.mapTo(self, bullet_base_pos),
					direction, 9, bullet_row_index))
		elif new_plant_id == 25:  # 香蒲
			plant_item.new_bullet_created.connect(
				lambda direction: self.show_bullet(
					plant_item, plant_item.mapTo(self, bullet_base_pos),
					direction, 6, bullet_row_index))
		elif new_plant_id == 5:  # 樱桃炸弹
			plant_item.boom_finished.connect(
				lambda range_effect: self.set_range_damage(plant_item,
														   range_effect,
														   ))
			plant_item.boom_timer.start()
		elif new_plant_id == 21:  # 缠绕水藻
			plant_item.flash_finished.connect(
				lambda:
				self.play_sound_effect("floop"))
		elif new_plant_id == 28:  # 魅惑蘑菇
			plant_item.charm_created.connect(
				lambda:
				self.play_sound_effect("floop"))
		elif new_plant_id == 33:  # 大蒜
			plant_item.on_zombie_sick.connect(
				lambda:
				self.play_sound_effect("yuck"))
		elif new_plant_id == 43:  # 三叶草
			plant_item.prepare_blow()
			self.play_sound_effect("blover")
		elif new_plant_id == 22:  # 毁灭菇
			plant_item.boom_finished.connect(
				lambda range_effect: self.set_range_damage(plant_item,
														   range_effect,
														   ))
			plant_item.bury_gen_signal.connect(lambda plant_law_tuple: self.add_placeholder_item(101, plant_law_tuple))
			plant_item.boom_timer.start()
		elif new_plant_id == 7:  # 火爆辣椒
			plant_item.boom_finished.connect(
				lambda range_effect: self.set_range_damage(plant_item,
														   range_effect,
														   ))
			plant_item.boom_timer.start()
		elif new_plant_id == 8:  # 倭瓜
			plant_item.boom_finished.connect(
				lambda range_effect: self.set_range_damage(plant_item,
														   range_effect,
														   ))
			plant_item.boom_timer.start()
		elif new_plant_id == 11:  # 阳光菇长大
			plant_item.grow_finished.connect(lambda: self.play_sound_effect("plant_grow"))
			plant_item.new_sunshine_produced.connect(lambda value: self.process_sunshine(value, "plus", "sm_"))
		elif new_plant_id == 12:  # 土豆地雷
			plant_item.boom_finished.connect(
				lambda range_effect: self.set_range_damage(plant_item,
														   range_effect,
														   ))
		elif new_plant_id == 16:  # 冰蘑菇
			plant_item.boom_finished.connect(
				lambda range_effect: self.set_range_damage(plant_item,
														   range_effect,
														   ))
			plant_item.boom_timer.start()
		elif new_plant_id == 14:  # 食人花
			plant_item.boom_finished.connect(
				lambda range_effect: self.set_range_damage(plant_item,
														   range_effect,
														   ))
		elif new_plant_id == 15:  # 地刺
			plant_item.boom_finished.connect(
				lambda range_effect: self.set_range_damage(plant_item,
														   range_effect,
														   ))
			plant_item.lurker_timer.start()
		elif new_plant_id == 36:  # 地刺王
			plant_item.boom_finished.connect(
				lambda range_effect: self.set_range_damage(plant_item,
														   range_effect,
														   ))
			plant_item.lurker_timer.start()
		elif new_plant_id == 37:  # 咖啡豆
			self.play_sound_effect("wakeup")
			plant_item.wake_up_finished.connect(lambda plant_item: self.wake_up_plant(plant_item))
		elif new_plant_id == 39:  # 墓碑吞噬者
			self.play_sound_effect("gravebusterchomp")
			plant_item.buster_finished.connect(lambda tomb_item: self.clear_plant_item(tomb_item, False))
		# 连接新植物信号
		plant_item.plant_died.connect(lambda plant_obj: self.clear_plant_item(plant_obj, force=force_remove))
		plant_item.plant_hp_changed.connect(lambda _: bus.effect_changed.emit("zombie_eating"))
		self.plant_set.add(plant_item)  # 将植物存起来
		self.grass_widget_items[lawn_tuple] = plant_item
		return True

	def wake_up_plant(self, plant_item):
		"""
		唤醒白天睡觉的植物
		"""

	def clear_plant_item(self, plant_item, play_eaten_effect=True, force=False):
		"""
		删除一个植物
		:param plant_item:
		:return:
		"""
		lawn_tuple = (plant_item.row_index, plant_item.col_index)
		try:
			if isinstance(lawn_tuple, tuple):
				if lawn_tuple not in self.grass_widget_items.keys(): return
				plant_item = self.grass_widget_items[lawn_tuple]
			else:
				plant_item = lawn_tuple
			if plant_item.plant_type != 0 and force is False: return  # 如果尝试铲除中立植物
			self.grass_widget_items.pop(lawn_tuple)
			self.grass_items[lawn_tuple].clear_plant()  # 清除原来的植物
		except:
			traceback.print_exc()
		try:
			if plant_item.plant_id not in [5, 7, 8, 12, 15, 16, 21,
										   22, 28, 43] and plant_item.plant_type != 1 and play_eaten_effect is True:
				self.play_sound_effect("eaten")  # 植物被吃掉了
			remove_list_item(plant_item, self.plant_set)
			for key, value in list(self.grass_widget_items.items()):
				if value == plant_item:
					del self.grass_widget_items[key]
					break  # 找到并删除后退出循环
		except:
			traceback.print_exc()
		try:
			plant_item.deleteLater()
		except:
			traceback.print_exc()

	def add_zombie(self, zombie_id=-1, line_index=-1, x=-1, y=-1):
		"""
		添加一个僵尸
		:return:
		"""
		if line_index == -1:
			aim_line_index = random.randint(0, 4)
		else:
			aim_line_index = line_index
		zombie_item = self.zombie_id_item_dict[zombie_id](self)
		zombie_item.zombie_died.connect(lambda zombie_obj: remove_list_item(zombie_obj, self.zombie_set))
		zombie_item.sound_effect_changed.connect(lambda sound_effect: self.play_sound_effect(sound_effect))
		zombie_item.enter_danger_zone.connect(lambda line_index: self.set_mower_activated(line_index, zombie_item))
		zombie_item.zombie_coord_changed.connect(
			lambda line_index, row_index: self.scan_plant_pos(line_index, row_index))
		base_width = self.gameScene.lawn.width()
		zombie_line_y = self.row_y_list[aim_line_index]
		if x != -1 and y != -1:
			zombie_item.set_zombie_pos(x, zombie_line_y)
		else:
			zombie_item.set_zombie_pos(base_width, zombie_line_y)
		zombie_item.set_line(aim_line_index)
		zombie_item.set_hp_flag(self.hp_visible_flag)
		zombie_item.move(-200, -200)  # 先移出场景
		if zombie_id == 1 and random.randint(1, 3) == 1:  # 僵尸ID为1且有三分之一概率  发出声音
			self.play_sound_effect("groan")
		elif zombie_id == 4:  # 旗帜僵尸总是发出声音
			self.play_sound_effect("groan")
		elif zombie_id == 13:  # 雪橇僵尸出场
			self.play_sound_effect("zamboni")
			zombie_item.ice_gen_signal.connect(
				lambda zombie_law_tuple: self.add_placeholder_item(102, zombie_law_tuple))
		elif zombie_id == 16:  # 舞王僵尸伴舞出场
			zombie_item.partner_gen.connect(lambda partner_pos_list: self.gen_dancer_partner(17, partner_pos_list))
		elif zombie_id == 15:  # 投篮车僵尸
			new_zombie_pos = zombie_item.pos()
			new_zombie_pos_x = int(new_zombie_pos.x() + zombie_item.width() * 0.7)
			bullet_base_pos = QPoint(new_zombie_pos_x, new_zombie_pos.y())
			zombie_item.basketball_gen.connect(
				lambda: self.show_bullet(
					zombie_item, zombie_item.mapTo(self, bullet_base_pos),
					QPoint(-1, 0), 10, aim_line_index))
		elif zombie_id == 19:  # disco僵尸伴舞出场
			zombie_item.partner_gen.connect(lambda partner_pos_list: self.gen_dancer_partner(20, partner_pos_list))
		elif zombie_id == 22:  # 气球出场
			self.play_sound_effect("ballooninflate")
		elif zombie_id == 23:  # 矿工出场
			self.play_sound_effect("digger_zombie")
		elif zombie_id == 24:  # 小丑僵尸出场
			self.play_sound_effect("jackinthebox")
		elif zombie_id == 27:  # 海豚骑士出场
			self.play_sound_effect("dolphin_appears")
		if zombie_id in [13, 15]:  # 车类型僵尸死亡
			zombie_item.zombie_died.connect(lambda: self.play_sound_effect("explosion"))
		if zombie_id in [25, 26]:  # 伽刚特尔僵尸死亡
			zombie_item.zombie_died.connect(lambda: self.play_sound_effect("gargantudeath"))
		if zombie_id in [16, 19]:  # 舞王僵尸伴舞出场
			zombie_item.dancing_start.connect(lambda: self.play_sound_effect("dancing"))
		zombie_item.show()
		self.zombie_set.add(zombie_item)

	def gen_dancer_partner(self, zombie_id, partner_pos_list):
		"""
		产生伴舞僵尸
		"""
		for (zombie_x, line) in partner_pos_list:
			self.add_zombie(zombie_id, line, x=zombie_x, y=1)

	def create_auto_sunflower(self):
		"""
		创建自由下落的阳光
		:return:
		"""
		if self.auto_sunshine_shown is True: return
		autoSunflower = AutoSunflower(self.gameScene, self.sunshine_basket_pos)
		autoSunflower.show()
		autoSunflower.raise_()
		self.auto_sunshine_shown = True

	def start_suhshine_animation(self, start_x, start_y, end_x, end_y):
		# 创建动画
		self.animation = QPropertyAnimation(self, b"pos")
		self.animation.setDuration(2000)  # 动画持续时间
		self.animation.setStartValue(QPoint(start_x, start_y))
		self.animation.setEndValue(QPoint(end_x, end_y))
		# 使用抛物线效果的插值函数
		self.animation.setEasingCurve(QEasingCurve.OutQuad)
		self.animation.start()

	def play_sound_effect(self, effect_key):
		"""
		播放音效
		:return:
		"""
		if effect_key in normal_conf.muti_effect_dict.keys():
			effect_qrc = random.choice(normal_conf.muti_effect_dict[effect_key])
		else:
			if effect_key not in normal_conf.sound_effect_dict.keys(): return
			effect_qrc = normal_conf.sound_effect_dict[effect_key]
		audio_thread = AudioThread(effect_qrc, parent=self)
		audio_thread.start()

	def show_menu(self):
		"""
		展示游戏场景内的菜单
		"""
		self.normal_control("pause")
		self.menuDialog.show()
		self.overlay.show()

	def close_menu(self):
		"""
		隐藏游戏场景内的菜单
		"""
		self.normal_control("play")
		self.menuDialog.hide()
		self.overlay.hide()

	def resizeEvent(self, event):
		self.overlay.setGeometry(self.rect())
		self.frost.setGeometry(self.rect())
		super(Window, self).resizeEvent(event)

	def register_shortcut(self):
		"""
		注册全局快捷键
		:return:
		"""
		# 绑定1 控制体力条展示与隐藏
		hp_shortcut = QShortcut(QKeySequence(Qt.Key_1), self)
		hp_shortcut.setContext(Qt.ApplicationShortcut)  # 使快捷键全局有效
		hp_shortcut.activated.connect(lambda: self.normal_control("hp"))

	def normal_control(self, control_type):
		"""
		控制游戏
		:param control_type:
		:return:
		"""
		if not self.stacked_widget.currentIndex() == 4: return  # 没在游戏中直接返回
		if control_type in ["pause", "play"]:  # 播放暂停的声音
			self.play_sound_effect("pause")
		if control_type == "hp":
			self.hp_visible_flag = not self.hp_visible_flag
			self.gameStartBG.mainSetDialog.mianSetItems.show_hp_check_box.setChecked(not self.hp_visible_flag)
			try:
				for each_item in self.plant_set:  # 处理植物集合
					try:
						if each_item.plant_type == 1: continue
						each_item.hp_line.setVisible(self.hp_visible_flag)
					except:
						pass
				for each_item in self.zombie_set:  # 处理僵尸集合
					try:
						each_item.hp_line.setVisible(self.hp_visible_flag)
					except:
						pass
			except:
				traceback.print_exc()
		elif control_type == "pause":  # 暂停与继续
			for each_item in list(self.plant_set):  # 处理植物集合
				try:
					if each_item.plant_type == 1: continue
					each_item.set_pause_status()
				except:
					pass
			for each_item in list(self.zombie_set):  # 处理僵尸集合
				try:
					each_item.set_pause_status(99999)
				except:
					pass
			self.bgm_player.pause()
			if self.map_timer.isActive():
				self.map_timer.stop()
			self.pause_status = True
		elif control_type == "play":  # 暂停与继续
			for each_item in list(self.plant_set):  # 处理植物集合
				try:
					if each_item.plant_type == 1: continue
					each_item.set_unpause_status()
				except:
					pass
			for each_item in list(self.zombie_set):  # 处理僵尸集合
				try:
					each_item.set_unpause_status()
				except:
					pass
			self.bgm_player.play()
			if not self.map_timer.isActive():
				self.map_timer.start()
			self.pause_status = False

	def load_map(self):
		"""
		加载地图
		:return:
		"""
		# # 检查是否已运行超过最大游戏时长
		# 每秒钟更新标签内容
		values = []
		if self.game_seconds in set(self.map_time_list):
			values = self.map_dict[self.game_seconds]
			self.add_zombie(zombie_id=values[1], line_index=values[2])  # 产生僵尸
		self.gameScene.gameProgressWidget.update_game_process(self.game_seconds, values)
		# 更新秒数
		self.game_seconds += 1
		# 检测游戏是否胜利
		if self.game_seconds > self.map_time_list[-1] + 5:
			if len(self.zombie_set) == 0:  # 游戏通关
				self.gameLevelSelectScene.save_current_levle(str(self.current_level))  # 记录下当前关卡
				self.map_timer.stop()
				for line_index, _ in enumerate(self.gameScene.lawn.row_y_list):  # 小推车启动
					self.set_mower_activated(line_index, None, play_effect=False, do_check=False)
				for each_bullet in list(self.bullet_set):
					try:
						each_bullet.deleteLater()
					except RuntimeError:
						pass
				QTimer.singleShot(1000, lambda: self.set_game_status(2))
				# 游戏胜利
				if self.current_level == self.gameLevelSelectScene.max_level_id:
					QTimer.singleShot(5000, lambda: self.change_stacked_index(5))  # 跳转到通关页面 播放movie
				else:
					QTimer.singleShot(5000, lambda: self.change_stacked_index(2))  # 跳转到关卡选择页面

	def change_node_sound_effect(self, node_type):
		"""
		游戏节点发生改变
		:return:
		"""
		node_type_effect_dict = {
			1: "i_am_coming",
			2: "huge_wave",
			3: "huge_wave",
		}
		if node_type not in node_type_effect_dict.keys(): return
		self.play_sound_effect(node_type_effect_dict[node_type])
		if node_type == 2:
			self.countdownElement.show_count_down("big_wave")  # 展示一大波僵尸
		elif node_type == 3:
			self.gen_tomb_zombies()
			self.countdownElement.show_count_down("final_wave")  # 展示最后一波
		if node_type in [3]:
			self.gen_big_wave()  # 产生一大波僵尸
			self.gen_tomb_zombies()

	def show_card_toolTip(self, card_obj, status):
		"""
		展示卡片状态提示
		:return:
		"""
		card_pos = card_obj.mapToGlobal(QPoint(-12, card_obj.height()))
		self.plantToolTip.set_toolTip(card_obj)
		self.plantToolTip.move(card_pos)
		self.plantToolTip.setVisible(status)

	def set_range_damage(self, plant_item, range_effect):
		"""
		范围伤害植物
		:param range_plant_pos:
		:return:
		"""

		def apply_damage_to_zombies():
			zombie_list = list(self.zombie_set)  # 将集合转换为列表
			plants_with_line_check = {7}  # 火爆辣椒 单行伤害
			plants_with_single_check = {14, 15, 36}  # 食人花、地刺 无吞噬声音
			plants_with_rect_check = {5, 12, 15, 21, 22, 36}  # 樱桃炸弹、土豆地雷、地刺、毁灭菇、缠绕水草、地刺王  范围伤害
			plants_with_screen_check = {16}  # 冰蘑菇 全屏伤害
			ash_counter = 0
			for zombie in zombie_list:
				zombie_line_index = zombie.row_index
				zombie_coord = (zombie_line_index, zombie.col_index)  # 僵尸当前坐标
				if plant_id in plants_with_line_check:  # 单行伤害
					if line_index == zombie_line_index:
						if (zombie.hp - boom_damage) <= 0:
							zombie.timer.stop()
						zombie.set_ash_state(boom_damage, plant_id not in plants_with_single_check)
						ash_counter += 1
				elif plant_id in plants_with_screen_check:  # 全屏伤害
					zombie.set_moderate(plant_item.moderate, plant_item.moderate_duration)  # 减速效果
					zombie.take_damage(boom_damage, self)  # 造成伤害
					zombie.set_freeze_status(plant_item.pause_duration)
				else:
					if check_coordinate_in_range(plant_coord, range_effect, zombie_coord) is True:  # 确定是否在爆炸范围之内
						if plant_id in plants_with_rect_check:
							if (zombie.hp - boom_damage) <= 0:
								zombie.timer.stop()
							zombie.set_ash_state(boom_damage, plant_id not in plants_with_single_check)
							ash_counter += 1
			if ash_counter > 0:
				self.gen_coins(plant_item, random.randint(2, 3))  # 随机产生2-3枚金币或银币
			if plant_id in plants_with_line_check:  # 清理掉当前行冰道
				plant_list = list(self.plant_set)
				for each_plant in plant_list:
					if each_plant.plant_id == 102 and line_index == each_plant.row_index:
						each_plant.ice_clear()

		line_index = plant_item.row_index
		plant_id = plant_item.plant_id
		plant_col_index = plant_item.col_index
		plant_coord = (line_index, plant_col_index)  # 植物所在坐标
		boom_damage = plant_item.damage
		if plant_id == 5:  # 樱桃炸弹
			self.play_sound_effect("cherry_boom")
		# 计算植物范围效果
		elif plant_id == 12:  # 土豆地雷
			self.play_sound_effect("potato_mine")
		elif plant_id == 22:  # 毁灭菇
			self.play_sound_effect("doomshroom")
		elif plant_id == 16:  # 冰霜蘑菇
			self.play_sound_effect("frozen")
			self.frost.show()  # 展示冰霜特效
		elif plant_id == 14:  # 食人花
			self.play_sound_effect("bigchomp")
		elif plant_id in [15, 36]:  # 地刺、地刺王
			self.play_sound_effect("hit")
		elif plant_id == 8:  # 倭瓜
			self.play_sound_effect("squash_hmm")
		elif plant_id == 7:  # 火爆辣椒
			self.play_sound_effect("jalapeno")
			grandson_pos_global = plant_item.mapToGlobal(QPoint(0, 0))
			grandson_pos_relative = self.mapFromGlobal(grandson_pos_global)
			self.ashFire.set_ash_data(":images/plants/Jalapeno/JalapenoAttack.png", grandson_pos_relative)
			self.ashFire.show()
			QTimer.singleShot(800, self.ashFire.hide)
		apply_damage_to_zombies()

	def on_game_start(self):
		"""
		游戏开始
		"""
		# 冷却开始
		self.gameScene.plantCardBasket.load_cards(
			self.gamePrepareScene.plantSelectWidget.selectedCardsBasket.get_card_id_list())
		self.set_bgm(self.map_item.bgm)
		if self.map_id in [1, 3]:  # 设置自动向日葵
			self.auto_sunshine_timer.start()
		self.map_timer.start()  # 游戏开始

	def show_countdown(self):
		"""
		展示开场倒计时
		"""
		self.countdownElement.show_count_down("game_start")
		self.play_sound_effect("game_ready")
		self.gameScene.plantCardBasket.clear_selected_cards()
		QTimer.singleShot(3200, self.on_game_start)

	def set_game_status(self, game_status):
		"""
		设置游戏状态
		: game_status 1失败 2成功
		"""
		game_status_effect_dict = {
			1: "lose",
			2: "win",
		}
		if game_status in game_status_effect_dict.keys() and self.game_status in [1, 2]:  # 播放成功 失败音效
			self.play_sound_effect(game_status_effect_dict[game_status])
		self.game_status = game_status
		if self.game_status == 1:
			self.normal_control("pause")  # 暂停游戏，游戏失败
			self.countdownElement.show_count_down("game_lose")
			self.gameOverDialog.show()
			if self.auto_sunshine_timer.isActive():  # 停止自动向日葵
				self.auto_sunshine_timer.stop()

	def load_lawn_mowers(self):
		"""
		加载除草机
		"""
		for line_index, line_y in enumerate(self.gameScene.lawn.row_y_list):
			lawn_mower = LawnMower(self, is_swimming_pool=(line_index in [2, 3] and self.map_id in [3, 4]),
								   line_index=line_index)
			lawn_mower.show()
			lawn_mower.move(40, line_y + 60)
			self.lawn_mower_line_dict[line_index] = [lawn_mower, None]

	def set_mower_activated(self, line_index, zombie_item, play_effect=True, do_check=True):
		"""
		指定除草机出动
		"""
		self.gameScene.lower()
		zombie_id = id(zombie_item)
		if self.lawn_mower_line_dict[line_index][1] is None:  # 判断是否启动小车
			aim_mower = self.lawn_mower_line_dict[line_index][0]
			sound_effect = "lawnmower"
			if self.is_swimming_map and line_index in [3, 4]:
				sound_effect = "pool_cleaner"
			if play_effect:
				self.play_sound_effect(sound_effect)
			aim_mower.start_moving(line_index)
			self.lawn_mower_line_dict[line_index][1] = zombie_id  # 记录下僵尸id
		elif self.lawn_mower_line_dict[line_index][1] == zombie_id:  # 如果是同一只僵尸 则不处理
			pass
		else:
			if do_check:
				# 游戏失败
				self.set_game_status(1)

	def gen_random_tomb(self):
		"""
		产生随机墓碑
		"""
		if self.map_id in [2, 4]:  # 夜晚地图
			tomb_set = set()
			row_number = self.map_item.line_count  # 覆盖所有行
			min_tomb = row_number * 2 - 1
			max_tomb = row_number * 2 + 4
			tomb_count = random.randint(min_tomb, max_tomb)
			# 确定可生成墓碑的列范围
			valid_columns = [4, 6, 7, 8]  # 在第 4 到第 8 列之间生成墓碑
			if self.map_id == 4:
				valid_rows = [row for row in range(row_number) if row not in [2, 3]]  # 排除第 2 和第 3 行
			else:
				valid_rows = list(range(row_number))  # 所有行
			# 首先确保每一个有效行至少有一个墓碑
			for row in valid_rows:
				col = random.choice(valid_columns)
				lawn_tuple = (row, col)
				tomb_set.add(lawn_tuple)
				tombStoneItem = self.placeholder_item_id_dict[100](self)  # 产生墓碑
				self.plant_new_plant(tombStoneItem, lawn_tuple)

			# 随机放置剩余的墓碑
			while len(tomb_set) < tomb_count:
				row = random.choice(valid_rows)  # 从有效行中随机选择
				col = random.choice(valid_columns)
				lawn_tuple = (row, col)
				if lawn_tuple not in tomb_set:
					tomb_set.add(lawn_tuple)
					tombStoneItem = self.placeholder_item_id_dict[100](self)  # 产生墓碑
					self.plant_new_plant(tombStoneItem, lawn_tuple)

	def gen_tomb_zombies(self):
		"""
		根据游戏场景里的墓碑 生成僵尸
		"""
		if not self.map_id in [2, 4]: return  # 黑夜才出僵尸
		for plant_coord, each_plant in self.grass_widget_items.items():
			if each_plant.plant_id == 100:  # 墓碑
				tomb_x = each_plant.col_index * self.grass_width
				line_index = plant_coord[0]
				self.add_zombie(random.choice([1, 2, 3, 4]), line_index=line_index, x=tomb_x, y=1)

	def gen_big_wave(self):
		"""
		产生一大波僵尸
		"""
		for row in range(len(self.row_y_list)):
			if row in [2, 3] and self.is_swimming_map:
				zombie_id_list = [9, 10, 12]  # 产生游泳僵尸
			else:
				zombie_id_list = [1, 2, 3]  # 产生一般僵尸
			self.add_zombie(random.choice(zombie_id_list), line_index=row)

	def add_placeholder_item(self, placeholder_item_id, lawn_tuple):
		"""
		添加中立占位植物
		"""
		if lawn_tuple in self.grass_widget_items: return
		placeholder_item = self.placeholder_item_id_dict[placeholder_item_id](self)
		self.plant_new_plant(placeholder_item, lawn_tuple, placeholder_item_id)
		if placeholder_item_id == 101:
			placeholder_item.set_bury_item(self.map_id, lawn_tuple[0])

	def scan_plant_pos(self, line_index, row_index):
		"""
		僵尸格数发生了变化，做一些操作
		"""
		plant_list = list(self.plant_set)
		for each_plant in plant_list:
			if each_plant.plant_type == 1: continue  # 中立植物
			if each_plant.plant_id == 9:  # 小喷菇逻辑
				each_plant.check_shroom_attack(self.zombie_set)
			if each_plant.plant_id == 13:  # 胆小菇逻辑
				each_plant.check_self_in_danger_zone(self.zombie_set)
			if each_plant.plant_id == 8:  # 倭瓜逻辑
				each_plant.scan_zombies(self.zombie_set)
			if each_plant.plant_id == 29:  # 磁力菇逻辑
				each_plant.scan_range_zombies(self.zombie_set)

	def show_game_tip(self, text):
		"""
		展示游戏中提示
		"""
		self.tipWidget.set_tip_text(text)

	def on_currency_changed(self, currency_type):
		"""
		货币数量发生了改变
		"""
		currency_type_effect_dict = {
			1: "diamond",  # 钻石
			2: "coin",  # 金币
			3: "coin",  # 银币
		}
		if currency_type not in currency_type_effect_dict.keys(): return
		self.play_sound_effect(currency_type_effect_dict[currency_type])
		self.gameScene.currencyWidget.update_coin_count(currency_type, 1)
		self.gameScene.currencyWidget.show()

	def gen_coins(self, plant_item, count=1):
		"""
		在草坪指定位置产生银币，并在格子内随机分布
		"""
		grandson_pos_global = plant_item.mapToGlobal(QPoint(0, 0))
		grandson_pos_relative = self.mapFromGlobal(grandson_pos_global)
		for _ in range(count):
			currencyItem = CurrencyItem(self.gameScene)
			currency_type_ = random.randint(2, 3)
			random_offset_x = random.randint(-60, 60)
			random_offset_y = random.randint(-60, 60)
			currencyItem.currency_clicked.connect(
				lambda _, currency_type=currency_type_: self.on_currency_changed(currency_type)
			)
			currencyItem.set_currency_type(currency_type_)
			currencyItem.move(grandson_pos_relative + QPoint(random_offset_x, random_offset_y))
			currencyItem.show()
			currencyItem.raise_()
