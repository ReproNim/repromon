import logging.config

from sqlalchemy import text

from repromon_app.config import app_config, app_config_init, app_settings
from repromon_app.dao import DAO, BaseDAO
from repromon_app.db import db_init
from repromon_app.model import (BaseEntity, DataProviderEntity, DataProviderId,
                                DeviceEntity, MessageCategoryEntity,
                                MessageCategoryId, MessageLevelEntity,
                                MessageLevelId, RoleEntity, Rolename,
                                StudyStatusEntity, UserEntity)
from repromon_app.service import MessageService, SecSysService

logger = logging.getLogger(__name__)
logger.debug(f"name={__name__}")


def fill_tables_with_init_data():
    logger.debug("fill_tables_with_init_data()")
    dao: BaseDAO = DAO.account

    if dao.count(DataProviderEntity) == 0:
        logger.info("fill data_provider")
        o = DataProviderEntity(id=1, provider="ReproIn")
        dao.add(o)
        o = DataProviderEntity(id=2, provider="ReproStim")
        dao.add(o)
        o = DataProviderEntity(id=3, provider="ReproEvents")
        dao.add(o)
        o = DataProviderEntity(id=4, provider="PACS")
        dao.add(o)
        o = DataProviderEntity(id=5, provider="Noisseur")
        dao.add(o)
        o = DataProviderEntity(id=6, provider="DICOM/QA")
        dao.add(o)
        o = DataProviderEntity(id=7, provider="MRI")
        dao.add(o)
        dao.commit()
    else:
        logger.info("skip data_provider fill")

    if dao.count(DeviceEntity) == 0:
        logger.info("fill device")
        o = DeviceEntity(id=1, kind="MRI",
                         description="DBIC 3T Siemens Prisma MRI")
        dao.add(o)
        dao.commit()
    else:
        logger.info("skip device fill")

    if dao.count(MessageCategoryEntity) == 0:
        logger.info("fill message_category")
        o = MessageCategoryEntity(id=1, category="Feedback")
        dao.add(o)
        dao.commit()
    else:
        logger.info("skip message_category fill")

    if dao.count(MessageLevelEntity) == 0:
        logger.info("fill message_level")
        o = MessageLevelEntity(id=1, level="INFO")
        dao.add(o)
        o = MessageLevelEntity(id=2, level="WARNING")
        dao.add(o)
        o = MessageLevelEntity(id=3, level="ERROR")
        dao.add(o)
        dao.commit()
    else:
        logger.info("skip message_level fill")

    if dao.count(RoleEntity) == 0:
        logger.info("fill role")
        o = RoleEntity(id=1, rolename=Rolename.ADMIN,
                       description="Administrator")
        dao.add(o)
        o = RoleEntity(id=2, rolename=Rolename.DATA_COLLECTOR,
                       description="Data Collector")
        dao.add(o)
        o = RoleEntity(id=3, rolename=Rolename.MRI_OPERATOR,
                       description="MRI Operator")
        dao.add(o)
        o = RoleEntity(id=4, rolename=Rolename.PARTICIPANT,
                       description="Participant")
        dao.add(o)
        o = RoleEntity(id=5, rolename=Rolename.SYS_DATA_ENTRY,
                       description="System Data Entry")
        dao.add(o)
        o = RoleEntity(id=6, rolename=Rolename.TESTER,
                       description="Automatic System Tester")
        dao.add(o)
        dao.commit()
    else:
        logger.info("skip role fill")

    if dao.count(StudyStatusEntity) == 0:
        logger.info("fill study_status")
        o = StudyStatusEntity(id=100, status="New")
        dao.add(o)
        o = StudyStatusEntity(id=101, status="Collecting MRI Data")
        dao.add(o)
        o = StudyStatusEntity(id=190, status="Completed")
        dao.add(o)
        o = StudyStatusEntity(id=191, status="Failed")
        dao.add(o)
        o = StudyStatusEntity(id=200, status="Entering Participant Data")
        dao.add(o)
        o = StudyStatusEntity(id=300, status="Designing Sequences")
        dao.add(o)
        dao.commit()
    else:
        logger.info("skip study_status fill")

    if dao.count(UserEntity) == 0:
        logger.info("fill user")
        o = UserEntity(username="user1",
                       is_active='Y', is_system='N',
                       first_name='John', last_name='Smith',
                       email='user1@repromon.com',
                       phone='321')
        dao.add(o)
        o = UserEntity(username="user2",
                       is_active='Y', is_system='N',
                       first_name='Dave', last_name='Cooper',
                       email='user2@repromon.com',
                       phone='231')
        dao.add(o)
        o = UserEntity(username="user3",
                       is_active='Y', is_system='N',
                       first_name='Lucy', last_name='Nelson',
                       email='user3@repromon.com',
                       phone='111')
        dao.add(o)
        o = UserEntity(username="mriuser",
                       is_active='Y', is_system='N',
                       first_name='MRI', last_name='User',
                       description='MRI User'
                       )
        dao.add(o)
        o = UserEntity(username="admin",
                       is_active='Y', is_system='N',
                       first_name='Admin', last_name='Admin',
                       email='admin@repromon.com',
                       description='Administrator')
        dao.add(o)
        o = UserEntity(username="poweruser",
                       is_active='Y', is_system='N',
                       first_name='Power', last_name='User',
                       email='poweruser@repromon.com',
                       description='Power user')
        dao.add(o)
        o = UserEntity(username="noisseur",
                       is_active='Y', is_system='Y',
                       first_name='noisseur', last_name='noisseur',
                       description='System con/noisseur user')
        dao.add(o)
        o = UserEntity(username="reprostim",
                       is_active='Y', is_system='Y',
                       first_name='reprostim', last_name='reprostim',
                       description='ReproStim Screen Capture')
        dao.add(o)
        o = UserEntity(username="reproevt",
                       is_active='Y', is_system='Y',
                       first_name='reproevt', last_name='reproevt',
                       description='ReproEvents Capture')
        dao.add(o)
        o = UserEntity(username="dicomqa",
                       is_active='Y', is_system='Y',
                       first_name='dicomqa', last_name='dicomqa',
                       description='DICOMS/QA')
        dao.add(o)
        o = UserEntity(username="tester1",
                       is_active='Y', is_system='N',
                       first_name='Tester', last_name='1',
                       email='tester1@repromon.com',
                       description='Account for testing')
        dao.add(o)
        o = UserEntity(username="tester2",
                       is_active='Y', is_system='Y',
                       first_name='Tester', last_name='2',
                       email='tester2@repromon.com',
                       description='Account for testing')
        dao.add(o)
        o = UserEntity(username="tester3",
                       is_active='Y', is_system='N',
                       first_name='Tester', last_name='3',
                       email='tester3@repromon.com',
                       description='Account for testing')
        dao.add(o)
        dao.commit()

        sec_svc: SecSysService = SecSysService()
        # set initial default password admin
        pwd = app_settings().INITIAL_ADMIN_PASSWORD
        if pwd and len(pwd) > 0:
            logger.info("set initial admin password ***")
            sec_svc.set_user_password("admin", pwd)

        # set user roles
        logger.info("set user roles")
        sec_svc.set_user_roles("user1", [Rolename.DATA_COLLECTOR])
        sec_svc.set_user_roles("user2", [Rolename.MRI_OPERATOR])
        sec_svc.set_user_roles("user3", [Rolename.PARTICIPANT])
        sec_svc.set_user_roles("mriuser", [Rolename.DATA_COLLECTOR,
                                           Rolename.MRI_OPERATOR])
        sec_svc.set_user_roles("admin", [Rolename.ADMIN,
                                         Rolename.DATA_COLLECTOR])
        sec_svc.set_user_roles("poweruser", [Rolename.DATA_COLLECTOR,
                                             Rolename.PARTICIPANT,
                                             Rolename.MRI_OPERATOR,
                                             Rolename.SYS_DATA_ENTRY])
        sec_svc.set_user_roles("noisseur", [Rolename.SYS_DATA_ENTRY])
        sec_svc.set_user_roles("reprostim", [Rolename.SYS_DATA_ENTRY])
        sec_svc.set_user_roles("reproevt", [Rolename.SYS_DATA_ENTRY])
        sec_svc.set_user_roles("dicomqa", [Rolename.SYS_DATA_ENTRY])
        sec_svc.set_user_roles("tester1", [Rolename.DATA_COLLECTOR])
        sec_svc.set_user_roles("tester2", [Rolename.SYS_DATA_ENTRY])
        sec_svc.set_user_roles("tester3", [Rolename.DATA_COLLECTOR,
                                           Rolename.SYS_DATA_ENTRY])

        # set user devices
        logger.info("set user devices")
        sec_svc.set_user_devices("user1", ["MRI"])
        sec_svc.set_user_devices("user2", ["MRI"])
        sec_svc.set_user_devices("user3", ["MRI"])
        sec_svc.set_user_devices("mriuser", ["MRI"])
        sec_svc.set_user_devices("admin", ["MRI"])
        sec_svc.set_user_devices("poweruser", ["MRI"])
        sec_svc.set_user_devices("noisseur", ["MRI"])
        sec_svc.set_user_devices("reprostim", ["MRI"])
        sec_svc.set_user_devices("reproevt", ["MRI"])
        sec_svc.set_user_devices("dicomqa", ["MRI"])
        sec_svc.set_user_devices("tester1", ["MRI"])
        sec_svc.set_user_devices("tester2", ["MRI"])
        sec_svc.set_user_devices("tester3", ["MRI"])

        # generate API key for system accounts
        logger.info("generate API key for system accounts")
        sec_svc.renew_user_apikey("noisseur")
        sec_svc.renew_user_apikey("reprostim")
        sec_svc.renew_user_apikey("reproevt")
        sec_svc.renew_user_apikey("dicomqa")
        sec_svc.renew_user_apikey("tester1")
        sec_svc.renew_user_apikey("tester2")
        sec_svc.renew_user_apikey("tester3")

        msg_svc: MessageService = MessageService()
        msg_svc.send_message(
            "tester1", None, "Test Study Name",
            MessageCategoryId.FEEDBACK,
            MessageLevelId.INFO,
            1,
            DataProviderId.MRI,
            "Test message from setup_db tool",
            "{'foo': 321}"
        )
    else:
        logger.info("skip user fill")


def main():
    app_config_init()
    logger.debug("main()")
    db_init(app_config().db.dict())
    session = DAO.account.session()
    engine = session.get_bind()

    if BaseDAO.default_schema:
        session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {BaseDAO.default_schema};"))
        session.commit()

    BaseEntity.metadata.create_all(engine)

    fill_tables_with_init_data()
    logger.debug("done.")


if __name__ == "__main__":
    main()
