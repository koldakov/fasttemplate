from fastapi import APIRouter, Response, status

router: APIRouter = APIRouter()


@router.get(
    "/health",
    include_in_schema=False,
    status_code=status.HTTP_200_OK,
)
async def health():
    return Response(status_code=status.HTTP_200_OK)
