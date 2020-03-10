from jira import JIRA
import argparse
from datetime import datetime, timedelta
from dateutil.parser import parse

def get_args():
    arg_parser = argparse.ArgumentParser('Delete worklog in a given JIRA for the user ONLY')
    arg_parser.add_argument('--jira_id', help='target jira', required=True)
    arg_parser.add_argument('--jira_server', help="jira server - e.g. to http://jira.mycompany.local/", required=True)
    arg_parser.add_argument('--username', help='username', required=True)
    arg_parser.add_argument('--password', help='password', required=True)
    arg_parser.add_argument('--start_date', help='from what date inclusive to delete the worklogs', required=True)
    arg_parser.add_argument('--end_date', help='until what date inclusive to delete the worklogs', required=None)

    return arg_parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    jira = JIRA(args.jira_server, auth=(args.username, args.password))
    jira_id = args.jira_id
    start_date_obj = parse(args.start_date)
    if args.end_date:
        end_date_obj = parse(args.end_date)
    else:
        end_date_obj = start_date_obj + timedelta(days=36500)
        
    print(f'Deleting worklogs for jira {jira_id} for user ...')
    worklogs = jira.worklogs(jira_id)
    for worklog in worklogs:
        if worklog.updateAuthor.key == args.username and \
            start_date_obj <= parse(worklog.started[:10]) <= end_date_obj:
            print(f'Deleting worklog {worklog.timeSpent} on {worklog.started} for user {worklog.updateAuthor.key}')
            worklog.delete()

    print('Done.')
