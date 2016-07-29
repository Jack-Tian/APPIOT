#!/usr/bin/python
#_*_coding:utf-8_*_ 
import unittest
import sys
from apkdownloader import ApkDownloader

reload(sys)
sys.setdefaultencoding("utf-8")
class TestApkDL(unittest.TestCase):
	def test_bd(self):
		a = ApkDownloader("bd")
		self.assertTrue(a.getTopApk(1, "//tjnas1/Dept_Floder/TEST/apk/"))
	def test_qihoo(self):
		a = ApkDownloader("qihoo")
		self.assertTrue(a.getTopApk(1, "//tjnas1/Dept_Floder/TEST/apk/"))
	def test_wdj(self):
		a = ApkDownloader("wdj")
		self.assertTrue(a.getTopApk(1, "//tjnas1/Dept_Floder/TEST/apk/"))
	def test_yyb(self):
		a = ApkDownloader("yyb")
		self.assertTrue(a.getTopApk(1, "//tjnas1/Dept_Floder/TEST/apk/"))
		
if __name__ == '__main__':
    unittest.main()
'''
		def test_init(self):
        d = Dict(a=1, b='test')
        self.assertEquals(d.a, 1)
        self.assertEquals(d.b, 'test')
        self.assertTrue(isinstance(d, dict))

    def test_key(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEquals(d.key, 'value')

    def test_attr(self):
        d = Dict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEquals(d['key'], 'value')

    def test_keyerror(self):
        d = Dict()
        with self.assertRaises(KeyError):
            value = d['empty']

    def test_attrerror(self):
        d = Dict()
        with self.assertRaises(AttributeError):
            value = d.empty
'''