#!/usr/bin/python
#_*_coding:utf-8_*_ 
import os
__dir__ = os.path.dirname(os.path.abspath(__file__))

import sys
sys.path.append(os.path.join(__dir__, "androguard.zip"))

from androguard.core.bytecodes import apk


def _xml2parse(dom):  
    root = dom.getElementsByTagName("manifest")[0]
    package = root.getAttribute('package')
    version = root.getAttribute('android:versionName')
    activity = ''
    for e in root.getElementsByTagName('activity'):
        name = e.getAttribute('android:name')
        t = e.getElementsByTagName('intent-filter')
        action = t and t[0].getElementsByTagName('action')
        category = t and t[0].getElementsByTagName('category')
        if action and action[0].getAttribute('android:name') == 'android.intent.action.MAIN' and \
                category and category[0].getAttribute('android:name') == 'android.intent.category.LAUNCHER':
            activity = name
    return (package, activity, version)

def parse_apk(filename):
    ''' return (package, activity, version) '''
    a = apk.APK(filename)
    dom = a.get_android_manifest_xml()
    return _xml2parse(dom)

#print parse_apk("1.apk")[2]


