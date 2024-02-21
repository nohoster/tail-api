from python_on_whales import docker
from modules import common
from pydantic import BaseModel
from typing import Union
import json

class Node(BaseModel):
    id: int
    user: Union[str, None] = None
    tags: Union[str, None] = None
    name: Union[str, None] = None

headscale = ["headscale", "-o", "json", "nodes"]

def get_node(id: int, nodes: str):
    node_list = json.loads(nodes)
    for node in node_list:
        if node["id"] == id:
            return node
    return None

def move_node(id: int, user: str):
    command_output = str(docker.execute(container="headscale-headscale-1", command = headscale + ["move", "-i", str(id), "-u", user]))
    common.error_check(command_output)

def rename_node(id: int, name: str):
    command_output = str(docker.execute(container="headscale-headscale-1", command = headscale + ["rename", "-i", str(id), name]))
    common.error_check(command_output)

def tag_node(id: int, tags: str):
    command_output = str(docker.execute(container="headscale-headscale-1", command = headscale + ["tag", "-i", str(id), "-t", tags]))
    common.error_check(command_output)

def nodes_get(user: str = ""):
    ## JSON output always displays tags so -t flag is unnecessary
    command_output = str(docker.execute(container="headscale-headscale-1", command = headscale + ["list", "-u", user]))
    common.error_check(command_output)
    return json.loads(command_output)
    
def nodes_delete(
        id: int,
        expire: bool = False
        ):
    common.id_check(id)
    command = "expire" if expire else "delete"
    headscale = ["headscale", "-o", "json", "nodes", command, "-i", str(id), "--force"]
    command_output = str(docker.execute(container="headscale-headscale-1", command=headscale))
    common.error_check(command_output)
    return {"Success"}

def nodes_post(node: Node):
    common.id_check(node.id)
    if node.user: move_node(node.id, node.user)
    if node.name: rename_node(node.id, node.name)
    if node.tags: tag_node(node.id, node.tags)
    return {"Success"}




