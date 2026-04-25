import time
from instagrapi import Client
from instagrapi.exceptions import RateLimitError


class Uploader:
    def __init__(self, username: str, password: str):
        self._client = Client()
        try:
            self._client.login(username, password)
        except Exception as e:
            raise RuntimeError(f"Login failed: {e}")

    def upload_photo(self, filepath: str) -> bool:
        try:
            self._client.photo_upload(filepath, caption="")
            return True
        except RateLimitError:
            print(f"  Rate limit hit on {filepath}, waiting 60s and retrying...")
            time.sleep(60)
            try:
                self._client.photo_upload(filepath, caption="")
                return True
            except Exception as e:
                print(f"  Retry failed for {filepath}: {e}")
                return False
        except Exception as e:
            print(f"  Upload failed for {filepath}: {e}")
            return False

