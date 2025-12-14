from fastapi import APIRouter, HTTPException, UploadFile, File

router = APIRouter(tags=["UserRequests"])

@router.post("/user/upload-and-create")
async def upload_and_create(file: UploadFile = File(...)):
    # SSoT: multipart upload -> CreateRequestResponse.
    raise HTTPException(status_code=501, detail="Not Implemented")