#!/usr/bin/python
#_*_coding:utf-8_*_ 
import sys,re,os,time,hashlib,json
import androaxml as apkparse
import urllib2,urllib
from bs4 import BeautifulSoup
import ApkDownloader
import atx
reload(sys)
sys.setdefaultencoding("utf-8")

def log(txt,content):
	f = open(txt,"a")
	t = time.strftime('%Y-%m-%d %H:%M:%S  ',time.localtime(time.time()))
	c = str(t + content+ "\n")
	f.writelines(c)
	f.flush
	print content+'\n'
	f.close

class Control():
	def __init__(self):
		self.xmlrecord = "runrecord.xml"
		if not os.path.exists(self.xmlrecord):
			f = open(self.xmlrecord,"w")
			f.close
	def __parseApk(self, file): 
		bn = os.path.basename(file)
		m = re.match('(.*?)__(.*?)__(.*?)__(.*?)__(.*?)\.apk$',bn)

		return {"filename":m.group(1),
				"package":m.group(4),
				"version":m.group(5),
				"category":m.group(3)
		}
	def __traverseApk(self,path):
		#遍历path下所有apk文件
		#待测任务列表，已完成列表，用xml记录。
		#中间断掉，可以重新读取xml和编写,继续后面的测试。
		#todo
		list_dirs = os.walk(path)
		result = []
		for root, dirs, files in list_dirs: 
			for f in files: 
				if re.match(r'.*\.apk$',f):
					p = os.path.join(root, f)
					result.append(p)
					#print result[-1]
		return result
	def getApkTable(self,path):
		result = []
		for x in self.__traverseApk(path):
			y =[]
			result.append((self.__parseApk(x).values()))
			for each in result[-1]:
				print each
		return result
	def wtXML(self):
		#todo:往xml文件中写入运行记录
		#数据有：
		pass
	def rdXML(self):
		pass
	def getYLog(self):
		pass
	def analyzYlog(self):
		pass
	def exReport(self):
		pass
	def runMonkey(self):
		pass
	
	
	
	
	
c = Control()
# c.parseApk("//tjnas1/Dept_Floder/TEST/apk/bd/bd主题壁纸__1__乐桌面__com.lenovo.launcher__7.0.278.150917.apk")
# c.traverseApk("//tjnas1/Dept_Floder/TEST/apk")
c.getApkTable("//tjnas1/Dept_Floder/TEST/apk")