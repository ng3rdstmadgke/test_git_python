import shutil
import os
from uuid import uuid4

import git

work_dir = f"/tmp/test_git_python/{str(uuid4())}"
repo_dir = f"{work_dir}/repo"
sample_dir = f"{work_dir}/repo/sample"
repo_url = "git@github.com:ng3rdstmadgke/test_git_python.git"
print(f"work_dir: {work_dir}")
print(f"repo_dir: {repo_dir}")
print(f"repo_url: {repo_url}")
os.makedirs(work_dir)

git.Git().clone(repo_url, repo_dir)
repo = git.Repo(repo_dir)

shutil.rmtree(sample_dir, ignore_errors=True)
shutil.copytree("./sample", sample_dir)
shutil.copyfile("./main.py", f"{repo_dir}/main.py")

repo.git.add(all=True)

repo.index.commit("message")

repo.remote("origin").push()
