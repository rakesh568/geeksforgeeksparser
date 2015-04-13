#--------geeksforgeeks site downloader for offline mobile reading-------#
#first script :)

import os
from bs4 import BeautifulSoup
import urllib2
import requests
import shutil
from requests.exceptions import ConnectionError
from xhtml2pdf import pisa

AllTags = ['tag/backtracking','tag/dynamic-programming','tag/advance-data-structures','tag/Greedy-Algorithm','tag/pattern-searching','tag/divide-and-conquer','tag/MathematicalAlgo','tag/recursion','tag/geometric-algorithms','category/c-arrays','category/bit-magic','category/c-puzzles','category/articles','category/linked-list','category/c-strings','category/tree','category/graph']

path = "/media/Local Disk E/geeksForGeeks/"      # Specify your path here


def findLink(AllTags,path):
	for i in AllTags:
		tagPath = path + i.split('/')[1]
		if os.path.exists(tagPath):
			shutil.rmtree(tagPath)
		os.mkdir(tagPath)
		pageNum=1
		url = "http://www.geeksforgeeks.org/" + i +"/"
		listofLinks=[]
		while 1:
			print url
			try:
			  data = urllib2.urlopen(url).read()
			except:
			  break
			soup = BeautifulSoup(data)
			allLinks = soup.findAll("h2",{"class":"post-title"})
			#print allLinks
			for link in allLinks:
				mainLink = str(link.findAll("a")[0]).split("<a href=\"")[1].split('" rel="bookmark"')[0]
				print mainLink+"\n"
				listofLinks.append(mainLink)
				#print listofLinks
			pageNum=pageNum+1
			url = "http://www.geeksforgeeks.org/" + i +"/page/" + str(pageNum) + "/"
		saveLinkAsHtml(listofLinks,tagPath,i)

def saveLinkAsHtml(listofLinks,tagPath,i):
	No=1
	listofLinks.reverse()
	for item in listofLinks:
		pageData = urllib2.urlopen(item).read()
		pageSoup=BeautifulSoup(pageData)
		print str(listofLinks.index(item)) +" "+item

	#Removing unnecessary elements
		#[s.extract() for s in pageSoup('script')]
		[s.extract() for s in pageSoup('h2',{'align':'right'})]
		[s.extract() for s in pageSoup('b')]
		[s.extract() for s in pageSoup('a',{'href':'http://www.geeksforgeeks.org/wp-login.php'})]
		[s.extract() for s in pageSoup('div',{'class':'blog-info'})]
		[s.extract() for s in pageSoup('div',{'id':'menu'})]
		[s.extract() for s in pageSoup('div',{'id':'navmenu'})]
		[s.extract() for s in pageSoup('ul')]
		#[s.extract() for s in pageSoup('div',{'class':'clear'})]
		[s.extract() for s in pageSoup('div',{'id':'footer'})]
		[s.extract() for s in pageSoup('div',{'id':'ajaxSpinner'})]
		[s.extract() for s in pageSoup('iframe')]
		#This needs to be corrected. Width has been set currently as per my mobile screen size.
		pageSoup.find("body")['style']='width:100em'
		pageSoup.find("div",{"id":"content"})['style']='width:350px'

		filePath = tagPath +"/" +str(No)+". "+item.split('http://www.geeksforgeeks.org/')[1].strip('/')
		with open(filePath+'.html',"wb") as f:
			f.write(str(pageSoup))

#if you want to convert it to pdf (dont set, it doesnt look good).
		#convertHtmlToPdf(open(filePath + '.html'), filePath + '.pdf')
	
		No = No +1

def convertHtmlToPdf(sourceHtml, outputFilename):
        """
         Open output file for writing (truncated binary) and
         converts HTML code into pdf file format

        :param sourceHtml: The html source to be converted to pdf
        :param outputFilename: Name of the output file as pdf
        :return: Error if pdf not generated successfully
        """
	resultFile = open(outputFilename, "w+b")

        # convert HTML to PDF
        pisaStatus = pisa.CreatePDF(sourceHtml, dest=resultFile)

        # close output file
        resultFile.close

findLink(AllTags,path)
