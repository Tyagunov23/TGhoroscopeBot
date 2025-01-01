import schedule
import time
import threading


def schedule_daily_task(task, time_of_day):
    """
    Расписание ежедневной задачи.

    :param task: функция, которую нужно запускать
    :param time_of_day: время запуска в формате "HH:MM"
    """
    schedule.every().day.at(time_of_day).do(task)

    while True:
        schedule.run_pending()
        time.sleep(60)


def start_scheduler(task, time_of_day="10:00"):
    """
    Запуск планировщика в отдельном потоке.

    :param task: функция, которую нужно запускать ежедневно
    :param time_of_day: время запуска в формате "HH:MM"
    """
    thread = threading.Thread(target=schedule_daily_task, args=(task, time_of_day))
    thread.daemon = True
    thread.start()
