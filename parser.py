import logging
from hashlib import sha256
from github import Github

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def match_file(diff, files, line=""):
    res = ""
    # check the SHA256.hexdigest() of each filename for a match to diff
    for file in files:
        h = sha256(file.filename.encode()).hexdigest()
        if h == diff:
            if line:
                res = f"{file.filename}#L{line}"
            else:
                res = f"{file.filename}"
            break
    return res


def get_blob(data):
    line = ""
    _branch = data.pop(0)
    data = "/".join(data)
    if "#L" in data:
        data, line = data.split("#L")
    if line:
        res = f"{data}#L{line}"
    else:
        res = f"{data}"
    return res


def get_commit(org, repo, commit_id, github_token):
    if "#diff" in commit_id:
        commit_id, diff = commit_id.split("#diff-")

        # 'R' separates the line number
        if "R" in diff:
            diff, line = diff.split("R")
        else:
            line = ""

        # grab the filenames of all files changed in this commit
        commit = (
            Github(github_token).get_repo(f"{org}/{repo}").get_commit(f"{commit_id}")
        )

        # check the SHA256.hexdigest() of each filename for a match to 'diff'
        res = match_file(diff, commit.files, line)
    else:
        res = f"commit: {commit_id}"
    return res


def get_pull(org, repo, pr, data, github_token):
    res = ""
    if data[0] == "commits":
        data.pop(0)
        res = get_commit(org, repo, "/".join(data), github_token)
    elif data[0].startswith("files"):
        _, diff = data[0].split("#diff-")
        if "R" in diff:
            diff, line = diff.split("R")
        else:
            line = ""
        files = Github(github_token).get_repo(f"{org}/{repo}").get_pull(pr).get_files()
        res = match_file(diff, files, line)
    return res


def parse_url(url, github_token):
    res = ""

    if "github.com" not in url:
        log.debug(f"No match in URL: {url}")
        return res
    log.info(f"Parsing GitHub url: {url}")
    data = url.split("github.com/")[1].split("/")
    org = data.pop(0)
    repo = data.pop(0)
    type_ = data.pop(0)

    if type_ == "blob":
        res = get_blob(data)
    elif type_ == "commit":
        commit_id = data.pop(0)
        res = get_commit(org, repo, commit_id, github_token)
    elif type_ == "pull":
        pr = int(data.pop(0))
        res = get_pull(org, repo, pr, data, github_token)
    else:
        log.info(f"Github link not understood by parser: {url}")

    return res
