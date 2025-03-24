import time
import proj_lib as p
import discovery_lib as d


'''
    Start reading jobs for this bot. bot.json file will be provided my mothership.
    It is a queue that bot is going to execute
'''

#Fetch bot jobs into a queue
queue = p.get_bot_jobs()

# start fetching tasks and executing them
while len(queue) > 0 :
    task = queue.pop()
    time.sleep(2)
    res = {}
    curr_time = time.strftime("%H:%M:%S", time.localtime())
    res["ts"] = curr_time

    print("Starting task : " + task["id"])
    if task["id"] == "repo_discovery":
        repos = p.get_gh_org_repo(1)
        res["code"] = "repo_discovery"
        res["data"] = repos
        print(res)
        #d.repo_discovery(queue,task)

    elif task["id"] == "repo_contributor_discovery":
        repos = p.get_gh_org_repo(0)
        params = p.get_gh_repo_contributors(repos)
        res["code"] = "repo_contributor_discovery"
        res["data"] = params
        print(res)

        ctrbs = []
        for param in params:
            for contributor in param["contributors"]:
                if contributor["login"] not in ctrbs:
                    ctrbs.append(contributor["login"])

        text_file = open("Output.txt", "w")
        text_file.write("%s" % ctrbs)
        text_file.close()

    elif task["id"] == "contributor_discovery":
        with open('Output.txt', 'r') as file:
            content = file.read()

        res["code"] = "contributor_discovery"
        res["data"] = content
        print(res)

    elif task["id"] == "user_discovery":
        with open('Output.txt', 'r') as file:
            users = file.readline().replace("[","").replace("]","").replace("'","").split(",")
            user_data = []
            for user in users:
                data = p.get_gh_user_details(user.strip())
                user_data.append(data)

        res["code"] = "contributor_discovery"
        res["data"] = user_data
        print(res)




