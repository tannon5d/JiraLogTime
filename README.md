# JiraLogTime

<pre>
usage: 
python JiraLogWork  [-h] --jira_id JIRA_ID --jira_server JIRA_SERVER --username
                    USERNAME --password PASSWORD --start_date START_DATE
                    [--end_date END_DATE] [--time_spent TIME_SPENT] [--days DAYS]
                    [--only_workday ONLY_WORKDAY]

optional arguments:
  -h, --help                    show this help message and exit
  --jira_id JIRA_ID             target jira
  --jira_server JIRA_SERVER     jira server - e.g. to http://jira.mycompany.local/
  --username USERNAME           username
  --password PASSWORD           password
  --start_date START_DATE       start date inclusive
  --end_date END_DATE           end date inclusive
  --time_spent TIME_SPENT       how long to log per day
  --days DAYS                   days to log - will not be used if end_date is specified
  --only_workday ONLY_WORKDAY   if it's only for workdays i.e. skip weekends. Default is True
  </pre>
