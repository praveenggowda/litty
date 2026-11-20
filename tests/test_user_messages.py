from src.errors import FailureCategory
from src.user_messages import FRIENDLY_MESSAGES


class TestUserMessages:
    def test_every_failure_category_has_a_friendly_message(self):
        assert set(FRIENDLY_MESSAGES) == set(FailureCategory)
        assert all(message.strip() for message in FRIENDLY_MESSAGES.values())
