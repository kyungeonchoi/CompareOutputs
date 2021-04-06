### Overview
- Compare two output directories from TRExFitter action `n`
- Subdirectory `Histograms` and `Systematics` are compared
- `Histograms`: compare all root files and its 1-D histograms
- `Systematics`: compare png file sizes

### Usage
```
python compare_root.py <folder1> <folder2>
```

generates a log file `comparison_result.log`.