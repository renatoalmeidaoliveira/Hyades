from __future__ import annotations

from dataclasses import dataclass, field
from typing import List
import asyncio

from hyades.parsers.fabric import ParserFabric
from hyades.connection.fabric import ConnectionFabric



class Device():
    name: str
    hostname: str
    platform: str
    username: str
    password: str
    transport: str = None
    groups: List[str] = []
    mode: str = 'async'
    parser: str = 'Default'
    connection_manager: str = 'scrapli'
    port: int = None
    enable_password: str = None
    
    def __init__(self, **kwargs) -> None:
        for attr in kwargs:
            setattr(self, attr, kwargs[attr])
        for attr in Device.__annotations__:
            if attr not in kwargs:
                try:
                    getattr(self, attr)
                except AttributeError:
                    raise MissingAttribute(f"Missing required attribute: {attr}")
                    
        self.parser_manager = ParserFabric(self).manager
        self.connection_manager = ConnectionFabric(self).manager

        

class MissingAttribute(Exception):
    ''' 
        Raises when Device __annotations__ attributes are missing when instantiating
        the object( required attributes )
    '''
