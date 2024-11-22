from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class AbstractRepository(Generic[T], ABC):
    @abstractmethod
    async def get(self, id: int) -> T:
        ...
        
    @abstractmethod
    async def add(self, id: int) -> T:
        ...
        
    # @abstractmethod
    # async def delete(self, id: int): #-> bool:
    #     ...
        
    # @abstractmethod
    # async def update(self, id: int): #-> T:
    #     ...
    