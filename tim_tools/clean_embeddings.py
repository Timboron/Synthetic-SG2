import os
import click
import shutil

@click.command()
@click.pass_context
@click.option('--imagepath', 'imgpathname', required=True)
@click.option('--embpath', 'embpathname', required=True)
def generate_match(ctx: click.Context, imgpathname: str, embpathname: str):

    identities = os.listdir(embpathname)

    for identity in identities:
        if os.path.exists(os.path.join(imgpathname, identity)):
            embeddings = os.listdir(os.path.join(embpathname, identity))
            images = [x[:-4] for x in os.listdir(os.path.join(imgpathname, identity))]
            for emb in embeddings:
                if emb[:-4] not in images:
                    os.remove(os.path.join(embpathname, identity, emb))
        else:
            shutil.rmtree(os.path.join(embpathname, identity))


if __name__ == "__main__":
    generate_match()