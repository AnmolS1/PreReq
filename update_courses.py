import httplib2
from bs4 import BeautifulSoup
import re

file = open ('testing.txt', 'w+')

http = httplib2.Http ()
status, response = http.request ('https://catalog.ucsd.edu/courses/CSE.html')

soup = BeautifulSoup (response, 'html.parser')
tag_remove = re.compile ('<.*?>')
credit_remove = re.compile ('\(.*?\)')

course_names = soup (class_='course-name')
course_descs = soup (class_='course-descriptions')
course_prereqs = []
prereq_string = 'Prerequisites'

for i in range (len (course_names)):
    ##### set up the list of course prerequisites #####
    # remove the html tags from each item
    description = re.sub (tag_remove, '', str (course_descs[i]))
    
    try:
         # get the index of the word "Prerequisites" in the string
        prereq_index = description.index (prereq_string)
        for_prereq = prereq_index + len (prereq_string) + 1
        
        # get the rest of the string, strip any extra spaces
        prereq = description[for_prereq:].strip ()
        # modify description to get rid of the prereq part of it
        course_descs[i] = description[:prereq_index].strip ()
        # capitalize the first letter
        prereq = prereq[0:1].capitalize () + prereq[1:]
        
        # if there was no prereq for this course just go to the except case
        if prereq == 'None.':
            raise ValueError
        
        # append it to the list
        course_prereqs.append (prereq)
    except ValueError:
        # we'll just say "No prerequisites"
        course_prereqs.append ('No ' + prereq_string.lower ())
    
    ##### set up the list of course names #####
    # remove the html tags from each name
    name = re.sub (tag_remove, '', str (course_names[i]))
    # remove the number of credits
    name = re.sub (credit_remove, '', name)
    # trim the string and reset the index
    course_names[i] = name.strip ()
    
    file.write (str (course_names[i]))
    file.write ('\n')
    file.write (str (course_descs[i]))
    file.write ('\n')
    file.write (str (course_prereqs[i]))
    file.write ('\n')

file.close ()