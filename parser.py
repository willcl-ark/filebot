import logging
from hashlib import sha256
from github import Github

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def parse_url(url, github_token):
    res = ""
    line = ""

    if "github.com" not in url:
        log.debug(f"No match in URL: {url}")
        return res
    log.info(f"Parsing GitHub url: {url}")

    url = url.split("github.com/")[1]

    # Handle blobs with or without line number
    if "blob" in url:
        if "#L" in url:
            url, line = url.split("#L")
        d = url.split("/")
        _org = d.pop(0)
        _repo = d.pop(0)
        d.pop(0)
        _branch = d.pop(0)
        filename = "/".join(d)
        if line:
            res = f"{filename}#L{line}"
        else:
            res = f"{filename}"

    # handle commits
    elif "commit" in url:
        if "pull" in url:
            org, repo, type_, _pull_id, _, commit_id = url.split("/")
        else:
            org, repo, type_, commit_id = url.split("/")
        if "#diff" in commit_id:
            commit_id, diff = commit_id.split("#diff-")

            # 'R' separates the line number
            if "R" in diff:
                diff, line = diff.split("R")

            # grab the filenames of all files changes in this commit
            g = Github(github_token)
            commit = g.get_repo(f"{org}/{repo}").get_commit(f"{commit_id}")

            # check the SHA256.hexdigest() of each filename for a match to 'diff'
            for file in commit.files:
                h = sha256(file.filename.encode()).hexdigest()
                if h == diff:
                    if line:
                        res = f"{file.filename}#L{line}"
                    else:
                        res = f"{file.filename}"
        else:
            res = f"commit: {commit_id}"
    else:
        # was a github link, but not something we can handle
        ...
    return res
