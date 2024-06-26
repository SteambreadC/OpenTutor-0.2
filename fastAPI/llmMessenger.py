import os
import time


def predict(paramA, paramB):
    time.sleep(1)
    process_files(paramA, paramB)
    return "predict result :D"


def process_files(csPath, files):
    processed_files = []
    maxFiles = 8
    # Make dictionary
    os.makedirs(os.path.join(csPath, "to_download"), exist_ok=True)

    for file in files:
        if maxFiles > 0:
            # 模拟处理文件，例如复制到 processed 文件夹
            processed_filename = os.path.join(csPath, "to_download", os.path.basename(file))
            with open(file, 'rb') as f_src, open(processed_filename, 'wb') as f_dst:
                f_dst.write(f_src.read())
            processed_files.append(processed_filename)
            maxFiles -= 1
    return processed_files
