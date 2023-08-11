import time
from biztest.config.dcs.xxljob_config import job_group_biz
from biztest.function.dcs.database_biz import get_task_close_biz, update_task_close_biz, update_task_at_biz
from biztest.util.xxl_job.xxl_job import XxlJob


# 执行biz的task，主要是放款的
def run_biz_tasks(env_test, task_type, item_no):
    for ii in range(0, 10):
        time.sleep(5)
        # step1 检查task的执行情况
        biz_tasks = get_task_close_biz(task_type, item_no)
        if biz_tasks:
            #time.sleep(60)
            # step2 关闭多余的task，以免task又一直running
            update_task_close_biz(item_no)
            # step3 修改本次task的执行时间，使其能被正确执行
            update_task_at_biz(task_type, item_no)
            # step4 由xxljob去执行task
            run_biz_job(env_test, "", "task")
        else:
            break


# 执行biz的job，biz的job没有 handle
def run_biz_job(env_test, job_params, job_type):
    biz_job = XxlJob(job_group_biz["biz" + env_test]["group_id"], "", password="123456", xxl_job_type="xxl_job_k8s")
    biz_job.trigger_job_for_id(job_group_biz["biz" + env_test][job_type + "_job_id"], job_params)




