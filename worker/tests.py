import pytest

from faststream.rabbit import TestRabbitBroker, RabbitBroker
from main import create_task, start_task, get_task_state, get_state
from worker.const import Queue

broker: RabbitBroker = RabbitBroker("amqp://admin:admin@localhost:5672/")


@pytest.mark.asyncio
async def test_create_task():
    async with TestRabbitBroker(broker) as br:
        await br.publish(queue=Queue.CREATE)
        await create_task.wait_call(timeout=3)
        create_task.mock.assert_called_once_with()

    assert create_task.mock is None


@pytest.mark.asyncio
async def test_start_task():
    async with TestRabbitBroker(broker) as br:
        await br.publish({"task_id": 1}, queue=Queue.START)
        await start_task.wait_call(timeout=3)
        start_task.mock.assert_called_once_with({"task_id": 1})

    assert start_task.mock is None


@pytest.mark.asyncio
async def test_get_task_state():
    async with TestRabbitBroker(broker) as br:
        await br.publish({"task_id": 1}, queue=Queue.ONE_TASK)
        await get_task_state.wait_call(timeout=3)
        get_task_state.mock.assert_called_once_with({"task_id": 1})

    assert get_task_state.mock is None


@pytest.mark.asyncio
async def test_get_state():
    async with TestRabbitBroker(broker) as br:
        await br.publish(queue=Queue.ALL_TASK)
        await get_state.wait_call(timeout=3)
        get_state.mock.assert_called_once_with()

    assert get_state.mock is None
