from aiogram.types import User
from asyncpg import Connection


class Repository:
    def __init__(self, conn: Connection):
        self._conn = conn

    async def save_user(self, user: User):
        save_user_q = ("INSERT INTO users(user_id,"
                       "username, name, surname) VALUES ($1, $2, $3, $4)"
                       " ON CONFLICT DO NOTHING;")
        await self._conn.execute(save_user_q, user.id, user.username,
                                 user.first_name, user.last_name)

    async def choose_character(self, user_id: int, character: str):
        char_choice_q = "UPDATE users SET character = $1 WHERE user_id = $2;"
        await self._conn.execute(char_choice_q, character, user_id)

    async def get_char(self, user_id: int) -> str | None:
        get_char_q = "SELECT character FROM users WHERE user_id = $1;"
        return await self._conn.fetchval(get_char_q, user_id)

    async def write_message(self, user_id: int, message: str) -> int:
        char = await self.get_char(user_id)
        write_message_q = ("INSERT INTO conversations(by_user, character, user_message)"
                           " VALUES($1, $2, $3) RETURNING conversation_id;")

        return await self._conn.fetchval(write_message_q, user_id, char, message)

    async def save_reply(self, reply: str, conv_id: int):
        save_reply_q = ("UPDATE conversations SET bot_reply = $1"
                        "WHERE conversation_id = $2;")
        await self._conn.execute(save_reply_q, reply, conv_id)

    async def get_char_greetings(self, character: str):
        gcg_q = "SELECT welcome_message FROM characters WHERE char_name = $1;"
        return await self._conn.fetchval(gcg_q, character)

    async def get_prompt(self, user_id: int):
        gp_q = ("SELECT prompt FROM characters c"
                " JOIN users u ON c.char_name = u.character"
                " WHERE u.user_id = $1;")
        return await self._conn.fetchval(gp_q, user_id)
