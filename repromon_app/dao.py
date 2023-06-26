import logging
from repromon_app.model import RoleInfoDTO, RoleEntity, UserInfoDTO, MessageLogInfoDTO, StudyInfoDTO
from sqlalchemy import MetaData, Table, Column, Integer, Numeric, String, DateTime, \
    ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import text


logger = logging.getLogger(__name__)
logger.debug("name=" + __name__)


############################################
# DAO

def dto(cls, proxy):
    if proxy:
        return cls.parse_obj(proxy._mapping)
    return None


def list_dto(cls, proxy):
    if proxy:
            return [cls.parse_obj(r._mapping) for r in proxy]
    return []


def to_dto(cls, proxy):
    if proxy:
        if isinstance(proxy, list):
            return [cls.parse_obj(r._mapping) for r in proxy]
        return cls.parse_obj(proxy._mapping)
    return None


class BaseDAO:
    """Base class for all DAO objects
    """
    default_session = None

    def __init__(self):
        pass

    def session(self):
        return BaseDAO.default_session


# User, role account DAO
class AccountDAO(BaseDAO):
    def __init__(self):
        pass

    def get_roles(self) -> list[RoleEntity]:
        return self.session().query(RoleEntity).all()

    def get_role_by_id(self, id: int) -> RoleEntity:
        return self.session().get(RoleEntity, id)

    def get_role_by_rolename(self, rolename: str) -> RoleEntity:
        return self.session(). \
            query(RoleEntity).filter(RoleEntity.rolename == rolename).first()

    def get_role_infos(self) -> list[RoleInfoDTO]:
        return list_dto(RoleInfoDTO, self.session().execute(
            text("""
                select
                    id, 
                    rolename, 
                    description
                from 
                    role    
            """
                 )
        ).all())

    def get_user_info(self, username: str) -> UserInfoDTO:
        return dto(UserInfoDTO, self.session().execute(
            text("""
                select
                    u.id,
                    u.username,
                    u.first_name,
                    u.last_name
                from
                    user u
                where
                    u.username = :username
            """
                 ), {'username': username}
        ).first())


# Message system DAO
class MessageDAO(BaseDAO):
    def __init__(self):
        pass

    def get_message_log_infos(self, study_id: int) -> list[MessageLogInfoDTO]:
        return list_dto(self.session().execute(
            text("""
                select
                    ml.id,
                    ml.study_id,
                    time(ml.created_on) as time,
                    mc.category,
                    ss.status,
                    ll.level,
                    dp.provider,
                    ml.description
                from
                    message_log ml
                    left join message_category mc on ml.category_id = mc.id
                    left join study_status ss on ml.status_id = ss.id
                    left join message_level ll on ml.level_id = ll.id
                    left join data_provider dp on ml.provider_id = dp.id
                where
                    ml.study_id = :study_id
                order by ml.created_on asc
                """
                 ), {'study_id': study_id}
        ).all())


# Security system DAO
class SecSysDAO(BaseDAO):
    def __init__(self):
        pass


# Study and related things DAO
class StudyDAO(BaseDAO):
    def __init__(self):
        pass

    def get_study_info(self, study_id: int) -> StudyInfoDTO:
        return dto(self.session().execute(
            text("""
                select
                    sd.id,
                    md.description as device,
                    ss.status,
                    sd.description as study,
                    sd.start_ts,
                    sd.end_ts
                from
                    study_data sd
                    left join study_status ss on sd.status_id = ss.id
                    left join device md on sd.device_id = md.id
                where
                    sd.id = :study_id
            """
                 ), {'study_id': study_id}
        ).first())


# DAO factory
class DAO:
    def __init__(self):
        self.account = AccountDAO()
        self.message = MessageDAO()
        self.study = StudyDAO()
        self.sec_sys = SecSysDAO()









