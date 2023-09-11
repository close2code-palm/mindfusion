import asyncio

import asyncpg
from asyncpg import Connection

from src.bot.config import read_db_conf


async def migrate():
    charactrs_q = ('CREATE TABLE characters('
                   'char_name TEXT PRIMARY KEY,'
                   'welcome_message TEXT,'
                   'prompt TEXT);')
    hellos_q = ('INSERT INTO character_hellos(char_name, welcome_message)'
                ' VALUES ("Mario", "Hi by Mario!"),'
                ' ("Albert", "Everything is relative!");')
    users_table_q = ('CREATE TABLE users('
                     'user_id BIGINT PRIMARY KEY,'
                     'username TEXT,'
                     'name TEXT NOT NULL,'
                     'character TEXT,'
                     'surname TEXT,'
                     'time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,'
                     'FOREIGN KEY(character) REFERENCES characters(char_name)'
                     ');')
    conversation_q = ('CREATE TABLE conversations('
                      'conversation_id SERIAL,'
                      'by_user BIGINT NOT NULL,'
                      'character TEXT NOT NULL,'
                      'user_message TEXT,'
                      'bot_reply TEXT,'
                      'FOREIGN KEY(character) REFERENCES characters(char_name),'
                      'FOREIGN KEY (by_user) REFERENCES users(user_id));')
    db = read_db_conf('../../config.ini')
    connection: Connection = await asyncpg.connect(db.dsn)
    await connection.execute(charactrs_q)
    # await connection.execute(hellos_q)
    await connection.execute(users_table_q)
    await connection.execute(conversation_q)
    await connection.close()


asyncio.run(migrate())
