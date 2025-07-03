import os

def save_file(file, save_dir: str, filename: str):
    if not filename:
        filename = os.path.basename(url.split("?")[0])  # 쿼리 제거
    save_path = os.path.join(save_dir, filename)
    try:
        with open(save_path, "wb") as f:
            f.write(file)
    except Exception as e:
        print("오류 발생:", e)