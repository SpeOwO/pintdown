import os
import time
import random
import re
import logging
import datetime
from urllib.parse import urlparse

logger = logging.getLogger("pintdown.utils")

def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing or replacing invalid characters.
    This helps avoid issues on Windows and other file systems.
    """
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def save_file(file: bytes, save_dir: str, filename: str):
    """
    Save binary data (e.g. image) to the specified directory and filename.
    Ensures directory exists, and filename is valid.
    """
    try:
        # Normalize the directory path (handles mixed slashes)
        save_dir = os.path.normpath(save_dir)

        # Create the directory if it does not exist
        os.makedirs(save_dir, exist_ok=True)

        if not filename:
            raise ValueError("Filename must be provided")

        # Sanitize filename to prevent OS-level issues
        filename = sanitize_filename(filename)

        # Full path to save the file
        save_path = os.path.join(save_dir, filename)

        # Write the binary content to file
        with open(save_path, "wb") as f:
            f.write(file)

        logger.debug(f"Saved file: {save_path}")

    except Exception as e:
        logger.error(f"Save failed (path: {save_path}) - {e}")
        raise Exception("Save Error") from e

def sleep():
    """
    Sleep for a random duration between 1.0 and 1.5 seconds.
    Helps avoid being flagged as a bot during repeated requests.
    """
    duration = random.uniform(0.5, 1.0)
    logger.debug(f"Sleeping for {duration:.2f} seconds")
    time.sleep(duration)

class NameFunction():
    # 1. �ϰ� ��ȣ ���
    @staticmethod
    def name_fn_number_only(url, idx):
        return f"pin_{idx+1}.jpg"  # 1���� ����

    # 2. ���� �̸�/ID ����
    @staticmethod
    def name_fn_original_id(url, idx):
        if not url:
            return f"pin_{idx+1}.jpg"
        # URL ��ο��� ������ �κ�(���ϸ� ����)
        path = urlparse(url).path
        filename = path.split("/")[-1]
        # �����ϰ� ���ϸ� ����
        filename = re.sub(r'[\\/*?:"<>|]', "_", filename)
        return filename

    # 3. ��¥/�ð� ��� �̸�
    @staticmethod
    def name_fn_datetime(url, idx):
        now = datetime.datetime.now()
        timestr = now.strftime("%Y%m%d_%H%M%S")
        return f"{timestr}_{idx+1}.jpg"

    # 4. Ŀ���� ���λ� + ��ȣ ����
    @staticmethod
    def name_fn_prefix_number(url, idx, prefix="pin"):
        return f"{prefix}_{idx+1}.jpg"

    # 5. ȥ���� (ID + ��ȣ)
    @staticmethod
    def name_fn_id_number(url, idx):
        if not url:
            return f"pin_{idx+1}.jpg"
        path = urlparse(url).path
        filename = path.split("/")[-1]
        # ���ϸ��� Ȯ���� ����, �� 7�ڸ��� ���� (���ϴ� ��ŭ ���� ����)
        basename = filename.split(".")[0][:7]
        return f"pin_{basename}_{idx+1}.jpg"
