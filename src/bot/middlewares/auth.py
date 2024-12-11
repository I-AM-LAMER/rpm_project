from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.types import TelegramObject
from aiogram.filters.command import CommandObject
from pprint import pprint

from ..states import AuthForm


class AuthMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        current_state = await data['state'].get_state()
        print(data['command'])
        if data['command'].command == 'cancel':
            if current_state:
                data['state'].clear()
                data['state'].set_state(AuthForm.authentificated)    
            data['command'] = CommandObject(command='start')
        print(data['command'])
        return await handler(event, data)
            

        