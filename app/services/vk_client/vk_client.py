from vk_api import VkApi
from vk_api.vk_api import VkApiMethod
from vk_api.exceptions import BadPassword


class EmptyCredentials(Exception):
    pass


class VKClient:
    def __init__(self, login: str = None, password: str = None):
        self.client_session = VkApi(login=login, password=password)

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
        if self.client_session.login is None or self.client_session.password is None:
            raise EmptyCredentials("call {0}set_credentials".format(self.__class__.__name__))
        self.client_session.auth()
        return self.client_session.get_api()

    def set_new_status(self, text: str):
        vk = self.auth_get_api
        vk.status.set(text=text)
    
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
