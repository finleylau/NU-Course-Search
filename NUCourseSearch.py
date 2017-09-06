import difflib
from google import search
import requests
import webbrowser

def get_search(subject_names):
	while True:
		q = input('Search for class by symbol and number (example: GEN LA 114): ')
		print('Searching course catalog...')
		if q in subject_names:
			return q
		else:
			most_relevant = 0
			search_success = False
			for course in subject_names:
				relevance = difflib.SequenceMatcher(None,q,course).ratio()
				if relevance >= .75:
					if relevance >= most_relevant:
						search_success = True
						most_relevant = relevance
						most_relevant_course = course
			if search_success:
				print('Couldn\'t find your exact search... did you mean {}?'.format(most_relevant_course))
			else:
				print('Couldn\'t find what you searched for, please try something else')

def check_quit():
	while True:
		quit = input('Done searching for classes? (Y or N) ')
		if quit == 'Y' or quit == 'y':
			return True
		elif quit == 'N' or quit == 'n':
			return False
		else:
			print('Invalid input')

"""
Get API data
"""
print('DISCLAIMER: This is NOT a Northwestern University application and is not affiliated with the University in any way.')
print()
API_KEY = '<NORTHWESTERN API KEY>'
# get latest term
params = {'key': API_KEY}
print('Getting latest term...')
terms = requests.get('http://api.asg.northwestern.edu/terms/', params=params).json()
latest_term = terms[0]

# get list of all subjects
params['term'] = latest_term['id']
print('Getting subjects...')
subjects = requests.get('http://api.asg.northwestern.edu/subjects/',params=params).json()

# get list of courses
courses = {}
wait = 1
print('Getting courses...')
for subject in subjects:
	params['subject'] = subject['symbol']
	subject_courses = requests.get('http://api.asg.northwestern.edu/courses/',params=params).json()

	# create course search name (EECS 111)
	for course in subject_courses:
		course['search_name'] = course['subject'].replace('_',' ') + ' ' + course['catalog_num']
		courses[course['search_name']] = course
	if wait % 57 == 0:
		print('Processing... please be patient...')
	wait += 1

print('Done getting courses!')


"""
Search for courses
"""

while True:
	# get user's input
	print()
	q = get_search(courses.keys())

	# display results

	# in command line, display subject, number, and title
	print()
	print('Course: {}'.format(courses[q]['search_name']))
	print('Title: {}'.format(courses[q]['title']))
	print()

	# search internet and display urls
	print('Searching the Internet...')
	search_q = 'Northwestern University '+ q + ' {}'.format(courses[q]['title'])

	print('Here are some relevant course links...')
	print()
	urls = []
	for url in search(search_q, stop=1):
		print(url)
		urls.append(url)

	# open top result in browser
	print()
	print('Opening {}...'.format(urls[0]))
	webbrowser.open_new_tab(urls[0])

	# end process
	if check_quit():
		print()
		print('Thanks for using NU Course Search!')
		print('Quitting...')
		print()
		break
	else:
		print()