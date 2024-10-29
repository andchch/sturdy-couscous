import enum


class GenderEnum(enum.StrEnum):
    MALE = 'мужской'
    FEMALE = 'женский'
    
class PurposeEnum(enum.StrEnum):
    FUN = 'Для развлечения'
    RESULT = 'На результат'
    
class SelfAssessmentLvlEnum(enum.StrEnum):
    LOW = 'Начинающий'
    MID = 'Средний'
    HIGH = 'Продвинутый'
    
class CommunicationTypeEnum(enum.StrEnum):
    VOICE = 'Голосовой'
    TEXT = 'Внутриигровой чат'
    NO = 'Нет'
    
class RatingEnum(enum.IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    