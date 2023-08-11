INSERT INTO `gaea_framework`.`finlab_case_prev_condition`
(
`prev_case_id`,
`prev_task_type`,
`prev_name`,
`prev_description`,
`prev_flag`,
`prev_setup_type`,
`prev_api_address`,
`prev_api_method`,
`prev_api_params`,
`prev_api_header`,
`prev_api_expression`,
`prev_sql_statement`,
`prev_sql_params`,
`prev_sql_database`,
`prev_sql_expression`,
`prev_expression`,
`prev_params`,
`prev_except_expression`,
`prev_except_value`
)
select `prev_case_id`,
case when prev_case_id = 0 then 'task'  when prev_case_id = -1 then  'msg' else 'common' end as prev_task_type,
`prev_name`,
`prev_description`,
`prev_flag`,
'setup' as `prev_setup_type`,
`prev_api_address`,
`prev_api_method`,
`prev_api_params`,
`prev_api_header`,
`prev_api_expression`,
case when prev_case_id =0 then 'select * from task where task_type ='+prev_flag+'task_order_no =%s' else
'select * from sendmsg where sendmsg_type ='+prev_flag+'send_order_no=%s' end as `prev_sql_statement`,
'{"item_no":""}' as `prev_sql_params`,
'#{env_name}' as `prev_sql_database`,
'{"$.request.data.asset.item_no":"$.item_no"}' as `prev_sql_expression`,
`prev_expression`,
`prev_params`,
`prev_except_expression`,
`prev_except_value`
from gaea_test.finlab_case_prev_condition where prev_case_id in (select case_id from gaea_test.finlab_cases where case_from_system='qbus');



INSERT INTO gaea_framework.`finlab_cases_init` (`case_init_case_id`, `case_init_type`, `case_init_name`, `case_init_description`, `case_init_api_address`
	, `case_init_api_method`, `case_init_api_params`, `case_init_api_header`, `case_init_api_expression`, `case_init_sql`
	, `case_init_sql_params`, `case_init_sql_expression`, `case_init_sql_database`, `case_init_indate`, `case_init_inuser`
	, `case_init_lastuser`, `case_init_lastdate`)

	SELECT 0 AS case_init_case_id, 'setup' AS case_init_type, case_init_name, case_init_description, case_init_api_address
		, case_init_api_method, case_init_api_params, case_init_api_header, case_init_api_expression, case_init_sql
		, case_init_sql_params, case_init_sql_expression, case_init_sql_database, `case_init_indate`, `case_init_inuser`
		, `case_init_lastuser`, `case_init_lastdate`
	FROM gaea_test.finlab_cases_init
	WHERE case_init_id IN (104, 105)



INSERT INTO `gaea_framework`.`finlab_cases`
(
`case_exec_priority`,
`case_from_system`,
`case_name`,
`case_description`,
`case_category`,
`case_executor`,
`case_exec_group`,
`case_exec_group_priority`,
`case_api_address`,
`case_api_method`,
`case_api_params`,
`case_api_header`,
`case_check_method`,
`case_except_value`,
`case_sql_actual_statement`,
`case_sql_actual_database`,
`case_sql_params`,
`case_sql_reference_name`,
`case_is_exec`,
`case_mock_flag`,
`case_next_msg`,
`case_next_task`,
`case_replace_expression`,
`case_init_id`,
`case_wait_time`,
`case_vars_name`,
`case_author`,
`case_in_date`,
`case_in_user`,
`case_last_user`,
`case_last_date`)
select `case_exec_priority`,
`case_from_system`,
`case_name`,
`case_description`,
 `case_category`,
case when case_exec_group<>'' then 'group' else 'common' end as`case_executor`,
`case_exec_group`,
case when case_exec_group<>'' then case_exec_group_priority else NULL end as  `case_exec_group_priority`,
`case_api_address`,
`case_api_method`,
`case_api_params`,
`case_api_header`,
`case_check_method`,
`case_except_value`,
`case_sql_actual_statement`,
`case_sql_actual_database`,
`case_sql_params`,
case_id as `case_sql_reference_name`,
`case_is_exec`,
'N' as `case_mock_flag`,
`case_next_msg`,
`case_next_task`,
`case_replace_expression`,
`case_init_id`,
`case_wait_time`,
'' as `case_vars_name`,
`case_author`,
`case_in_date`,
`case_in_user`,
`case_last_user`,
`case_last_date` from `gaea_test`.`finlab_cases` where case_from_system='data_proxy';


