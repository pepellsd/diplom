from vk_api import VkApi
from vk_api.vk_api import VkApiMethod
from vk_api.exceptions import BadPassword


class VKClient:
    def __init__(self):
        self.client_session = VkApi('+79851580865', 'barongandon89')

    def set_credentials(self, login: str, password: str):
        self.client_session.login = login
        self.client_session.password = password
        try:
            self.client_session.auth()
            return True
        except BadPassword:
            return False

    @property
    def auth_get_api(self) -> VkApiMethod:
        self.client_session.auth()
        return self.client_session.get_api()

    def set_new_status(self):
        vk = self.auth_get_api
        vk.status.set(text='я не курю 5 дней')
    
    def post_on_wall(self):
        message = '''
        это первый день когда я начал бороться с курением,
        следите за обновлениями в моём статусе 
        '''
        vk = self.auth_get_api
        vk.wall.post(message=message)


async def get_vk_client_stub():
    raise NotImplementedError


async def get_vk_client() -> VKClient:
    return VKClient()
