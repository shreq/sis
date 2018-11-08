import subprocess

for i in '1234':
    subprocess.call('python main.py astr manh ./../../puzzlegen/4x4_02_0000' + i + '.txt ./output/stop4x4_02_0000' + i + '.txt ./output/stats4x4_02_0000' + i + '.txt', shell=True)
