from typing import Union
from fastapi import FastAPI, HTTPException 
from python_on_whales import docker
import json

def error_check(command_output: str):
    if "User not found" in command_output:
        raise HTTPException(status_code=400, detail="User not found")
    if "record not found" in command_output:
            raise HTTPException(status_code=400, detail="Identifier not found")

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

    if command == "list" or command == "ls" :
        ## JSON output always displays tags so -t flag is unnecessary
        command_output = str(docker.execute(container="headscale-headscale-1", command=headscale + [command, "-u", user]))
        error_check(command_output)
        return json.loads(command_output)
    
    elif command == "delete" or command == "del" or command == "expire" or command == "logout":
        if id <= 0:
            raise HTTPException(status_code=400, detail="Identifier invalid or not set")
        command_output = str(docker.execute(container="headscale-headscale-1", command=headscale + [command, "-i", str(id)]))
        error_check(command_output)
        return json.loads(command_output)

    elif command == "move" or command == "mv":
        if id <= 0:
            raise HTTPException(status_code=400, detail="Identifier invalid or not set")
        command_output = str(docker.execute(container="headscale-headscale-1", command=headscale + [command, "-i", str(id), "-u", user]))
        error_check(command_output)
        return json.loads(command_output)

    elif command == "tag" or command == "tags":
        if id <= 0:
            raise HTTPException(status_code=400, detail="Identifier invalid or not set")
        command_output = str(docker.execute(container="headscale-headscale-1", command=headscale + [command, "-i", str(id), "-t", tags]))
        error_check(command_output)
        return json.loads(command_output)

    elif command == "rename":
        if id <= 0:
            raise HTTPException(status_code=400, detail="Identifier invalid or not set")
        command_output = str(docker.execute(container="headscale-headscale-1", command=headscale + [command, "-i", str(id), name]))
        error_check(command_output)
        return json.loads(command_output)
       
    else:
        raise HTTPException(status_code=400, detail="Unkonwn command")
