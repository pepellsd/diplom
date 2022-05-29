import asyncio
import logging
from fastapi import APIRouter, Depends
from fastapi.background import BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Any

from app.services import scheduler
from app.services.database.base import get_repository
from app.schemas import RegisterDevice, MachineResponse, AnalyzeMioActivity
from app.services.database.repository.user_repository import UserRepository
from app.services.database.repository.statistic_repository import StatisticRepository
from app.services.vk_client.vk_client import VKClient, get_vk_client_stub
from app.services.machine_learning.machine_learning_model import get_machine_learning_model_stub

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
    data: AnalyzeMioActivity,
    background_task: BackgroundTasks,
    stat_repo: StatisticRepository = Depends(get_repository(StatisticRepository)),
    clf: Any = Depends(get_machine_learning_model_stub)
):
    smoke_status = clf.predict(data.mio_values)
    background_task.add_task(
        stat_repo.create_stat,
        mio_values=data.mio_values,
        user_id=data.user_id,
        status=smoke_status
    )
    return MachineResponse(status_smoke=smoke_status)


@router.post('/register', description='register device in system and create user for device')
async def register_device(
    data: RegisterDevice,
    background_task: BackgroundTasks,
    vk_client: VKClient = Depends(get_vk_client_stub),
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
):
    loop = asyncio.get_running_loop()
    is_auth = await loop.run_in_executor(None, vk_client.set_credentials, data.vk_login, data.vk_password)
    if is_auth is False:
        return JSONResponse(status_code=400, content={'message': 'wrong password for vk account'})
    user = await user_repo.create_user(data.vk_login, data.vk_password)
    if user is None:
        return JSONResponse(status_code=400, content={'message': 'vk account already in use'})
    background_task.add_task(vk_client.post_on_wall)
    return JSONResponse(status_code=201, content={'message': 'user successfully create', 'user_id': user.id})


@router.on_event("startup")
async def startup_event(loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()):
    logging.basicConfig(level=logging.DEBUG)
    loop.create_task(scheduler.run_scheduler())

