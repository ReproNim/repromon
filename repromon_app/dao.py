import logging

from sqlalchemy.sql import text

from repromon_app.model import (BaseDTO, DataProviderEntity,
                                MessageLevelEntity, MessageLogEntity,
                                MessageLogInfoDTO, RoleEntity, RoleInfoDTO,
                                StudyDataEntity, StudyInfoDTO, UserInfoDTO)

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


class BaseDAO:
    """Base class for all DAO objects"""

    default_session = None

    def __init__(self):
        pass

    def add(self, o: BaseDTO):
        return self.session().add(o)

    def commit(self):
        self.session().commit()

    def flush(self):
        self.session().flush()

    def session(self):
        return BaseDAO.default_session


# User, role account DAO
class AccountDAO(BaseDAO):
    def __init__(self):
        pass

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
                    """
                select
                    id,
                    rolename,
                    description
                from
                    role
            """
                )
            )
            .all(),
        )

    def get_user_info(self, username: str) -> UserInfoDTO:
        return _dto(
            UserInfoDTO,
            self.session()
            .execute(
                text(
                    """
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
                ),
                {"username": username},
            )
            .first(),
        )


# Message system DAO
class MessageDAO(BaseDAO):
    def __init__(self):
        pass

    def get_data_providers(self) -> list[DataProviderEntity]:
        return self.session().query(DataProviderEntity).all()

    def get_message_levels(self) -> list[MessageLevelEntity]:
        return self.session().query(MessageLevelEntity).all()

    def get_message_log_infos(self, study_id: int) -> list[MessageLogInfoDTO]:
        return _list_dto(
            MessageLogInfoDTO,
            self.session()
            .execute(
                text(
                    """
                select
                    ml.id,
                    ml.study_id,
                    ml.study_name as study,
                    time(ml.created_on) as time,
                    ml.created_on as ts,
                    ml.event_ts,
                    ml.processing_ts,
                    mc.category,
                    ss.status,
                    ll.level,
                    ml.device_id,
                    dv.kind as device,
                    dp.provider,
                    ml.description
                from
                    message_log ml
                    left join message_category mc on ml.category_id = mc.id
                    left join study_status ss on ml.status_id = ss.id
                    left join message_level ll on ml.level_id = ll.id
                    left join device dv on ml.device_id = dv.id
                    left join data_provider dp on ml.provider_id = dp.id
                where
                    (:study_id is null or ml.study_id = :study_id) and
                    ml.is_visible = 'Y'
                order by ml.event_ts, ml.created_on asc
                """
                ),
                {"study_id": study_id},
            )
            .all(),
        )

    def get_message_log_info(self, message_id: int) -> MessageLogInfoDTO:
        return _dto(
            MessageLogInfoDTO,
            self.session()
            .execute(
                text(
                    """
                select
                    ml.id,
                    ml.study_id,
                    ml.study_name as study,
                    time(ml.created_on) as time,
                    ml.created_on as ts,
                    ml.event_ts,
                    ml.processing_ts,
                    mc.category,
                    ss.status,
                    ll.level,
                    ml.device_id,
                    dv.kind as device,
                    dp.provider,
                    ml.description
                from
                    message_log ml
                    left join message_category mc on ml.category_id = mc.id
                    left join study_status ss on ml.status_id = ss.id
                    left join message_level ll on ml.level_id = ll.id
                    left join device dv on ml.device_id = dv.id
                    left join data_provider dp on ml.provider_id = dp.id
                where
                    ml.id = :message_id
                """
                ),
                {"message_id": message_id},
            )
            .first(),
        )

    def update_message_log_visibility(self, study_id: int,
                                      is_visible: str,
                                      levels: list[int]) -> int:
        return self.session().query(MessageLogEntity).filter(
            MessageLogEntity.study_id == study_id,
            MessageLogEntity.level_id.in_(levels)
        ).update(
            {
                MessageLogEntity.is_visible: is_visible
            },
            synchronize_session=False
        )


# Security system DAO
class SecSysDAO(BaseDAO):
    def __init__(self):
        pass

    def get_device_id_by_username(self, username: str) -> list[str]:
        return _list_scalar(
            int,
            self.session()
            .execute(
                text(
                    """
                select
                    ud.device_id
                from
                    user u, sec_user_device ud
                where
                    u.username = :username and
                    u.id = ud.user_id
            """
                ),
                {"username": username},
            )
            .all(),
        )

    def get_rolename_by_username(self, username: str) -> list[str]:
        return _list_scalar(
            str,
            self.session()
            .execute(
                text(
                    """
                select
                    r.rolename
                from
                    user u, role r, sec_user_role ur
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
                    """
                select
                    sd.id,
                    md.description as device,
                    ss.status,
                    sd.name as study,
                    sd.start_ts,
                    sd.end_ts
                from
                    study_data sd
                    left join study_status ss on sd.status_id = ss.id
                    left join device md on sd.device_id = md.id
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
