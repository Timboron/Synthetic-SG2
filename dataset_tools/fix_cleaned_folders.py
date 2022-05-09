import os
import click
import shutil

@click.command()
@click.pass_context
@click.option('--path', 'pathname', required=True)
def generate_match(ctx: click.Context, pathname: str):

    identities = os.listdir(pathname)
    to_delete = []
    print("original folders:", len(os.listdir(pathname)))

    for identity in identities:
        images = os.listdir(os.path.join(pathname, identity))
        if len(images) < 2:
            to_delete.append(identity)

    for identity in to_delete:
        shutil.rmtree(os.path.join(pathname, identity))

    print("remaining folders:", len(os.listdir(pathname)))


if __name__ == "__main__":
    generate_match()