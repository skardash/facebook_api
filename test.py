import time
import urllib3
import facebook
import requests
import json
import pycountry
import matplotlib as mpl
import matplotlib.pyplot as plt
from pylab import figure

import os, sys

reload(sys)
sys.setdefaultencoding('utf-8')

dr = "results"
if not(os.path.exists(dr)):
	os.mkdir(dr, 0755 );

mpl.rcParams['font.size'] = 7.0

# creating mapping {country code:country name}

token= 'EAAa6GjT5ZCKEBADNEq3Wv3UR6anD5d7d13W7K8odmojkUYqAAk1ZAK2NvWLP6mccxsjfZCdiEWUsva6pXb5XY4Th7lDsPwzAmmxWf87ZAaBQLTU0nQy1PH3PS06scieWUuF6BeQRIkWgIvqLF4g5mO4SEOJwsN4ZD'

graph = facebook.GraphAPI(access_token=token, version = 2.7)
events = graph.request("142419476309361/insights?metric=page_fans,page_fans_gender_age,page_fans_country,page_fans_city")
f = open('insights', 'w')
jstr = json.dumps(events, indent=4, sort_keys=True)
f.write(jstr)
f.close()

#total likes
print("--------------------------------------")
total_likes = events["data"][0]["values"][1]["value"]
print("total likes: " + str(total_likes))

#gender_age
print("--------------------------------------")
gender_age = events["data"][1]["values"][1]["value"]
for key, value in gender_age.iteritems():
	print(key + ":" + str(value))

#separate the data
mk = []
mv = []
fk = []
fv = []
for key, value in gender_age.iteritems():
	if key[0] == 'M':
		mk.append(key)
		mv.append(value)
	else:
		fk.append(key)
		fv.append(value)


explode_single = 0.2
explode_general = 0.05

labels_list = gender_age.keys()
vals_combined = gender_age.values()

labels_combined = tuple(sorted(labels_list))
vals_combined = [vals for (labels,vals) in sorted(zip(labels_list, vals_combined))]
explode_combined = (explode_single,) + (explode_general,)*(len(labels_combined)-1)

labels_male = tuple(sorted(mk))
vals_male = [vals for (labels,vals) in sorted(zip(mk, mv))]
explode_male = (explode_single,) + (explode_general,)*(len(labels_male)-1)

labels_female = tuple(sorted(fk))
vals_female = [vals for (labels,vals) in sorted(zip(fk, fv))]
explode_female = (explode_single,) + (explode_general,)*(len(labels_female)-1)

f, ax = plt.subplots(2, 2, sharey=True)
f.canvas.set_window_title('Pizzaforest gender&age statistics')
p = ax[0,0].pie(vals_combined, explode=explode_combined, labels=labels_combined, autopct='%1.0f%%', shadow=True, startangle=90)
ax[0,0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax[0,0].legend(labels_combined, loc="upper left")
ax[0,0].set_title('Averall statistics')

ax[0,1].pie(vals_male, explode=explode_male, labels=labels_male, autopct='%1.1f%%', shadow=True, startangle=90)
ax[0,1].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax[0,1].set_title('Male statistics')
ax[1,0].pie(vals_female, explode=explode_female, labels=labels_female, autopct='%1.1f%%', shadow=True, startangle=90)
ax[1,0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax[1,0].set_title('Female statistics')
ax[1,1].axis('off')

f.savefig(dr+'/gender_age.png')

#country
print("--------------------------------------")
t = list(pycountry.countries)
cc = {}
for country in t:
    cc[country.alpha_2]=country.name
country = events["data"][2]["values"][1]["value"]
list_country = []
list_values = []
for key, value in country.iteritems():
	if key in cc:
		print(cc[key] + ":" + str(value))
		list_country.append(cc[key])
	else:
		print(key + ":" + str(value) + "(unknown country key code)")
		list_country.append(key)
	list_values.append(value)

labels = tuple(sorted(list_country))
sizes = [val for (label,val) in sorted(zip(list_country, list_values))]

explode_single = 0.2
explode_general = 0.05
explode = (explode_single,) + (explode_general,)*(len(labels)-1)

f2, ax = plt.subplots()
f2.canvas.set_window_title('Pizzaforest country statistics')
patches, texts, xxx = ax.pie(sizes, labels=labels, explode = explode, autopct='%1.1f%%', shadow=True, startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.legend(patches, labels, loc="upper left")

f2.savefig(dr+'/country.png')

#city
print("--------------------------------------")
f = open(dr+'/citystats.txt', 'w')
city = events["data"][3]["values"][1]["value"]
for key, value in city.iteritems():
	print(key + ":" + str(value))
	f.write(key + ":" + str(value) + "\n")
f.close()

# create kind of diagram for that data
plt.show()