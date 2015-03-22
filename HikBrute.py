#!/usr/bin/env python

# -==[ Hikvision DVR Brute forcer - V 1.0 ]==-
# -==[ Author : XD4rker ]==-
#
# Copyright 2015 XD4rker
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import httplib2, sys, os.path, signal, hashlib

if len(sys.argv) == 1:
	print "Error: Usage: ./script.py <WORDLIST_PATH>"
	sys.exit()

if not os.path.isfile(sys.argv[1]):
	print "Error: File doesn't exist"
	sys.exit()

HEADER = "\033[95m"
BLUE = "\033[94m"
GREEN = "\033[92m"
ENDLINE = "\033[0m"
INFO = "[+]"
hostCount = 0;

wordlist_path = sys.argv[1]
f = open(wordlist_path)
lines = f.readlines()
v = open("liveHosts.list", "a");

h = httplib2.Http(timeout=10)
#h.follow_all_redirects = False

print "\n" + HEADER + BLUE + INFO + ENDLINE + " " + "Using file : "+wordlist_path+"\n"

for i in range(len(lines)):
	link = "http://www.hiddns.com/"+lines[i].rstrip()
	
	try:
		resp = h.request(link, "GET")
		#location = resp[0]['content-location']
		content = resp[1]
		checksum = hashlib.md5(content).hexdigest()
		if (checksum != "a559ac794b5224cee24996c589ea293d") & (checksum != "64291e186bb8db6585ae01193957964f"):
			print HEADER + BLUE + INFO + ENDLINE + " " + link + " - " + checksum
			#v.write(link+"\n");
			hostCount += 1;
	except:
		pass
v.close();
print "\n" + HEADER + GREEN + INFO + ENDLINE + " " + str(hostCount) + " total Hosts were found\n";
