import pytest
from unittest.mock import patch, MagicMock
from api.quant.scheduler import QuantScheduler

@patch('api.quant.scheduler.BackgroundScheduler')
@patch('api.quant.scheduler.QuantService')
def test_start_scheduler(MockQuantService, MockBackgroundScheduler):
    
    mock_scheduler = MockBackgroundScheduler.return_value
    mock_quant_service = MockQuantService.return_value

    # Create an instance of QuantScheduler
    scheduler = QuantScheduler()

    # Ensure the scheduler is not running initially
    mock_scheduler.running = False

    # Call the start method
    scheduler.start()

    # Check if add_job was called with the correct parameters
    mock_scheduler.add_job.assert_called_once_with(
        mock_quant_service.check_and_notify, 'interval', minutes=30
    )

    # Check if the scheduler was started
    mock_scheduler.start.assert_called_once()