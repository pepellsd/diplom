import asyncio
import datetime
from fastapi import APIRouter, Depends
from fastapi.background import BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List
from clepsydra import create_async_scheduler, IntervalRule

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
        mio_values: List[int], user_id: int,
        background_task: BackgroundTasks,
        stat_repo: StatisticRepository = Depends(get_repository(StatisticRepository))
):
    # space for machine learning model
    background_task.add_task(stat_repo.create_stat, mio_values=mio_values, user_id=user_id, status=False)
    return MachineResponse(status_smoke=True)  # late


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


async def check_users_for_achievements(
        user_repo: UserRepository = Depends(get_repository(UserRepository)),
        loop: asyncio.AbstractEventLoop = asyncio.get_running_loop(),
        vk_client: VKClient = Depends(get_vk_client_stub)
):
    users = await user_repo.get_users()
    for user in users:
        loop.run_in_executor(None, vk_client.set_credentials, user.vk_login, user.vk_password)
        if len(user.statistics) > 0:
            for stat in user.statistics:
                if stat.status is True:
                    loop.run_in_executor(None, vk_client.set_new_status, "я все таки покурил")
                    break
            no_smoke_count = user.no_smoke_count + 1
            await user_repo.update_user_smoke_count(user_id=user.id, no_smoke_count=no_smoke_count)
            loop.run_in_executor(None, vk_client.set_new_status, f'я  не курю уже {no_smoke_count} день/дня/дней')
        else:
            no_smoke_count = user.no_smoke_count + 1
            await user_repo.update_user_smoke_count(user_id=user.id, no_smoke_count=no_smoke_count)
            loop.run_in_executor(None, vk_client.set_new_status, f'я  не курю уже {no_smoke_count} день/дня/дней')


@router.on_event("startup")
async def startup_event():
    scheduler = create_async_scheduler()
    await scheduler.add_job(
        'check_users_for_achievements',
        rule=IntervalRule(
            start=datetime.datetime.now(),
            period=datetime.timedelta(days=1)
        )
    )
    await scheduler.run()
