import pytest
from celery.result import AsyncResult
from datetime import datetime, timedelta
from bson import ObjectId
from unittest.mock import patch
from agentforge.tasks import master_scheduler, execute_event, send_notification

@pytest.mark.celery
def test_master_scheduler(celery_session_worker):
    result = master_scheduler.apply_async()
    result.wait()

    assert result.successful()

@pytest.mark.celery
def test_execute_event(celery_session_worker):
    event_id = str(ObjectId())

    result = execute_event.apply_async(args=[event_id])
    result.wait()

    assert result.successful()

@pytest.mark.celery
def test_send_notification(celery_session_worker):
    mock_session = MockSessionContainer()
    mock_event = {"event_name": "Test Event"}

    with patch("pywebpush.webpush") as mock_webpush:
        result = send_notification.apply_async(args=[mock_session, mock_event])
        result.wait()

        assert result.successful()

        mock_webpush.assert_called_once()

# Mock SessionContainer class for testing
class MockSessionContainer:
    def get_user_id(self):
        return "mock_user_id"
