import datetime
import logging
from enum import Enum, IntEnum
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import (JSON, TIMESTAMP, Column, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import as_declarative

logger = logging.getLogger(__name__)


############################################
# Model/Constants

class IntEnumEx(IntEnum):
    @classmethod
    def parse(cls, v: str) -> int:
        try:
            n: int = int(v)  # parse as an integer first
            if n in iter(cls):
                return n
            raise Exception(f"'{v}' is not a valid ID for {cls.__name__}")
        except ValueError:
            pass

        try:
            return cls[v.upper()]
        except KeyError:
            raise ValueError(f"'{v}' is not a valid {cls.__name__}")


class DataProviderId(IntEnumEx):
    REPROIN = 1
    REPROSTIM = 2
    REPROEVENTS = 3
    PACS = 4
    NOISSEUR = 5
    DICOM_QA = 6
    MRI = 7


class MessageCategoryId(IntEnumEx):
    FEEDBACK = 1


class MessageLevelId(IntEnumEx):
    ANY = -1
    INFO = 1
    WARNING = 2
    ERROR = 3

    @classmethod
    def parse(cls, v: str) -> int:
        try:
            return MessageLevelId.ANY if v == '*' else super().parse(v)
        except KeyError:
            raise ValueError(f"'{v}' is not a valid MessageLevel")


class Rolename(str, Enum):
    ANY: str = "*"
    ADMIN: str = "admin"
    DATA_COLLECTOR: str = "data_collector"
    MRI_OPERATOR: str = "mri_operator"
    PARTICIPANT: str = "participant"
    SYS_DATA_ENTRY: str = "sys_data_entry"
    TESTER: str = "tester"


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


class LoginInfoDTO(BasePydantic):
    """Logged user info
    """

    is_logged_in: bool = False
    username: str = None
    first_name: str = None
    last_name: str = None


class MessageLogInfoDTO(BasePydantic):
    """Message log info view information
    """

    id: int = 0
    study_id: Optional[int] = None
    study: str = None
    event_on: datetime.datetime = None
    registered_on: datetime.datetime = None
    recorded_on: datetime.datetime = None
    recorded_by: str = None
    category: str = None
    level: str = None
    device_id: Optional[int] = 0
    device: str = None
    provider: str = None
    description: str = None


class PushMessageDTO(BasePydantic):
    """Basic envelope for server to client push messages
    """

    topic: str = None
    ts: datetime.datetime = None
    sender: str = None
    body: object = None


class RoleInfoDTO(BasePydantic):
    """Short role info DTO
    """

    id: int = 0
    rolename: str = None
    description: str = None


class StudyInfoDTO(BasePydantic):
    """Study header info view
    """

    id: int = 0
    device: str = None
    status: str = None
    study: str = 0
    start_ts: datetime.datetime = None
    end_ts: datetime.datetime = None


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

    def copy(self):
        o = self.__class__()
        for column in self.__table__.columns:
            setattr(o, column.name, getattr(self, column.name))
        return o

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            if not isinstance(
                getattr(self, column.name), (datetime.datetime, datetime.date)
            )
            else getattr(self, column.name).isoformat()
            for column in self.__table__.columns
        }


class DataProviderEntity(BaseEntity):
    """Entity for "data_provider" table
    """
    __tablename__ = 'data_provider'

    id = Column(Integer, primary_key=True)
    provider = Column(String(15), nullable=False, unique=True, index=True)

    def __repr__(self):
        return "DataProviderEntity(id={self.id}, " \
               "provider='{self.provider}')".format(self=self)


class DeviceEntity(BaseEntity):
    """Entity for "device" table
    """
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True)
    kind = Column(String(15), nullable=False)
    description = Column(String(128), nullable=False)

    def __repr__(self):
        return "DeviceEntity(id={self.id}, " \
               "kind='{self.kind}', " \
               "description='{self.description}')".format(self=self)


class MessageCategoryEntity(BaseEntity):
    """Entity for "message_category" table
    """
    __tablename__ = 'message_category'

    id = Column(Integer, primary_key=True)
    category = Column(String(45), nullable=False)

    def __repr__(self):
        return "MessageCategoryEntity(id={self.id}, " \
               "category='{self.category}')".format(self=self)


class MessageLevelEntity(BaseEntity):
    """Entity for "message_level" table
    """
    __tablename__ = 'message_level'

    id = Column(Integer, primary_key=True)
    level = Column(String(8), nullable=False)

    def __repr__(self):
        return "MessageLevelEntity(id={self.id}, " \
               "level='{self.level}')".format(self=self)


class MessageLogEntity(BaseEntity):
    """Entity for "message_log" table
    """
    __tablename__ = 'message_log'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    level_id = Column(Integer, nullable=False)
    category_id = Column(Integer, nullable=False, index=True)
    device_id = Column(Integer, nullable=False, index=True)
    provider_id = Column(Integer, nullable=False, index=True)
    study_id = Column(Integer, index=True)
    study_name = Column(String(255), index=True)
    is_visible = Column(String(1), default='Y', nullable=False, index=True)
    visible_updated_on = Column(TIMESTAMP)
    visible_updated_by = Column(String(15))
    description = Column(String(255))
    payload = Column(JSON)
    event_on = Column(TIMESTAMP, nullable=False, index=True)
    registered_on = Column(TIMESTAMP, nullable=False)
    recorded_on = Column(TIMESTAMP, nullable=False)
    recorded_by = Column(String(15), nullable=False)

    def __repr__(self):
        return "MessageLogEntity(id={self.id}, " \
               "level_id='{self.level_id}', " \
               "category_id='{self.category_id}', " \
               "device_id='{self.device_id}', " \
               "provider_id='{self.provider_id}', " \
               "study_id='{self.study_id}', " \
               "study_name='{self.study_name}', " \
               "is_visible='{self.is_visible}', " \
               "visible_updated_on='{self.visible_updated_on}', " \
               "visible_updated_by='{self.visible_updated_by}', " \
               "description='{self.description}', " \
               "payload='{self.payload}', " \
               "event_on='{self.event_on}', " \
               "registered_on='{self.registered_on}', " \
               "recorded_on='{self.recorded_on}', " \
               "recorded_by='{self.recorded_by}')".format(self=self)


class RoleEntity(BaseEntity):
    """Entity for "role" table
    """
    __tablename__ = 'role'
    __table_args__ = (
        UniqueConstraint('rolename'),
    )

    id = Column(Integer, primary_key=True, nullable=False)
    rolename = Column(String(45), nullable=False, index=True)
    description = Column(String(128), nullable=False)

    def __repr__(self):
        return "RoleEntity(id={self.id}, " \
               "rolename='{self.rolename}', " \
               "description='{self.description}')".format(self=self)


class SecUserDeviceEntity(BaseEntity):
    """Entity for "sec_user_device" table
    """
    __tablename__ = 'sec_user_device'
    __table_args__ = (
        UniqueConstraint('user_id', 'device_id'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    device_id = Column(Integer, nullable=False, index=True)

    def __repr__(self):
        return "SecUserDeviceEntity(id={self.id}, " \
               "user_id='{self.user_id}', " \
               "device_id='{self.device_id}')".format(self=self)


class SecUserRoleEntity(BaseEntity):
    """Entity for "sec_user_role" table
    """
    __tablename__ = 'sec_user_role'
    __table_args__ = (
        UniqueConstraint('user_id', 'role_id'),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)
    role_id = Column(Integer, nullable=False, index=True)

    def __repr__(self):
        return "SecUserRoleEntity(id={self.id}, " \
               "user_id='{self.user_id}', " \
               "role_id='{self.role_id}')".format(self=self)


class StudyDataEntity(BaseEntity):
    """Entity for "study_data" table
    """
    __tablename__ = 'study_data'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(128), nullable=False, index=True)
    device_id = Column(Integer, index=True)
    status_id = Column(Integer, index=True)
    start_ts = Column(TIMESTAMP)
    end_ts = Column(TIMESTAMP)
    info = Column(JSON)

    def __repr__(self):
        return "StudyDataEntity(id={self.id}, " \
               "name='{self.name}', " \
               "device_id='{self.device_id}', " \
               "status_id='{self.status_id}', "\
               "start_ts='{self.start_ts}', " \
               "end_ts='{self.end_ts}', " \
               "info='{self.info}')".format(self=self)


class StudyStatusEntity(BaseEntity):
    """Entity for "study_status" table
    """
    __tablename__ = 'study_status'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    status = Column(String(45), nullable=False, index=True, unique=True)

    def __repr__(self):
        return "StudyStatusEntity(id={self.id}, " \
               "status='{self.status}')".format(self=self)


class UserEntity(BaseEntity):
    """Entity for "user" table
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(15), nullable=False, unique=True, index=True)
    is_active = Column(String(1), default='N', index=True)
    is_system = Column(String(1), nullable=False, default='N', index=True)
    first_name = Column(String(45), index=True)
    last_name = Column(String(45), index=True)
    email = Column(String(128), unique=True, index=True)
    phone = Column(String(16))
    description = Column(String(128))
    password = Column(String(128))
    password_changed_on = Column(TIMESTAMP)
    apikey = Column(String(64))
    apikey_data = Column(String(45))
    apikey_issued_on = Column(TIMESTAMP)
    last_login_on = Column(TIMESTAMP)

    def clean_sensitive_info(self):
        self.password = "***"
        return self

    def __repr__(self):
        return "RoleEntity(id={self.id}, " \
               "username='{self.username}', " \
               "is_active='{self.is_active}', "\
               "is_system='{self.is_system}', " \
               "first_name='{self.first_name}', " \
               "last_name='{self.last_name}', " \
               "email='{self.email}', " \
               "phone='{self.phone}', " \
               "description='{self.description}', " \
               "password='***', " \
               "password_changed_on='{self.password_changed_on}', " \
               "last_login='{self.last_login}')".format(self=self)
