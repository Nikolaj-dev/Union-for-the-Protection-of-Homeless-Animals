from typing import Annotated
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, func, ForeignKey
from enum import Enum


intpk = Annotated[int, mapped_column(primary_key=True)]
str128 = Annotated[str, mapped_column(String(128))]
current_time = Annotated[str, mapped_column(DateTime(), server_default=func.now(), server_onupdate=func.now(), nullable=True)]


class Base(DeclarativeBase):
    pass


class Advertisement(Base):
    __tablename__ = "advertisement"

    pk: Mapped[intpk]
    title: Mapped[str128]
    body: Mapped[str] = mapped_column(Text())
    image_path: Mapped[str] = mapped_column(Text())
    published_time: Mapped[current_time]

    def __repr__(self):
        return str(self.title)


class Shelter(Base):
    __tablename__ = "shelters"

    pk: Mapped[intpk]
    title: Mapped[str128]
    address: Mapped[str] = mapped_column(String(512))
    phone_number: Mapped[str] = mapped_column(String(13))
    telegram: Mapped[str] = mapped_column(String(128), nullable=True)
    instagram: Mapped[str] = mapped_column(String(128), nullable=True)
    twitter: Mapped[str] = mapped_column(String(128), nullable=True)
    website: Mapped[str] = mapped_column(String(256), nullable=True)
    animals = relationship('Animal', back_populates='shelters')

    def __repr__(self):
        return str(self.title)


class SexEnum(Enum):
    female = "female"
    male = "male"


class SpeciesEnum(Enum):
    cat = "cat"
    kitty = "kitty"
    dog = "dog"
    puppy = "puppy"
    other = "other"


class Animal(Base):
    __tablename__ = "animals"

    pk: Mapped[intpk]
    name: Mapped[str128]
    sex: Mapped[SexEnum]
    age: Mapped[int]
    species: Mapped[SpeciesEnum]
    since_time: Mapped[str] = mapped_column(DateTime())
    shelter_id: Mapped[int] = mapped_column(ForeignKey('shelters.pk', ondelete='SET NULL'), nullable=True)
    shelters = relationship('Shelter', back_populates='animals')

    def __repr__(self):
        return str(self.name)
    