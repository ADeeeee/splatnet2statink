# eli fessler
import os.path, argparse
import requests, json

A_NAME = "splatnet2statink"
A_VERSION = "0.0.7"

API_KEY = "emITHTtDtIaCjdtPQ0s78qGWfxzj3JogYZqXhRnoIF4" # testing account API key. please replace with your own!

YOUR_COOKIE = "" # keep this secret!

# auth app.splatoon2.nintendo.net, generate cookie
# ???

# I/O
parser = argparse.ArgumentParser()
parser.add_argument("-i", dest="filename", required=False,
help="path to results JSON", metavar="/path/to/results.json")
result = parser.parse_args()

if result.filename != None: # local file provided
	if not os.path.exists(result.filename):
		parser.error("File %s does not exist!" % result.filename) # exit
	with open(result.filename) as data_file:
		data = json.load(data_file)
else: # no argument
	print "Pulling data from online..." # grab data from SplatNet
	url = "https://app.splatoon2.nintendo.net/api/results"
	r = requests.get(url, cookies=dict(iksm_session=YOUR_COOKIE))
	data = json.loads(r.text)

try:
	results = data["results"] # all we care about
except KeyError: # no 'results' key, which means...
	print "Bad cookie."
	exit(1)

try:
	n = int(raw_input("Number of recent battles to upload (0-50)? "))
except ValueError, ex:
	print "Please enter an integer between 0 and 50."
	exit(1)
if n == 0:
	print "Exiting without uploading anything."
	exit(0)
elif n > 50:
	print "Cannot upload battle #" + str(n) + ". SplatNet 2 only stores the 50 most recent battles."
else:
	pass

# JSON parsing, fill out payload
# https://github.com/fetus-hina/stat.ink/blob/master/doc/api-2/post-battle.md
payload = {'agent': A_NAME, 'agent_version': A_VERSION}

# Weapon database
# https://stat.ink/api/v2/weapon
translate_weapons = {
	'.52 Gal': '52gal',
	'.96 Gal': '96gal', # 50
	'Clash Blaster': 'clashblaster', # 230
	'Dualie Squelchers': 'dualsweeper', # 5030
	'H-3 Nozzlenose': 'h3reelgun',
	'Custom Blaster': 'hotblaster_custom',
	'Blaster': 'hotblaster', # 210
	'Jet Squelcher': 'jetsweeper',
	'L-3 Nozzlenose': 'l3reelgun', # 300
	'Enperry Splat Dualies': 'maneuver_collabo',
	'Splat Dualies': 'maneuver', # 5010
	'Luna Blaster': 'nova',
	'N-ZAP \'85': 'nzap85',
	'Splattershot Pro': 'prime', # 70
	'Aerospray MG': 'promodeler_mg', # 30
	'Aerospray RG': 'promodeler_rg',
	'Rapid Blaster': 'rapid',
	'Splash-o-matic': 'sharp',
	'Dapple Dualies': 'sputtery',
	'Tentatek Splattershot': 'sshooter_collabo',
	'Splattershot': 'sshooter',
	'Splattershot Jr.': 'wakaba',
	'Carbon Roller': 'carbon', # 1000
	'Dynamo Roller': 'dynamo',
	'Octobrush': 'hokusai', # 1110
	'Inkbrush': 'pablo',
	'Krak-On Splat Roller': 'splatroller_collabo',
	'Splat Roller': 'splatroller',
	'Flingza Roller': 'variableroller',
	'E-liter 4K Scope': 'liter4k_scope', # check capitalization, en_GB spelling
	'E-litre 4K Scope': 'liter4k_scope',
	'E-liter 4K ': 'liter4k',
	'E-litre 4K ': 'liter4k',
	'Goo Tuber': 'soytuber',
	'Firefin Splat Charger': 'splatcharger_collabo',
	'Splat Charger': 'splatcharger',
	'Firefin Splatterscope': 'splatscope_collabo',
	'Splatterscope': 'splatscope',
	'Slosher': 'bucketslosher', # 3000
	'Tri-Slosher': 'hissen', # 3010
	'Heavy Splatling': 'barrelspinner',
	'Mini Splatling': 'splatspinner' # 4000
}

# Stage database
# codes @ https://app.splatoon2.nintendo.net/api/data/stages (needs auth)
translate_stages = {
	0: 'battera', # The Reef
	1: 'fujitsubo', # Musselforge Fitness
	2: 'gangaze', # Starfish Mainstage
	3: 'chozame', # Sturgeon Shipyard
	4: 'ama', # Inkblot Art Academy
	5: 'combu', # Humpback Pump Track
	# wtf nintendo
	7: 'hokke', # Port Mackerel
	8: 'tachiuo', # Moray Towers
	9999: 'mystery' # Shifty Station (Splatfest only)
}

# # Gear database
# translate_headgear = {
# 	5000: 'Studio Headphones',
# }
# translate_clothing = {
# 	5018: 'Takoroka Windcrusher',
# }
# translate_shoes = {
# 	4009: 'Snow Delta Straps',
# }

# Ability database
# Still missing a few abilities (100 - 111), I think I know what they are but need confirmation
translate_ability = {
	-1:  'Not Unlocked', # The slot is either waiting to be levelled (?) or not unlocked yet
	0:   'Ink Saver (Main)',
	1:   'Ink Saver (Sub)',
	2:   'Ink Recovery Up',
	3:   'Run Speed Up',
	4:   'Swim Speed Up',
	5:   'Special Charge Up',
	6:   'Special Saver',
	7:   'Special Power Up',
	8:   'Quick Respawn',
	9:   'Quick Super Jump',
	10:  'Sub Power Up',
	11:  'Ink Resistance Up',
	12:  'Bomb Defense Up',
	13:  'Cold-Blooded',
	100: 'Opening Gambit',
	101: 'UNKNOWN', # Last-Ditch Effort?
	102: 'Tenacity',
	103: 'UNKNOWN', # Comeback?
	104: 'UNKNOWN', # Ninja Squid
	105: 'UNKNOWN', # Thermal Ink
	106: 'UNKNOWN', # Haunt
	107: 'UNKNOWN', # Respawn Punisher
	108: 'Ability Doubler',
	109: 'UNKNOWN', # Stealth Jump?
	110: 'UNKNOWN', # Object Shredder?
	111: 'UNKNOWN' # Drop Roller?
}

# Prepare to POST to stat.ink
url     = 'https://stat.ink/api/v2/battle'
auth    = {'Authorization': 'Bearer ' + API_KEY}

for i in range (0, n):
	# regular, league_team, league_pair, private
	lobby          = results[i]["game_mode"]["key"]
	# regular, gachi, league, ???
	mode           = results[i]["type"]
	# turf_war, rainmaker, splat_zones, tower_control
	rule           = results[i]["rule"]["key"]
	stage          = results[i]["stage"]["id"]                               # string (see above)
	weapon         = results[i]["player_result"]["player"]["weapon"]["name"] # string (see above)
	# victory, defeat
	result         = results[i]["my_team_result"]["key"]
	turfinked      = results[i]["player_result"]["game_paint_point"]         # WITHOUT bonus
	kill           = results[i]["player_result"]["kill_count"]
	kill_or_assist = results[i]["player_result"]["assist_count"] + kill
	special        = results[i]["player_result"]["special_count"]
	death          = results[i]["player_result"]["death_count"]
	level_after    = results[i]["player_rank"]
	level_before   = results[i]["player_result"]["player"]["player_rank"]
	start_time     = results[i]["start_time"]
	try:
		rank_before    = results[i]["udemae"]["name"]
		rank_after     = results[i]["player_result"]["player"]["udemae"]["name"]
	except KeyError:
		pass # don't need to handle - won't be put into the payload unless relevant
	try:
		elapsed_time   = results[i]["elapsed_time"] # apparently only a thing in ranked
	except KeyError:
		elapsed_time   = 180 # turf war - 3 minutes in seconds

	# headgear_id  = results[i]["player_result"]["player"]["head"]["id"]
	# clothing_id  = results[i]["player_result"]["player"]["clothes"]["id"]
	# shoes_id     = results[i]["player_result"]["player"]["shoes"]["id"]

	headgear_main  = results[i]["player_result"]["player"]["head_skills"]["main"]["id"]
	clothing_main  = results[i]["player_result"]["player"]["clothes_skills"]["main"]["id"]
	shoes_main     = results[i]["player_result"]["player"]["shoes_skills"]["main"]["id"]

	headgear_subs = [-1,-1,-1]
	for j in range (0, 3):
		try:
			headgear_subs[j] = results[i]["player_result"]["player"]["head_skills"]["subs"][j]["id"]
		except TypeError:
			headgear_subs[j] = '-1'

	clothing_subs = [-1,-1,-1]
	for j in range (0, 3):
		try:
			clothing_subs[j] = results[i]["player_result"]["player"]["clothes_skills"]["subs"][j]["id"]
		except TypeError:
			clothing_subs[j] = '-1'

	shoes_subs = [-1,-1,-1]
	for j in range (0, 3):
		try:
			shoes_subs[j] = results[i]["player_result"]["player"]["shoes_skills"]["subs"][j]["id"]
		except TypeError:
			shoes_subs[j] = '-1'

	# lobby
	if lobby == "regular":
		payload["lobby"] = "standard"
	elif lobby == "league_pair":
		payload["lobby"] = "squad_2"
	elif lobby == "league_team":
		payload["lobby"] = "squad_4"
	elif lobby == "private":
		payload["lobby"] = "private"
		payload["mode"] = "private"

	# mode
	if mode == "regular":
		payload["mode"] = "regular"
	elif mode == "gachi" or mode == "league":
		payload["mode"] = "gachi"
	# to do - splatfest
	# private handled above

	# rule
	if rule == "turf_war":
		payload["rule"] = "nawabari"
	elif rule == "splat_zones":
		payload["rule"] = "area"
	elif rule == "tower_control":
		payload["rule"] = "yagura"
	elif rule == "rainmaker":
		payload["rule"] = "hoko"

	# stage
	payload["stage"] = translate_stages[int(stage)]

	# weapon
	payload["weapon"] = translate_weapons[weapon]

	# result
	if result == "victory":
		payload["result"] = "win"
	elif result == "defeat":
		payload["result"] = "lose"

	# team percents/counts
	if mode == "regular":
		payload["my_team_percent"] = results[i]["my_team_percentage"]
		payload["his_team_percent"] = results[i]["other_team_percentage"]
	elif mode == "gachi" or mode == "league":
		payload["my_team_count"] = results[i]["my_team_count"]
		payload["his_team_count"] = results[i]["other_team_count"]
	# private...

	# my_point
	if rule == "turf_war": # only upload if TW
		if result == "victory":
			payload["my_point"] = turfinked + 1000 # win bonus
		else:
			payload["my_point"] = turfinked

	# kills, etc.
	payload["kill"] = kill
	payload["kill_or_assist"] = kill_or_assist
	payload["special"] = special
	payload["death"] = death

	# level
	payload["level"] = level_before
	payload["level_after"] = level_after

	# rank
	if rule != "turf_war": # only upload if Ranked
		payload["rank"] = rank_before.lower()
		payload["rank_after"] = rank_after.lower()

	# battle times
	payload["start_at"] = start_time
	payload["end_at"] = start_time + elapsed_time

	# gear - not implemented in stat.ink API v2 yet
	# API v1: https://github.com/fetus-hina/stat.ink/blob/master/doc/api-1/constant/gear.md
	# payload["headgear"] = translate_headgear[int(headgear_id)]
	# payload["clothing"] = translate_clothing[int(clothing_id)]
	# payload["shoes"] = translate_shoes[int(shoes_id)]

	# abilities - also not implemented in stat.ink API v2 (yet)
	# API v1: https://github.com/fetus-hina/stat.ink/blob/master/doc/api-1/constant/ability.md
	# payload["headgear_main"] = translate_ability[int(headgear_main)]
	# payload["clothing_main"] = translate_ability[int(clothing_main)]
	# payload["shoes_main_name"] = translate_ability[int(shoes_main)]
	# payload["headgear_sub1"] = translate_ability[int(headgear_subs[0])]
	# payload["headgear_sub2"] = translate_ability[int(headgear_subs[1])]
	# payload["headgear_sub3"] = translate_ability[int(headgear_subs[2])]
	# payload["clothing_sub1"] = translate_ability[int(clothing_subs[0])]
	# payload["clothing_sub2"] = translate_ability[int(clothing_subs[1])]
	# payload["clothing_sub3"] = translate_ability[int(clothing_subs[2])]
	# payload["shoes_sub1"] = translate_ability[int(shoes_subs[0])]
	# payload["shoes_sub2"] = translate_ability[int(shoes_subs[1])]
	# payload["shoes_sub3"] = translate_ability[int(shoes_subs[2])]

	# debugging
	# print payload

	# POST request
	r = requests.post(url, headers=auth, data=payload)

	# Response
	try:
		print "Battle #" + str(i+1) + " uploaded to " + r.headers.get('location') # display url
	except TypeError: # r.headers.get is likely NoneType, i.e. we received an error
		print "Error uploading battle #" + str(i+1) + ". Message from server:"
		print r.content