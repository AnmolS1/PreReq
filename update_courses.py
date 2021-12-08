import httplib2
from bs4 import BeautifulSoup
import re

file = open('courses.txt', 'w+')

http = httplib2.Http()
status, response = http.request('https://catalog.ucsd.edu/courses/CSE.html')

soup = BeautifulSoup(response, 'html.parser')
remover = re.compile('<.*?>|\(.*?\)')
prereq_string = 'Prerequisites: '

course_names = soup(class_='course-name')
course_descs = soup(class_='course-descriptions')

descriptions = []
course_dict = {}

for i in range(len(course_names)):
    course_descs[i] = re.sub(remover, '', str(course_descs[i]))
    description = course_descs[i]
    
    temp = course_descs[i].split(prereq_string)
    
    if len(temp) == 1:
        descriptions.append([course_descs[i].strip(), "No Prerequisites."])
    else:
        temp[1] = temp[1][0:1].capitalize() + temp[1][1:]
        descriptions.append([temp[0].strip(), temp[1].strip()])
    
    temp = re.sub(remover, '', str(course_names[i])).strip().split(". ")
    
    course_dict[temp[0]] = descriptions[i]
    course_dict[temp[1]] = descriptions[i]
    
    name = temp[0] + " = " + temp[1]
    desc = descriptions[i][0] + " Prerequisites: " + descriptions[i][1]
    file.write (name + "\n" + desc + "\n")

file.close()