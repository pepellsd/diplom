import datetime
import asyncio

from clepsydra import create_async_scheduler, IntervalRule, Context
from app.services.database.base import async_session
from app.services.database.repository.user_repository import UserRepository
from app.services.vk_client.vk_client import VKClient


scheduler = create_async_scheduler()


@scheduler.task
async def check_users_for_achievements(context: Context):
    loop = asyncio.get_running_loop()
    user_repo = context.data['user_repo']
    VkClient = context.data["vk_client_class_ref"]
    users = await user_repo.get_users()
    print(users)
    for user in users:
        print(user.id)
        vk_client = VkClient(login=user.vk_login, password=user.vk_password)
        print("init vk_client")
        if len(user.statistics) > 0:
            smoke_status = False
            for stat in user.statistics:
                if stat.status is True:
                    smoke_status = True
                    break
            if smoke_status is True:
                print("set status")
                loop.run_in_executor(None, vk_client.set_new_status, "я все таки покурил")
            else:
                no_smoke_count = user.no_smoke_count + 1
                await user_repo.update_user_smoke_count(user_id=user.id, no_smoke_count=no_smoke_count)
                loop.run_in_executor(None, vk_client.set_new_status, f'я  не курю уже {no_smoke_count} день/дня/дней')
        else:
            no_smoke_count = user.no_smoke_count + 1
            await user_repo.update_user_smoke_count(user_id=user.id, no_smoke_count=no_smoke_count)
            loop.run_in_executor(None, vk_client.set_new_status, f'я  не курю уже {no_smoke_count} день/дня/дней')
    print("finish task")
    await user_repo.db.close()


@scheduler.middleware
async def m(context, *args, **kwargs):
    user_repo = UserRepository(db=async_session())
    context.data["user_repo"] = user_repo
    context.data["vk_client_class_ref"] = VKClient


async def run_scheduler():
    now = datetime.datetime.now()
    start_date = now.replace(hour=23)
    rule = IntervalRule(period=datetime.timedelta(days=1), start=start_date)
    await scheduler.add_job('check_users_for_achievements', rule=rule)
    await scheduler.run()

