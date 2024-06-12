class Time:
    @staticmethod
    def seconds_to_hms(seconds: int):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"


def is_float(input:str) -> bool:
    try:
        float(input)
        return True
    except:
        return False
