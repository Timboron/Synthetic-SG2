import numpy as np
import json
from tqdm import tqdm
import os

import click


@click.command()
@click.pass_context
@click.option('--path', 'pathname', required=True)
@click.option('--datapath', 'datapathname', required=True)
@click.option('--rate', 'cleaningrate', required=True)
def generate_match(ctx: click.Context, pathname: str, datapathname: str, cleaningrate: str):
    # delete images
    with open(pathname) as outfile:
        data = json.load(outfile)
    rate = float(cleaningrate)
    del_amount = round(len(data) * rate)
    print(del_amount)
    del_image_paths = list(data.keys())[:del_amount]
    print(len(del_image_paths))
    for image_path in del_image_paths:
        os.remove(os.path.join(datapathname, image_path + ".png"))

    # delete empty folders
    identities = os.listdir(pathname)
    empty_labels = []
    one_labels = []

    for identity in identities:
        images = os.listdir(os.path.join(pathname, identity))
        if len(images) == 0:
            empty_labels.append(identity)
        if len(images) == 1:
            one_labels.append(identity)
        if len(images) < 200:
            print(len(images))

    print("empty:", len(empty_labels))
    print("one:", len(one_labels))

if __name__ == "__main__":
    generate_match()