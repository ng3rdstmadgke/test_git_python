from typing import List
import shutil
import os
from uuid import uuid4

import git
import yaml
from pydantic import BaseModel

class SkyportDeviceSchema(BaseModel):
    name: str
    ip_addr: str

class SkyportSchema(BaseModel):
    ssid: str
    devices: List[SkyportDeviceSchema]


tmp = {}
tmp["ssid"] = "skyport01"
tmp["devices"] = []
for i in range(0, 10):
    tmp["devices"].append(
        {
            "name": f"node{i}",
            "ip_addr": f"192.168.50.{i}"
        }
    )

schema = SkyportSchema.parse_obj(tmp)

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
shutil.copyfile("./requirements.txt", f"{repo_dir}/requirements.txt")
with open(f"{repo_dir}/vars.yml", "w") as writer:
    writer.write(yaml.dump(schema.dict()))


repo.git.add(all=True)

repo.index.commit("message")

repo.remote("origin").push()
