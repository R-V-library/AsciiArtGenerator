import pytest
import logging
import os

from ascii_art_app.app import App

# from ascii_art_app.version import __version__


logger = logging.getLogger(__name__)

TEST_BASE = os.path.join(os.environ.get("PRJROOT"), "tests", "assets")

# argparser


def test_argparser_basic():
    filepath = os.path.join(TEST_BASE, "valid")
    for file in os.listdir(filepath):
        logger.info(f"Testing file: {file}")
        app = App()
        app.run([os.path.join(filepath, file)])


def test_argparser_unknown_argument():  # TODO: check output?
    app = App()
    with pytest.raises(SystemExit):  # as excinfo:
        app.run(["-z"])
    # assert isinstance(excinfo, Exception)


def test_argparser_help():  # TODO: check output using capsys?
    app = App()
    with pytest.raises(SystemExit):
        app.run(["-h"])


def test_argparser_help_long():  # TODO: check output using capsys?
    app = App()
    with pytest.raises(SystemExit):
        app.run(["--help"])


def test_argparser_version():  # TODO: check output using capsys?
    app = App()
    with pytest.raises(SystemExit):
        app.run(["-v"])


def test_argparser_version_long():  # TODO: check output using capsys?
    app = App()
    with pytest.raises(SystemExit):
        app.run(["--version"])


def test_argparser_colours_and_styles():
    filepath = os.path.join(TEST_BASE, "valid")
    file = "oranges.jpg"
    colours = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    styles = ["regular", "lines"]
    for style in styles:
        for colour in colours:
            app = App()
            logger.info(f"Testing colour: {colour}")
            app.run([os.path.join(filepath, file), "-c", colour, "-s", style])

            with open(os.path.join(os.environ.get("PRJROOT"), "output.txt"), "r") as f:

                if colour == "black":
                    assert f.read(5) == "\x1b[30m"

                elif colour == "red":
                    assert f.read(5) == "\x1b[31m"

                elif colour == "green":
                    assert f.read(5) == "\x1b[32m"

                elif colour == "yellow":
                    assert f.read(5) == "\x1b[33m"

                elif colour == "blue":
                    assert f.read(5) == "\x1b[34m"

                elif colour == "magenta":
                    assert f.read(5) == "\x1b[35m"

                elif colour == "cyan":
                    assert f.read(5) == "\x1b[36m"

                elif colour == "white":
                    assert f.read(5) == "\x1b[37m"

                lines = f.readlines()
                assert lines[-1] == "\x1b[0m"


def test_argparser_debug():
    filepath = os.path.join(TEST_BASE, "valid", "oranges.jpg")
    app = App()
    app.run([filepath, "-d"])


def test_argparser_invalid_lines():
    filepath = os.path.join(TEST_BASE, "valid", "oranges.jpg")
    app = App()
    with pytest.raises(ValueError):
        app.run([filepath, "-l", "0"])


def test_argparser_invalid_lines_2():
    filepath = os.path.join(TEST_BASE, "valid", "oranges.jpg")
    app = App()
    with pytest.raises(ValueError):
        app.run([filepath, "-l", "-10"])


def test_argparser_output_dir():
    filepath = os.path.join(TEST_BASE)
    app = App()
    app.run(
        [
            os.path.join(filepath, "valid", "oranges.jpg"),
            "-o",
            os.path.join(filepath, "test.txt"),
        ]
    )
    assert os.path.exists(os.path.join(TEST_BASE, "output.txt"))


def test_argparser_style():
    filepath = os.path.join(TEST_BASE, "valid")
    for file in os.listdir(filepath):
        logger.info(f"Testing file: {file}")
        app = App()
        app.run([os.path.join(filepath, file), "-s", "regular"])

    for file in os.listdir(filepath):
        logger.info(f"Testing file: {file}")
        app = App()
        app.run([os.path.join(filepath, file), "-s", "lines"])


def test_argparser_invalid_style():
    pass


def test_argparser_invalid_style_long():
    pass


def test_argparser_trim_whitespace():
    filepath = os.path.join(TEST_BASE, "valid")
    for file in os.listdir(filepath):
        logger.info(f"Testing file: {file}")
        app = App()
        app.run([os.path.join(filepath, file), "-t"])


def test_argparser_max_characters():
    pass


def test_argparser_max_characters_long():
    pass


def test_argparser_invalid_max_characters():
    app = App()
    with pytest.raises(ValueError):
        app.run([os.path.join(TEST_BASE, "valid", "oranges.jpg"), "-w", "0"])


def test_argparser_invalid_max_characters_2():
    app = App()
    with pytest.raises(ValueError):
        app.run([os.path.join(TEST_BASE, "valid", "oranges.jpg"), "-w", "-10"])


def test_argparser_invalid_file():
    app = App()
    with pytest.raises(TypeError):
        app.run([os.path.join(TEST_BASE, "invalid", "invalid_file.txt")])


def test_argparser_nonexisting_file():
    app = App()
    with pytest.raises(FileNotFoundError):
        app.run([os.path.join(TEST_BASE, "invalid", "nonexisting_file.txt")])


def test_argparser_invalid_dir():
    app = App()
    with pytest.raises(IsADirectoryError):
        app.run(
            [os.path.join(TEST_BASE, "valid", "oranges.jpg"), "-o", "./invalid_dir/"]
        )


def test_argparser_missing_config(monkeypatch):
    monkeypatch.delenv("PRJROOT", raising=False)

    with pytest.raises(RuntimeError) as e:
        App()
    assert str(e.value) == "$PRJROOT was not set"
