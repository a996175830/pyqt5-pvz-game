
![请添加图片描述](https://i-blog.csdnimg.cn/direct/f1c1618ffe384dccb8cafb1e7ba8621d.png#pic_center)



# 一．前言
笔者近期没有发布新的PyQt5软件，并不是去摸鱼了，而是在认真研发新游戏。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/62e30b83b4884ab68420a062087945f8.png#pic_center)
本次使用PyQt5开发了一款植物VS僵尸游戏，包含<font color=green>45种植物</font>和<font color=rgb(83,78,97)>28种僵尸</font>，欢迎各位下载体验啊！撰写本篇记录下我的开发思路和设计流程。
# 二．预览
我们这里只预览一些值得预览的场景。
## 1.关卡选择
本次只设计了冒险模式

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8bdc91aa0d85497aa8ead306d96ceed7.png)
## 2.关卡选择
本次针对四种地图：白天、黑夜、白天泳池、黑夜泳池设计了20个关卡（PS：所有关卡通关后会有个彩蛋哦~）
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6c39317d833c43028643fce47b382aae.png)


## 3.游戏准备
游戏准备玩家要选择合适的卡牌开对抗出现的僵尸
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8568815000c9481d816f20e939733ce2.png)
## 4.进行游戏
### 4.1地图1
这是一关白天地图 请忽略我的测试阳光数据
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/22b832700d434d25a06d9bb1515ef597.png)


### 4.2地图2
我们可以通过按下数字键1来控制显示、隐藏体力

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/1929440c08c4455e8e61501f83d9ebd9.png)
### 4.3地图3

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d9839f3d64174f2e979f1f69a0955531.png)

## 5.图鉴
游戏准备阶段可以点击查看图鉴
### 5.1图鉴索引
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/a03e151bd60647e08951abff3e0cc8af.png)


### 5.2植物图鉴
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0270769f6b7f40589b3176b88f27e527.png)

### 5.3僵尸图鉴

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/37781eff8d104a43a1b24b885fcbbcc4.png)
太喜欢这些图鉴了，再来一张~
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/308b9c26afcd4334a37307f58d3cb753.png)
# 三．开发思路
本小结写一下我的开发思路
## 1.游戏原理

> 游戏原理就是两个字：贴图
本游戏是个2D游戏，所有的立体效果都是gif贴图，通过将gif放到QLabel中实现动图的展示，每类元素内部采用多继承，这考验了作者的面向对象编程：植物、僵尸、子弹都以QLabe为基类，再去实现自己内部特殊的属性，比如：豌豆射手属于射手类，所有射手类的植物都会发射直线的子弹，撑杆跳僵尸会跳过遇到的第一株植物，这属于他的特性，但是归根结底他是一类直线行走僵尸。在此笔者贴一张xmaind图来表示元素之间的继承关系吧~

![请添加图片描述](https://i-blog.csdnimg.cn/direct/5b964605fe7048e79df7e5d21185d797.png)
对我的代码继承关系感兴趣的朋友可以[点击下载](https://wwrr.lanzoul.com/iL7Db2ry6zaf)这个思维导图
## 2.困难

> 本次游戏开发实际耗时比预计长，主要是遇到了一些困难：子弹碰撞僵尸检测、僵尸攻击植物碰撞检测、僵尸攻击僵尸碰撞检测、特殊植物特性开发、僵尸特性开发、这是主要的耗时点，加上不同的游戏场景联动，测试也是耗费了很长时间。

## 3.UI设计

> 本次的UI设计为纯代码设计，请读者不要和我要.ui代码，因为没有ui代码，所有的组件和效果都是手写的，每个组件和元素都支持单元模块测试，大大地节省了测试消耗的时间，让我们有更多精力去挖掘游戏细节。
这里介绍一下游戏场景吧：整个游戏场景是一个5x9的网格布局，布局里是一个个的item，我们种植的植物通过addWidget放到item的layout里，然后僵尸都是直线僵尸，通过设置的定时器来减少僵尸x的数据，实现僵尸的自右向左移动，在此期间遇到植物后停下来攻击植物直到自己死亡或者植物死亡再继续向左移动。
那么如何实现的魅惑菇的效果呢？这很简单改变贴图运动方向即可，在僵尸被魅惑期后让僵尸调转移动方向（矿工僵尸除外~）。本次开发ui有些小遗憾就是僵尸的实际大小正确，这个我是知悉的，尝试了很多方法比如：切图放大、直接放大，效果不尽人意，相信应该会有更好的方案只是笔者还没发掘。
## 4.音频处理
> 一款游戏一定是音视频结合的，这样能给玩家带来舒适的游戏体验，本次将音乐和音效分开处理，在循环播放的背景音乐中加入特定触发的音效，每次触发的音效可叠加，通过使用线程的方式播放wav音效，播放完成后自动销毁线程，优化了用户体验和游戏性能。
## 4.打包
> 本次打包遇到了点小阻力，但是最后还是解决了。本次打包采用的nuitka，最后使用inno setup来制作的安装包，欢迎大家安装体验！
## 5.如何处理资源
> 本次所有的图片、音频、视频资源都直接从qrc里读取，我们的游戏项目含有大量的音频、音效，每次添加一个都需要在qrc文件里添加一条，这样太繁琐了，而且很机械，为了方便笔者写了一个脚本，用于整理、扫描资源，生成qrc里xml语句，和大家分享一下

```python
import os
import subprocess


def generate_qrc_content(root_dir):
	files = [
		"<file>{}</file>".format(os.path.relpath(os.path.join(root, file), root_dir).replace('\\', '/'))
		for root, _, files in os.walk(root_dir)
		for file in files
		if
		".qrc" not in file and ".py" not in file and "video" not in os.path.relpath(os.path.join(root, file), root_dir)
	]
	return "<RCC>\n    <qresource>\n" + "\n".join(
		"        {}".format(file) for file in files) + "\n    </qresource>\n</RCC>"


def generate_qrc_file(qrc_file_path, content):
	with open(qrc_file_path, 'w') as qrc_file:
		qrc_file.write(content)


def compile_qrc_to_py(qrc_file_path):
	py_file_path = qrc_file_path.replace('.qrc', '_rc.py')
	subprocess.run(['pyrcc5', qrc_file_path, '-o', py_file_path], check=True)


def main():
	root_dir = "../resources"
	qrc_file_path = root_dir + "/resource.qrc"
	qrc_content = generate_qrc_content(root_dir)
	generate_qrc_file(qrc_file_path, qrc_content)
	compile_qrc_to_py(qrc_file_path)


if __name__ == "__main__":
	main()

```
## 6.项目结构
下面截图是我们的项目结构，整体比较清晰，每个模块通过包或者.py文件分离开来。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/bdb3392b11a843d394766317dd91697e.png#pic_center)

## 7.关于游戏数据

> 本次开发采用的pvz一代原版数据，具体数据参考了[植物大战僵尸全图鉴3.6.0](https://wwrr.lanzoul.com/iqNlV2asnsmj)欢迎各位玩家测试！

# 四．总结
本次是笔者第二次开发2d游戏，望大家不喜勿喷哈~强烈推荐去下载体验一下，欢迎大家提交BUG，欢迎欢迎！
给我点个赞吧，谢谢大家了！
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/34ef3a8a28704b76863c5de645fe8468.png#pic_center)
