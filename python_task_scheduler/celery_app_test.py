from celery_task_scheduler_test import config_celery_scheduler, prepare_celery_tasks

celery_app = config_celery_scheduler()
prepare_celery_tasks()
