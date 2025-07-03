import os

def save_file(file, save_dir: str, filename: str):
    if not filename:
        filename = os.path.basename(url.split("?")[0])  # remove query
    save_path = os.path.join(save_dir, filename)
    try:
        with open(save_path, "wb") as f:
            f.write(file)
    except Exception as e:
        print("error occurs", e)