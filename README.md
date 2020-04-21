# IDA Trace Analysis Helper

从指定行开始回溯使用到的寄存器，从而得到计算过程。

## 安装

`pip install ida_trace_analysis_helper`

python >= 3.7

## 使用

```python
from ida_trace_analysis_helper import TraceFileAnalysisHelper


test_file_path = "../tests/raw_trace_005.log"
analysis_helper = TraceFileAnalysisHelper(test_file_path)
analysis_helper.begin_with(begin_line_index, end_line_index)

```

## TODO

- 将跟踪到的指令保存到文件中
- 生成指令集合，并让unicorn运行计算加密内容
- 如果指令为`LDURB           W10, [X29,#-0x94]` 应该再继续跟踪
