import hashlib
import hmac


class UserIdHasher:
    """
    Create confirmation code using user id and HMAC SHA-256 algorithm.

    - encode(user_id: int) -> str:
    Create confirmation code using user id as message.

    - check_code(current_value: str, user_id: int) -> bool:
    Check that the given token is corresponded to the user id.
    """

    def __init__(self) -> None:
        self.key = 'user_id'

    def encode(self, user_id: int) -> str:
        """Create confirmation code."""
        return hmac.new(
            bytes(self.key, 'utf-8'),
            msg=bytes(str(user_id), 'utf-8'),
            digestmod=hashlib.sha256,
        ).hexdigest()

    def check_code(self, current_value: str, user_id: int) -> bool:
        """Check confirmation code."""
        print(self.encode(user_id))
        return self.encode(user_id) == current_value
