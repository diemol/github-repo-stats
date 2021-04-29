import json, datetime
from os import environ, path
from github3 import login
from itertools import groupby
from json_datetime import DateTimeEncoder, extract_datetime

GITHUB_ORG = environ.get("GITHUB_ORG", None)
GITHUB_REPO = environ.get("GITHUB_REPO", None)
GITHUB_TOKEN = environ.get("GITHUB_TOKEN", None)
REPO_DATA_FILE = f"{GITHUB_ORG.lower()}_{GITHUB_REPO.lower()}_data.json"
PROCESSED_DATA_FILE = f"pages/{GITHUB_ORG.lower()}_{GITHUB_REPO.lower()}/data.js"

def import_data():
  """This function gets the issue data
  from the configured GitHub repo"""
  data = {}
  gh = login(token=GITHUB_TOKEN)

  print(f"Retrieving issues/prs from GitHub...")

  repo_issues = gh.issues_on(GITHUB_ORG, GITHUB_REPO, state='all')
  for issue in repo_issues:
    data[issue.number] = {
      'created_at': issue.created_at,
      'closed_at': issue.closed_at,
      'is_pull_request': (issue.pull_request_urls is not None)
    }

  print(f"{len(data)} issues/prs retrieved from GitHub...")

  with open(REPO_DATA_FILE, 'w') as json_file:
    json.dump(data, json_file, cls=DateTimeEncoder)

def process_data():
  """This function processes the issue data
  and aggregates them by date"""
  data = {}
  if path.isfile(REPO_DATA_FILE):
    with open(REPO_DATA_FILE) as f:
      data = json.load(f)
  else:
    raise SystemExit()

  if len(data) == 0:
    raise SystemExit()

  # convert all date strings to datetime objects
  for i in data.keys():
    data[i]['created_at'] = extract_datetime(data[i]['created_at'])
    if data[i]['closed_at'] is not None:
      data[i]['closed_at'] = extract_datetime(data[i]['closed_at'])

  # retrieve lowest issue number & date
  last_number = min([int(i) for i in data.keys()])
  first_date = extract_datetime(data[str(last_number)]['created_at'])

  one_day = datetime.timedelta(days=1)
  now = datetime.datetime.now(datetime.timezone.utc)
  day = datetime.datetime(first_date.year, first_date.month, first_date.day, tzinfo=datetime.timezone.utc)
  day += one_day

  result = {}

  processed_data_by_day = {}
  print(f"Processing data...")
  while day < now:
    key = day.strftime('%Y-%m-%d')
    year_month = day.strftime('%Y-%m')
    year = day.strftime('%Y')

    open_pr_count = 0
    closed_pr_count = 0
    open_issue_count = 0
    closed_issue_count = 0

    for i in data:
      element = data[i]

      if element['created_at'] > day:
        continue

      is_open = True
      if isinstance(element['closed_at'], datetime.datetime) and element['closed_at'] < day:
        is_open = False
      if element['is_pull_request']:
        if is_open:
          open_pr_count += 1
        else:
          closed_pr_count += 1
      else:
        if is_open:
          open_issue_count += 1
        else:
          closed_issue_count += 1

    processed_data_by_day[key] = {
      'open_issues': open_issue_count,
      'closed_issues': closed_issue_count,
      'open_pull_requests': open_pr_count,
      'closed_pull_requests': closed_pr_count,
      'year_month': year_month,
      'year': year
    }

    day += one_day
  
  # We take the values of the last day of each period
  processed_data_by_month = {}  
  for k,v in groupby(sorted(processed_data_by_day.items()), key=lambda i:i[1]['year_month']):
    last_day = list(v)[-1]
    open_issues_count = last_day[1]['open_issues']
    open_pull_requests_count = last_day[1]['open_pull_requests']
    processed_data_by_month[last_day[0]] = {
      'open_issues': open_issues_count,
      'open_pull_requests': open_pull_requests_count
    }

  processed_data_by_year = {}  
  for k,v in groupby(sorted(processed_data_by_day.items()), key=lambda i:i[1]['year']):
    last_day = list(v)[-1]
    open_issues_count = last_day[1]['open_issues']
    open_pull_requests_count = last_day[1]['open_pull_requests']
    processed_data_by_year[last_day[0]] = {
      'open_issues': open_issues_count,
      'open_pull_requests': open_pull_requests_count
    }

  # Break data in arrays to easily load it 
  formatted_data = ""
  dates = '["x",'
  open_issues = '["Open Issues"'
  open_pull_requests = '["Open Pull Requests"'
  for i in processed_data_by_day.keys():
    dates += f'"{i}",'
    open_issues += f",{processed_data_by_day[i]['open_issues']}"
    open_pull_requests += f",{processed_data_by_day[i]['open_pull_requests']}"
  dates += "]"
  open_issues += "]"
  open_pull_requests += "]"
  daily_processed_data = f"window.dailyData = [{dates}, {open_issues}, {open_pull_requests}];"

  formatted_data = ""
  dates = '["x",'
  open_issues = '["Open Issues"'
  open_pull_requests = '["Open Pull Requests"'
  for i in list(processed_data_by_day)[-30:]:
    dates += f'"{i}",'
    open_issues += f",{processed_data_by_day[i]['open_issues']}"
    open_pull_requests += f",{processed_data_by_day[i]['open_pull_requests']}"
  dates += "]"
  open_issues += "]"
  open_pull_requests += "]"
  last_thirty_days_processed_data = f"window.lastThirtyDays = [{dates}, {open_issues}, {open_pull_requests}];"

  formatted_data = ""
  dates = '["x",'
  open_issues = '["Open Issues"'
  open_pull_requests = '["Open Pull Requests"'
  for i in processed_data_by_month.keys():
    dates += f'"{i}",'
    open_issues += f",{processed_data_by_month[i]['open_issues']}"
    open_pull_requests += f",{processed_data_by_month[i]['open_pull_requests']}"
  dates += "]"
  open_issues += "]"
  open_pull_requests += "]"
  monthly_processed_data = f"window.monthlyData = [{dates}, {open_issues}, {open_pull_requests}];"

  formatted_data = ""
  dates = '["x",'
  open_issues = '["Open Issues"'
  open_pull_requests = '["Open Pull Requests"'
  for i in processed_data_by_year.keys():
    dates += f'"{i}",'
    open_issues += f",{processed_data_by_year[i]['open_issues']}"
    open_pull_requests += f",{processed_data_by_year[i]['open_pull_requests']}"
  dates += "]"
  open_issues += "]"
  open_pull_requests += "]"
  yearly_processed_data = f"window.yearlyData = [{dates}, {open_issues}, {open_pull_requests}];"

  print(f"Processing completed!")

  with open(PROCESSED_DATA_FILE, 'w') as json_file:
    json_file.write(f"{daily_processed_data}\n")
    json_file.write(f"{last_thirty_days_processed_data}\n")
    json_file.write(f"{monthly_processed_data}\n")
    json_file.write(f"{yearly_processed_data}\n")


import_data()
process_data()