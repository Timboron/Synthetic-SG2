import numpy as np
import json
from tqdm import tqdm
import os

import click

def similarity(emb0, emb1):
    if emb0.ndim < 2 or emb1.ndim < 2:
        print("ERROR")
        print(emb0, emb1)
        return []
    assert (emb0.shape[0] == emb1.shape[0])
    assert (emb0.shape[1] == emb1.shape[1])
    dot = np.sum(np.multiply(emb0, emb1), axis=1)
    norm = np.linalg.norm(emb0, axis=1) * np.linalg.norm(emb1, axis=1)
    sim = np.clip(dot / norm, -1., 1.)
    return sim


@click.command()
@click.pass_context
@click.option('--path', 'pathname', required=True)
@click.option('--datapath', 'datapathname', required=True)
@click.option('--rate', 'cleaningrate', required=True)
def generate_match(ctx: click.Context, pathname: str, datapathname: str, cleaningrate: str):
    with open(pathname) as outfile:
        data = json.load(outfile)
    rate = float(cleaningrate)
    del_amount = round(len(data) * rate)
    print(del_amount)
    del_image_paths = data.keys()[:del_amount]
    print(len(del_image_paths))
    return
    for image_path in del_image_paths:
        os.remove(os.path.join(datapathname, image_path + ".png"))

if __name__ == "__main__":
    generate_match()