import time


def send_log_message(message):
    print("[Bot, {0}]: {1}".format(time.strftime("%H:%M:%S", time.localtime()), message))


def log_change_user_interval(user_id, new_interval):
    send_log_message("Change interval for <{0}> to {1} minutes".format(user_id, new_interval))


def log_add_user_to_db(user_id):
    send_log_message("Add <{0}> in DB".format(user_id))


def log_send_mem(user_id, url):
    send_log_message("Send mem for <{0}>, url: {1}".format(user_id, url))


def log_elapsed_time(minutes):
    send_log_message("{0} minutes have passed since the bot was launched".format(minutes))
