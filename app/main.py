from fastapi import FastAPI

from app.routers import device
from app.services.database.base import get_session, get_session_stub
from app.services.vk_client.vk_client import get_vk_client, get_vk_client_stub
from app.services.machine_learning.machine_learning_model import (
    get_machine_learning_model_stub, get_machine_learning_model
)


def application_factory():
    application = FastAPI()

    application.dependency_overrides[get_session_stub] = get_session
    application.dependency_overrides[get_vk_client_stub] = get_vk_client
    application.dependency_overrides[get_machine_learning_model_stub] = get_machine_learning_model

    application.include_router(device.router)

    return application


app = application_factory()





