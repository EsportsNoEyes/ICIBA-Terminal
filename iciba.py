#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import re
import string
import exceptions
import sys
import copy

def iciba_search(url):

	# Try to fetch html file of the target word
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent','Chrome')
		response1 = urllib2.urlopen(req)
		response2 = urllib2.urlopen(req)
	except Exception:
		# Throw an exception in case of no Internet connection or other exceptions
		print 'Search failed. Something is wrong. \n'
		sys.exit(1)

	# Obtain the content of the html file
	html_content = response1.read()
	
	# Filter out CETs
	results = re.findall('(?<=<li class="clearfix">).*?(?=</li>)', html_content, re.S)
	# Merge results into a single str
	results_merge1 = ' '.join(results)
	# Discard useless spaces
	results_no_space = results_merge1.replace(' ','')
	# Discard <span> tags
	results_no_span = re.findall('(?<=<spanclass="prop">).*?(?=</span>)|(?<=<span>).*?(?=</span>)', results_no_space, re.S)
	# Merge results 
	results_merge2 = ' '.join(results_no_span)

	# Formatting
	results_formatted = results_merge2.replace('；','\n     ')
	# Separate the meanings by its part of speech
	results_formatted = results_formatted.replace('vi.','\nvi.  ')
	results_formatted = results_formatted.replace('vt.','\nvt.  ')
	results_formatted = results_formatted.replace('v.','\nv.   ')
	results_formatted = results_formatted.replace('n.','\nn.   ')
	results_formatted = results_formatted.replace('adj.','\nadj. ')
	results_formatted = results_formatted.replace('adv.','\nadv. ')
	results_formatted = results_formatted.replace('prep.','\nprep.')
	results_formatted = results_formatted.replace('aux.','\naux. ')
	results_formatted = results_formatted.replace('  &\n','& ')
	results_formatted = results_formatted.replace('& vi.   ','& vi. ')

	print word.capitalize() + ' 一词在爱词霸上的释义:\n'

	# Obtain phonetic symbols of Americans
	soup = BeautifulSoup(response2, "html.parser")	
	tag = soup.find('div', class_='base-speak')

	#Deal with edge cases
	if (not tag is None) and (len(tag.contents) > 3):
		print tag.contents[1].span.string + ' ' + tag.contents[3].span.string
	elif (not tag is None) and (len(tag.contents) < 4) and (len(tag.contents) > 1) and (not tag.contents[1].span is None):
		print tag.contents[1].span.string + '\n'
	else:
		pass

	print ' ' + results_formatted + '\n'
	print "--------------------------------------------------------------\n"


print """
--------------------------------------------------------------
This is a dictionary for Terminal. 

It fetches the meanings of a specific word from iciba.com




Author: PLANCK_C

Update Log
2017/06/07: Basic functionality
2017/06/22: Use BS4 to display phonetic symbols
2017/06/23: Add logics to deal with edge cases on symbols
2017/06/30: Fix edge cases logics 
2017/07/06: Fix edge cases logics
--------------------------------------------------------------
"""
while True:
	word = raw_input("Enter the word you want to search for: ")
	iciba_url = 'http://www.iciba.com/' + word
	print "--------------------------------------------------------------\n"
	iciba_search(iciba_url)





