import os
import logging
import requests
import json
import argparse
import pprint

def shortenMiddle(s, n):
    sLen = len(s)
    if sLen > n:
        halfN = int(n / 2)
        return s[:halfN] + '...' + s[-halfN:]
    return s

logger = logging.getLogger('enable_req_status_check')
logger.setLevel(logging.DEBUG)
logger.handlers = []

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
logger.addHandler(sh)

ghRootEndpoint = 'https://api.github.com'
createRepoURL = ghRootEndpoint + "/user/repos"
deleteRepoURL = ghRootEndpoint + "/repos/tejakummarikuntla/{repo_name}"

ghAPIToken = os.environ['GITHUB_API_TOKEN']

logger.info("GITHUB_API_TOKEN='{}'".format(shortenMiddle(ghAPIToken, 6)))
headers = {'Authorization': 'token ' + ghAPIToken}

repoCreationPayload = json.dumps(
    {
        "name": "Hello-World",
        "description": "This is your first repository",
        "homepage": "https://github.com",
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    })

def createRepo(repo):

    load_dict = json.loads(repoCreationPayload)
    load_dict["name"]=repo
    # repoCreationPayload["private"] = mode
    ghApiCreateResponse = requests.post(createRepoURL,
                                        json.dumps(load_dict),
                                        headers = headers).json()
    logger.info(pprint.pprint(ghApiCreateResponse))

def deleteRepo(repo):

    ghApiDeleteResponse = requests.delete(deleteRepoURL.format(repo_name=repo),
                                          headers = headers
                                          )
    logger.info(pprint.pprint(ghApiDeleteResponse))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog= 'CLI to Create or Delete a Repo',
        usage='''
        
        ''',
        description='''
        
        ''',
        add_help= True
    )

    parser.add_argument("--create", "-c", type=str, help="Enter the name of the Repo", metavar="")
    parser.add_argument("--delete", "-d", type=str, )

    arg = parser.parse_args()

    if arg.create is not None:
        createRepo(arg.create)

    else:
        if arg.delete is not None:
            deleteRepo(arg.delete)