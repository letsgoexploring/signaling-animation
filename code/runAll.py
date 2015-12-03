import os

files = os.listdir(os.getcwd())
for f in files:
	if f != 'runAll.py' and f.endswith('py'):
		print(f)
		os.system("python "+f)