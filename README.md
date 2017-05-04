
### Requirements
- `python3`
- `ffmpeg` for ffii2vid.py

### ffii2vid.py

Converts ffii file to video. Frame rate defaults to `15/4`. 

#### Usage:
```
python ffii2vid.py INPUT OUTPUT [frame rate]
```
#### Example:
Convert train1.ffii into webm format, at frame rate of 5 fps.
```
python ffii2vid.py train1.ffii train1.webm 5
```

### ffdd2csv.py

Extracts frame-by-frame motion index from ffdd file. 

#### Usage:
```
python ffdd2csv.py INPUT OUTPUT
```
If `OUTPUT` is an existing directory, ffdd2csv.py exports the data for each animal into
a separate csv file in the `OUTPUT` directory.

If `OUTPUT` ends with `.pkl` extension, output is a python pickle of a list of
dictionaries, where each dictionary represents data from a single animal.

