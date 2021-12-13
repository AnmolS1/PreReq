# library imports
import httplib2               # get information from the website
from bs4 import BeautifulSoup # get specific pieces of the html
import re                     # regex to make our job easier

# open the file we're writing to with read and write privileges
file = open('courses.txt', 'w+')

# get the html from the website as a tuple
# first value is website status, second is the response as a string
http = httplib2.Http()
status, response = http.request('https://catalog.ucsd.edu/courses/CSE.html')

# set up some pre-code necessities, the parser using the string
# the regex to remove tags and stuff in parentheses
# and "Prerequisites: " to make our code easier to read
soup = BeautifulSoup(response, 'html.parser')
remover = re.compile('<.*?>|\(.*?\)')
prereq_string = 'Prerequisites: '

# get all the course names and descriptions
course_names = soup(class_='course-name')
course_descs = soup(class_='course-descriptions')

# loop through everything
for i in range(len(course_names)):
    # get the description and remove any tags we don't wanna see
    course_descs[i] = re.sub(remover, '', str(course_descs[i]))
    
    # split by 'Prerequisites: '
    desc = course_descs[i].split(prereq_string)
    
    # if the 'Prerequisites: ' string isn't there then put it in because
    # that'll make the javascript parsing of the file easier for us
    # otherwise capitalize the first word of the prerequisites and smush
    # them back together
    if len(desc) == 1:
        desc = desc[0].strip() + ' ' + prereq_string + 'None.'
    else:
        desc[1] = desc[1][0:1].capitalize() + desc[1][1:]
        desc = desc[0].strip() + ' ' + prereq_string + desc[1].strip()
    
    # remove tags/credits from course names. also if the course name has more
    # than one name (i.e. 'CSE 282/BENG 202') then replace the slash with
    # the equal sign, again makes the javscript much simpler
    name = re.sub(remover, '', str(course_names[i])).strip().split(". ")
    name = name[0].replace("/", " = ") + " = " + name[1]
    
    # write to the file :)
    file.write (name + "\n" + desc + "\n")

file.close()