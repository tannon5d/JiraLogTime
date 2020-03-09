from jira import JIRA
import argparse
from dateutil.parser import parse
from datetime import datetime, timedelta


def get_args():
    arg_parser = argparse.ArgumentParser('Log work.')
    arg_parser.add_argument('--jira_id', help='target jira', required=True)
    arg_parser.add_argument('--jira_server', help="jira server - e.g. to http://jira.mycompany.local/", required=True)
    arg_parser.add_argument('--username', help='username', required=True)
    arg_parser.add_argument('--password', help='password', required=True)
    arg_parser.add_argument('--start_date', help='start date inclusive', required=True)
    arg_parser.add_argument('--end_date', help='end date inclusive', required=None)
    arg_parser.add_argument('--time_spent', help='how long to log per day', default='7.6h',required=None)
    arg_parser.add_argument('--days', help='days to log - will not be used if end_date is specified', default=1, required=None)
    arg_parser.add_argument('--only_workday', help="if it's only for workdays i.e. skip weekends. Default is True", default=True, required=None)

    return arg_parser.parse_args()

def log_date_if_weekend(log_date, weekend_diff):
    """
        Skip weekends and keep track of how many days to keep skipping
    """
    weekday = log_date.weekday()
    if weekday in (5, 6):
        offset = 7 - weekday
    else:
        offset = 0
    
    return log_date + timedelta(days=offset), weekend_diff + offset
        

if __name__ == "__main__":
    args = get_args()
    jira = JIRA(args.jira_server, auth=(args.username, args.password))
    weekend_diff = 0
    print(f'Adding worklog for jira {args.jira_id}...')
    start_date_obj = parse(args.start_date)
    if args.end_date:
        end_date_obj = parse(args.end_date)
        days = 36500
    else:
        end_date_obj = start_date_obj + timedelta(days=36500)
        days = int(args.days)

    for d in range(0, days):
        log_date = parse(args.start_date) + timedelta(days=d + weekend_diff)
        # add 1-2 days if it's a weekend
        if args.only_workday:
            log_date, weekend_diff = log_date_if_weekend(log_date, weekend_diff)

        if log_date > end_date_obj:
            break

        print(f'Adding {args.time_spent} for {log_date} to {args.jira_id}')
        jira.add_worklog(args.jira_id, timeSpent=args.time_spent, started=log_date)

    print('Done.')
