from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import StreamingResponse

from src.medol.dependencies.dependencies import get_file_service, oauth2_scheme
from src.medol.schemas.file_schema import FileInfo, FileList
from src.medol.services.file_service import FileService

router = APIRouter()


@router.post("/", response_model=FileInfo)
async def upload_file(
        file: UploadFile = File(...),
        file_service: FileService = Depends(get_file_service),
        token: str = Depends(oauth2_scheme)
):
    return await file_service.upload_file(file)


@router.get("/", response_model=FileList)
async def list_files(
        prefix: str = "",
        file_service: FileService = Depends(get_file_service),
        token: str = Depends(oauth2_scheme)
):
    files = file_service.list_files(prefix)
    return FileList(files=files)


@router.get("/{file_path:path}")
async def download_file(
        file_path: str,
        file_service: FileService = Depends(get_file_service),
        token: str = Depends(oauth2_scheme)
):
    file_data, content_type, file_name = file_service.download_file(file_path)

    return StreamingResponse(
        content=file_data,
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={file_name}"}
    )


@router.delete("/{file_path:path}", response_model=dict)
async def delete_file(
        file_path: str,
        file_service: FileService = Depends(get_file_service),
        token: str = Depends(oauth2_scheme)
):
    return file_service.delete_file(file_path)
