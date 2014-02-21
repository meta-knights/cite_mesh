#!/usr/bin/python

import os
from bs4 import BeautifulSoup
import lxml

ID = 0

class Paper:
	doi = None
	refs = []
	
	def pprint(self):
		print "DOI: %s" % self.doi
		print "--- REFS ---"
		for ref in self.refs:
			print "  DOI: %s" % ref
		print "------------"
	

def parse_file(filename=None):
	f = open(filename, 'r')
	soup = BeautifulSoup(f.read())
	paper = Paper()
	
	try:
		paper.doi = soup.find(attrs={"pub-id-type" : "doi"}).text
	except:
		return False
	
	if paper.doi:
		for ref in soup.find_all("ref"):
			try:
				paper.refs.append(ref.find(attrs={"pub-id-type" : "doi"}).text)
			except:
				pass
	return paper
	

def write_header(f):
	f.write("""<?xml version="1.0" encoding="UTF-8"?>
<graphml xmlns="http://graphml.graphdrawing.org/xmlns"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
     http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
  <graph id="G" edgedefault="undirected">
  """)
	
def write_footer(f):
	f.write("""  </graph>
</graphml>""")

def write_out(f, paper):
	global ID
	f.write('<node id="%s"/>\n' % paper.doi)
	for ref in paper.refs:
		f.write('<edge id="%i" source="%s" target="%s"/>\n' % (ID, paper.doi, ref))
		ID += 1
		#f.write('<edge id="%s%s" source="%s" target="%s"/>\n' % (paper.doi, ref, paper.doi, ref))


def traverse(folder=None, f=None):
	print "traversing: %s" % folder
	for item in os.listdir(folder):
		if os.path.isdir("%s/%s" % (folder, item)):
			traverse("%s/%s" % (folder, item), f)
		else:
			if item.endswith(".nxml"):
				p = parse_file("%s/%s" % (folder, item))
				if p:
					write_out(f, p)
				#p.pprint()

f = open('out.graphml', 'w')
write_header(f)
traverse("./data", f)
write_footer(f)

