import enum


class Weekdays(enum.StrEnum):
    MONDAY = 'Понедельник'
    TUESDAY = 'Вторник'
    WEDNESDAY = 'Среда'
    THURSDAY = 'Четверг'
    FRIDAY = 'Пятница'
    SATURDAY = 'Суббота'
    SUNDAY = 'Воскресенье'
    
class Genres(enum.StrEnum):
    RPG = 'РПГ'
    SHOOTER = 'Шутер'
    MOBA = 'Моба'
    STRATEGY = 'Стратегия'
    HORROR = 'Хоррор'
    SIMULATOR = 'Симулятор'
    