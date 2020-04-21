# IDA Trace Analysis Helper

[TOC]

## How Install

`pip install ida_trace_analysis_helper`

python >= 3.7

## How Use

```python
from ida_trace_analysis_helper import TraceFileAnalysisHelper


test_file_path = "../tests/raw_trace_005.log"
analysis_helper = TraceFileAnalysisHelper(test_file_path)
analysis_helper.begin_with(begin_line_index, end_line_index)

```

then output the track registers.

## TODO

- track registers to file
- comment the track info to the raw file
- extract the track instructions to unicorn and run 
- if is from like `LDURB           W10, [X29,#-0x94]` track
