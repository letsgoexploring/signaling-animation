import os

# files = os.listdir(os.getcwd())
# for f in files:
# 	if f != 'runAll.py' and f.endswith('py'):
# 		print(f)
# 		os.system("python "+f)

# Equilibria with both types stacked
os.system("python "+"signalingAnimationSeparating.py")
os.system("python "+"signalingAnimationPooling.py")

# Pooling figures by type:
os.system("python "+"signalingAnimationPoolingHighType.py")
os.system("python "+"signalingAnimationPoolingLowType.py")

# Separating figures by type:
os.system("python "+"signalingAnimationSeparatingHighType.py")
os.system("python "+"signalingAnimationSeparatingLowType.py")