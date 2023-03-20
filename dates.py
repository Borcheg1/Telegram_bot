from datetime import datetime


month_replace = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}


class Date:
    def __init__(self, webinar_date):
        self.start_webinar = webinar_date

    def get_webinar_date(self):
        if self.start_webinar.minute // 10 == 0:
            date = (
                f"{self.start_webinar.day} "
                f"{month_replace[self.start_webinar.month]} "
                f"в {self.start_webinar.hour}:0{self.start_webinar.minute}"
            )
        else:
            date = (
                f"{self.start_webinar.day} "
                f"{month_replace[self.start_webinar.month]} "
                f"в {self.start_webinar.hour}:{self.start_webinar.minute}"
            )
        return date

    def days_left(self):
        days = int(self.start_webinar.strftime("%j")) - int(datetime.today().strftime("%j"))
        if days > 0 and (days % 10 == 0 or days % 10 > 4 or days in [11, 12, 13, 14, 111, 112, 113, 114]):
            return f"{days} дней"
        elif days > 0 and 1 < days % 10 < 5:
            return f"{days} дня"
        elif days > 0 and days % 10 == 1:
            return f"{days} день"
