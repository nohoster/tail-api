from typing import Union
from fastapi import FastAPI
from python_on_whales import docker
import json
from modules import nodes, common
from modules.nodes import Node

app = FastAPI()

@app.get("/api/v1/headscale/preauthkeys/list")
def preauthkey_list(
        user: str, 
        tags: Union[str, None] = None
        ):

    headscale = ["headscale", "-o", "json", "preauthkeys", "list"]

    command_output = str(docker.execute(container="headscale-headscale-1", command=headscale + ["-u", user]))
    common.error_check(command_output)

    keys = json.loads(command_output)
    if tags:
        for key_dict in keys:
           if "acl_tags" in key_dict and tags in key_dict["acl_tags"] :
                return key_dict
    else:
        return keys

## Node management methods

@app.get("/api/v1/headscale/nodes/")
def nodes_get_wrapper(user: str = ""):
    return nodes.nodes_get(user)

@app.delete("/api/v1/headscale/nodes/")
def nodes_delete_wrapper(id: int, expire: bool = False):
    return nodes.nodes_delete(id, expire)

@app.post("/api/v1/headscale/nodes/")
def nodes_post_wrapper(node: Node):
    return nodes.nodes_post(node)

