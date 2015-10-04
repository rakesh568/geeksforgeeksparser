#--------geeksforgeeks site downloader for offline mobile reading-------#

import os
from bs4 import BeautifulSoup
import urllib2
import requests
import shutil

allTags = ['tag/backtracking','tag/dynamic-programming','tag/advance-data-structures','tag/Greedy-Algorithm','tag/pattern-searching','tag/divide-and-conquer','tag/MathematicalAlgo','tag/recursion','tag/geometric-algorithms','category/c-arrays','category/bit-magic','category/c-puzzles','category/articles','category/linked-list','category/c-strings','category/tree','category/graph', 'category/interview-experiences']

path = "/home/rranjan/geeks/"      # Specify your path here


def findLink(allTags,path):
	for currTag in allTags:
		tagPath = path + currTag.split('/')[1]
		if os.path.exists(tagPath):
			shutil.rmtree(tagPath)
		os.mkdir(tagPath)
		pageNum=1
		url = "http://www.geeksforgeeks.org/" + currTag +"/"
		listofLinks=[]
		while 1:
			print url
			try:
			  data = urllib2.urlopen(url).read()
			except:
			  break
			soup = BeautifulSoup(data, "lxml")

			allLinks = soup.findAll("h2",{"class":"entry-title"})
			for link in allLinks:
                                mainLink = str(link.findAll("a")[0]).split("<a href=\"")[1].split('" rel="bookmark"')[0]
				listofLinks.append(mainLink)

			pageNum=pageNum+1

			url = "http://www.geeksforgeeks.org/" + currTag +"/page/" + str(pageNum) + "/"

		saveLinkAsHtml(listofLinks,tagPath,currTag)

def saveLinkAsHtml(listofLinks,tagPath,currTag):
	No=1
	listofLinks.reverse()
	for item in listofLinks:
                print item
		pageData = urllib2.urlopen(item).read()
		pageSoup=BeautifulSoup(pageData, "lxml")

		filePath = tagPath +"/" +str(No)+". "+item.split('http://www.geeksforgeeks.org/')[1].strip('/')
		with open(filePath+'.html',"wb") as f:
			f.write(str(pageSoup))

		No = No +1

findLink(allTags,path)
