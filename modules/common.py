from fastapi import HTTPException

def error_check(command_output: str):
    if "User not found" in command_output:
        raise HTTPException(status_code=400, detail="User not found")
    if "record not found" in command_output:
        raise HTTPException(status_code=400, detail="Identifier not found")
    if "tag must start" in command_output:
        raise HTTPException(status_code=400, detail="Tag must start with the string 'tag:'")

def id_check(id:int):
    if id <= 0:
        raise HTTPException(status_code=400, detail="Identifier invalid or not set")

