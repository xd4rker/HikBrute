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

import httplib2, sys, os.path, signal, hashlib, json, re

if len(sys.argv) == 1:
	print "Error: Usage: ./script.py <WORDLIST_PATH>"
	sys.exit()

if not os.path.isfile(sys.argv[1]):
	print "Error: File doesn't exist"
	sys.exit()

def GetIP(source):
	regex="var url='(.+?)';"
	pattern=re.compile(regex)
	url = re.findall(pattern,source)
	ip = re.findall('[0-9]+(?:\.[0-9]+){3}', url[0])
	
	return ip[0]

def GetLocation(ip):
	h = httplib2.Http(timeout=100)
	link = "http://www.ipinfo.io/"+ip.rstrip()
	resp = h.request(link, headers={'Accept':'application/json'})
	content = resp[1]
	json_decoded = json.loads(content)

	info = [ json_decoded['country'], json_decoded['city'] ]
	info = map(str, info)

	return info

HEADER = "\033[95m"
BLUE = "\033[94m"
GREEN = "\033[92m"
ENDLINE = "\033[0m"
INFO = "[+]"
hostCount = 0;

NotRegistered = "75df0ef069c0dd3f0ccde6e4d7eabe87"
NullRedirect = "eb503a81d7f04f9b4537d0bd67b5c9db"


wordlist_path = sys.argv[1]
f = open(wordlist_path)
lines = f.readlines()
v = open("liveHosts.list", "a");

h = httplib2.Http(timeout=100)

print "\n" + HEADER + BLUE + INFO + ENDLINE + " " + "Using file : "+wordlist_path+"\n"

for i in range(len(lines)):
	link = "http://www.hiddns.com/"+lines[i].rstrip()
	
	try:
		resp = h.request(link, "GET")
		content = resp[1]
		checksum = hashlib.md5(content).hexdigest()

		if (checksum != NotRegistered) & (checksum != NullRedirect):
			Addr = GetIP(content)
			Location = GetLocation(Addr)

			print HEADER + BLUE + INFO + ENDLINE + " " + link + " \t->\t" + Addr + "\t" + Location[0] + " - " + Location[1]
			hostCount += 1;

	except:
		pass
v.close();
print "\n" + HEADER + GREEN + INFO + ENDLINE + " " + str(hostCount) + " total Hosts were found\n";
