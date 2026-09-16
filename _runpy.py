import subprocess, os
os.chdir(r'E:\Cecillia2011-04\总经办助理 20190819\营运部\门店报表\.workbuddy\github_pages\bake-ops')
p = subprocess.run(['git', 'ls-remote', 'origin', 'HEAD'], capture_output=True, text=True, timeout=90)
open(r'E:\Cecillia2011-04\总经办助理 20190819\营运部\门店报表\.workbuddy\github_pages\bake-ops\_push_log.txt', 'w', encoding='utf-8').write(f'exit={p.returncode}\nSTDOUT:{p.stdout}\nSTDERR:{p.stderr}')
