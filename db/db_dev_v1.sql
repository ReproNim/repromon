-- export DDL
-- sqlite3 db_dev.sqlite3 '.schema' > db_dev.ddl

select * from user;
select * from role;
select * from sec_user_role;

-- update user set is_active='Y';


select
	u.username,
	u.id as user_id,
	u.first_name ,
	u.last_name,
	r.rolename
from
	user u, role r, sec_user_role ur
where
	u.id = ur.user_id and
	ur.role_id = r.id
 ;


select * from study_data where id=1;

--------------------------
-- show study header

select
	sd.id,
	d.description as device,
	json_extract(sd.info, '$.participant') as participant,
	json_extract(sd.info, '$.data_collector') as data_collector,
	json_extract(sd.info, '$.mri_operator') as mri_operator,
	ss.status,
	sd.description as study,
	sd.start_ts,
	sd.end_ts
from
	study_data sd
	left join study_status ss on sd.status_id = ss.id
	left join device d on sd.device_id = d.id
where
	sd.id = 1
;

-------------------------
-- show message log

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
	ml.study_id = 1
order by ml.created_on asc
;

