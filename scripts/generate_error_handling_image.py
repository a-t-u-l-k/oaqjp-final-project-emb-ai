"""Generate a PNG preview of the error-handling UI state."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUTPUT = Path(__file__).resolve().parents[1] / "7c_error_handling_interface.png"


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a system font with a safe fallback."""

    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold
        else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/SFNSDisplay.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def _rounded_box(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    radius: int,
    fill: tuple[int, int, int],
    outline: tuple[int, int, int] | None = None,
    width: int = 1,
) -> None:
    """Draw a rounded rectangle."""

    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def main() -> None:
    """Render the error-handling preview image."""

    width, height = 1440, 1024
    image = Image.new("RGB", (width, height), (239, 245, 251))
    draw = ImageDraw.Draw(image)

    for y in range(height):
        blend = y / height
        color = (
            int(230 - 16 * blend),
            int(244 - 7 * blend),
            int(255 - 13 * blend),
        )
        draw.line((0, y, width, y), fill=color)

    browser = (130, 90, 1310, 920)
    _rounded_box(draw, browser, 28, (246, 249, 253), outline=(185, 198, 214), width=2)
    draw.rectangle((130, 90, 1310, 150), fill=(226, 233, 242))
    for index, color in enumerate(((255, 95, 86), (255, 189, 46), (39, 201, 63))):
        draw.ellipse((160 + index * 28, 112, 178 + index * 28, 130), fill=color)

    address_bar = (300, 106, 1180, 136)
    _rounded_box(draw, address_bar, 15, (255, 255, 255), outline=(195, 205, 219))
    draw.text((325, 111), "http://127.0.0.1:5001/", fill=(77, 93, 113), font=_font(20))

    card = (300, 210, 1140, 820)
    _rounded_box(draw, card, 36, (255, 255, 255), outline=(220, 229, 239), width=2)

    draw.text((365, 265), "WATSON NLP", fill=(49, 103, 168), font=_font(24, bold=True))
    draw.text((365, 315), "Emotion Detector", fill=(16, 32, 51), font=_font(48, bold=True))
    draw.text(
        (365, 385),
        "Enter a sentence and the application will classify the dominant emotion",
        fill=(57, 73, 92),
        font=_font(26),
    )
    draw.text(
        (365, 420),
        "along with the individual emotion scores.",
        fill=(57, 73, 92),
        font=_font(26),
    )

    draw.text((365, 485), "Text to analyze", fill=(16, 32, 51), font=_font(24, bold=True))
    textarea = (365, 525, 1075, 650)
    _rounded_box(draw, textarea, 18, (255, 255, 255), outline=(197, 211, 225), width=2)
    draw.text(
        (395, 560),
        "",
        fill=(88, 103, 122),
        font=_font(28),
    )

    button = (365, 685, 675, 750)
    _rounded_box(draw, button, 32, (15, 98, 254))
    draw.text((418, 704), "Run Emotion Analysis", fill=(255, 255, 255), font=_font(26, bold=True))

    result_box = (365, 775, 1075, 930)
    _rounded_box(draw, result_box, 20, (255, 242, 242), outline=(242, 186, 186), width=2)
    draw.text((395, 805), "Result", fill=(16, 32, 51), font=_font(28, bold=True))
    draw.text(
        (395, 855),
        "Invalid text! Please try again.",
        fill=(154, 34, 34),
        font=_font(28, bold=True),
    )

    image.save(OUTPUT)


if __name__ == "__main__":
    main()
