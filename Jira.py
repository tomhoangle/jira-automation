#STILL NEED TO GET RID OF GLOBAL VARIABLES SOMETIME

from jira.client import JIRA
from tkinter import *
from atlassian import Confluence
import tkinter.scrolledtext as scrolledText
import csv
#options = {'server': 'https://jiradev1.daicompanies.com/'}
#jira = JIRA(options, auth=('tom.le', 'Whatever1!'))

#Query by name
def query_issue(nameInput):
    global employee_name
    global job_title
    global issue
    nameSearch = f'project=WONNOC and summary~"{nameInput}"'
    issueTest = jira.search_issues(nameSearch)
    try:
        issue = issueTest[0]
        employee_name = issue.fields.summary
        job_title = issue.fields.customfield_11000
        employeeText.delete(0, END)
        titleText.delete(0, END)
        employeeText.insert(0, issue.fields.summary)
        titleText.insert(0, issue.fields.customfield_11000)
    except IndexError:
        #issue = 'null'
        textBox.insert(END,nameInput + " doesn't exist\n")

#Create account
def create_issue(issueInput):
    with open('Master.csv') as csv_master:
        csv_reader = csv.reader(csv_master, delimiter='\n')
        templateExisted = False
        for row in csv_reader:
            if issue.fields.customfield_11000 in row:
                templateExisted = True
                #print("Template exists, making tickets now")
                textBox.insert(END,job_title + "'s template exists, making tickets now\n" )
                #if position exist, read the templates job file and create tickets
                #read CVS file to determine list of access to make
                open_file = issue.fields.customfield_11000 + ".csv"
                with open(open_file) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter='\n')
                    my_list = list(csv_reader)
                #Create access according to CSV template
                for x in range(0 , len(my_list)):
                    myStr=''.join(my_list[x])
                    childIssue = jira.create_issue(project='WONNOC', summary=employee_name + ': ' + myStr,
                                                  description='This is made by API', issuetype={'name': 'Task'});
                    jira.create_issue_link(type="Relates", inwardIssue=childIssue.key, outwardIssue=issue.key)
                    #print(myStr + " ticket created: " + childIssue.permalink() + '\n')
                    textBox.insert(END, myStr + " ticket created: " + childIssue.permalink() + '\n')
                #print("Done")
                textBox.insert(END, "Creating confluence page now\n")
                create_confluence(employee_name, job_title)
                textBox.insert(END, "All Done\n")
                break;
        if(templateExisted == False):
            textBox.insert(END, job_title + "'s template doesn't exist.\n")
            template_window()

#Create confluence page
def create_confluence(employee_name, job_title):
    bodyTemplate = """
    <p><ac:structured-macro ac:name="toc" ac:schema-version="1" ac:macro-id="8528bc69-21fc-4738-9a51-d1adc6567465" /></p>
    <h1>General Employee Information</h1>
    <p><ac:structured-macro ac:name="jira" ac:schema-version="1" ac:macro-id="5e516ceb-6982-465d-8db0-9f35f52b7fc3"><ac:parameter ac:name="server">DAI JIRA</ac:parameter><ac:parameter ac:name="columns">key,summary,status</ac:parameter><ac:parameter ac:name="maximumIssues">20</ac:parameter><ac:parameter ac:name="jqlQuery">project = &quot;WONNOC&quot;AND issuetype = &quot;Task&quot; AND summary ~ &quot;""" + employee_name + """&quot;      </ac:parameter><ac:parameter ac:name="serverId">2b3f1951-f097-3d9f-90fe-d1251cb44908</ac:parameter></ac:structured-macro></p>
    <p><br /></p>
    <hr />
    <h1>Access Tickets</h1>
    <p><ac:structured-macro ac:name="jira" ac:schema-version="1" ac:macro-id="610d8a0a-ac12-4cc4-90ac-b1b116ad47fc"><ac:parameter ac:name="server">DAI JIRA</ac:parameter><ac:parameter ac:name="columns">key,summary,due,status</ac:parameter><ac:parameter ac:name="maximumIssues">1000</ac:parameter><ac:parameter ac:name="jqlQuery">project = &quot;WONNOC&quot; AND issuetype = &quot;Task&quot; AND Summary ~ &quot;""" + employee_name + """&quot; ORDER BY duedate DESC     </ac:parameter><ac:parameter ac:name="serverId">2b3f1951-f097-3d9f-90fe-d1251cb44908</ac:parameter></ac:structured-macro></p>
    <h1>Support Tickets</h1>
    <p><ac:structured-macro ac:name="jira" ac:schema-version="1" ac:macro-id="f3b66d01-30e4-440f-9f1f-66f366f09f3f"><ac:parameter ac:name="server">DAI JIRA</ac:parameter><ac:parameter ac:name="columns">key,summary,type,created,updated,due,assignee,reporter,priority,status,resolution</ac:parameter><ac:parameter ac:name="maximumIssues">20</ac:parameter><ac:parameter ac:name="jqlQuery">(project = techserv OR project = Purchasing) AND Summary ~ &quot;Employee Name&quot;  </ac:parameter><ac:parameter ac:name="serverId">2b3f1951-f097-3d9f-90fe-d1251cb44908</ac:parameter></ac:structured-macro></p>"""
    confluence = Confluence(
        url='https://confluencedev1.daicompanies.com',
        username='tom.le',
        password='Whatever1!')
    confluence.create_page(
        space='APITEST',
        parent_id=27951106,
        title=employee_name,
        body=bodyTemplate)
    textBox.insert(END, "Confluence page created: https://confluencedev1.daicompanies.com/display/APITEST/" + employee_name.replace(' ', '+') + '\n')

#Template window GUI
def template_window():
    global daiVar
    global odsVar
    global jiraVar
    global slackVar
    global phoneVar
    global emailVar
    global templateWindow
    templateWindow = Toplevel(window)
    templateWindow.title("Create new template")
    templateWindow.geometry("600x600")
    Label(templateWindow, text ="Template doesn't exist, please choose accesses for the new template ").grid(row=0, column=0, columnspan=2)
    daiVar = IntVar()
    Checkbutton(templateWindow, text="AD(DAI)", variable=daiVar).grid(row=1, column=0, sticky=W)
    odsVar = IntVar()
    Checkbutton(templateWindow, text="AD(ODS)", variable=odsVar).grid(row=1, column=1, sticky=W)
    jiraVar = IntVar()
    Checkbutton(templateWindow, text="Jira", variable=jiraVar).grid(row=1, column=2, sticky=W)
    slackVar = IntVar()
    Checkbutton(templateWindow, text="Slack", variable=slackVar).grid(row=2, column=0, sticky=W)
    phoneVar = IntVar()
    Checkbutton(templateWindow, text="3cx Phone", variable=phoneVar).grid(row=2, column=1, sticky=W)
    emailVar = IntVar()
    Checkbutton(templateWindow, text="Email", variable=emailVar).grid(row=2, column=2, sticky=W)
    Button(templateWindow, text="Create new template", command=lambda : create_template()).grid(row=3,column=1,columnspan=2)

#Create new Template
def create_template():
    global newTemplate
    newTemplate = []
    if(daiVar.get()==1):
        newTemplate.append("AD(DAI)")
    if(odsVar.get()==1):
        newTemplate.append("AD(ODS)")
    if(jiraVar.get()==1):
        newTemplate.append("Jira")
    if(slackVar.get()==1):
        newTemplate.append("Slack")
    if(phoneVar.get()==1):
        newTemplate.append("Phone")
    if(emailVar==1):
        newTemplate.append("Email")
    #update Master list
    with open('Master.csv', 'a') as masterFile:
        masterFile.write(job_title + '\n')
    #store in file
    open_file = job_title + ".csv"
    with open (open_file, 'w') as newFile:
        writeNew = csv.writer(newFile, dialect='excel')
        newFile.write("\n".join(newTemplate))
    textBox.insert(END, "New template for " + job_title + " created.\nYou can create tickets for this job title now.\n")
    templateWindow.destroy()

def show_template(*args):
        #with open(*args + '.csv') as csv_master:
        #    template_reader = csv.reader(csv_master, delimiter='\n')
        #    templateList = list(template_reader)
        print(*args)
        #if "3cx" in templateList:
        #    phoneTemp.set(1)
        #print(phoneTemp.get())

def modify_template():
    global phoneTemp
    phoneTemp = IntVar()
    currentTemplate = []
    modWindow = Toplevel(window)
    modWindow.title("Check/Modify existing template")
    modWindow.geometry("600x600")
    Label(modWindow, text="List of template").grid(row=0,column=0, sticky=W)
    tempVar = StringVar()
    tempVar.set('NOC Engineer')
    with open('Master.csv') as csv_master:
        csv_reader = csv.reader(csv_master, delimiter='\n')
        tempList = list(csv_reader)
    templateMenu = OptionMenu(modWindow, tempVar, *tempList)
    templateMenu.grid(row=0, column=1,sticky=W,columnspan=2)
    phoneTemp = IntVar()
    Checkbutton(modWindow, text="3cx Phone", variable=phoneTemp).grid(row=2, column=0, sticky=W)
    tempVar.trace('w', show_template)



#Create Main GUI
window = Tk()
window.title("Employee Access Tickets Automation by Tom")
window.geometry('1200x600') #Set size
#Input Ticket number
Label(window, text ="Employee Name: ").grid(column=0, row=0,sticky=W)
nameText = Entry(window, width = 40)
nameText.grid(column=1, row=0, sticky=W)
#Search button
searchButton = Button(window, text="Search", command=lambda : query_issue(nameText.get()))
searchButton.grid(column=1, row=1)
#Output search
Label(window, text ="Employee Name: ").grid(column=0, row=2, sticky=W)
employeeText = Entry(window)
employeeText.grid(column=1, row=2, sticky=W)
Label(window, text ="Employee Title: ").grid(column=0, row=3, stick=W)
titleText = Entry(window)
titleText.grid(column=1, row=3, sticky=W)
#Create ticket button
createButton = Button(window, text="Create Tickets", command=lambda : create_issue(issue))
createButton.grid(column=0, row=4)
#Create output text box
textBox = scrolledText.ScrolledText(window)
textBox.grid(column=1, row=5, columnspan=5)
textBox.insert(INSERT, "Output here: \n")
#Modify Template File Menu
menu=Menu(window)
window.config(menu=menu)
fileMenu = Menu(menu)
menu.add_cascade(labe="File", menu=fileMenu)
fileMenu.add_command(label="Modify Template", command=lambda : modify_template())
window.mainloop()


#Debugging codes--------------------------------------------------------------
#Search issue by name
"""nameInput = input("Please enter the employee name: ")
nameSearch = f'project=WONNOC and summary~"{nameInput}"'
issueTest = jira.search_issues(nameSearch)
for issueTest in issueTest:
    print(issueTest.fields.customfield_11000)"""

#Query an issue
#issueNumber = input("Please enter the ticket ID: ")
#issueSearch = 'WONNOC-' + issueNumber
"""nameInput = input("Please enter the employee name: ")
nameSearch = f'project=WONNOC and summary~"{nameInput}"'
issueTest = jira.search_issues(nameSearch)
#issue = jira.issue(issueSearch, fields='summary,customfield_11000')
issue = issueTest[0]
employee_name = issue.fields.summary
job_title = issue.fields.customfield_11000
print("Employee's name: " + employee_name)
print("Employee's title: " + job_title)

#Search through template master list to determine if position exist
#job_title = issue.fields.customfield_11000
with open('Master.csv') as csv_master:
    csv_reader = csv.reader(csv_master, delimiter='\n')
    for row in csv_reader:
        if job_title in row:
            print("Template exists, making tickets now")
            #if position exist, read the templates job file and create tickets
            #read CVS file to determine list of access to make
            open_file = job_title + ".csv"
            with open(open_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='\n')
                my_list = list(csv_reader)
            #Create access according to CSV template
            for x in range(0 , len(my_list)):
                myStr=''.join(my_list[x])
                childIssue = jira.create_issue(project='WONNOC', summary=employee_name + ': ' + myStr,
                                              description='This is made by API', issuetype={'name': 'Task'});
                jira.create_issue_link(type="Relates", inwardIssue=childIssue.key, outwardIssue=issue.key)
                print(myStr + " ticket created: " + childIssue.permalink())
            print("Done")
            break;
        #template doesn't exist, make a new one
        else:
            #Create new template and store it
            print("Template doesn't exist, please follow instruction below to create a new one")
            newTemplate = []
            userInput = ''
            print("What accesses do you want to give to this title?")
            while(userInput != "exit"):
                userInput = input("Please enter an access then press enter(enter exit to quit): ")
                if(userInput != "exit"):
                    newTemplate.append(userInput)
            #update Master list
            with open('Master.csv', 'a') as masterFile:
                masterFile.write(job_title)
            #store in file
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
                childIssue = jira.create_issue(project='WONNOC', summary=employee_name + ': ' + myStr,
                                              description='This is made by API', issuetype={'name': 'Task'});
                jira.create_issue_link(type="Relates", inwardIssue=childIssue.key, outwardIssue=issue.key)
                print(myStr + " ticket created: " + childIssue.permalink())
            print("Done")
            break;"""

#by ID
"""def query_issue(issueInput):
    #global employee_name
    #global job_title
    issueSearch = 'WONNOC-' + issueInput
    issue = jira.issue(issueSearch, fields='summary,customfield_11000')
    #employee_name = issue.fields.summary
    #job_title = issue.fields.customfield_11000
    employeeText.delete(0, END)
    titleText.delete(0, END)
    employeeText.insert(0, issue.fields.summary)
    titleText.insert(0, issue.fields.customfield_11000)"""

#Search for an issue WIP use ID for now
#employeeSearch = jira.search_issues('project=WONNOC', maxResults=1)
#print('{}: {}'.format(employeeSearch.fields.summary))

#jira.create_issue(project='WONNOC', summary='Tom: Python DAI',
                              #description='Testing', issuetype={'name': 'Task'})

#with open('Master.csv', 'a') as masterFile:
#    masterFile.write("CSM")

#create jira ticket function
"""def create_issue( employeeInput, account):
    jira.create_issue(project='WONNOC', summary= employeeInput + ': ' + account,
                                 description='', issuetype={'name': 'Task'})"""

#Create user
#add_user(username, email)
#add user to existing group
#add_user_to_group(username, group)[source]
