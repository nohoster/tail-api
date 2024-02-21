from typing import Union
from fastapi import FastAPI, HTTPException 
from python_on_whales import docker
import json

def error_check(command_output: str):
    if "User not found" in command_output:
        raise HTTPException(status_code=400, detail="User not found")
    if "record not found" in command_output:
            raise HTTPException(status_code=400, detail="Identifier not found")

def id_check(id:int):
    if id <= 0:
        raise HTTPException(status_code=400, detail="Identifier invalid or not set")


app = FastAPI()

@app.get("/api/v1/headscale/preauthkeys/list")
def preauthkey_list(
        user: str, 
        tags: Union[str, None] = None
        ):

    headscale = ["headscale", "-o", "json", "preauthkeys", "list"]

    command_output = str(docker.execute(container="headscale-headscale-1", command=headscale + ["-u", user]))
    error_check(command_output)

    keys = json.loads(command_output)
    if tags:
        for key_dict in keys:
            if "acl_tags" in key_dict and tags in key_dict["acl_tags"] :
                return key_dict
    else:
        return keys

@app.get("/api/v1/headscale/nodes/{command}")
def nodes_commands(
        command: str,
        user: str = "",
        id: int = 0,
        tags: str = "",
        name: str = ""
        ):
    
    headscale = ["headscale", "-o", "json", "nodes"]

    if command in ["list", "ls"] :
        ## JSON output always displays tags so -t flag is unnecessary
        command_output = str(docker.execute(container="headscale-headscale-1", command=headscale + [command, "-u", user]))
        error_check(command_output)
        return json.loads(command_output)
    
    elif command in ["delete", "del", "expire", "logout"]:
        id_check(id)
        command_output = str(docker.execute(container="headscale-headscale-1", command=headscale + [command, "-i", str(id)]))
        error_check(command_output)
        return json.loads(command_output)

    elif command in ["move", "mv"]:
        id_check(id)
        command_output = str(docker.execute(container="headscale-headscale-1", command=headscale + [command, "-i", str(id), "-u", user]))
        error_check(command_output)
        return json.loads(command_output)

    elif command in ["tag", "tags"]:
        id_check(id)
        command_output = str(docker.execute(container="headscale-headscale-1", command=headscale + [command, "-i", str(id), "-t", tags]))
        error_check(command_output)
        return json.loads(command_output)

    elif command == "rename":
        id_check(id)
        command_output = str(docker.execute(container="headscale-headscale-1", command=headscale + [command, "-i", str(id), name]))
        error_check(command_output)
        return json.loads(command_output)
       
    else:
        raise HTTPException(status_code=400, detail="Unkonwn command")
