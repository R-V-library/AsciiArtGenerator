import sys
from .app import App

def main(argv=sys.argv[1:]):
    app = App()
    return app.run(argv)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))  # pragma: no cover
