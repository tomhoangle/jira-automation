#STILL NEED TO GET RID OF GLOBAL VARIABLES SOMETIME
#access type field = 11002
#confluence link field = 11001
#user code field = 11003
#Company field = 10501
#Manager field = 11005

from jira.client import JIRA
from tkinter import *
from tkinter import messagebox
from atlassian import Confluence
import tkinter.scrolledtext as scrolledText
import csv
import tkinter
options = {'server': 'https://jiradev1.daicompanies.com/'}
jira = JIRA(options, auth=('', ''))


def helper_function(newTitleInput):
    global job_title
    job_title = newTitleInput
    template_window()
#Query by name
def query_issue(nameInput):
    global employee_name
    global issue
    global job_title
    global managerName
    global companyName
    nameSearch = f'project=WONNOC and summary~"{nameInput}"'
    issueTest = jira.search_issues(nameSearch)
    try:
        issue = issueTest[0]
        employee_name = issue.fields.summary
        job_title = issue.fields.customfield_11000
        companyName = issue.fields.customfield_10501
        managerName = issue.fields.customfield_11005
        employeeText.delete(0, END)
        titleText.delete(0, END)
        companyText.delete(0, END)
        managerText.delete(0,END)
        employeeText.insert(0, employee_name)
        titleText.insert(0, job_title)
        companyText.insert(0, companyName)
        managerText.insert(0, managerName)
    except IndexError:
        #issue = 'null'
        textBox.insert(END,nameInput + " doesn't exist\n")

#Create tickets
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
                #OPTIMIZE THIS!!!!!!!!!!!!!!!!!!! O(N^2) SUCK!!!!
                for x in range(0 , len(my_list)):
                    myStr=''.join(my_list[x])
                    #childIssue = jira.create_issue(project='WONNOC', summary=employee_name + ': ' + myStr,
                    #                              description='Its alive!!!', issuetype={'name': 'Task'});
                    #jira.create_issue_link(type="Relates", inwardIssue=childIssue.key, outwardIssue=issue.key)
                    #print(myStr)
                    if(myStr == "AD(DAI)"):
                        tempString = "dai\\" + employee_name.replace(" ",".")
                        tempString = tempString.lower()
                        #childIssue.update(fields={'customfield_11003': tempString})
                    elif(myStr == "AD(ODS)"):
                        tempString = "odsdai\\" + employee_name.replace(" ",".")
                        tempString = tempString.lower()
                        #childIssue.update(fields={'customfield_11003': tempString})
                    elif(myStr == "Email"):
                        tempString = ""
                    else:
                        tempString = employee_name.replace(" ",".")
                        tempString = tempString.lower()
                        #childIssue.update(fields={'customfield_11003': tempString})
                    #childIssue.update(fields={'customfield_11002': {'value': myStr}})
                    childIssue = jira.create_issue(project='WONNOC', summary=employee_name + ': ' + myStr,
                                                  description='Its alive!!!', issuetype={'name': 'Task'}, customfield_11002 = {'value': myStr}, customfield_11003 = tempString);
                    jira.create_issue_link(type="Relates", inwardIssue=childIssue.key, outwardIssue=issue.key)
                    textBox.insert(END, myStr + " ticket created: " + childIssue.permalink() + '\n')
                    textBox.see(END)
                    textBox.update_idletasks()
                #print("Done")
                textBox.insert(END, "Attached all access tickets to main employee ticket.\nCreating confluence page now\n")
                textBox.see(END)
                textBox.update_idletasks()
                create_confluence(employee_name, job_title)
                confluenceLink = "https://confluencedev1.daicompanies.com/display/APITEST/" + employee_name.replace(' ', '+')
                issue.update(fields={'customfield_11001': confluenceLink})
                textBox.insert(END, employee_name + " is all done, yay\n")
                break;
        if(templateExisted == False):
            textBox.insert(END, job_title + "'s template doesn't exist. Lets change that\n")
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
    <p><ac:structured-macro ac:name="jira" ac:schema-version="1" ac:macro-id="f3b66d01-30e4-440f-9f1f-66f366f09f3f"><ac:parameter ac:name="server">DAI JIRA</ac:parameter><ac:parameter ac:name="columns">key,summary,type,created,updated,due,assignee,reporter,priority,status,resolution</ac:parameter><ac:parameter ac:name="maximumIssues">20</ac:parameter><ac:parameter ac:name="jqlQuery">(project = techserv) AND Summary ~ &quot;""" + employee_name + """&quot;  </ac:parameter><ac:parameter ac:name="serverId">2b3f1951-f097-3d9f-90fe-d1251cb44908</ac:parameter></ac:structured-macro></p>"""
    confluence = Confluence(
        url='https://confluencedev1.daicompanies.com',
        username='',
        password='')
    confluence.create_page(
    #confluence.update_or_create(
        space='APITEST',
        parent_id=27951106,
        title=employee_name,
        body=bodyTemplate)
    textBox.insert(END, "Confluence page created and attached: https://confluencedev1.daicompanies.com/display/APITEST/" + employee_name.replace(' ', '+') + '\n')

#Template window GUI
def template_window():
    global daiVar
    global odsVar
    global jiraVar
    global slackVar
    global phoneVar
    global emailVar
    global duoVar
    global gitLabDaiVar
    global cloudFlareVar
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
    duoVar = IntVar()
    Checkbutton(templateWindow, text="Duo", variable=duoVar).grid(row=3, column=0, sticky=W)
    cloudFlareVar = IntVar()
    Checkbutton(templateWindow, text="CloudFlare", variable=cloudFlareVar).grid(row=3, column=1, sticky=W)
    gitLabDaiVar = IntVar()
    Checkbutton(templateWindow, text="Gitlab(DAI)", variable=gitLabDaiVar).grid(row=3, column=2, sticky=W)
    Button(templateWindow, text="Create new template", command=lambda : create_template()).grid(row=4,column=1,columnspan=2)

#Create new Template
def create_template():
    #print(job_title)
    global newTemplate
    newTemplate = []
    if(daiVar.get()==1): newTemplate.append("AD(DAI)")
    if(odsVar.get()==1): newTemplate.append("AD(ODS)")
    if(jiraVar.get()==1): newTemplate.append("Jira")
    if(slackVar.get()==1): newTemplate.append("Slack")
    if(phoneVar.get()==1): newTemplate.append("Phone")
    if(emailVar.get()==1): newTemplate.append("Email")
    if(duoVar.get()==1): newTemplate.append("Duo")
    if(cloudFlareVar.get()==1): newTemplate.append("Cloudflare")
    if(gitLabDaiVar.get()==1): newTemplate.append("Gitlab(DAI)")
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

#Set checkbox according to templates
def show_template(inName):
    #print (inName)
    accessList = []
    open_file = inName + ".csv"
    with open(open_file, newline ='') as csv_file:
        for row in csv.reader(csv_file):
            accessList.append(row[0])
    #print(accessList)
    #clear all checkbox
    emailButton.deselect()
    daiButton.deselect()
    odsButton.deselect()
    jiraButton.deselect()
    slackButton.deselect()
    phoneButton.deselect()
    duoButton.deselect()
    cloudFlareButton.deselect()
    gitLabDaiButton.deselect()
    #Check template and set checkbox
    if ("AD(DAI)" in accessList): daiButton.select()
    if("AD(ODS)" in accessList): odsButton.select()
    if("Jira" in accessList): jiraButton.select()
    if("Email" in accessList): emailButton.select()
    if("Slack" in accessList): slackButton.select()
    if("Phone" in accessList): phoneButton.select()
    if("Duo" in accessList): duoButton.select()
    if("Cloudflare" in accessList): cloudFlareButton.select()
    if("Gitlab(DAI)" in accessList): gitLabDaiButton.select()

def modify_existTemplate(inName):
    #print(inName)
    modTemplate = []
    if(daiTemp.get() == 1) : modTemplate.append("AD(DAI)")
    if(odsTemp.get() == 1) : modTemplate.append("AD(ODS)")
    if(jiraTemp.get() == 1) : modTemplate.append("Jira")
    if(slackTemp.get() == 1) : modTemplate.append("Slack")
    if(phoneTemp.get() == 1) : modTemplate.append("Phone")
    if(duoTemp.get() == 1) : modTemplate.append("Duo")
    if(cloudFlareTemp.get() == 1) : modTemplate.append("Cloudflare")
    if(emailTemp.get() == 1) : modTemplate.append("Email")
    if(gitLabDaiTemp.get() == 1) : modTemplate.append("Gitlab(DAI)")
    with open (inName + '.csv', 'w+') as newFile:
        writeNew = csv.writer(newFile, dialect='excel')
        newFile.write("\n".join(modTemplate))
    messagebox.showinfo("Success", inName + " template has been modified")

#create modify template window
def modify_template():
    #delcare buttons
    global emailButton
    global daiButton
    global odsButton
    global jiraButton
    global slackButton
    global phoneButton
    global duoButton
    global cloudFlareButton
    global gitLabDaiButton
    #declare variable
    global daiTemp
    global odsTemp
    global jiraTemp
    global slackTemp
    global phoneTemp
    global emailTemp
    global duoTemp
    global cloudFlareTemp
    global gitLabDaiTemp
    modWindow = Toplevel(window)
    modWindow.title("Check/Modify existing template")
    modWindow.geometry("600x600")
    Label(modWindow, text="Select from drop down list of templates").grid(row=0,column=0, sticky=W,columnspan=3)
    #Set up drown down list from templates Master
    tempList = []
    with open('Master.csv', newline='') as csv_master:
        for row in csv.reader(csv_master):
            tempList.append(row[0])
    tempVar = StringVar(modWindow)
    tempVar.set("Click here")
    templateMenu = OptionMenu(modWindow, tempVar, *tempList)
    templateMenu.grid(row=0, column=3,sticky=W,columnspan=2)
    #Set up check button
    daiTemp = IntVar()
    odsTemp = IntVar()
    jiraTemp = IntVar()
    slackTemp = IntVar()
    phoneTemp = IntVar()
    emailTemp = IntVar()
    duoTemp = IntVar()
    cloudFlareTemp = IntVar()
    gitLabDaiTemp = IntVar()
    daiButton = Checkbutton(modWindow, text="AD(DAI)", variable=daiTemp)
    daiButton.grid(row=2, column=0, sticky=W)
    odsButton = Checkbutton(modWindow, text="AD(ODS)", variable=odsTemp)
    odsButton.grid(row=2, column=1, sticky=W)
    jiraButton = Checkbutton(modWindow, text="Jira", variable=jiraTemp)
    jiraButton.grid(row=2, column=2, sticky=W)
    slackButton = Checkbutton(modWindow, text="Slack", variable=slackTemp)
    slackButton.grid(row=3, column=0, sticky=W)
    phoneButton = Checkbutton(modWindow, text="Phone", variable=phoneTemp)
    phoneButton.grid(row=3, column=1, sticky=W)
    emailButton = Checkbutton(modWindow, text="Email", variable=emailTemp)
    emailButton.grid(row=3, column=2, sticky=W)
    duoButton = Checkbutton(modWindow, text="Duo", variable=duoTemp)
    duoButton.grid(row=4, column=0, sticky=W)
    cloudFlareButton = Checkbutton(modWindow, text="Cloud Flare", variable=cloudFlareTemp)
    cloudFlareButton.grid(row=4, column=1, sticky=W)
    gitLabDaiButton = Checkbutton(modWindow, text="Git Lab(DAI)", variable=gitLabDaiTemp)
    gitLabDaiButton.grid(row=4, column=2, sticky=W)
    accessList = []
    tempVar.trace('w', lambda *args: show_template(tempVar.get()))
    modifyButton = Button(modWindow, text="Modify Template", command=lambda : modify_existTemplate(tempVar.get()))
    modifyButton.grid(row=0, column=6, sticky=W)

#create template window yay
def create_newTemplate():
    newTemplateWindow = Toplevel(window)
    newTemplateWindow.title("Create new template")
    newTemplateWindow.geometry("300x300")
    Label(newTemplateWindow, text ="Enter title to be created").grid(column=0, row=0, stick=W)
    newTitleText = Entry(newTemplateWindow)
    newTitleText.grid(column=1, row=0, sticky=W,columnspan=3)
    newCreateButton = Button(newTemplateWindow, text="OK", command=lambda : helper_function(newTitleText.get()))
    newCreateButton.grid(column=1, row=1)

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
Label(window, text ="Company: ").grid(column=2, row=2, stick=W)
companyText = Entry(window)
companyText.grid(column=3, row=2, sticky=W)
Label(window, text ="Manager: ").grid(column=2, row=3, stick=W)
managerText = Entry(window)
managerText.grid(column=3, row=3, sticky=W)
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
fileMenu.add_command(label="Create Template", command=lambda : create_newTemplate())
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
#add_user_to_group(username, group)
