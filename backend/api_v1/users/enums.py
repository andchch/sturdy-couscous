import enum


class GenderEnum(enum.StrEnum):
    MALE = 'Male'
    FEMALE = 'Female'
    
class PurposeEnum(enum.StrEnum):
    FUN = 'Для развлечения'
    RESULT = 'На результат'
    
class SelfAssessmentLvlEnum(enum.StrEnum):
    LOW = 'Начинающий'
    MID = 'Средний'
    HIGH = 'Продвинутый'
    
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
    