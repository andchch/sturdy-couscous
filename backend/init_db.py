import asyncio
from alembic.config import Config
from alembic import command

async def init_db():
    # Получаем путь к директории с alembic.ini
    alembic_cfg = Config('alembic.ini')
    
    # Запускаем миграции
    command.upgrade(alembic_cfg, 'head')
    
    print('Database migrations completed successfully!')

if __name__ == '__main__':
    asyncio.run(init_db()) 