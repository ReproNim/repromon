import logging
from datetime import datetime, timedelta

from sqlalchemy.sql import func, text

from repromon_app.model import (BaseDTO, DataProviderEntity, DeviceEntity,
                                MessageLevelEntity, MessageLogEntity,
                                MessageLogInfoDTO, RoleEntity, RoleInfoDTO,
                                SecUserDeviceEntity, SecUserRoleEntity,
                                StudyDataEntity, StudyInfoDTO, UserEntity,
                                UserInfoDTO)

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


############################################
# DAO


def _dto(cls, proxy):
    if proxy:
        return cls.parse_obj(proxy._mapping)
    return None


def _list_dto(cls, proxy):
    if proxy:
        return [cls.parse_obj(r._mapping) for r in proxy]
    return []


def _list_scalar(cls, proxy):
    if proxy:
        return [cls(row[0]) for row in proxy]
    return []


def _scalar(cls, proxy):
    if proxy:
        return cls(proxy[0])
    return None


_prefix_: str = ''


class BaseDAO:
    """Base class for all DAO objects"""

    default_session = None
    default_schema = None

    def __init__(self):
        pass

    def add(self, o: BaseDTO):
        return self.session().add(o)

    def commit(self):
        self.session().commit()

    def count(self, entity):
        return self.session().query(func.count('*')).select_from(entity).scalar()

    def delete(self, o: BaseDTO):
        return self.session().delete(o)

    def flush(self):
        self.session().flush()

    @classmethod
    def set_default_schema(cls, db_schema: str):
        if db_schema is not None and len(db_schema) > 0:
            BaseDAO.default_schema = db_schema
        else:
            BaseDAO.default_schema = None
        global _prefix_
        _prefix_ = f"{BaseDAO.default_schema}." if BaseDAO.default_schema else ''

    def session(self):
        return BaseDAO.default_session


# User, role account DAO
class AccountDAO(BaseDAO):
    def __init__(self):
        pass

    def add_role(self, rolename: str, description: str) -> RoleEntity:
        o: RoleEntity = RoleEntity(rolename, description)
        self.session().add(o)
        self.session().commit()
        return o

    def add_user(self, username: str, is_active: str, is_system: str,
                 first_name: str, last_name: str, email: str,
                 phone: str, description: str) -> UserEntity:
        if self.get_user(username):
            raise Exception(f"User already exists: {username}")

        o: UserEntity = UserEntity()
        o.username = username
        o.is_active = is_active
        o.is_system = is_system
        o.first_name = first_name
        o.last_name = last_name
        o.email = email
        o.phone = phone
        o.description = description
        self.session().add(o)
        self.session().commit()
        return o

    def get_roles(self) -> list[RoleEntity]:
        return self.session().query(RoleEntity).all()

    def get_role_by_id(self, role_id: int) -> RoleEntity:
        return self.session().get(RoleEntity, role_id)

    def get_role_by_rolename(self, rolename: str) -> RoleEntity:
        return (
            self.session()
            .query(RoleEntity)
            .filter(RoleEntity.rolename == rolename)
            .first()
        )

    def get_role_infos(self) -> list[RoleInfoDTO]:
        return _list_dto(
            RoleInfoDTO,
            self.session()
            .execute(
                text(
                    f"""
                select
                    id,
                    rolename,
                    description
                from
                    {_prefix_} role
            """
                )
            )
            .all(),
        )

    def get_user(self, username: str) -> UserEntity:
        return (
            self.session()
            .query(UserEntity)
            .filter(UserEntity.username == username)
            .first()
        )

    def get_user_by_apikey(self, apikey: str) -> UserEntity:
        return (
            self.session()
            .query(UserEntity)
            .filter(UserEntity.apikey == apikey)
            .first()
        )

    def get_users(self) -> list[UserEntity]:
        return self.session().query(UserEntity).all()

    def get_user_info(self, username: str) -> UserInfoDTO:
        return _dto(
            UserInfoDTO,
            self.session()
            .execute(
                text(
                    f"""
                select
                    u.id,
                    u.username,
                    u.first_name,
                    u.last_name
                from
                    {_prefix_} user u
                where
                    u.username = :username
            """
                ),
                {"username": username},
            )
            .first(),
        )

    def update_user_apikey(self, username: str,
                           apikey: str,
                           apikey_data: str) -> UserEntity:
        o: UserEntity = self.get_user(username)
        if o:
            o.apikey = apikey
            o.apikey_data = apikey_data
            o.apikey_issued_on = datetime.now()
            self.session().commit()
        else:
            raise Exception(f"User not found: {username}")
        return o

    def update_user_is_active(self, username: str,
                              is_active: str) -> UserEntity:
        o: UserEntity = self.get_user(username)
        if o:
            o.is_active = is_active
            self.session().commit()
        else:
            raise Exception(f"User not found: {username}")
        return o

    def update_user_password(self, username: str,
                             pwd: str) -> UserEntity:
        o: UserEntity = self.get_user(username)
        if o:
            o.password = pwd
            o.password_changed_on = datetime.now()
            self.session().commit()
        else:
            raise Exception(f"User not found: {username}")
        return o


# Message system DAO
class MessageDAO(BaseDAO):
    def __init__(self):
        pass

    def get_data_providers(self) -> list[DataProviderEntity]:
        return self.session().query(DataProviderEntity).all()

    def get_devices(self) -> list[DeviceEntity]:
        return self.session().query(DeviceEntity).all()

    def get_message_levels(self) -> list[MessageLevelEntity]:
        return self.session().query(MessageLevelEntity).all()

    def get_message_log_infos(self, category_id: int,
                              study_id: int,
                              interval_sec: int) -> list[MessageLogInfoDTO]:
        start_event_on: datetime.datetime = \
            (datetime.now() - timedelta(seconds=interval_sec)) \
            if interval_sec else None
        return _list_dto(
            MessageLogInfoDTO,
            self.session()
            .execute(
                text(
                    f"""
                select
                    ml.id,
                    ml.study_id,
                    ml.study_name as study,
                    ml.event_on,
                    ml.registered_on,
                    ml.recorded_on,
                    ml.recorded_by,
                    mc.category,
                    ll.level,
                    ml.device_id,
                    dv.kind as device,
                    dp.provider,
                    ml.description
                from
                    {_prefix_} message_log ml
                    left join {_prefix_} message_category mc on ml.category_id = mc.id
                    left join {_prefix_} message_level ll on ml.level_id = ll.id
                    left join {_prefix_} device dv on ml.device_id = dv.id
                    left join {_prefix_} data_provider dp on ml.provider_id = dp.id
                where
                    (:study_id is null or ml.study_id = :study_id) and
                    (:category_id is null or ml.category_id = :category_id) and
                    (:start_event_on is null or
                        ml.event_on >= :start_event_on) and
                    ml.is_visible = 'Y'
                order by ml.event_on, ml.recorded_on asc
                limit 10000
                """
                ),
                {
                    "study_id": study_id,
                    "category_id": category_id,
                    "start_event_on": start_event_on,
                },
            )
            .all(),
        )

    def get_message_log_info(self, message_id: int) -> MessageLogInfoDTO:
        return _dto(
            MessageLogInfoDTO,
            self.session()
            .execute(
                text(
                    f"""
                select
                    ml.id,
                    ml.study_id,
                    ml.study_name as study,
                    ml.event_on,
                    ml.registered_on,
                    ml.recorded_on,
                    ml.recorded_by,
                    mc.category,
                    ll.level,
                    ml.device_id,
                    dv.kind as device,
                    dp.provider,
                    ml.description
                from
                    {_prefix_} message_log ml
                    left join {_prefix_} message_category mc on ml.category_id = mc.id
                    left join {_prefix_} message_level ll on ml.level_id = ll.id
                    left join {_prefix_} device dv on ml.device_id = dv.id
                    left join {_prefix_} data_provider dp on ml.provider_id = dp.id
                where
                    ml.id = :message_id
                """
                ),
                {"message_id": message_id},
            )
            .first(),
        )

    def update_message_log_visibility(self, category_id: int,
                                      is_visible: str,
                                      levels: list[int],
                                      interval_sec: int,
                                      updated_by: str) -> int:
        query = self.session().query(MessageLogEntity).filter(
            MessageLogEntity.category_id == category_id,
            MessageLogEntity.level_id.in_(levels)
        )

        if interval_sec and interval_sec > 0:
            start_event_on: datetime.datetime = \
                (datetime.now() - timedelta(seconds=interval_sec))
            query = query.filter(MessageLogEntity.event_on >= start_event_on)

        return query.update(
            {
                MessageLogEntity.is_visible: is_visible,
                MessageLogEntity.visible_updated_by: updated_by,
                MessageLogEntity.visible_updated_on: func.current_timestamp()
            },
            synchronize_session=False
        )

    def update_message_log_visibility_by_ids(self, ids: list[int],
                                             is_visible: str, updated_by: str) -> int:
        query = self.session().query(MessageLogEntity) \
            .filter(MessageLogEntity.id.in_(ids))

        return query.update(
            {
                MessageLogEntity.is_visible: is_visible,
                MessageLogEntity.visible_updated_by: updated_by,
                MessageLogEntity.visible_updated_on: func.current_timestamp()
            },
            synchronize_session=False
        )


# Security system DAO
class SecSysDAO(BaseDAO):
    def __init__(self):
        pass

    def add_sec_user_device(self, user_id: int, device_id: int) -> SecUserDeviceEntity:
        o: SecUserDeviceEntity = SecUserDeviceEntity(
            user_id=user_id, device_id=device_id)
        self.session().add(o)
        self.session().commit()
        return o

    def add_sec_user_role(self, user_id: int, role_id: int) -> SecUserRoleEntity:
        o: SecUserRoleEntity = SecUserRoleEntity(user_id=user_id, role_id=role_id)
        self.session().add(o)
        self.session().commit()
        return o

    def delete_sec_user_device_by_id(self, entity_id: int) -> int:
        res = (self.session().query(SecUserDeviceEntity).
               filter_by(id=entity_id).delete())
        self.session().commit()
        return res

    def delete_sec_user_role_by_id(self, entity_id: int) -> int:
        res = (self.session().query(SecUserRoleEntity).
               filter_by(id=entity_id).delete())
        self.session().commit()
        return res

    def get_device_id_by_username(self, username: str) -> list[str]:
        return _list_scalar(
            int,
            self.session()
            .execute(
                text(
                    f"""
                select
                    ud.device_id
                from
                    {_prefix_} user u, {_prefix_} sec_user_device ud
                where
                    u.username = :username and
                    u.id = ud.user_id
            """
                ),
                {"username": username},
            )
            .all(),
        )

    def get_sec_user_device_by_user_id(self, user_id: int) -> list[SecUserDeviceEntity]:
        return (
            self.session()
            .query(SecUserDeviceEntity)
            .filter(SecUserDeviceEntity.user_id == user_id)
            .all()
        )

    def get_sec_user_role_by_user_id(self, user_id: int) -> list[SecUserRoleEntity]:
        return (
            self.session()
            .query(SecUserRoleEntity)
            .filter(SecUserRoleEntity.user_id == user_id)
            .all()
        )

    def get_username_by_rolename(self, rolename: str) -> list[str]:
        return _list_scalar(
            str,
            self.session()
            .execute(
                text(
                    f"""
                select
                    u.username
                from
                    {_prefix_} role r,
                    {_prefix_} user u,
                    {_prefix_} sec_user_role ur
                where
                    r.rolename = :rolename and
                    ur.role_id = r.id and
                    u.id = ur.user_id
            """
                ),
                {"rolename": rolename},
            )
            .all(),
        )

    def get_rolename_by_username(self, username: str) -> list[str]:
        return _list_scalar(
            str,
            self.session()
            .execute(
                text(
                    f"""
                select
                    r.rolename
                from
                    {_prefix_} user u,
                    {_prefix_} role r,
                    {_prefix_} sec_user_role ur
                where
                    u.username = :username and
                    u.id = ur.user_id and
                    ur.role_id = r.id
            """
                ),
                {"username": username},
            )
            .all(),
        )


# Study and related things DAO
class StudyDAO(BaseDAO):
    def __init__(self):
        pass

    def get_study_data(self, study_id: int) -> StudyDataEntity:
        return self.session().get(StudyDataEntity, study_id)

    def get_study_info(self, study_id: int) -> StudyInfoDTO:
        return _dto(
            StudyInfoDTO,
            self.session()
            .execute(
                text(
                    f"""
                select
                    sd.id,
                    md.description as device,
                    ss.status,
                    sd.name as study,
                    sd.start_ts,
                    sd.end_ts
                from
                    {_prefix_} study_data sd
                    left join {_prefix_} study_status ss on sd.status_id = ss.id
                    left join {_prefix_} device md on sd.device_id = md.id
                where
                    sd.id = :study_id
            """
                ),
                {"study_id": study_id},
            )
            .first(),
        )


# DAO factory
class DAO:
    account: AccountDAO = AccountDAO()
    message: MessageDAO = MessageDAO()
    sec_sys: SecSysDAO = SecSysDAO()
    study: StudyDAO = StudyDAO()
