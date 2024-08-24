import os, shutil, time
from subprocess import getoutput
from pathlib import Path

DEBUG = False
def main():
    scan_bin = Path("eval.exe")
    if scan_bin.exists():
        os.remove(scan_bin)
    build_cmd = "cargo fmt && cargo build"
    if not DEBUG:
        build_cmd += " -r"
    print(getoutput(build_cmd))
    if DEBUG:
        t = "debug"
    else:
        t = "release"
    shutil.copy(Path("target/{}/atcoder.exe".format(t)), scan_bin)
    assert(scan_bin.exists())
    score_sum = 0
    score_norm = 0
    for i in range(100):
        cmd = str(scan_bin)
        #cmd = "python sample/sample_submission.py"
        cmd += "< tools/in/{0:04d}.txt > tools/out/{0:04d}.txt".format(i, i)
        t0 = time.time()
        ret = getoutput(cmd)
        t1 = time.time()
        score = int(ret)
        score_sum += score
        score_norm += 1
        print(i, score, "{}ms".format(int(1000 * (t1 - t0))), "ave", score_sum / score_norm)
    print("ave", score_sum / score_norm)

if __name__ == "__main__":
    main()