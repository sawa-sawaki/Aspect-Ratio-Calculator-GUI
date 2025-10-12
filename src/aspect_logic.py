import os
from PIL import Image


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def simplify_aspect_ratio(width: float, height: float) -> str:
    if width is None or height is None or width <= 0 or height <= 0:
        return "N/A"

    w_int = int(round(width * 100))
    h_int = int(round(height * 100))
    if w_int == 0 or h_int == 0:
        return f"{width:.2f}:{height:.2f}"

    common_divisor = gcd(w_int, h_int)

    simple_w = w_int // common_divisor
    simple_h = h_int // common_divisor

    return f"{simple_w}:{simple_h}"


def calculate_new_dimensions(ratio: str, target_w: float, target_h: float, fallback_w: float = None, fallback_h: float = None) -> tuple[float, float]:
    try:
        r_parts = ratio.split(':')
        ratio_w = float(r_parts[0])
        ratio_h = float(r_parts[1])
    except (ValueError, IndexError):
        return fallback_w, fallback_h

    if ratio_w <= 0 or ratio_h <= 0:
        return fallback_w, fallback_h

    if target_w is not None:
        new_w = target_w
        new_h = (target_w / ratio_w) * ratio_h
        return new_w, new_h

    elif target_h is not None:
        new_h = target_h
        new_w = (target_h / ratio_h) * ratio_w
        return new_w, new_h

    elif fallback_w is not None:
        new_w = fallback_w
        new_h = (fallback_w / ratio_w) * ratio_h
        return new_w, new_h

    elif fallback_h is not None:
        new_h = fallback_h
        new_w = (fallback_h / ratio_h) * ratio_w
        return new_w, new_h

    return None, None


def get_image_dimensions(image_path: str) -> tuple[int, int]:
    if not os.path.exists(image_path):
        return None, None

    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception:
        return None, None
