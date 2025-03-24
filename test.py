import proj_lib as p
import settings

params = {}
data = {}
headers = settings.headers
parent_org = settings.parent_org
org_gh_url = settings.org_gh_url


#r = p.postReq(url,data,headers)
#print(r)

# List Organization repos
repos = p.get_gh_org_repo()
print(repos)

#List repo contributors
for repo in repos:
    url = org_gh_url + "/repos/" + repo["full_name"] + "/contributors"
    res = p.getReq(url, params, headers)
    print(repo)
    for contributors in res:
        print(contributors)

