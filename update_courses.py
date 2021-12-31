# library imports
import httplib2               # get information from the website
from bs4 import BeautifulSoup # get specific pieces of the html
import re                     # regex to make our job easier

# open the file we're writing to with read and write privileges
file = open('courses.json', 'w+')
file.write('[')

# get the html from the website as a tuple
# first value is website status, second is the response as a string
http = httplib2.Http()
status, response = http.request('https://catalog.ucsd.edu/front/courses.html')

# set up some pre-code necessities, the parser using the string
# the regex to remove tags and stuff in parentheses
# and "Prerequisites: " to make our code easier to read
soup = BeautifulSoup(response, 'html.parser')
remover = re.compile('<.*?>|\(.*?\)')
replacer = re.compile('\/|(\. )')
prereq_string = 'Prerequisites: '

# get all the links and then make sure we only look at the ones about courses at UCSD
all_links = soup.select('a[href]')
fixer = filter(lambda link: 'courses' in link, all_links)
all_links = list(fixer)

# go through each link and get all the courses
for i in range(len(all_links)):
	# use the link starter and just tack on the name of each course
	status, response = http.request('https://catalog.ucsd.edu' + all_links[i].get('href')[2:])
	soup = BeautifulSoup(response, 'html.parser')

	# get all the course names and descriptions
	course_names = soup(class_='course-name')
	# the course descriptions will always be right after the course names
	# we have to do this because one case arose where the paragraph tag
	# did not have the class attribute which causes an error
	course_descs = []
	for name in course_names:
		course_descs.append(name.next_element.next_element.next_element)

	# loop through everything
	for j in range(len(course_names)):
		# get the name(s) of the course
		names = re.sub(replacer, ' = ', re.sub(remover, '', str(course_names[j]))).split(' = ')

		# get the description and remove any tags we don't wanna see
		course_descs[j] = re.sub(remover, '', str(course_descs[j]))
		# split by 'Prerequisites: '
		desc = course_descs[j].split(prereq_string)

		# if the 'Prerequisites: ' string isn't there then put it in because
		# that'll make the javascript parsing of the file easier for us
		# otherwise capitalize the first word of the prerequisites and smush
		# them back together
		desc[0] = desc[0].strip()
		if len(desc) == 1:
			desc.append('None.')
		else:
			desc[1] = desc[1][0:1].capitalize() + desc[1][1:]

		# write to the file :)
		to_write = ''
		for n in range(len(names)):
			to_write += '\n\t{\n\t\t"name": "' +  names[n].strip() + '",\n'
			to_write += '\t\t"description": "' + desc[0].strip() + '",\n'
			to_write += '\t\t"prerequisites": "' + desc[1].strip() + '"\n\t}'
			to_write += ',' if i != len(all_links) - 1 or j != len(course_names) - 1 or n != len(names) - 1 else ''

		file.write(to_write)

file.write('\n]')
file.close()
