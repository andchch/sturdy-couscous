import enum
from enum import Enum


class GenderEnum(enum.StrEnum):
    MALE = 'Male'
    FEMALE = 'Female'
    
class PurposeEnum(enum.StrEnum):
    FUN = 'Для развлечения'
    RESULT = 'На результат'
    
class CommunicationTypeEnum(enum.StrEnum):
    VOICE = 'Согл'
    NO_VOICE = 'Внутриигровой чат'
    INDIFFERENT = 'Все равно'
    
class WeekdayEnum(enum.StrEnum):
    MONDAY = 'Понедельник'
    TUESDAY = 'Вторник'
    WEDNESDAY = 'Среда'
    THURSDAY = 'Четверг'
    FRIDAY = 'Пятница'
    SATURDAY = 'Суббота'
    SUNDAY = 'Воскресенье'
    
class PreferredDaysEnum(str, Enum):
    WEEKDAYS = 'weekdays'
    WEEKENDS = 'weekends'

class PreferredTimeEnum(str, Enum):
    MORNING = 'morning'
    AFTERNOON = 'afternoon'
    EVENING = 'evening'
    NIGHT = 'night'
    
class RatingEnum(str, Enum):
    ONE_STAR = '1'
    TWO_STARS = '2'
    THREE_STARS = '3'
    FOUR_STARS = '4'
    FIVE_STARS = '5'
    