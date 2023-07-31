import datetime
import logging

from pydantic import BaseModel
from sqlalchemy import (JSON, TIMESTAMP, Column, Index, Integer, String, Text,
                        UniqueConstraint)
from sqlalchemy.orm import as_declarative

logger = logging.getLogger(__name__)


############################################
# Model/Constants

class DataProvider:
    ID_REPROIN: int = 1
    ID_REPROSTIM: int = 2
    ID_REPROEVENTS: int = 3
    ID_PACS: int = 4
    ID_NOISSEUR: int = 5
    ID_DICOM_QA: int = 6
    ID_MRI: int = 7


class MessageCategory:
    ID_FEEDBACK: int = 1


class MessageLevel:
    ANY: str = "*"
    INFO: str = "INFO"
    WARN: str = "WARN"
    ERROR: str = "ERROR"
    #
    ID_INFO: int = 1
    ID_WARN: int = 2
    ID_ERROR: int = 3

    @classmethod
    def parse(cls, level: str) -> int:
        if level == MessageLevel.INFO:
            return MessageLevel.ID_INFO
        if level == MessageLevel.WARN:
            return MessageLevel.ID_WARN
        if level == MessageLevel.ERROR:
            return MessageLevel.ID_ERROR
        raise Exception(f"Unknown level: {level}")


class Rolename:
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
    study_id: int = 0
    time: datetime.time = None
    ts: datetime.datetime = None
    category: str = None
    status: str = None
    level: str = None
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

    id = Column(Integer, primary_key=True, autoincrement=True)
    provider = Column(String(15), nullable=False, unique=True)

    def __repr__(self):
        return "DataProviderEntity(id={self.id}, " \
               "provider='{self.provider}')".format(self=self)


class DeviceEntity(BaseEntity):
    """Entity for "device" table
    """
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True, autoincrement=True)
    kind = Column(String(15))
    description = Column(String(128))

    def __repr__(self):
        return "DeviceEntity(id={self.id}, " \
               "kind='{self.kind}', " \
               "description='{self.description}')".format(self=self)


class MessageCategoryEntity(BaseEntity):
    """Entity for "message_category" table
    """
    __tablename__ = 'message_category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(45))

    def __repr__(self):
        return "MessageCategoryEntity(id={self.id}, " \
               "category='{self.category}')".format(self=self)


class MessageLevelEntity(BaseEntity):
    """Entity for "message_level" table
    """
    __tablename__ = 'message_level'

    id = Column(Integer, primary_key=True)
    level = Column(String(8))

    def __repr__(self):
        return "MessageLevelEntity(id={self.id}, " \
               "level='{self.level}')".format(self=self)


class MessageLogEntity(BaseEntity):
    """Entity for "message_log" table
    """
    __tablename__ = 'message_log'

    id = Column(Integer, primary_key=True, autoincrement=True)
    level_id = Column(Integer)
    category_id = Column(Integer)
    provider_id = Column(Integer)
    study_id = Column(Integer)
    status_id = Column(Integer)
    is_visible = Column(String(1), default='Y')
    description = Column(String(255))
    payload_id = Column(Integer)
    created_on = Column(TIMESTAMP)
    created_by = Column(String(15))

    def __repr__(self):
        return "MessageLogEntity(id={self.id}, " \
               "level_id='{self.level_id}', " \
               "category_id='{self.category_id}', "\
               "provider_id='{self.provider_id}', " \
               "study_id='{self.study_id}', " \
               "status_id='{self.status_id}', " \
               "is_visible='{self.is_visible}', " \
               "description='{self.description}', " \
               "payload_id='{self.payload_id}', " \
               "created_on='{self.created_on}', " \
               "created_by='{self.created_by}')".format(self=self)


class MessagePayloadEntity(BaseEntity):
    """Entity for "message_payload" table
    """
    __tablename__ = 'message_payload'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(36))
    payload = Column(Text)
    created_on = Column(TIMESTAMP)
    created_by = Column(String(15))

    def __repr__(self):
        return "MessagePayloadEntity(id={self.id}, " \
               "uid='{self.uid}', " \
               "payload='{self.payload}', " \
               "created_on='{self.created_on}', " \
               "created_by='{self.created_by}')".format(self=self)


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


class SecUserDeviceEntity(BaseEntity):
    """Entity for "sec_user_device" table
    """
    __tablename__ = 'sec_user_device'
    __table_args__ = (
        UniqueConstraint('user_id', 'device_id'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    device_id = Column(Integer, nullable=False)

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

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    role_id = Column(Integer, nullable=False)

    def __repr__(self):
        return "SecUserRoleEntity(id={self.id}, " \
               "user_id='{self.user_id}', " \
               "role_id='{self.role_id}')".format(self=self)


class StudyDataEntity(BaseEntity):
    """Entity for "study_data" table
    """
    __tablename__ = 'study_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(128))
    device_id = Column(Integer)
    status_id = Column(Integer)
    start_ts = Column(TIMESTAMP)
    end_ts = Column(TIMESTAMP)
    info = Column(JSON)

    def __repr__(self):
        return "StudyDataEntity(id={self.id}, " \
               "description='{self.description}', " \
               "device_id='{self.device_id}', " \
               "status_id='{self.status_id}', "\
               "start_ts='{self.start_ts}', " \
               "end_ts='{self.end_ts}', " \
               "info='{self.info}')".format(self=self)


class StudyStatusEntity(BaseEntity):
    """Entity for "study_status" table
    """
    __tablename__ = 'study_status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(45))

    def __repr__(self):
        return "StudyStatusEntity(id={self.id}, " \
               "status='{self.status}')".format(self=self)


class UserEntity(BaseEntity):
    """Entity for "user" table
    """
    __tablename__ = 'user'
    __table_args__ = (
        UniqueConstraint('email'),
        Index('idx_user_name', 'username')
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(15), nullable=False, unique=True)
    is_active = Column(String(1), default='N')
    is_system = Column(String(1), nullable=False, default='N')
    first_name = Column(String(45))
    last_name = Column(String(45))
    email = Column(String(128), unique=True)
    phone = Column(String(16))
    description = Column(String(128))
    password = Column(String(45))
    password_changed_on = Column(TIMESTAMP)
    last_login = Column(TIMESTAMP)

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
               "password='{self.password}', " \
               "password_changed_on='{self.password_changed_on}', " \
               "last_login='{self.last_login}')".format(self=self)
