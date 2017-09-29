import json

from behave import then


@then(u'{created} celery tasks of type start_scan are in the broker')
def step_impl(context, created):
    created = int(created)

    # assert that only 1 task in the celery queue
    task_found = context.redis_db.llen('celery')
    assert task_found == created

    if created > 0:
        # get the task
        item = context.redis_db.lpop('celery')
        item = json.loads(item)
        headers = item.get('headers')

        # asserts the correct task is in the list
        assert headers.get('task') == 'start_scan'
