from jira.client import JIRA
from tkinter import *
import csv
#options = {'server': 'http://localhost:8080/'}
options = {'server': 'https://jiradev1.daicompanies.com/'}
#jira = JIRA(options, basic_auth=('xxxxx', 'xxxxxxx'))

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
issueNumber = input("Please enter the ticket ID: ")
issueSearch = 'WONNOC-' + issueNumber
issue = jira.issue(issueSearch, fields='summary,customfield_10102')
employee_name = issue.fields.summary
job_title = issue.fields.customfield_10102
print("Employee's name: " + employee_name)
print("Employee's title: " + job_title)

#Search through template master list to determine if position exist
#job_title = issue.fields.customfield_10102


with open('Master.csv') as csv_master:
    csv_reader = csv.reader(csv_master, delimiter='\n')
    for row in csv_reader:
        if job_title in row:
            print("Template existed, making tickets now")
            #if position exist, read the templates job file and create tickets
            #read CVS file to determine list of access to make
            open_file = job_title + ".csv"
            with open(open_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='\n')
                my_list = list(csv_reader)
            #Create access according to CSV template
            for x in range(0 , len(my_list)):
                myStr=''.join(my_list[x])
                jira.create_issue(project='WONNOC', summary=employee_name + ': ' + myStr,
                                              description='This is made by API', issuetype={'name': 'Task'});
                print(myStr + " ticket created")
            print("Done")
            break;
        #template doesn't exist, make a new one
        else:
            #Create new template and store it
            print("Template doesn't exist, please follow instruction below to create a new one")
            newTemplate = []
            userInput = ''
            print("The job title doesn't have a template, what access do you want to give to this title?")
            while(userInput != "exit"):
                userInput = input("Please enter an access then press enter(enter exit to quit)")
                if(userInput != "exit"):
                    newTemplate.append(userInput)
            open_file = job_title + ".csv"
            with open (open_file, 'w') as newFile:
                writeNew = csv.writer(newFile, dialect='excel')
                newFile.write("\n".join(newTemplate))
            print("New template for " + job_title + " has been created.")
            #start creating tickets with new template
            with open(open_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='\n')
                my_list = list(csv_reader)
            #Create access according to CSV template
            for x in range(0 , len(my_list)):
                myStr=''.join(my_list[x])
                jira.create_issue(project='WONNOC', summary=employee_name + ': ' + myStr,
                                              description='This is made by API', issuetype={'name': 'Task'});
                print(myStr + " ticket created")
            print("Done")
            break;


#Search for an issue WIP use ID for now
#employeeSearch = jira.search_issues('project=WONNOC', maxResults=1)
#print('{}: {}'.format(employeeSearch.fields.summary))


#for debugging
#jira.create_issue(project='WONNOC', summary='Tom: Python DAI',
                              #description='Testing', issuetype={'name': 'Task'})
