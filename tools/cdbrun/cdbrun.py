#!/usr/bin/python
# -*- coding: UTF-8 -*-

import subprocess
import os
import shutil
import sys
import time
import psutil
from datetime import datetime

class cdbfuzz:
	def __init__(self,app,crashd,debugger):
		if os.path.exists(app) == True & os.path.exists(crashd) == True & os.path.exists(debugger) == True:
			global program
			global crashdir
			global cdblocation
		else:
			print "[+] Please check all given paths"
			exit()
		program = app
		print "[+] Target application path =>",program
		crashdir = crashd
		print "[+] Crash Dir => ",crashdir
		cdblocation = debugger
		print "[+] Debugger path => ",cdblocation
		
	def startapp(self,input_file):
		filename = input_file.split('\\')[-1:][0]
		fp = open(crashdir+filename+'.log', 'w')
		cmd = cdblocation+' '+'-c ".logopen '+crashdir+filename+'.log;g;g;r;kv;.logclose;" '+program+' '+input_file
		process = subprocess.Popen(cmd)
		fp.close()
		return process
		
	def kill(self,proc_obj):
		proc_obj.terminate()
		
	def wascrash(self,test_filename):#Did the prog. crash last time ??
		log = open(crashdir+test_filename.split('\\')[-1:][0]+'.log').read()
		if ("Access violation - code" in log) or ("!!! second chance !!!" in log) or ("divide-by-zero") in log:
			return True
		else:
			return False
		

	def dumpcrash(self,crash_filename):
		print "[+] Dump Crash File !"
		prog = program.split('\\')[-1:][0]
		shutil.copyfile(crash_filename, crashdir+prog+'_'+crash_filename.split('\\')[-1:][0])
	
	def check(self, proc, file):
		begin = time.time()
		while 1:	
			if self.wascrash(file) == True:	
				print "[+] Crashed"
				self.dumpcrash(file)
				return
			elif (time.time() - begin) > timeout:
				self.kill(proc)
				#os.remove(crashdir+file.split('\\')[-1:][0]+'.log')
				return
			else:
				#os.remove(crashdir+file.split('\\')[-1:][0]+'.log')
				continue
				
timeout = 3

'''
if len(sys.argv) < 3:
	print "[Usage]: python cdbfuzzer.py <program> <file/dir> [timeout]"
	sys.exit()
else:
	program = sys.argv[1]
	input = sys.argv[2]
if len(sys.argv) == 4:
	timeout = sys.argv[3]
'''
cdblocation = "E:\\fuzzer\\riufuzz\\tools\\cdb.exe"
program = "E:\\ResearchTarget\\webex\\Webex\\500\\nbrplay.exe"
input = "E:\\fuzzer\\riufuzz\\arf"
crashdir = "./"
fuzz = cdbfuzz(program,crashdir,cdblocation)

if os.path.isdir(input):
	if input[-1] != '\\':
		input+='\\'
	dir = os.listdir(input)
	for file in dir:
		print "[+] Test " + file
		proc = fuzz.startapp(input+file)
		fuzz.check(proc, input+file)

else:
	proc = fuzz.startapp(input)
	fuzz.check(proc, input)

print "Test End !"		


