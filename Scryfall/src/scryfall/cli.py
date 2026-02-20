import typer

from scryfall.scryfall import scryfall


app = typer.Typer()
app.command()(scryfall)


if __name__ == "__main__":
    app()