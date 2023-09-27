from hamcrest import assert_that, equal_to

from src.matchers.asset_type import verify_asset_type


def test_update_asset_type(service, create_asset_type):
    data = create_asset_type.response.json
    data.update({'isSourceLanguage': False})

    create_asset_type.update(data)

    response = service.asset_type.get(item=create_asset_type.response.id)
    assert_that(response.obj.ok, f"Ok was not received. {response.text}")
    assert_that(response.obj.isSourceLanguage, equal_to(False))

    verify_asset_type(create_asset_type.response, data)
