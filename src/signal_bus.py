# coding:utf-8
from PyQt5.QtCore import QObject, pyqtSignal, QCoreApplication


class SignalBus(QObject):
	# 定义信号
	cursor_changed = pyqtSignal(str)  # 鼠标样式变更信号
	lawn_chunk_clicked = pyqtSignal(tuple)  # 草坪块被单击
	game_finished = pyqtSignal(bool)  # 游戏结束 0失败 1成功
	sunshine_produced = pyqtSignal(int)  # 阳光生产出来了
	sunshine_cost = pyqtSignal(int)  # 阳光被花费了
	sunshine_finished = pyqtSignal()  # 阳光生产结束了
	effect_changed = pyqtSignal(str)  # 音效改变
	plant_cooling_finished = pyqtSignal()  # 有植物冷却结束了
	game_node_changed = pyqtSignal(int)  # 游戏结点发生改变
	card_hovered = pyqtSignal(QObject, bool)  # 卡片被hover
	game_level_selected = pyqtSignal(dict)  # 关卡选择
	currency_gen = pyqtSignal(int)  # 产生了奖励货币

	def __init__(self):
		super().__init__()


bus = SignalBus()
