from typing import Union
from fastapi import FastAPI, HTTPException 
from python_on_whales import docker
import json

app = FastAPI()

@app.get("/api/v1/headscale/preauthkeys/list")
def preauthkey_list(
        user: str, 
        tags: Union[str, None] = None
        ):
    headscale = ["headscale", "-o", "json", "preauthkeys", "list"]
    command_output = docker.execute(container="headscale-headscale-1", command=headscale + ["-u", user])
    
    keys = json.loads(command_output)

    if "error" in keys:
        if "User not found" in keys["error"]:
            raise HTTPException(status_code=400, detail="User not found")

    if tags:
        for key_dict in keys:
            if "acl_tags" in key_dict and tags in key_dict["acl_tags"] :
                return key_dict
    else:
        return keys

