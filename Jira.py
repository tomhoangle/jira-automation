from jira.client import JIRA
from tkinter import *
import csv
#options = {'server': 'http://localhost:8080/'}
#options = {'server': 'https://jiradev1.daicompanies.com/'}
#jira = JIRA(options, basic_auth=('tom.le', 'PAcka87s!'))

#create jira ticket function
def create_issue( employeeInput, account):
    jira.create_issue(project='WONNOC', summary= employeeInput + ': ' + account,
                                 description='', issuetype={'name': 'Task'})

#Create GUI
"""window = Tk()
window.title("Employee Access Tickets")
window.geometry('600x900') #Set size
#Input Text
nameLabel = Label(window, text ="Employee name")
nameLabel.grid(column=0, row=0)
nameText = Entry(window, width = 40)
nameText.grid(column=1, row=0)

companyList = StringVar(window)
companyList.set("DAI") # default value
companyDrop = OptionMenu(window, companyList, "DAI", "WON", "ODS")
companyDrop.grid(column=1, row=1)
companyLabel = Label(window, text ="Company")
companyLabel.grid(column=0, row =1)

template = StringVar(window)
template.set("NOC")
templateDrop = OptionMenu(window, template, "NOC", "CSM", "Programmer")
templateDrop.grid(column=1, row=2)
templateLabel = Label(window, text='Template')
templateLabel.grid(column=0, row=2)

#print(template.get()) #debug template value
window.mainloop()"""

#Query an issue
"""issueNumber = '792'
issueSearch = 'WONNOC-' + issueNumber
issue = jira.issue(issueSearch, fields='summary,customfield_10102')
print(issue.fields.customfield_10102)"""

#Search through template master list to determine if position exist
#job_title = issue.fields.customfield_10102
job_title = "NOC Master"
job_existed = True;
with open('Master.csv') as csv_master:
    csv_reader = csv.reader(csv_master, delimiter='\n')
    for row in csv_reader:
        if job_title in row:
            job_existed = True
            print("job existed")
        else:
            job_existed = False
            print("Nope, make a new one")

#if position exist, read the templates job file and create tickets
#read CVS file to determine list of access to make
#open_file = issue.fields.customfield_10102 + ".csv"
"""with open('NOC Engineer.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\n')
    my_list = list(csv_reader)

#Create access according to CSV template
for x in range(0 , len(my_list)):
    myStr=''.join(my_list[x])
    #jira.create_issue(project='WONNOC', summary='Tom: ' + myStr,
    #                              description='This is made by API', issuetype={'name': 'Task'})"""


#If template doesn't exist, create a new one with user input and add it to master list after
if(job_existed == False):
    newTemplate = []
    userInput = ''
    print("The job title doesn't have a template, what access do you want to give to this title?")
    while(userInput != "exit"):
        userInput = raw_input("Please enter an access then press enter(enter exit to quit)")
        newTemplate.append(userInput)


print(newTemplate)

#Search for an issue WIP use ID for now
#employeeSearch = jira.search_issues('project=WONNOC', maxResults=1)
#print('{}: {}'.format(employeeSearch.fields.summary))



#jira.create_issue(project='WONNOC', summary='Tom: Python DAI',
                              #description='Testing', issuetype={'name': 'Task'})
