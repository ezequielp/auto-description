from datetime import date, timedelta, datetime

def connect(options):
    from jira import JIRA
    return JIRA(**options)

def get_in_progress(jira_client, date):
    in_progress_before = date
    not_resolved_before = date - timedelta(days=1)
    query = """assignee = currentUser()
    AND status changed TO 'In Progress' before {in_progress_before}
    AND NOT status changed TO 'Resolved' before {not_resolved_before}""".format(
        in_progress_before=in_progress_before.isoformat(),
        not_resolved_before=not_resolved_before.isoformat()
    )
    return jira_client.search_issues(query)

def get_finished(jira_client, date):
    resolved_by = date
    query = """assignee = currentUser() AND status changed TO 'Resolved' ON '{resolved_by}'""".format(
        resolved_by=resolved_by.isoformat()
    )
    return jira_client.search_issues(query)

def format_string(ongoing_issues, finished_issues):
    from configuration import ongoing_template, finished_template, output_template

    cs_ongoing_issues = ', '.join([issue.key for issue in ongoing_issues])
    cs_finished_issues = ', '.join([issue.key for issue in finished_issues])

    ongoing_text = ongoing_template.format(comma_separated_issues=cs_ongoing_issues) if cs_ongoing_issues else ''
    finished_issues = finished_template.format(comma_separated_issues=cs_finished_issues) if cs_finished_issues else ''
    
    return output_template.format(ongoing=ongoing_text, finished=finished_issues)
    

def main(description_date):
    from configuration import jira_auth
    client=connect(jira_auth)

    in_progress = get_in_progress(client, description_date)
    finished = get_finished(client, description_date)

    print(format_string(in_progress, finished))

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--date",
        help="Generate description for given date",
        required=False,
        type=valid_date)
    group.add_argument("--today",
        help="Generate description for today",
        action='store_true',
        required=False)
    group.add_argument("--yesterday",
        help="Generate description for yesterday",
        action='store_true',
        required=False
    )
    args = parser.parse_args()

    provided_date = None

    if args.date:
        provided_date = args.date
    if args.today:
        provided_date = date.today()
    if args.yesterday:
        provided_date = date.today()-timedelta(days=1)

    if not provided_date:
        provided_date = date.today()
    
    main(provided_date)