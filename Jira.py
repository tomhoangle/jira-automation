"""from jira.client import JIRA
options = {'server': 'http://localhost:8080'}
jira = JIRA(options, basic_auth=('tom.le', 'PAcka87s1!'))"""

#create jira ticket
def create_issue( employeeInput, account, desInput = '' ):
   #jira.create_issue(project='EA', summary= employeeInput + ': ' + account,
    #                             description=desInput, issuetype={'name': 'Task'})
    print (employeeInput + ': ' + account);
    return;

employeeName = raw_input("What is the Employee name?:  ")
daiAD = 1
phone3cx = 1
slack = 1

if(daiAD == 1):
    create_issue(employeeName, "daiAD")
    


"""jira.create_issue(project='EA', summary='Tom: Python DAI',
                              description='Look into this one', issuetype={'name': 'Task'})
jira.create_issue(project='EA', summary='Tom: Python Slack',
                              description='Look into this one', issuetype={'name': 'Task'})"""
