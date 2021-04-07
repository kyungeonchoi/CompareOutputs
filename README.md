### Overview
- Compare two output directories from TRExFitter action `n`
- Subdirectory `Histograms` and `Systematics` are compared
- `Histograms`: compare all root files and its 1-D histograms
- `Systematics`: compare png file sizes

### Usage
```
from compare_TRExFitter_outputs import compare_root
compare_root('<folder1>', '<folder2>')
```

- Returns number of differences 
- generates a log file `comparison_result_<folder1>_and_<folder2>.log`