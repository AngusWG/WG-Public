import datetime

day_end_time = 18, 40


def main():
    now = datetime.datetime.now()
    end_time = datetime.datetime(now.year, now.month, now.day, *day_end_time)
    day_off_hours = end_time - now
    weekday = day_off_hours + datetime.timedelta((4 - now.weekday()) % 7)
    print(
        "{:02}:{:02} to go after work".format(
            int(day_off_hours.total_seconds() // 3600),
            int(day_off_hours.total_seconds() % 3600 / 3600 * 60),
        )
    )
    print(
        "{:02}:{:02} hours to go vacation".format(
            int(weekday.total_seconds() // 3600),
            int(weekday.total_seconds() % 3600 / 3600 * 60),
        )
    )


if __name__ == "__main__":
    main()
