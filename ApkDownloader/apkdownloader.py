#!/usr/bin/python
#_*_coding:utf-8_*_ 
import sys,re,os,time,hashlib,json
import androaxml as apkparse
import urllib2,urllib
from bs4 import BeautifulSoup


reload(sys)
sys.setdefaultencoding("utf-8")
try:
	os.remove("log.log")
except:
	pass
def log(txt,content):
	f = open(txt,"a")
	t = time.strftime('%Y-%m-%d %H:%M:%S  ',time.localtime(time.time()))
	c = str(t + content+ "\n")
	f.writelines(c)
	f.flush
	print content+'\n'
	f.close

class ApkDownloader():
	def __init__(self, vendor):
		self.vendor = vendor
	def baselink(self):
		if self.vendor =="bd":
			return "http://shouji.baidu.com"
		if self.vendor =="qihoo":
			return "http://zhushou.360.cn" 
		if self.vendor =="yyb":
			return "http://sj.qq.com/myapp"
		if self.vendor =="wdj":
			return  "http://www.wandoujia.com"
		
	def getHtml(self,url):
		req_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
				'Accept':'*/*',
				'Accept-Language':'zh-CN,zh;q=0.8',
				'Connection':'close',
				'Referer':None 
				}
		req_timeout = 10
		req = urllib2.Request(url,None,req_header)
		resp = urllib2.urlopen(req,None,req_timeout)
		html = resp.read()
		return html
		
	def getSoup(self,url):
		return BeautifulSoup(self.getHtml(url),"lxml")
		
	def __removeCheck(self,file):
		'''
		return:
		文件不存在：0
		文件存在，且小于100k:0 删除掉。
		文件存在，且大于100k:1
		'''
		if os.path.exists(file):
			if os.stat(file).st_size < 100000:
				os.remove(file)
				log("log.log","%s <100000, removed"%file.encode('gbk'))
				return 0
			else:
				return 1
		else:
			return 0
		
		
	def getApkVersionName(self, path):
		try:
			(pkg_name, activity, version) = apkparse.parse_apk(path)
			print "apk version = " + version
			return version
		except:
			print "getApkVersionName error, change to 0.0.0"
			return "0.0.0"
			
	def wtCsv(csvpath, data_name,category, package,version,path,rank):
		'''
		分析目录下所有apk的版本号
		腾讯视频,视频,com.tencent.qqlive,4.9.5.10537,,视频\腾讯视频_4.9.5.10537.apk,1
		data_name,category, package name, version,,path,rank
		'''
		f = open(csvpath,"a")
		c = "%s,%s,%s,%s,,%s,%d"%(data_name,category, package,version,path,rank)
		f.write(c)
		f.write("\n")
		f.flush
		#print c
		f.close
		rank +=1

		
	def __getCategory(self,link):
		soup = self.getSoup(link)
		if "bd" == self.vendor:
			#print soup.find('a',"cur", href=re.compile("/software/|/game/")).encode('gbk')
			category = soup.find('a',"cur", href=re.compile("/software/|/game/")).get_text()
		elif "qihoo"== self.vendor:
			category = soup.find('a', "aurr").get_text()
		elif "yyb" == self.vendor:
			for x in soup.findAll('a',href=re.compile("categoryId")):
				if re.search(r"\d{3}",link).group() in x.get("href"):
					category = x.get_text()
		elif "wdj" == self.vendor:
			category = soup.find('h1',class_="crumb-h1").get_text()
			category = re.sub(u'\u4e0b\u8f7d',"",category)
		else:
			log( "log.log","vendor \"%s\" is not in the list"%self.vendor)
		return category
	
	def __getApkLinkInfo(self,node):
		if self.vendor == "bd":
			data_name = node.get("data_name")
			package = node.get('data_package')
			version = node.get('data_versionname')
			url = node.get('data_url')
		elif self.vendor == "qihoo":
			pattern = re.match(r'.*?name=(.+?)&.*?appmd5=(\w+?)&.*?url=(.*/(.*?)_\d+\.apk)',node.get("href"))
			data_name = pattern.group(1)
			appmd5 = pattern.group(2)
			tmp = self.getSoup("http://zhushou.360.cn/detail/index/soft_id/%s"%node.get("sid"))
			#version=tmp.find(text= re.compile('\d+\.\d+\.\d*\.*\d*\.*\d*'))
			version = "0.0.0"
			for t in tmp.findAll("td"):
				#print t.strong.encode("gbk")
				if "版本" in t.strong.encode("gbk"):
					version =t.find(text= re.compile('\d+\.\d+\.*\d*\.*\d*\.*\d*'))
			#print 'version %s'%version
			package = pattern.group(4)
			url = pattern.group(3)
		elif self.vendor == "yyb":
			data_name = node["appName"]
			package = node["pkgName"]
			url = node["apkUrl"]
			version = node["versionName"]
		elif self.vendor == "wdj":
			data_name = node.get("data-name")
			package = node.get("data-pn") 
			url = re.sub(r'/binding','/download',node.get("href"))
			tmp = self.getSoup("http://www.wandoujia.com/apps/%s"%package)
			version = tmp.find(text= re.compile(u'\u7248\u672c\uff1a\d+\.\d+\.\d*\.*\d*\.*\d*'))
			#print version
			version = re.sub(u'\u7248\u672c\uff1a','',version)
		else:
			log("log.log","error getApkLinkInfo")
		return (data_name, package, version, url) 
	def __getSaveApkPath(self,category,rank,name,package,version,savepath):
		# print category,rank,name,package,version
		# print savepath
		name = re.sub(r":|\\|/|\*|\?|\"|>|<|\|| ","",name)
		path = "%s/%s%s__%d__%s__%s__%s.apk"%(savepath,self.vendor,category.encode("gbk"),rank,name.encode("gbk"),package.encode("gbk"),version.encode("gbk"))
		#print path
		return path
	def __checkExistApk(self,savedpath):
		if not os.path.exists(savedpath):
			return 0
		try:
			print apkparse.parse_apk(savedpath)[2]
			return 1
		except:
			log("log.log","apk exist, but not integrated, need to re-download:%s"%savedpath)
			return 0

	def __getApk(self,nodes,category,mainpath): 
		'''
		nodes是节点内容的list,
		originpath是存储路径
		'''
		mainpath = "%s%s"%(mainpath,self.vendor)
		rank = 1
		for x in nodes:
			info = self.__getApkLinkInfo(x)
			savedpath = self.__getSaveApkPath(category,rank,info[0],info[1],info[2],mainpath)
			if self.__checkExistApk(savedpath):
				log("log.log","%s not updated"%savedpath)
			else:
				if not os.path.exists(mainpath):
					os.makedirs(mainpath)
				try:
					print "downloading %s"%savedpath
					urllib.urlretrieve(info[3], savedpath)
				except:
					log("log.log","%s error:cannot download!"%info[0].encode('gbk'))
			if self.__removeCheck(savedpath):
				rank +=1

	def __getCategorylink(self):
		clist=[]
		if self.vendor =="bd":
			link = 'http://shouji.baidu.com/software/501/'
			soup = self.getSoup(link)
			for x in soup.find_all('a',href = re.compile("/software/\d{3,}/")):
				clist.append("http://shouji.baidu.com%s"%x.get("href"))
				#print clist[-1]
			link = 'http://shouji.baidu.com/game/401/'
			soup = self.getSoup(link)
			for x in soup.find_all('a',href = re.compile("/game/\d{3,}/")):
				clist.append("http://shouji.baidu.com%s"%x.get("href"))
				#print clist[-1]
		elif self.vendor == "qihoo":
			link1 = "http://zhushou.360.cn/list/index/cid/1" #软件
			link2 = "http://zhushou.360.cn/list/index/cid/2" #game
			for l in [link1,link2]:
				soup = self.getSoup(l)
				for x in soup.find_all('a',href = re.compile("/list/index/cid/\d{2,}")):
					clist.append("http://zhushou.360.cn%s"%x.get("href"))
		elif self.vendor == "yyb":	
			link1 = "http://sj.qq.com/myapp/category.htm?orgame=1" #软件
			link2 = "http://sj.qq.com/myapp/category.htm?orgame=2" #游戏
			for l in [link1,link2]:
				soup = self.getSoup(l)
				for x in soup.find_all('a',href = re.compile("\?orgame=\d&categoryId=\d{3}")):
					clist.append("http://sj.qq.com/myapp/category.htm%s"%x.get("href"))
		elif self.vendor == "wdj":	
			list_tmp=[]
			link = "http://www.wandoujia.com/category/app" #软件
			soup = self.getSoup(link)
			for x in soup.find_all('a',class_="cate-link"):
				if x.get_text():
					list_tmp.append(x.get("href"))
			clist = list(set(list_tmp))
		else:
			log("log.log","error getCategorylink")
		return clist


	def __getApkRangeList(self,link,top):#link是每个category的link
		nodes =[]
		#print link
		if self.vendor =="bd":
			for x in range(1,3):
				l = "%slist_%d.html"%(link,x) 
				soup = self.getSoup(l)
				category = self.__getCategory(l)
				nodes.extend(soup.find_all('span',class_="inst-btn inst-btn-small quickdown"))
			apkrangelist = nodes[:top]
		elif self.vendor =="qihoo":
			for x in range(1,3):
				l = "%s?page=%d"%(link,x) 
				soup = self.getSoup(l)
				category = self.__getCategory(l)
				nodes.extend(soup.find_all('a',sid=re.compile("\d+"),href=re.compile("zhushou360.*\.apk")))
			apkrangelist = nodes[:top]
		elif self.vendor == "yyb":
			category = self.__getCategory(link)
			link = re.sub(r'category.htm','cate/appList.htm',link)
			j = self.getHtml("%s&pageSize=100"%link)
			d = json.loads(j)
			apkrangelist = d["obj"][:top]
		elif self.vendor == 'wdj':
			category = self.__getCategory(link)
			for x in range(1,3):
				l = "%s_%d"%(link,x) 
				soup = self.getSoup(l)
				nodes.extend(soup.find_all('a', attrs={'data-feat' : "binded"}))
			apkrangelist = nodes[:top]
		else:
			log("log.log","error getApkRangeList")
		return (apkrangelist,category)

	def getTopApk(self,top,originpath):
		if top<51:
			for link in self.__getCategorylink():
				apkrangelist,category = self.__getApkRangeList(link,top)
				# print apkrangelist,category
				self.__getApk(apkrangelist,category,originpath)
			return True
		else:
			log("log.log","%s 每个分类最多下载50个"%self.vendor)
			return False

