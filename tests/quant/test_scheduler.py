import pytest
from unittest.mock import patch
from api.quant.scheduler import QuantScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

@patch('api.quant.scheduler.BackgroundScheduler')
def test_start_scheduler(MockBackgroundScheduler):
    
    mock_scheduler = MockBackgroundScheduler.return_value

    # Create an instance of QuantScheduler
    scheduler = QuantScheduler()

    # Ensure the scheduler is not running initially
    mock_scheduler.running = False

    # Call the start method
    scheduler.start()

    # 메서드 호출 확인
    mock_scheduler.add_job.assert_called_once()
    
    # 호출 인자 확인
    call_args = mock_scheduler.add_job.call_args[0]
    call_kwargs = mock_scheduler.add_job.call_args[1]
    
    assert call_args[0] == scheduler._run_check_and_notify
    assert isinstance(call_kwargs['trigger'], CronTrigger)
        # CronTrigger의 필드를 문자열로 변환하여 확인
    cron_fields = str(call_kwargs['trigger'])
    assert "hour='22'" in cron_fields
    assert "minute='30'" in cron_fields
    assert call_kwargs['timezone'] == timezone('Asia/Seoul')

    # Check if the scheduler was started
    mock_scheduler.start.assert_called_once()