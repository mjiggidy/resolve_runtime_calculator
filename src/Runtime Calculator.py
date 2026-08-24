import sys, logging



try:
	from resolvecommon.session import bmd, resolve, fusion
except ImportError as e:
	print("Cannot find the Davinci Resolve API.  Please ensure Davinci Resolve Studio is installed and operational.", file=sys.stderr)
	sys.exit(1)

if not resolve:
	print("Cannot connect to Davinci Resolve Studio.  Please ensure it is running, and has scripting enabled.", file=sys.stderr)
	sys.exit(2)

if not fusion:
	print("Cannot connect to Fusion.", file=sys.stderr)
	sys.exit(3)	

if __name__ == "__main__":

	from trt_calculator.main import main
	main()