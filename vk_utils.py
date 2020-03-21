# -*- coding: cp1251 -*-
import vk
import config
import users_data_controller


def get_vk_api():
    session = vk.Session()
    session.access_token = config.VK_ACCESS_TOKEN
    return vk.API(session, v='5.85')


def get_mem(user_id):
    api = get_vk_api()
    counter = users_data_controller.get_counter_value(user_id)
    users_data_controller.change_user_counter(user_id)
    post = api.wall.get(owner_id=config.GROUPS[0], count=1, offset=counter)['items'][0]
    attachment = post['attachments'][0]
    if "photo" in attachment:
        return attachment['photo']['sizes'][4]['url']
    else:
        return ""
