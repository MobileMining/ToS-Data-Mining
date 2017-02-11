#help from http://docs.python-guide.org/en/latest/scenarios/scrape/

from lxml import html
import requests
import csv

def url_to_list(i): # -> string
	if txt(i) != '\n':
		return (txt(i)[:-1])

def card_to_list(i): # -> list

	card_id = str(txt(i[0][2]))
	card_name = str(txt(i[0][4]).encode('ascii','ignore'))
	card_attribute = str(txt(i[0][6]))
	card_element = str(txt(i[0][8]))
		
	card_maxlvl = str(txt(i[1][1]))
	card_expcurve = str(txt(i[1][3]))
	card_maxexp = str(txt(i[1][5]))
	card_rarity = str(txt(i[1][7])[1].encode('ascii','ignore')) #encode is needed as this element is in unicode
														   #first element is the unicode for star, and 2nd is the star #
	card_cost = str(txt(i[1][9]))
	card_series = str(txt(i[1][11])[:-1].encode('ascii','ignore')) #this gives a string with '\n' concatenated at the end, therefore splice it out
	
	card_lvl_1_HP = str(txt(i[2][1]))
	card_lvl_1_ATK = str(txt(i[2][3]))
	card_lvl_1_REC = str(txt(i[2][5]))
	card_lvl_max_HP = str(txt(i[2][7]))
	card_lvl_max_ATK = str(txt(i[2][9]))
	card_lvl_max_REC = str(txt(i[2][11]))
	
	if len(i[3]) == 4:
		card_active_skill_1_title = str(txt(i[3][1][0]).encode('ascii','ignore')) #this is needed as there is a seperate br tag for <a href>
		card_active_skill_1_desc = str(txt(i[3][1])[len(card_active_skill_1_title):-1].encode('ascii','ignore')) #seperate title from description
		
		card_leader_skill_title = str(txt(i[3][3][0]).encode('ascii','ignore')) #like card_active_skill_title
		card_leader_skill_desc = str(txt(i[3][3])[len(card_leader_skill_title):].encode('ascii','ignore'))
		
		card_active_skill_2_title = ''
		card_active_skill_2_desc = ''
	elif len(i[3]) == 6: #this is for cards with two active skills
		card_active_skill_1_title = str(txt(i[3][1][0]).encode('ascii','ignore')) #this is needed as there is a seperate br tag for <a href>
		card_active_skill_1_desc = str(txt(i[3][1])[len(card_active_skill_1_title):-1].encode('ascii','ignore')) #seperate title from description
		
		card_active_skill_2_title = str(txt(i[3][3][0]).encode('ascii','ignore')) #this is needed as there is a seperate br tag for <a href>
		card_active_skill_2_desc = str(txt(i[3][3])[len(card_active_skill_2_title):-1].encode('ascii','ignore')) #seperate title from description		
		
		card_leader_skill_title = str(txt(i[3][5][0]).encode('ascii','ignore')) #like card_active_skill_title
		card_leader_skill_desc = str(txt(i[3][5])[len(card_leader_skill_title):].encode('ascii','ignore'))
	else: #in case of weird stuff, makes it easier to see in csv file
		card_active_skill_1_title = ''
		card_active_skill_1_desc = ''
		card_active_skill_2_title = ''
		card_active_skill_2_desc = ''
		card_leader_skill_title = ''
		card_leader_skill_desc = ''
	
	return [card_id,card_name,card_attribute,card_element,
			card_maxlvl,card_expcurve,card_maxexp,card_rarity,card_cost,card_series,
			card_lvl_1_HP,card_lvl_1_ATK,card_lvl_1_REC,
			card_lvl_max_HP,card_lvl_max_ATK,card_lvl_max_REC,
			card_active_skill_1_title,card_active_skill_1_desc,
			card_active_skill_2_title,card_active_skill_2_desc,
			card_leader_skill_title,card_leader_skill_desc]
		
def txt(ele): #turn HTML element into string
	return ele.text_content()
	
base_url = 'http://towerofsaviors.wikia.com/wiki/Gallery_'

#to initially grab the indexing
page = requests.get('http://towerofsaviors.wikia.com/wiki/Gallery_001-050')
tree = html.fromstring(page.content)

#----- INDEXING -----
index_db = [] #this will be for the used to index through the site
xpath_index = '//*[@id="mw-content-text"]/table[1]'
index_tree = tree.xpath(xpath_index)

for row in range(1,len(index_tree[0])): #cannot start from 0 as it is just a string. should be 1,5 (for now)
	for col in range(len(index_tree[0][row])): #goes up to 10
		index = txt(index_tree[0][row][col])
		if index != '\n':
			index_db.append(index[:-1])

#print index_db
		
#----- CARD INDEXING -----
card_db = []
#first element are the names of the columns
card_db.append(['ID','Name','Attribute','Race','Max Lvl','Exp Curve','Max Exp','Rarity','Cost','Series',
				'Lvl 1 HP','Lvl 1 ATK','Lvl 1 REC','Lvl Max HP','Lvl Max ATK','Lvl Max REC',
				'Active Skill 1','Active Skill 1 Description','Active Skill 2','Active Skill 2 Description','Leader Skill','Leader Skill Description'])

for ext_url in index_db:
	full_url = base_url + ext_url
	new_page = requests.get(full_url)
	tree = html.fromstring(new_page.content)
	
	xpath_cards = '//*[@id="mw-content-text"]'
	gallery_tree = tree.xpath(xpath_cards)
	card_root = gallery_tree[0].find_class('wikitable shadow')
	
	for card in card_root:
		card_db.append(card_to_list(card))
	
print len(card_db)

with open('tosdb.csv', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows(card_db)