import os
import csv
import datetime
import gitlab_stats

GITLAB_TOKEN_ENV = 'GITLAB_TOKEN'


def check_token(token):
    if token is None:
        try:
            token = os.environ[GITLAB_TOKEN_ENV]
        except KeyError:
            print("\nEnvironment variable containing your gitlab token could not be found"
                  "\nSet it using `export GITLAB_TOKEN=<your gitlab token>")

    return token


def format_proxy(url):
    return {'http': url, 'https': url}


def get_name_and_id(project_dict):
    project_info = []
    for elem in project_dict:
        project_info.append({'id': elem['id'], 'name': elem['name']})

    return project_info


def get_pipelines_id(pipeline_dict):
    pipelines = []
    for elem in pipeline_dict:
        pipelines.append(elem['id'])

    return pipelines


def get_pipeline_info(elem):
    pipeline_info = {'id': elem['id'],
                     'status': elem['status'],
                     'duration': elem['duration'],
                     'date': str(elem['finished_at'])[:10]
                     }
    return pipeline_info


def seconds_to_min(seconds):
    mins, sec = divmod(round(seconds), 60)
    return "{} min {}s".format(round(mins), sec)


def clean_null_from(a_list):
    a_list = filter(lambda x: x is not None, a_list)
    return a_list


def get_duration_moy(project_info):
    duration = (pipeline['duration'] for pipeline in project_info['pipelines'])
    duration = list(filter(lambda x: x is not None, duration))

    return round(sum(duration) / len(duration), 1) if len(duration) else None


def get_success_percentagex(project_info):
    success = 0
    for pipeline in project_info['pipelines']:
        if pipeline['status'] == 'success':
            success += 1

    return round(success * 100 / len(project_info['pipelines']))


def get_success_percentage(project_info):
    success = list((pipeline['status'] for pipeline in project_info['pipelines']))

    return round(success.count('success') * 100 / len(success)) if len(success) else None


def get_pipeline_info_from(project_info, days=15):
    date = datetime.datetime.now() - datetime.timedelta(days=days)
    pipelines = []
    for pipeline in project_info['pipelines']:
        if datetime.datetime.strptime(pipeline['date'], "%Y-%m-%d") > date:
            pipelines.append(pipeline)
        else:
            break
    project_info['pipelines'] = pipelines

    return project_info


def enhance_project_info(project_info):
    project_info.update({'duration_moy': get_duration_moy(project_info)})
    project_info.update({'duration_in_minutes': seconds_to_min(project_info['duration_moy'])})
    project_info.update({'success_percentage': get_success_percentage(project_info)})

    project_info.pop('pipelines', None)
    return project_info


def print_cli_report(project_info):
    print(gitlab_stats.CLI_REPORT.format(project_info['name'],
                                         project_info['id'],
                                         datetime.date.today(),
                                         project_info['duration_in_minutes'],
                                         project_info['success_percentage']))


def generate_report(project_info, path='output.csv'):
    if os.path.isfile(path):
        write_dict_to_csv(project_info, path)
    else:
        create_dict_to_csv(project_info, path)


def write_dict_to_csv(project_info, path):
    with open(path, 'a') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, project_info.keys())
        w.writerow(project_info)


def create_dict_to_csv(project_info, path):
    with open(path, 'w') as f:
        w = csv.DictWriter(f, project_info.keys())
        w.writeheader()
        w.writerow(project_info)
