from .controller import Controller
from datetime import datetime


def main():
    time_server_start = datetime.utcnow()
    Controller.save_time_server_start_and_time_between_job(time_server_start)

    return Controller.create_job()
