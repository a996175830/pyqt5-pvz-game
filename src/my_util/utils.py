import base64
import math
import os.path
import random
import sys
import traceback
from PyQt5.QtCore import QResource
from PyQt5.QtGui import QPixmap, QImage, QMovie, QColor, qRed, qGreen, qBlue, qRgb, qRgba, qAlpha

# 获取项目根目录路径 (假设根目录是当前文件的父目录)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 将项目根目录添加到 sys.path
sys.path.append(project_root)


def load_gif_from_qrc(gif_path):
	# 确保已经将.qrc文件编译为Python模块
	QResource.registerResource(gif_path)
	pixmap = QPixmap(':/path/to/your.gif')  # 替换为实际的GIF路径
	return pixmap


def pix_to_gary(pixmap):
	image = pixmap.toImage()
	image = image.convertToFormat(QImage.Format_Grayscale8)
	return QPixmap.fromImage(image)


def remove_list_item(list_item, data_list):
	"""
	从列表中移除一项
	:return:
	"""
	try:
		if list_item in data_list:
			data_list.remove(list_item)
	except:
		traceback.print_exc()


def pix_to_color(pixmap: QPixmap, color: QColor) -> QPixmap:
	"""Apply a color filter to a QPixmap."""
	image = pixmap.toImage().convertToFormat(QImage.Format_RGBA8888)
	width, height = image.width(), image.height()
	for y in range(height):
		for x in range(width):
			pixel = image.pixel(x, y)
			alpha = qAlpha(pixel)
			if alpha != 0:
				r = qRed(pixel)
				g = qGreen(pixel)
				b = qBlue(pixel)
				# Apply color filter
				new_r = min(255, int(r * color.red() / 255))
				new_g = min(255, int(g * color.green() / 255))
				new_b = min(255, int(b * color.blue() / 255))
				image.setPixel(x, y, qRgba(new_r, new_g, new_b, alpha))
	return QPixmap.fromImage(image)


def get_random_line(current_line, is_swimming_map=False):
	"""
	随机获取一条线路
	:param current_line: 当前线路
	:param is_swimming_map: 是否是游泳图模式
	:return: 目标线路
	"""
	max_line = 5
	if is_swimming_map:
		max_line = 6
	if is_swimming_map:
		# 游泳图模式的特殊处理
		if current_line in [0, 1]:
			return 1 if current_line == 0 else 0
		elif current_line in [4, 5]:
			return 5 if current_line == 4 else 4
		else:
			# 在游泳图模式下选择相邻的线路
			if current_line == 0:
				return 1
			elif current_line == max_line:
				return max_line - 1
			else:
				return random.choice([current_line - 1, current_line, current_line + 1])
	else:
		# 非游泳图模式的处理
		if current_line == 0:
			return 1
		elif current_line == max_line - 1:
			return max_line - 2
		else:
			# 随机选择当前线路的相邻线路，确保选择在有效范围内
			return random.choice([current_line - 1, current_line + 1])


# 保存字符串列表到文件
def save_to_saved_file(file_path, plant_card_id_list):
	# 将字符串列表转换为Base64编码并写入文件
	os.makedirs(os.path.dirname(file_path), exist_ok=True)
	try:
		encoded_data = base64.b64encode(','.join(plant_card_id_list).encode('utf-8')).decode('utf-8')
		with open(file_path, 'w') as file:
			file.write(encoded_data)
	except:
		traceback.print_exc()


# 从文件中读取字符串列表
def read_saved_file(file_path):
	# 从文件中读取Base64编码的数据并解码为字符串列表
	os.makedirs(os.path.dirname(file_path), exist_ok=True)
	plant_card_id_list = []
	try:
		with open(file_path, 'r') as file:
			encoded_data = file.read()
			decoded_data = base64.b64decode(encoded_data).decode('utf-8')
			plant_card_id_list = decoded_data.split(',')
	except:
		traceback.print_exc()
	return plant_card_id_list


def clear_layout(layout):
	widget_count = 0
	try:
		widget_count = layout.count()
		for i in range(widget_count):
			widget = layout.itemAt(i).widget()
			widget.deleteLater()
	except:
		pass
	return widget_count > 0


def check_coordinate_in_range(a, range_tuple, b):
	"""
	判断坐标b是否在以坐标a为中心的指定范围内。

	:param a: 起始坐标，格式为(x, y)
	:param range_tuple: 范围元组，格式为(左, 上, 右, 下)
	:param b: 需要检查的坐标，格式为(x, y)
	:return: 如果b在范围内，返回True，否则返回False
	"""
	x, y = a
	left, top, right, bottom = range_tuple
	# 计算范围的边界
	x_min = x - left
	x_max = x + right
	y_min = y - top
	y_max = y + bottom
	# 检查b是否在范围内
	return x_min <= b[0] <= x_max and y_min <= b[1] <= y_max


def get_aim_item_data(input_id, data_item, field):
	"""
	冲指定data_item中找id是input_id的field字段
	"""
	for each_item in list(data_item.values()):
		if each_item.get("id", "") == input_id:
			return each_item[field]


def query_item_infos(item_id, aim_list):
	"""
	根据id查询id所在的数据item
	"""
	try:
		for each_item in aim_list:
			if each_item['id'] == item_id:
				return each_item
	except:
		traceback.print_exc()
	return {}


def convert_cooling(cooling):
	"""
	根据冷却时间转成对应的文字
	"""
	cooling_word = "未知"
	try:
		cooling_num = int(cooling)
		if cooling_num < 8:
			cooling_word = "短"
		elif 8 <= cooling_num <= 50:
			cooling_word = "长"
		elif cooling_num > 50:
			cooling_word = "非常长"
	except:
		pass
	return cooling_word
