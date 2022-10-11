import os
import json
import sys
import shutil
import schedule
import time
from datetime import datetime
from pprint import pprint


# TODO: if needed to access paths outside of the directory of the script, need to construct relative path and absolute path,
#  i.e: abs path, main_dir = os.path.abspath(os.path.dirname(__file__))
#       relative path, some_file = os.path.join(this_dir, 'path/to/the/file', 'file.extension'),
#       as it was not a requirement of the task, I chose not to implement it, but just wanted to mention  that it is possible.
#       at this moment the script need to be in the shared/mutual directory of both the source and destination folder


def folder_sync(src: str = None, dest: str = None, log_path: str = None):
    if not (src, dest, log_path):
        message = {"Error": "No argements passed!"}
    else:
        # check if the passed path arguments exist or not
        if os.path.isdir(src) and os.path.isdir(dest):
            src_file_list = os.listdir(src)
            dest_file_list = os.listdir(dest)

            # checks if log path exixts or not. If not, creates a file at path
            if not os.path.isfile(log_path):
                open(log_path, "a+")

            # check if new file has been created in source, on the first run, it will count all the files found as newly created files
            with open('creation_track.json', 'r') as f:
                data_track = json.load(f)

            # copy all files that exist in src but not in dest
            src_file_count = 0
            new_file_count = 0
            new_created_files = []
            copy_count = 0
            copy_list = []
            for src_file in src_file_list:
                src_file_count += 1
                # check if new file has been created or not
                if src_file not in data_track["prev_files_list"]:
                    data_track["prev_files_list"].append(src_file)
                    new_created_files.append(src_file)
                # check if the file already exists in destination
                if src_file in dest_file_list:
                    pass
                else:
                    copy_count += 1
                    copy_list.append(src_file)
                    buffer_path = f"src/{src_file}"
                    shutil.copy(buffer_path, dest)

            if data_track["prev_files_count"] < src_file_count:
                new_file_count = src_file_count - data_track["prev_files_count"]
                data_track["prev_files_count"] = src_file_count

            # update tracking json
            with open("creation_track.json", "w") as updateJson:
                json.dump(data_track, updateJson)

            # delete file in dest that does not exist in src anymore
            del_count = 0
            del_list = []
            for dest_file in dest_file_list:
                if dest_file not in src_file_list:
                    del_count += 1
                    del_list.append(dest_file)
                    buffer_path = f"dest/{dest_file}"
                    os.remove(buffer_path)

            # aggregate all the actions that took place to add to log file and to print in CLI
            message = {
                "timestamp": datetime.timestamp(datetime.now()),
                f"number of new files in {src}": new_file_count,
                f"new files created in {src}": new_created_files,
                f"files copied to {dest}": copy_count,
                "copied files list": copy_list,
                f"files deleted from {dest}": del_count,
                "deleted file list": del_list
            }

        else:
            message = {"Error": "One or more given paths does not exist!"}

    with open(log_path, "a") as logfile:
        logfile.write(str(message) + "," + "\n")

    pprint(message)


if len(sys.argv) != 5:
    pprint({"Error": "Invalid argements passed!"})

else:
    src = sys.argv[1]
    dest = sys.argv[2]
    log_path = sys.argv[3]
    sync_period = int(sys.argv[4])


schedule.every(sync_period).seconds.do(lambda: folder_sync(src=src, dest=dest, log_path=log_path))

while True:
    schedule.run_pending()
    time.sleep(5)
