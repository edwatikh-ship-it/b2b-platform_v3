from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["ModeratorTasks"])

@router.get("/moderator/tasks")
async def list_moderator_tasks(status: str | None = None, limit: int = 50):
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/moderator/tasks/{taskId}")
async def get_moderator_task(taskId: int):
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.post("/moderator/requests/{requestId}/start-parsing")
async def start_parsing(requestId: int):
    raise HTTPException(status_code=501, detail="Not Implemented")