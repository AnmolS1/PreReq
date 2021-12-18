# library imports
import httplib2               # get information from the website
from bs4 import BeautifulSoup # get specific pieces of the html
import re                     # regex to make our job easier

# open the file we're writing to with read and write privileges
file = open('courses.json', 'w+')
file.write('[\n')

# get the html from the website as a tuple
# first value is website status, second is the response as a string
http = httplib2.Http()
status, response = http.request('https://catalog.ucsd.edu/courses/CSE.html')

# set up some pre-code necessities, the parser using the string
# the regex to remove tags and stuff in parentheses
# and "Prerequisites: " to make our code easier to read
soup = BeautifulSoup(response, 'html.parser')
remover = re.compile('<.*?>|\(.*?\)')
replacer = re.compile('\/|(\. )')
prereq_string = 'Prerequisites: '

# get all the course names and descriptions
course_names = soup(class_='course-name')
course_descs = soup(class_='course-descriptions')

# loop through everything
for i in range(len(course_names)):
    # step 1: remove tags/credits from the course name
    # step 2: replace '. ' and '/' with ' = '
    # step 3: split by ' = '
    # making it a one liner because i can.
    names = re.sub(replacer, ' = ', re.sub(remover, '', str(course_names[i]))).split(' = ')

    # get the description and remove any tags we don't wanna see
    course_descs[i] = re.sub(remover, '', str(course_descs[i]))
    # split by 'Prerequisites: '
    desc = course_descs[i].split(prereq_string)

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
        to_write += '\t{\n'
        to_write += '\t\t"name": "' +  names[n].strip() + '",\n'
        to_write += '\t\t"description": "' + desc[0].strip() + '",\n'
        to_write += '\t\t"prerequisites": "' + desc[1].strip() + '"\n'
        to_write += '\t}'
        if not (i == len(course_names) - 1 and n == len(names) - 1):
            to_write += ','
        to_write += '\n'

    file.write(to_write)

file.write(']')
file.close()
