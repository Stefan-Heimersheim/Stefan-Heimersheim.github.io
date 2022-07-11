from copy import copy, deepcopy
from os import listdir, mkdir
from os.path import isdir, isfile, join
from shutil import copyfile, copy2


output_path = "docs/"
content_path = "content/"
template_path = "templates/"
resource_path = "resources/"

with open(template_path+"header.html", "r") as f:
    header = f.readlines()
source = "".join(header)

with open(template_path+"footer.html", "r") as f:
    footer = f.readlines()
footer = "".join(footer)

menu = "	<a href='//heimersheim.eu/'><b>heimersheim.eu</b></a>"


website = {
	'Home':{
		'url': 'index',
		'shortdesc': "Who I am",
		'enabled': True,
		'content': {
			'Hello, world!': {
				'tag': 'HelloWorld',
				'html': "about.html",
				},
			},
		},
	'Science & Outreach':{
		'url': 'science',
		'shortdesc': "Various Science and Outreach things",
		'enabled': True,
		'content': {
			'Ask An Astronomer': {
				'tag': 'AskAnAstronomer',
				'html': "aaa.html",
				},
			'Evaluating Planck likelihoods': {
				'tag': 'PlanckLikelihoods',
				'html': "planck.html",
				},
			},
		},
	'Talks':{
		'shortdesc': "Slides for talks I have given",
		'enabled': False,
		'content': "",
	},
	'Projects':{
		'url': 'projects',
		'shortdesc': "Various (usually non-science) projects",
		'enabled': True,
		'content': {
			'Fingerprint-based full-disk encryption on Linux': {
				'tag': 'secure',
				'html': "secureboot_fingerprint.html",
			},
		},
	},
	'Contact':{
		'url': 'contact',
		'shortdesc': "Contact me",
		'enabled': True,
		'content': {
			'Contact me': {
				'tag': 'contactme',
				'html': "contactme.html",
				},
			'Legal information': {
				'tag': 'legal',
				'html': "legal.html",
				},
			},
		},
	}

website = {}
for topic in listdir(content_path):
	name = topic.capitalize()
	website[name] = {}
	url = topic.lower()
	if url=="home":
		website[name]["url"] = "index"
	else:
		website[name]["url"] = url
	item_path = content_path+"/"+topic+"/"
	website[name]["content"] = []
	#shortdesc, enabled not needed
	for item in listdir(item_path):
		website[name]["content"].append(item)
		# key is already html, tag not needed


if not isdir(output_path):
	mkdir(output_path)

rs = [f for f in listdir(resource_path) if isfile(join(resource_path, f))]
for resource in rs:
	copy2(join(resource_path, resource), join(output_path, resource))


topics = list(website.keys())
topics.sort()
topics = [topics[i+1] for i in range(len(topics)-1)]+[topics[0]]

for currenttopic in topics:
	currentsource = copy(source)
	menu = ""
	for topic in topics:
		#topiclink = "https://heimersheim.eu/"+website[topic]['url']
		topiclink = "./"+website[topic]['url']+'.html'
		if topic == currenttopic:
			menu+="	<a href='{0:}' title='{1:}'><b>{2:}</b></a>\n".format(topiclink, topic, topic)
		else:
			menu+="	<a href='{0:}' title='{1:}'>{2:}</a>\n".format(topiclink, topic, topic)
	currentcontent = ""
	nav = ""
	for item in website[currenttopic]['content']:
		tag = item[:-5] #.html
		title = "Hello, world!" if tag=="about" else tag.capitalize()
		nav += "		<li><a href='#{0:}'>{1:}</a></li>\n".format(tag, title)
		currentcontent += "<a href='#{0:}'><h1 id='{0:}'>{1:}</h1></a>\n".format(tag,title)
		with open(content_path+"/"+currenttopic+"/"+item, 'r') as html:
			currentcontent += html.read()+"\n"
	currentcontent += footer
	currentsource = currentsource.format(currenttopic, menu[:-1], nav[:-1], currentcontent)
	with open(output_path+website[currenttopic]['url']+'.html', "w+") as f:
		f.write(currentsource)
		
