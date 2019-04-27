prod_Database = {
    'host': 'pgresqljiraprod.dai.netdai.com',
    'database': 'jiraautomation',
    'port' : '5432',
    'confluenceUrl': 'https://confluence1.daicompanies.com',
    'jiraUrl': {'server': 'https://jira1.daicompanies.com/'}
}

dev_Database = {
    'host': 'pgresqljiradev.dai.netdai.com',
    'database': 'jiraautomation',
    'port' : '5432',
    'confluenceUrl': 'https://confluencedev1.daicompanies.com',
    'jiraUrl': {'server': 'https://jiradev1.daicompanies.com/'}
}


import psycopg2
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as scrolledText
import tkinter.messagebox as messageBox
import tkinter.simpledialog as simpleDialog
from jira.client import JIRA
from jira.exceptions import JIRAError
from atlassian import Confluence
import time
import string
from datetime import datetime

#TODO: Remove global newList, issue, columnName
#BUG: ticket with same name, will only get latest one, ignore other duplicate

#newdev
#job title = 10858
#access type field = 11603
#confluence link field = 11705
#user code field = 11602
#Company field = 10501
#Manager field = 11704
#Prefered Name = 11701
#Contracting Agency = 11703

#Credential setup
DbName = ''
DbPass = ''

#enviroment Setup
def envi_setup(enviDB):
    global host
    global database
    global port
    global jiraUrl
    global confluenceUrl
    host = enviDB['host']
    database = enviDB['database']
    port = enviDB['port']
    confluenceUrl = enviDB['confluenceUrl']
    jiraUrl = enviDB['jiraUrl']

#choose enviroment prod_Database or dev_Database
envi_setup(dev_Database)

#Database Setup
mydb = psycopg2.connect(user = DbName,
            password = DbPass,
            host = host,
            port = port,
            database = database)
mycursor = mydb.cursor()
#confluenceUrl = 'https://confluencedev1.daicompanies.com'
#jiraUrl = {'server': 'https://jiradev1.daicompanies.com/'}

def count_word(string):
    temp = string.split()
    lengthTemp = len(temp)
    return lengthTemp

def find_securirty(columnName):
    for x in range(len(columnName)):
        if(columnName[x] == 'A/D security group'):
            return x
            break;

def query_issue(nameInput):
    global issue
    nameSearch = f'project=HR and summary~"{nameInput}"'
    issueTest = jira.search_issues(nameSearch)
    try:
        employeeText.configure(state="normal")
        titleText.configure(state="normal")
        companyText.configure(state="normal")
        managerText.configure(state="normal")
        preferedText.configure(state="normal")
        startText.configure(state="normal")
        issue = issueTest[-1]
        employeeText.delete(0, END)
        titleText.delete(0, END)
        companyText.delete(0, END)
        managerText.delete(0,END)
        preferedText.delete(0,END)
        startText.delete(0,END)
        employeeText.insert(0, issue.fields.summary)
        #print(issue.fields.customfield_10858)
        titleText.insert(0, issue.fields.customfield_10858)
        companyText.insert(0, issue.fields.customfield_10501)
        managerText.insert(0, issue.fields.customfield_11704)
        startText.insert(0, issue.fields.customfield_11200)
        if(issue.fields.customfield_11701):
            preferedText.insert(0, issue.fields.customfield_11701)
            if(count_word(issue.fields.customfield_11701) == 1):
                textBox.insert(END, "Prefered name only included first or last name. Please fix by changing to fullname or remove it\n")
                messageBox.showinfo("Warning","Prefered name only included first or last name. Please fix by changing to fullname or remove it")
        else:
            preferedText.insert(0, "N/A")
        employeeText.configure(state="disable")
        titleText.configure(state="disable")
        companyText.configure(state="disable")
        managerText.configure(state="disable")
        preferedText.configure(state="disable")
        startText.configure(state="disable")
    except IndexError:
        textBox.insert(END,nameInput + " doesn't exist, try again\n")
        employeeText.configure(state="normal")
        titleText.configure(state="normal")
        companyText.configure(state="normal")
        managerText.configure(state="normal")
        preferedText.configure(state="normal")
        startText.configure(state="normal")
        employeeText.delete(0, END)
        titleText.delete(0, END)
        companyText.delete(0, END)
        managerText.delete(0,END)
        preferedText.delete(0,END)
        startText.delete(0,END)
        employeeText.configure(state="disable")
        titleText.configure(state="disable")
        companyText.configure(state="disable")
        managerText.configure(state="disable")
        preferedText.configure(state="disable")
        startText.configure(state="disable")

def get_template(templateName, buttonList, securityList, tempList):
    mycursor.execute("select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = 'templates' order by column_name asc;")
    oriName = []
    secIndex = 0
    for column in mycursor.fetchall():
        if(column[0] == 'job_title'):
            pass
        else:
            oriName.append(column[0])
    sqlString = ""
    for x in range(len(columnName)):
         sqlString += oriName[x] + ","
    sqlString = sqlString.rstrip(',')
    newString = "Select " + sqlString + " from templates where job_title = '" + templateName + "'"
    mycursor.execute(newString)

    myresult = mycursor.fetchone()
    myresult = list(myresult)
    #del myresult[0:1]
    #Clear all checklist
    for x in range(len(myresult)):
        buttonList[x].deselect()
    #Check all access in list
    for x in range(len(myresult)):
        if(myresult[x] == 1):
            buttonList[x].select()
    print(find_securirty(columnName))
    if(tempList[find_securirty(columnName)].get()==1):
        #securityList.configure(state="normal")
        #Check security List
        mycursor.execute("Select * from ad_security where job_title = '%s'" % (templateName))
        secResult = mycursor.fetchone()
        secResult = list(secResult)
        del secResult [0:1]
        secResult[:] = (value for value in secResult if value != None)
        tempString = ';'.join(secResult)
        securityList.delete(0, END)
        securityList.insert(0, tempString)
    else:
        #securityList.configure(state="normal")
        securityList.delete(0, END)
        securityList.insert(0, "N/A")
        #securityList.configure(state="disable")

def modify_template(jobChange, valueChange, securityText):
    #Fetch original List
    mycursor.execute("select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = 'templates' order by column_name asc;")
    oriName = []
    for column in mycursor.fetchall():
        if(column[0] == 'job_title'):
            pass
        else:
            oriName.append(column[0])
    sqlString = "UPDATE templates SET "
    for x in range(len(columnName)):
         sqlString += oriName[x] + "=" + str(valueChange[x].get()) + ","
    sqlString = sqlString.rstrip(',') + " WHERE job_title = '" + jobChange.get() + "'"
    mycursor.execute(sqlString)
    mydb.commit()
    tempSec = securityText.get()
    tempSec = tempSec.split(';')
    sqlString = "UPDATE ad_security SET "
    mycursor.execute("select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = 'ad_security';")
    secName = []
    for column in mycursor.fetchall():
        secName.append(column[0])
    del secName[0:1]
    for x in range(len(tempSec)):
         sqlString += secName[x] + "='" + str(tempSec[x]) + "',"
    sqlString = sqlString.rstrip(',') + " WHERE job_title = '" + jobChange.get() + "'"
    mycursor.execute(sqlString)
    mydb.commit()
    messageBox.showinfo("Success", jobChange.get() + " template has been modified")

#change access from SQL column to match customfield set
def cleaningAccess(columnName):
    for column in mycursor.fetchall():
        if(column[0] == "ad_odsdai"):
            columnName.append("A/D (ODSDAI)")
        elif(column[0] == "ad_dai"):
            columnName.append("A/D (DAI)")
        elif(column[0] == "ad_securitygroup"):
            columnName.append("A/D security group")
        elif(column[0] == "aws_dai"):
            columnName.append("AWS (DAI)")
        elif(column[0] == "aws_odsdai"):
            columnName.append("AWS (ODS)")
        elif(column[0] == "email"):
            columnName.append("email")
        elif(column[0] == "fileshare"):
            columnName.append("fileshare")
        elif(column[0] == "gitlab_dai"):
            columnName.append("Gitlab (DAI)")
        elif(column[0] == "gitlab_ocm"):
            columnName.append("Gitlab (OCM)")
        elif(column[0] == "gitlab_ods"):
            columnName.append("Gitlab (ODS)")
        elif(column[0] == "grant_access_dai"):
            columnName.append("Grant Access (DAI)")
        elif(column[0] == "grant_access_ods"):
            columnName.append("Grant Access (ODS)")
        elif(column[0] == "investors_com"):
            columnName.append("Investors.com")
        elif(column[0] == "jira_local"):
            columnName.append("Jira (local)")
        elif(column[0] == "jira_cloud"):
            columnName.append("Jira (cloud)")
        elif(column[0] == "jenkins_ods"):
            columnName.append("Jenkins (ODS)")
        elif(column[0] == "nav"):
            columnName.append("NAV")
        elif(column[0] == "ods_compliance"):
            columnName.append("ODS Compliance")
        elif(column[0] == "ops_genie"):
            columnName.append("OpsGenie")
        elif(column[0] == "phone"):
            columnName.append("phone")
        elif(column[0] == "ssrs"):
            columnName.append("SSRS")
        elif(column[0] == "supermon_dai"):
            columnName.append("SuperMon (DAI)")
        elif(column[0] == "supermon_ods"):
            columnName.append("SuperMon (ODS)")
        elif(column[0] == "tableau_ibd"):
            columnName.append("Tableau (IBD)")
        elif(column[0] == "tableau_ods"):
            columnName.append("Tableau (ODS)")
        elif(column[0] == "timetrack"):
            columnName.append("TimeTrack")
        elif(column[0] == "vpn"):
            columnName.append("VPN")
        elif(column[0] == "websites_ods"):
            columnName.append("Websites (ODS)")
        elif(column[0] == "wonda"):
            columnName.append("WONDA")
        elif(column[0] == "job_title"):
            pass
        else:
            columnName.append(string.capwords(column[0].replace('_',' ')))

def add_access(parentWindow):
    global columnName
    accessToAdd = simpleDialog.askstring("Input", "What access you want to add?(use _ to replace space)", parent=parentWindow)
    sqlString = ''
    if(accessToAdd):
        sqlString = "ALTER TABLE templates ADD COLUMN " + accessToAdd +" TINYINT(1) NOT NULL DEFAULT 0;"
        mycursor.execute(sqlString)
        mydb.commit()
        #reload column name
        mycursor.execute("select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = 'templates';")
        columnName = []
        cleaningAccess(columnName)
        #remove title column
        #del columnName[0:1]
        messageBox.showinfo("Success", "A new access was added, please reopen the window you were on")
        parentWindow.destroy()

def modify_window():
    modWindow = Toplevel(window)
    modWindow.title("Check/Modify Existing Templates")
    modWindow.geometry('1000x600')
    modWindow.focus_force() #Testing
    buttonList = []
    tempList = []
    Label(modWindow, text="Select from drop down list of templates").grid(row=0,column=0, sticky=W,columnspan=2)
    tempVar = StringVar(modWindow)
    tempVar.set("Click here")
    templateMenu = OptionMenu(modWindow, tempVar, *newList)
    templateMenu.grid(row=0, column=2,sticky=W,columnspan=3)
    modButton = Button(modWindow, text="Modify Templates", command=lambda : modify_template(tempVar, tempList, securityText))
    modButton.grid(row=0,column=5,sticky=W)
    #Instantiate list of IntVar
    for x in range(len(columnName)):
        tempList.append(IntVar())
    #Create list of buttons and arrange it
    tempRow = 1
    tempCol = 0
    for x in range(len(columnName)):
        #print(columnName[x])
        tempButton = Checkbutton(modWindow, text=columnName[x], variable=tempList[x])
        tempButton.grid(row=tempRow,column=tempCol,sticky=W)
        buttonList.append(tempButton)
        tempCol = tempCol + 1
        if(tempCol == 4):
            tempRow = tempRow + 1
            tempCol = 0
    #Create new access
    #addButton = Button(modWindow, text="Add new access type", command=lambda : add_access(modWindow))
    #addButton.grid(row=tempRow,column=tempCol,sticky=W)
    Label(modWindow, text ="A/D Security Group: ").grid(row=tempRow+1,column=0, sticky=W)
    securityText = Entry(modWindow, width = 100)
    securityText.grid(column=1, row=tempRow+1, sticky=W,columnspan=8)
    #check the box that has accesses
    tempVar.trace('w', lambda *args: get_template(tempVar.get(),buttonList, securityText, tempList))

def create_window(jobInput=''):
    creWindow = Toplevel(window)
    creWindow.title("Create Template")
    creWindow.geometry('1000x600')
    creWindow.configure(background='#645959')
    buttonList = []
    tempList = []
    Label(creWindow, text ="Job Title: ", background='#FF850A', justify='center', width = 20).grid(column=0, row=0,sticky=W)
    jobText = Entry(creWindow, width = 40)
    jobText.grid(column=1, row=0, columnspan=3,sticky=W)
    jobText.insert(0,jobInput)
    creTempButton = ttk.Button(creWindow, text="Create Template", command=lambda : create_template(creWindow,jobText.get(),tempList,securityText))
    creTempButton.grid(column=5, row=0,sticky=W)
    #Instantiate list of IntVar
    for x in range(len(columnName)):
        tempList.append(IntVar())
    #Create list of buttons and arrange it
    tempRow = 1
    tempCol = 0
    for x in range(len(columnName)):
        tempButton = Checkbutton(creWindow, text=columnName[x], variable=tempList[x])
        tempButton.grid(row=tempRow,column=tempCol,sticky=W)
        tempButton.config(background='white')
        buttonList.append(tempButton)
        tempCol = tempCol + 1
        if(tempCol == 4):
            tempRow = tempRow + 1
            tempCol = 0
    #addButton = Button(creWindow, text="Add new access", command=lambda : add_access(creWindow))
    #addButton.grid(row=tempRow,column=tempCol,sticky=W)
    Label(creWindow, text ="A/D Security Group: ").grid(row=tempRow+1,column=0, sticky=W)
    securityText = Entry(creWindow, width = 100)
    securityText.grid(column=1, row=tempRow+1, sticky=W,columnspan=8)

def create_template(mainWindow, jobTitle, accessList, securityText):
    global newList
    tempSql = ""
    tempList = "'" + jobTitle + "', " + ', '.join(str(e.get()) for e in accessList)
    mycursor.execute("select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = 'templates' order by column_name asc;")
    oriName = []
    sqlString = ""
    secIndex = 0
    for column in mycursor.fetchall():
        if(column[0] == 'job_title'):
            pass
        else:
            oriName.append(column[0])
    for x in range(len(columnName)):
        tempSql += oriName[x] + ","
    tempSql = tempSql.rstrip(',')
    sqlString = "INSERT INTO templates (job_title, " + tempSql + ") Values (%s)" %(tempList)
    mycursor.execute(sqlString)
    mydb.commit()
    #Re-import template List
    mycursor.execute("Select job_title from templates order by job_title asc")
    jobList = mycursor.fetchall()
    newList = []
    for x in jobList:
        newList.append(x[0])
    secName = []
    mycursor.execute("select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = 'ad_security';")
    for column in mycursor.fetchall():
        secName.append(column[0])
    del secName[0:1]
    sqlString1 = "Insert into ad_security (job_title,"
    sqlString2 = "Values('" + jobTitle + "',"
    tempSec = securityText.get()
    tempSec = tempSec.split(';')
    for x in range(len(tempSec)):
        sqlString1 += secName[x] + ","
        sqlString2 += "'" + str(tempSec[x]) + "',"
    sqlString = sqlString1.rstrip(',') + ") " + sqlString2.rstrip(',') + ")"
    mycursor.execute(sqlString)
    mydb.commit()
    textBox.insert(END,jobTitle + "'s template has been created\nYou can create tickets for this job now\n")
    mainWindow.destroy()

def create_confluence(confluence, legalName, employee_name, job_title):
    bodyTemplate = """
    <p><ac:structured-macro ac:name="toc" ac:schema-version="1" ac:macro-id="8528bc69-21fc-4738-9a51-d1adc6567465" /></p>
    <h1>General Employee Information</h1>
    <p><ac:structured-macro ac:name="jira" ac:schema-version="1" ac:macro-id="5e516ceb-6982-465d-8db0-9f35f52b7fc3"><ac:parameter ac:name="server">DAI JIRA</ac:parameter><ac:parameter ac:name="columns">key,summary,status,employment type,start date,manager</ac:parameter><ac:parameter ac:name="maximumIssues">20</ac:parameter><ac:parameter ac:name="jqlQuery">project = &quot;HR&quot;AND issuetype = &quot;Employee&quot; AND summary ~ &quot;""" + legalName + """&quot;      </ac:parameter><ac:parameter ac:name="serverId">2b3f1951-f097-3d9f-90fe-d1251cb44908</ac:parameter></ac:structured-macro></p>
    <p><br /></p>
    <hr />
    <h1>Access Tickets</h1>
    <p><ac:structured-macro ac:name="jira" ac:schema-version="1" ac:macro-id="610d8a0a-ac12-4cc4-90ac-b1b116ad47fc"><ac:parameter ac:name="server">DAI JIRA</ac:parameter><ac:parameter ac:name="columns">key,summary,access type,due,status,usercode</ac:parameter><ac:parameter ac:name="maximumIssues">1000</ac:parameter><ac:parameter ac:name="jqlQuery">project = &quot;DAIEMP&quot; AND issuetype = &quot;Access&quot; AND Summary ~ &quot;""" + employee_name + """&quot; ORDER BY duedate DESC     </ac:parameter><ac:parameter ac:name="serverId">2b3f1951-f097-3d9f-90fe-d1251cb44908</ac:parameter></ac:structured-macro></p>
    <h1>Support Tickets</h1>
    <p><ac:structured-macro ac:name="jira" ac:schema-version="1" ac:macro-id="f3b66d01-30e4-440f-9f1f-66f366f09f3f"><ac:parameter ac:name="server">DAI JIRA</ac:parameter><ac:parameter ac:name="columns">key,summary,type,created,updated,due,assignee,reporter,priority,status,resolution</ac:parameter><ac:parameter ac:name="maximumIssues">20</ac:parameter><ac:parameter ac:name="jqlQuery">(project = techserv OR project = Purchasing) AND Summary ~ &quot;""" + employee_name + """&quot;  </ac:parameter><ac:parameter ac:name="serverId">2b3f1951-f097-3d9f-90fe-d1251cb44908</ac:parameter></ac:structured-macro></p>"""
    confluence.create_page(
        space='DAIEMP',
        parent_id=32571673,
        title=employee_name,
        body=bodyTemplate)
    textBox.insert(END, "Confluence page created and attached: " + confluenceUrl + "/display/DAIEMP/" + employee_name.replace(' ', '+') + '\n')

#Create tickets
def create_issue():
    #Check if template exist
    templateExist = False
    for x in newList:
        if(x == titleText.get()):
            templateExist = True
            break;
        else:
            templateExist = False
    if(issue.fields.customfield_11705):
        textBox.insert(END, "Employee access tickets/confluence page already created, please check it again at " + issue.permalink() + "\n")
        messageBox.showinfo("Error","Accesses already created, please recheck HR ticket. \nIf false error, please clear confluence link on ticket")
    elif(templateExist == True):
        if(issue.fields.customfield_11701):
            employeeName = issue.fields.customfield_11701
            textBox.insert(END, "Using employee prefered name instead: " + issue.fields.customfield_11701 + "\n")
        else:
            employeeName = issue.fields.summary
        #Insert new employee into table history
        mycursor.execute("INSERT INTO accesshistory (EmployeeName) values ('%s')" % (employeeName))
        mydb.commit()
        #Get list of accesses
        mycursor.execute("select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = 'templates' order by column_name asc;")
        oriName = []
        secIndex = 0
        for column in mycursor.fetchall():
            if(column[0] == 'job_title'):
                pass
            else:
                oriName.append(column[0])
        sqlString = ""
        for x in range(len(oriName)):
             sqlString += oriName[x] + ","
        sqlString = sqlString.rstrip(',')
        newString = "Select " + sqlString + " from templates where job_title = '" + titleText.get() + "'"
        mycursor.execute(newString)
        tempResult = mycursor.fetchone()
        tempResult = list(tempResult)
        countVar = 0
        for x in range(len(tempResult)):
            if(tempResult[x] == 1):
                desTemp = ""
                if(columnName[x] == "A/D (DAI)"):
                    tempString = "dai\\" + employeeName.replace(" ",".")
                    tempString = tempString.lower()
                    #childIssue.update(fields={'customfield_11003': tempString})
                elif(columnName[x] == "A/D (ODSDAI)"):
                    tempString = "odsdai\\" + employeeName.replace(" ",".")
                    tempString = tempString.lower()
                    #childIssue.update(fields={'customfield_11003': tempString})
                elif(columnName[x] == "email" or columnName[x] == "Slack" or columnName[x] == "Jira (cloud)"):
                    if('Hengtian Services, LLC' in str(issue.fields.customfield_11703) and columnName[x] == "email"):
                        tempString = ''
                        desTemp = "Ask their manager for their email, don't give E1 or E3 unless manager say otherwise"
                    else:
                        if "DAI" in companyText.get():
                            tempString = employeeName.replace(" ",".").lower() + "@daicompanies.com"
                            desTemp = "E1"
                        elif "IBD" in companyText.get():
                            tempString = employeeName.replace(" ",".").lower() + "@investors.com"
                            desTemp = "E1"
                        elif "OCM" in companyText.get():
                            tempString = employeeName.replace(" ",".").lower() + "@oneilcapital.com"
                            desTemp = "E1"
                        elif "ODS" in companyText.get():
                            tempString = employeeName.replace(" ",".").lower() + "@oneildata.com"
                            desTemp = "E3"
                        elif "ONS" in companyText.get():
                            tempString = employeeName.replace(" ",".").lower() + "@oneilsecurities.com"
                            desTemp = "E3"
                        elif "WON" in companyText.get():
                            tempString = employeeName.replace(" ",".").lower() + "@williamoneil.com"
                            desTemp = "E3"
                        elif "WON China" in companyText.get():
                            tempString = employeeName.replace(" ",".").lower() + "@williamoneilchina.com"
                            desTemp = "E1"
                        elif "WON India" in companyText.get():
                            tempString = employeeName.replace(" ",".").lower() + "@williamoneilindia.com"
                            desTemp = "E1"
                        else:
                            desTemp = ""
                            tempString = ""
                        if(columnName[x] == 'Slack'):
                            desTemp = ""
                        elif(columnName[x] == "Jira (cloud)"):
                            desTemp = ""
                elif(columnName[x] == "A/D security group"):
                    mycursor.execute("Select * from ad_security where job_title = '%s'" % (titleText.get()))
                    secResult = mycursor.fetchone()
                    secResult = list(secResult)
                    del secResult [0:1]
                    secResult[:] = (value for value in secResult if value != None)
                    desTemp = ';'.join(secResult)
                elif(columnName[x] == "phone"):
                    tempString = ""
                else:
                    tempString = employeeName.replace(" ",".")
                    tempString = tempString.lower()
                childIssue = jira.create_issue(project='DAIEMP', summary=employeeName + ': ' + columnName[x],
                                              description=desTemp, issuetype={'name': 'Access'}, customfield_11602 = tempString,
                                              customfield_11603 = {'value': columnName[x]});

                jira.create_issue_link(type="Relates", inwardIssue=childIssue.key, outwardIssue=issue.key)
                #insert history to table
                countVar = countVar + 1
                accessName = "access" + str(countVar)
                #print(accessName)
                mycursor.execute("UPDATE accesshistory SET " + accessName + " = ('%s') WHERE timecreated is NULL and EmployeeName = '%s'" %(childIssue.key, employeeName))
                mydb.commit()
                textBox.insert(END, columnName[x] + " ticket created: " + childIssue.permalink() + '\n')
                textBox.see(END)
                textBox.update_idletasks()
                #time.sleep(1)
        create_confluence(confluence, employeeText.get(),employeeName, titleText.get())  #eRROR:PROBLEM HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        confluenceLink = confluenceUrl + "/display/DAIEMP/" + employeeName.replace(' ', '+')
        issue.update(fields={'customfield_11705': confluenceLink})
        textBox.insert(END, employeeName + " is all done, yay\n")
        mycursor.execute("UPDATE accesshistory SET timecreated = ('%s') WHERE timecreated is NULL and EmployeeName = '%s'" %(datetime.now(), employeeName))
        mydb.commit()
    else:
        create_window(titleText.get())

def deleteTicket(nameInput):
    warningMessage = messageBox.askquestion ('Delete made tickets','Are you sure you want to delete tickets for ' + employeeText.get(),icon = 'warning')
    if warningMessage == 'yes':
        #delete tickets
        rowsCount = mycursor.execute("Select * from accesshistory where timedeleted is NULL and employeename = '%s' order by timecreated desc" % (nameInput))
        if(mycursor.rowcount == 0):
            messageBox.showerror("Error", nameInput + "'s tickets have already been deleted or haven't been created")
        else:
            tempResult = mycursor.fetchone()
            tempResult = list(tempResult)
            del tempResult[0:2]
            for x in range(len(tempResult)):
                if(not tempResult[x]):
                    break;
                else:
                    issuetemp1 = jira.issue(tempResult[x])
                    textBox.insert(END, issuetemp1.key + " has been deleted\n")
                    textBox.see(END)
                    textBox.update_idletasks()
                    issuetemp1.delete()
            issue.update(fields={'customfield_11705': ''})
            confluence.remove_page(confluence.get_page_id('DAIEMP', employeeText.get()), status=None)
            textBox.insert(END, "Confluence link removed and deleted\n")
            textBox.see(END)
            textBox.update_idletasks()
            mycursor.execute("UPDATE accesshistory SET timedeleted = ('%s') WHERE timedeleted is NULL and EmployeeName = '%s'" %(datetime.now(), nameInput))
            mydb.commit()

def refreshOpen():
    textBox.insert(END, "Refreshing.......")
    textBox.see(END)
    textBox.update_idletasks()
    openBox.delete(0,'end')
    jqlSearch = f'project=HR and status = open order by "cf[11200]" asc'
    issues = jira.search_issues(jqlSearch)
    for issue in issues:
        if(str(issue.fields.status) == 'Open' and not issue.fields.customfield_11705):
            openBox.insert(END, issue.fields.summary)
    openBox.select_set(0)
    openBox.bind("<Double-Button-1>", OnDouble)
    textBox.insert(END, "Done refreshing\n")

def helperFunc1(confluenceUrl, jiraUrl):
    global confluence
    global jira
    if nameEnter.get() and not nameEnter.get().isspace():
        confluenceName = nameEnter.get()
        confluencePass = passwordEnter.get()
        confluence = Confluence(
            url=confluenceUrl,
            username=confluenceName,
            password=confluencePass)
        #try:
        jira = JIRA(jiraUrl, auth=(nameEnter.get(), passwordEnter.get()))
        textBox.insert(END, "logged in as " + nameEnter.get() + "\n")
        window.deiconify()
        top.destroy()
        jqlSearch = f'project=HR and status = open order by "cf[11200]" asc'
        issues = jira.search_issues(jqlSearch)
        for issue in issues:
            if(str(issue.fields.status) == 'Open' and not issue.fields.customfield_11705):
                openBox.insert(END, issue.fields.summary)
        openBox.select_set(0)
        openBox.bind("<Double-Button-1>", OnDouble)
        #except Exception as e:
            #print e.status_code, e.text
        #    messageBox.showinfo("Login Failed","Login Failed. Please try again\n(You may have trigger captcha from too many failed login. Please login to jira directly and clear it)")
    else:
        messageBox.showinfo("Failure","Please enter both username and password")

def OnDouble(self):
    selection=openBox.curselection()
    value = openBox.get(selection[0])
    query_issue(value)

def helperFunc2():
    top.destroy()
    window.destroy()

#Store access name from database into list
mycursor.execute("select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = 'templates' order by column_name asc;")
columnName = []
#Database column name doesn't like space and special character, need to rename them
cleaningAccess(columnName)
#remove title column
#print(columnName)
#del columnName[0:1]
#Get list of templates in database
mycursor.execute("Select job_title from templates order by job_title asc")
jobList = mycursor.fetchall()
newList = []
for x in jobList:
    newList.append(x[0])



window = Tk()
window.title("Jira Automation")
window.geometry('1200x900') #Set size
window.configure(background='#645959')
window.style = ttk.Style()
#print(window.style.theme_names())
window.style.theme_use("vista")
#Input Ticket number
Label(window, text ="Enter Name: ", background='#FF850A', justify='center', width=15).grid(column=0, row=0,sticky=W)
nameText = Entry(window, width = 40, highlightbackground='white', highlightthickness = 2)
nameText.grid(column=1, row=0, sticky=W)
#Search button
searchButton = ttk.Button(window, text="Search", command=lambda : query_issue(nameText.get()))
searchButton.grid(column=2, row=0, sticky=W, columnspan=1)
Label(window, text ="Employee Name: ", background='#FF850A', justify='center', width=15).grid(column=0, row=2, sticky=W)
employeeText = Entry(window, width = 40, highlightbackground='white', highlightthickness = 2)
employeeText.grid(column=1, row=2, sticky=W)
employeeText.configure(state="disable")
Label(window, text ="Employee Title: ", background='#FF850A', justify='center',width=15).grid(column=0, row=3, sticky=W)
titleText = Entry(window, width = 40, highlightbackground='white', highlightthickness = 2)
titleText.grid(column=1, row=3, sticky=W)
titleText.configure(state="disable")
Label(window, text ="Company: ", background='#FF850A', justify='center', width=15).grid(column=3, row=3, sticky=W)
companyText = Entry(window, width = 40, highlightbackground='white', highlightthickness = 2)
companyText.grid(column=4, row=3, sticky=W)
companyText.configure(state="disable")
Label(window, text ="Prefered Name: ", background='#FF850A', justify='center', width=15).grid(column=3, row=2, sticky=W)
preferedText = Entry(window, width = 40, highlightbackground='white', highlightthickness = 2)
preferedText.grid(column=4, row=2, sticky=W)
preferedText.configure(state="disable")
Label(window, text ="Manager: ", background='#FF850A', justify='center',width=15).grid(column=3, row=4, sticky=W)
managerText = Entry(window, width = 40, highlightbackground='white', highlightthickness = 2)
managerText.grid(column=4, row=4, sticky=W)
managerText.configure(state="disable")
Label(window, text ="Start Date: ", background='#FF850A', justify='center', width=15).grid(column=0, row=4, sticky=W)
startText = Entry(window, width = 40, highlightbackground='white', highlightthickness = 2)
startText.grid(column=1, row=4, sticky=W)
startText.configure(state="disable")
createButton = ttk.Button(window, text="Create Tickets", command=lambda : create_issue())
createButton.grid(column=0, row=5)
deleteButton = ttk.Button(window, text="Delete Tickets", command=lambda : deleteTicket(employeeText.get()))
deleteButton.grid(column=4, row=5)
refreshButton = ttk.Button(window, text="Refresh", command=lambda: refreshOpen())
refreshButton.grid(column=7, row=5)
textBox = scrolledText.ScrolledText(window, background='beige')
textBox.grid(column=1, row=7, columnspan=5)
textBox.insert(INSERT, "Output here: \n")
Label(window, text ="Employee without ticket(sorted by closest startdate) ", background='#FF850A').grid(column=7, row=0)
openBox = Listbox(window)
openBox.grid(column=7, row=1, columnspan=4, rowspan=4)

#Modify Template File Menu
menu=Menu(window)
window.config(menu=menu)
fileMenu = Menu(menu)
menu.add_cascade(labe="File", menu=fileMenu)
fileMenu.add_command(label="Modify Template", command=lambda : modify_window())
fileMenu.add_command(label="Create Template", command=lambda : create_window())
window.withdraw()

#login window
#Create Main GUI
top = Toplevel()
#top.geometry('400x200')
top.configure(background='#645959')
top.style = ttk.Style()
top.style.theme_use("clam")
nameEnter = Entry(top)
passwordEnter = Entry(top, show="*")
loginButton = Button(top, text="Login", command=lambda:helperFunc1(confluenceUrl,jiraUrl))
cancelButton = Button(top, text="Cancel", command=lambda:helperFunc2())

Label(top, text ="Username: ", background='#FF850A', justify='center', width=15).grid(column=0, row=0, sticky=W)
nameEnter.grid(column=1, row=0,columnspan=2, sticky=W)
Label(top, text ="Password: ",background='#FF850A', justify='center', width=15).grid(column=0, row=1, sticky=W)
passwordEnter.grid(column=1, row=1, columnspan=2, sticky=W)
loginButton.grid(column=1, row=2, sticky=W)
cancelButton.grid(column=2, row=2, sticky=W)

window.mainloop()
