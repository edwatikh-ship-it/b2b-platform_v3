from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["UserMessaging"])

@router.put("/user/requests/{requestId}/recipients")
async def update_recipients(requestId: int, payload: dict):
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.post("/user/requests/{requestId}/send")
async def send_request_messages(requestId: int, payload: dict):
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.post("/user/requests/{requestId}/send-new")
async def send_request_messages_new(requestId: int, payload: dict):
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/user/requests/{requestId}/messages")
async def list_request_messages(requestId: int, limit: int = 50, offset: int = 0, includedeleted: bool = False):
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.delete("/user/messages/{messageId}")
async def delete_message(messageId: int):
    raise HTTPException(status_code=501, detail="Not Implemented")