import json

from dataclasses import dataclass
from hamcrest import assert_that, equal_to

from src.schemes.asset_type import AssetTypeResponse
from src.utils.common import search
from src.utils.common import generate_random_value
from src.utils.data import login_data, headers


@dataclass
class Session:
    site: None

    id: str = None
    jwt: str = None
    csrf: str = None

    def __post_init__(self):
        self.id, self.jwt, self.csrf = self.login()

    def login(self):
        jwt_response = self.site.login.post(form_data=login_data,
                                            headers=headers(Origin=self.site.project.client.host,
                                                            Referer=self.site.project.client.host))
        response = self.site.main.get()

        csrf_token = search(r'name="YII_CSRF_TOKEN" content="(\w*)"', response.text)

        return jwt_response.cookies['PHPSESSID'], json.loads(jwt_response.text)['jwt'], csrf_token

    def logout(self):
        return self.site.logout.get(cookies={'PHPSESSID': self.id})


@dataclass
class AssetType:
    service: None
    session: Session = None

    response: AssetTypeResponse = None

    def __post_init__(self):
        name = f'AutoTest_{generate_random_value()}'
        self.service.asset_type.post(token=self.session.jwt,
                                     json={'name': name})
        self.response = self.service.asset_type.get(filters={"name": name}).obj_list[0]

    def update(self, data: dict):
        response = self.service.asset_type.put(item=self.response.id, json=data)
        assert_that(response.text, equal_to(''))
