import requests
import settings
import json, copy

def getReq(url, params, headers):
    try:
        r = requests.get(url, params=params, headers=headers)
        code = r.status_code
        if code >= 200 and code <= 210:
            return r.json()
    except:
        return {"err": "Error"}

def postReq(url, data, headers):
    try:
        r = requests.post(url, json=data, headers=headers)
        code = r.status_code
        if code >= 200 and code <= 210:
            return r.json()
    except:
        return {"err": "Error"}

def get_gh_org_repo(deep) :
    url = settings.org_gh_url + "/orgs/" + settings.parent_org + "/repos"
    headers = settings.headers
    params = {}
    repos = []

    try:
        res = getReq(url, params, headers)
        # loop through all repo info and get names
        for r in res:

            # deep ==1 for all metadata, deep=0 for no metadata for
            # operations like get contributors
            repo_details = {}
            if deep ==0 :
                repo_details["full_name"] = r["full_name"]
            else :
                repo_details["full_name"] = r["full_name"]
                repo_details["url"] = r["url"]
                repo_details["created_at"] = r["created_at"]
                repo_details["updated_at"] = r["updated_at"]
                repo_details["size"] = r["size"]
                repo_details["owner"] = r["owner"]["login"]
                repo_details["language"] = r["language"]
                repo_details["forks"] = r["forks"]
                repo_details["permissions"] = r["permissions"]

            repos.append(repo_details)
        return repos

    except:
        return {"err": "Error"}



def get_gh_repo_contributors(repos):
    params = []
    #List repo contributors
    for repo in repos:
        url = settings.org_gh_url + "/repos/" + repo["full_name"] + "/contributors"
        res = getReq(url, {}, settings.headers)
        #print(repo["full_name"] + "  :: ")

        contributors = []
        for contributor in res:
            contributors.append(contributor)

        params.append({"full_name": repo["full_name"], "contributors" : contributors })

    return params


def get_gh_user_details(uname):
    params = {}
    headers = settings.headers
    url = settings.org_gh_url + "/users/" + uname + "/repos"
    res = getReq(url, params, headers)

    return res


def get_bot_jobs():
    with open('bot.json', 'r') as file:
        data = json.load(file)

    jobs = data["jobs"]
    # creating a job queues for the Bot
    arr = []
    for job in jobs:
        arr.append(job)

    queue = arr[::-1] #reversing array
    return queue


def task_closure(t_id,data,queue,task):
    '''
        if task is successful -->
          1) update the status of job from ytd to done
          2) write back to bot.json
          3) Send update to UX server of task completed
          4) Send data to Audience server
    '''
    qcopy = copy.deepcopy(queue)
    qcopy.append(task)
    data = qcopy[::-1]
    # Serializing json
    json_object = json.dumps(data, indent=4)
    # Writing to result.json
    with open("result.json", "w") as outfile:
        outfile.write(json_object)

    return 0