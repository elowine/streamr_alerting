import os

if os.path.exists(f'{os.path.dirname( __file__ )}/common/config.py'):
    from common import config
    from handler.handler import Handler as h

    from apscheduler.schedulers.blocking import BlockingScheduler
    import time


    def exec_get_info():
        print('begin get_info...')
        try:
            h().get_info()
        except Exception as e:
            print(e)
        print('end get_info...')


    def exec_check_status_node():
        print('begin check status node...')
        try:
            h().check_status_node()
        except Exception as e:
            print(e)
        print('end check status node...')


    if __name__ == '__main__':
        try:
            exec_get_info()
            if config.cron_active:
                scheduler = BlockingScheduler(timezone='Europe/Paris')
                # Execution every hour
                scheduler.add_job(exec_check_status_node, trigger='cron', hour="0/1")
                # Execution every Monday at 10:00 am
                scheduler.add_job(exec_get_info, trigger='cron', hour="10", minute="0", day="2/1")

                scheduler.print_jobs()
                scheduler.start()

                try:
                    while True:
                        time.sleep(10)
                except (KeyboardInterrupt, SystemExit):
                    scheduler.shutdown()
        except Exception as error:
            print(error)
else:
    raise ValueError("File config.py not found in the src/common directory")

