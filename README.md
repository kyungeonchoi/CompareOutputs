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

generates a log file `comparison_result.log`.