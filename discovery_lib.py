import proj_lib as p

def repo_discovery(queue, task):
    repos = p.get_gh_org_repo(1)
    try:
        # check for Error, if error occurs calling above function.
        print(repos["err"])
        task["status"] = "failed"
        p.task_closure(task["id"], repos, queue, task)
    except:
        print(task["id"])
        task["status"] = "completed"
        p.task_closure(task["id"], repos, queue, task)
        print(repos)