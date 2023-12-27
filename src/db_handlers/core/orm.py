from datetime import datetime, timedelta
from .models import Advertisement, Shelter, Animal
from .services import retrieve_attributes, row_to_dict
from sqlalchemy.future import select
from typing import Type, Optional, Dict
from src.db_handlers.core.models import Base
from src.db_handlers.db_manage import AsyncSessionLocal


class BaseRepository:
    """
    Generic base class for interacting with the data storage.
    """

    def __init__(self,  model_type: Type[Base]):
        """
        Initialize the BaseRepository object.

        :param model_type: The type of the SQLAlchemy model.
        """
        self.session = AsyncSessionLocal()
        self.model_type = model_type

    async def retrieve_one(self, pk: int):
        """
        Retrieve one object by its identifier.

        :param pk: Object identifier.
        :return: Dictionary with object data or a message indicating that the object was not found.
        """
        async with self.session as ss:
            async with ss.begin():
                result = await ss.get(self.model_type, pk)
                return await retrieve_attributes(result) if result else {"message": f"{self.model_type.__name__} not found."}

    async def retrieve_all(self):
        """
        Retrieve all objects.

        :return: Dictionary with data of all objects or a message indicating that there are no objects.
        """
        async with self.session as ss:
            async with ss.begin():
                result = await ss.execute(self.model_type.__table__.select())
                return await row_to_dict(result) if result else {"message": f"No {self.model_type.__name__} objects."}

    async def filter_all(self, filter_condition: Optional[Dict] = None):
        """
        Retrieve objects based on a filter condition.

        :param filter_condition: Dictionary representing the filter condition.
        :return: Dictionary with data of objects or a message indicating that there are no objects.
        """
        async with self.session as ss:
            async with ss.begin():
                query = select(self.model_type.__table__)
                if filter_condition:
                    query = query.filter_by(**filter_condition)
                result = await ss.execute(query)
                return await row_to_dict(result) if result else {"message": f"No {self.model_type.__name__} objects."}

    async def create(self, **kwargs):
        """
        Create a new object.

        :param kwargs: Keyword arguments representing the object data.
        :return: Created object.
        """
        async with self.session as ss:
            async with ss.begin():
                new_object = self.model_type(**kwargs)
                try:
                    ss.add(new_object)
                    return {"message": f"A new {self.model_type.__name__} created: {new_object}."}
                except Exception as e:
                    print(e)
                    return {"message": f"Database error!"}

    async def delete(self, pk: int):
        """
        Delete an object by its identifier.

        :param pk: Object identifier.
        :return: True if the object is successfully deleted, None if the object is not found.
        """
        async with self.session as ss:
            async with ss.begin():
                obj = await ss.get(self.model_type, pk)
                if obj:
                    await ss.delete(obj)
                    return {"message": f"The {self.model_type.__name__} with ID {pk} was deleted."}
                else:
                    return {"message": f"No {self.model_type.__name__} objects."}

    async def update(self, pk: int, new_data: dict):
        """
        Update object data.

        :param pk: Object identifier.
        :param new_data: New data for updating.
        :return: True if the object is successfully updated, False if the object is not found.
        """
        async with self.session as ss:
            async with ss.begin():
                obj = await ss.get(self.model_type, pk)
                if obj:
                    for key, value in new_data.items():
                        setattr(obj, key, value)
                    return {"message": f"The {self.model_type.__name__} with ID {pk} was updated."}
                else:
                    return {"message": f"No {self.model_type.__name__} objects."}


class AdvertisementRepository(BaseRepository):
    def __init__(self):
        super().__init__(Advertisement)

    async def filter_by_time(self, days):
        """
        Retrieve advertisements published in the last N days.

        :param days: Number of days to retrieve advertisements for.
        :return: Dictionary with data of advertisements or a message indicating that there are no advertisements.
        """
        time_interval = datetime.now() - timedelta(days=days)
        async with self.session as ss:
            async with ss.begin():
                result = await ss.execute(
                    select(Advertisement.__table__).where(Advertisement.published_time >= time_interval))
                return await row_to_dict(result) if result else {"message": "No advertisements."}


class ShelterRepository(BaseRepository):
    def __init__(self):
        super().__init__(Shelter)


class AnimalRepository(BaseRepository):
    def __init__(self):
        super().__init__(Animal)
