import sys
from pathlib import Path
current_file_path = Path(__file__).resolve()
src_dir = (current_file_path.parent / 'src').resolve()
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))


def main():
    app = AspectRatioCalculator()
    app.mainloop()


if __name__ == "__main__":
    from src.aspect_calculator_gui import AspectRatioCalculator
    main()
