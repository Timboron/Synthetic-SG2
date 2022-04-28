import shutil
import os

inpath = "/data/trieber/syn_datasets/sg2idbn_aligned"
outpath = "/data/trieber/syn_datasets/sg2idbn_aligned_prog"
identity = "000000"
image = "000000.png"
shutil.copyfile(os.path.join(inpath, identity, image), os.path.join(outpath, identity, image))