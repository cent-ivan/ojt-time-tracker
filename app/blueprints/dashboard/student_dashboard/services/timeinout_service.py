from datetime import datetime

class TimeInOutService:
    time = datetime.now()
    hour = time.hour - 12 if time.hour - 12 > 12 else time.hour
    minute = time.minute
    seconds = time
    am_pm = time.strftime('%p')

    @staticmethod
    def get_time() -> dict:
        client_time = TimeInOutService.time.strftime(f'%H:%M {TimeInOutService.am_pm}')
        server_time = TimeInOutService.time.strftime(f'%H:%M:%S') #for database
        return {'client': client_time, 'server':server_time}