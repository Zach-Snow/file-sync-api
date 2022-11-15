# file-sync-application

- have to install the packages from requirements.txt first
```commandline
pip3 install -r requirements.txt
```

- For the initial run, remember to replace the "creation_track.json" file to below json values,

```json
{"prev_files_count": 0, 
  "prev_files_list": []}
```

- when running the script it should be run as
```commandline
python3 folder_sync.py "source path" "destination path" "log file path" 60
```
- The paths should be contained within quotes cause space in the path will cause issues.
- the time unit here is seconds and is needed for the interval
- The script must be in a mutual folder that both source and destination share. I have added two mock folders that are being used as source and destination in the repo. More information is given on the folder_sync module.
