from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QEventLoop
from PyQt5.QtMultimedia import QSound


class AudioThread(QThread):
	finished = pyqtSignal()

	def __init__(self, audio_file, parent=None):
		super().__init__(parent)
		self.audio_file = audio_file
		self.sound = None

	def run(self):
		try:
			self.sound = QSound(self.audio_file)
			self.sound.play()

			# 创建事件循环
			event_loop = QEventLoop()

			# 定期检查音频播放状态
			while not self.sound.isFinished():
				event_loop.processEvents()
				self.msleep(100)  # Check every 100 milliseconds
		except:
			pass
		self.finished.emit()
