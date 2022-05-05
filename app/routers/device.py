from fastapi import APIRouter, Depends
from fastapi.background import BackgroundTasks
from fastapi.responses import JSONResponse

from app.services.database.base import get_repository
from app.schemas import RegisterDevice, MachineResponse
from app.services.database.repository.user_repository import UserRepository
from app.services.database.repository.statistic_repository import StatisticRepository
from app.services.vk_client.vk_client import VKClient, get_vk_client_stub

router = APIRouter(
    prefix='/api/v1/device',
    tags=['device']
)


@router.post(
    '/analyze',
    description='''
    take data from client and analyze it
    return true or false depends on data,
    response mean shock person or not''',
    response_model=MachineResponse
)
async def analyze_mio_activity(
        mio_value: int, user_id: str,
        background_task: BackgroundTasks,
        stat_repo: StatisticRepository = Depends(get_repository(StatisticRepository)),
        user_repo: UserRepository = Depends(get_repository(UserRepository))
):
    background_task.add_task(stat_repo.create_stat, mio_value=mio_value, user_id=user_id)
    return MachineResponse(status_smoke=True)  # late


@router.post('/register', description='register device in system and create user for device')
async def register_device(
    data: RegisterDevice,
    background_task: BackgroundTasks,
    vk_client: VKClient = Depends(get_vk_client_stub),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
):
    if not await vk_client.set_credentials(login=data.vk_login, password=data.vk_password):
        return JSONResponse(status_code=400, content={'message': 'wrong password for vk account'})
    user = await user_repo.create_user(data.vk_login, data.vk_password)
    if user is None:
        return JSONResponse(status_code=400, content={'message': 'vk account already in use'})
    background_task.add_task(vk_client.post_on_wall)
    return JSONResponse(status_code=201, content={'message': 'user successfully create', 'user_id': user.id})

