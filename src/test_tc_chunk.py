import sys
from trt_calculator.formatting import format_string_as_timecode

print(format_string_as_timecode(sys.argv[1], 24))