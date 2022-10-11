# file-sync-api

- have to install the packages from requirements.txt first
```commandline
pip3 install -r requirements.txt
```

- when running the script it should be run as
```commandline
python3 folder_sync.py "source path" "destination path" "log file path" 60
```
- The paths should be contained within quotes cause space in the path will cause issues.
- the time unit here is seconds and is needed for the interval
- The script much be in a mutual folder that both source and destination share. I have added two mock folders that are being used as source and destination in the repo. More information is given on the folder_sync module.