import logging
import datetime
from sqlalchemy import MetaData, Table, Column, Integer, Numeric, String, DateTime, \
    ForeignKey, Float, Boolean, UniqueConstraint
from sqlalchemy.orm import as_declarative
from pydantic import BaseModel

logger = logging.getLogger(__name__)


############################################
# Model/Constants

class Rolename:
    ADMIN: str = "admin"
    DATA_COLLECTOR: str = "data_collector"
    MRI_OPERATOR: str = "mri_operator"
    PARTICIPANT: str = "participant"
    SYS_DATA_ENTRY: str = "sys_data_entry"


############################################
# Model/DTO


class BaseDTO:
    """Base class for all DTOs
    """

    def __init__(self):
        pass


class BasePydantic(BaseModel, BaseDTO):
    """Base class for all pydantic based DTOs
    """
    pass


class RoleInfoDTO(BasePydantic):
    """Short role info DTO
    """

    id: int = 0
    rolename: str = None
    description: str = None


class UserInfoDTO(BasePydantic):
    """Short user info DTO
    """

    id: int = 0
    username: str = None
    first_name: str = None
    last_name: str = None


############################################
# Model/Entity


@as_declarative()
# the same as BaseEntity = declarative_base(cls=BaseDTO)
class BaseEntity(BaseDTO):
    """Base class for all entity ORM based DTOs
    """

    def __init__(self):
        pass

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(
                getattr(self, column.name), (datetime.datetime, datetime.date)
            )
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }


class RoleEntity(BaseEntity):
    """Entity for "role" table
    """
    __tablename__ = 'role'
    __table_args__ = (
        UniqueConstraint('rolename'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    rolename = Column(String(45), nullable=False)
    description = Column(String(128))

    def __repr__(self):
        return "RoleEntity(id={self.id}, " \
               "rolename='{self.rolename}', " \
               "description='{self.description}')".format(self=self)
