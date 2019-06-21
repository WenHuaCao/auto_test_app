from appium import webdriver
import time
import random
import subprocess
import os
from data import data
def fast_input(str,element):
	'快速输入仅仅支持英文'
	x = '127.0.0.1:7555'
	element.click()
	time.sleep(0.3)
	subprocess.Popen('adb -s %s shell input text %s'%(x,str), shell=True)
	time.sleep(0.5)
desired_caps = {

				'platformName': 'Android',

				'deviceName': '127.0.0.1:7555',
				# 'deviceName': '33008257a94ac2b3',


				'platformVersion': '6.0.1',

				# apk包名

				'appPackage': 'com.netease.yanxuan',

				# apk的launcherActivity
				'unicodeKeyboard': True,

				'resetKeyboard': True,
				'appActivity': 'com.netease.yanxuan.module.splash.SplashActivity'

				}
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
print('the type of the drive is',type(driver))
time.sleep(15)
# search_btn = do_action(driver.find_element_by_id,"com.netease.yanxuan:id/tv_home_search")
# search_btn.click()



# def randomgetclassname(classname):
# 	allobject = None
# 	while(1):
# 		try:
# 			allobject = driver.find_element_by_class_name(classname)
# 			break;
# 		except:
# 			print('no tag name')
# 			time.sleep(2)
# 	return allobject
def do_action(method,string,iter = 2):
	object = None
	for i in range(iter):
		try:
			object = method(string)
			break
		except:
			object = None
			print('do action error')
			time.sleep(1)
	if object == None:
		print(string)
		quit()
	return object

	
class page:
	def getaction(self):
		'abstract'
	def return_choices(self):
		'abstract'
class beforeinput(page):
	def getaction(self):
		prob = random.random()
		if prob >0.6:self.choice1()
		else :self.choice2()
	def choice1(self):
		print('正在输入某一个关键字')
		search_btn = do_action(driver.find_element_by_id,"com.netease.yanxuan:id/tv_home_search")
		search_btn.click()
		search_btn.send_keys(random.choice(data))
		time.sleep(2)

	def choice2(self):
		print('根据搜索词来搜索')
		history = do_action(driver.find_element_by_id,'com.netease.yanxuan:id/search_history_rv')
		elements = do_action(driver.find_elements_by_class_name,'android.widget.TextView')
		print(type(elements))
		valid_list = []
		for ele in elements :
			text = ele.get_attribute('text')
			if text!= '历史记录' or text != '热门搜索':
				valid_list.append(ele)
		this_choice = random.choice(valid_list)
		this_choice.click()
	def return_choices(self):
		return [self.choice1,self.choice2]
class homepage(page):
	def getaction(self):
		self.choice1()
	def return_choices(self):
		return [self.choice1]
	def choice1(self): #尝试找到搜索按钮并且点击
		search_btn = do_action(driver.find_element_by_id,"com.netease.yanxuan:id/tv_home_search")
		search_btn.click()
class afterinput(page): #
	def getaction(self):
		print('确认搜索次关键词')
		prob = random.random()
		if prob  > 0.5:self.choice1()
		else : self.choice2()
	def choice1(self):#确定搜索的内容
		os.system('adb shell ime set com.sohu.inputmethod.sogou/.SogouIME')
		driver.find_element_by_id("com.netease.yanxuan:id/tv_home_search").click()
		driver.press_keycode(66)
		os.system('adb shell ime set io.appium.android.ime/.UnicodeIME')
	def choice2(self):#随机的选择搜索列表
		print('按照提示词搜索')
		box = do_action(driver.find_element_by_id,'com.netease.yanxuan:id/search_associate_rv')
		words = do_action(box.find_elements_by_class_name,'android.widget.TextView')
		if  words == []:
			self.choice1()
			return 
		random.choice(words).click()
	def return_choices(self):
		return [self.choice1,self.choice2]
class contentpage(page):
	def getaction(self):
		prob = random.random()
		if prob > 0.8:self.choice1()
		elif prob > 0.4:self.choice2()
		else:self.choice3()
		# self.choice3()
	def choice1(self): #返回
		print('返回')
		return_btn = do_action(driver.find_element_by_id,'com.netease.yanxuan:id/search_bar_return')
		return_btn.click()

	def choice2(self):
		print('排序')
		time.sleep(0.5)
		price_sort_btn  =driver.find_elements_by_class_name('android.widget.TextView')[1]
		try:
			driver.find_element_by_id('com.netease.yanxuan:id/selector_item')
		except:
			self.choice1()
			return 
		price_sort_btn.click()


	def choice3(self):
		print('筛选')
		time.sleep(0.5)
		price_sort_btn  =driver.find_elements_by_class_name('android.widget.TextView')[2]
		try:
			driver.find_element_by_id('com.netease.yanxuan:id/selector_item')
		except:
			self.choice1()
			return 
		price_sort_btn.click()

	def return_choices(self):
		return [self.choice1,self.choice2]
class selepage(page):
	def getaction(self):
		prob = random.random()
		if prob > 0.6:self.choice1()
		elif prob >0.5:self.choice2()
		else :self.choice3()
	def return_choices(self):
		return [self.choice1,self.choice2,self.choice3]
	def choice1(self):#确定
		print('筛选完成')
		btn = do_action(driver.find_element_by_id,'com.netease.yanxuan:id/rv_combine_filter_confirm')
		btn.click()
	def choice2(self):#重置
		print('重置')
		btn = do_action(driver.find_element_by_id,'com.netease.yanxuan:id/rv_combine_filter_reset')
		btn.click()
	def choice3(self):#其他
		print('其他操作')
		btns = do_action(driver.find_elements_by_xpath,'//android.view.ViewGroup/android.view.ViewGroup/android.widget.FrameLayout')
		if btns == []:
			self.choice1()
			return
		# for btn in btns:
		# 	print(btn.get_attribute('clickable'))
		random.choice(btns).click()

	def return_choices(self):
		return [self.choice1,self.choice2]
def judge():
	print('judge')
	time.sleep(2)
	if driver.find_elements_by_xpath('//android.widget.TextView[@text="扫一扫"]') != []:
		print('homepage')
		return homepage
	if driver.find_elements_by_xpath('//android.widget.TextView[@text="历史记录"]')!= []:
		print('beforeinput')
		return beforeinput
	if driver.find_elements_by_xpath('//android.widget.TextView[@text="取消"]')!= []:
		print('afterinput')
		return afterinput
	if driver.find_elements_by_xpath('//android.widget.TextView[@text="重置"]')!= []:
		print('selectpage')
		return selepage
	try: 
		driver.find_element_by_id('com.netease.yanxuan:id/search_input')
		print('contentpage')
		return contentpage
	except:
		# os.system('adb shell ime set com.sohu.inputmethod.sogou/.SogouIME')
		print('回退递归中')
		driver.press_keycode(4)
		return judge()
		# os.system('adb shell ime set io.appium.android.ime/.UnicodeIME')
def mainloop(iter = 100):
	for i in range(iter):
		mypage = judge()()
		mypage.getaction()
		
mainloop()
# t = homepage()
# t.choice1()
# t = beforeinput()
# t.choice1()
# t = afterinput()
# t.choice2()
# t = contentpage()
# # t.choice3()
# print('finish')
# y = driver.find_element_by_id('com.netease.yanxuan:id/selector_item')
# print(y.get_attribute('text'))
# try:
# 	d = driver.find_element_by_xpath('//android.widget.FrameLayout[@index = 5]')
# 	print('find')
# except:
# 	pass
# r  =driver.find_elements_by_class_name('android.widget.TextView')
# t= r[2].find_element_by_xpath('//android.widget.TextView[@text = "筛选"]')
# node[4].click()
#综合价格筛选
#某些元素不存在的问题
#某些元素不可点击的问题