#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent.parent
BRAND_DIR = ROOT / "assets" / "brand"

INK = (13, 18, 22, 255)
PAPER = (246, 244, 238, 255)
MIST = (226, 232, 224, 255)
GREEN = (53, 255, 155, 255)
CYAN = (61, 206, 255, 255)
VIOLET = (190, 74, 255, 255)
RED = (255, 91, 109, 255)
AMBER = (222, 184, 88, 255)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)

    return ImageFont.load_default()


def alpha_layer(size: tuple[int, int]) -> Image.Image:
    return Image.new("RGBA", size, (0, 0, 0, 0))


def draw_network_mark(image: Image.Image, box: tuple[int, int, int, int], dark: bool = True) -> None:
    draw = ImageDraw.Draw(image)
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    scale = min(w, h)
    cx = x0 + w / 2
    cy = y0 + h / 2
    stroke = PAPER if dark else INK
    soft = (246, 244, 238, 90) if dark else (13, 18, 22, 90)

    nodes = [
        (cx - scale * 0.26, cy - scale * 0.10, GREEN, 0.080),
        (cx - scale * 0.05, cy - scale * 0.30, CYAN, 0.060),
        (cx + scale * 0.22, cy - scale * 0.18, VIOLET, 0.052),
        (cx + scale * 0.25, cy + scale * 0.14, GREEN, 0.070),
        (cx - scale * 0.02, cy + scale * 0.28, AMBER, 0.050),
        (cx - scale * 0.28, cy + scale * 0.20, RED, 0.045),
        (cx, cy, PAPER if dark else INK, 0.095),
    ]
    edges = [(0, 1), (1, 2), (2, 6), (6, 0), (6, 3), (3, 4), (4, 5), (5, 0), (1, 6), (3, 2)]

    for a, b in edges:
        ax, ay, _, _ = nodes[a]
        bx, by, _, _ = nodes[b]
        draw.line((ax, ay, bx, by), fill=soft, width=max(2, int(scale * 0.012)))

    draw.ellipse(
        (cx - scale * 0.33, cy - scale * 0.33, cx + scale * 0.33, cy + scale * 0.33),
        outline=soft,
        width=max(2, int(scale * 0.010)),
    )
    draw.arc(
        (cx - scale * 0.42, cy - scale * 0.24, cx + scale * 0.42, cy + scale * 0.24),
        start=190,
        end=350,
        fill=CYAN,
        width=max(3, int(scale * 0.018)),
    )
    draw.arc(
        (cx - scale * 0.24, cy - scale * 0.42, cx + scale * 0.24, cy + scale * 0.42),
        start=15,
        end=178,
        fill=GREEN,
        width=max(3, int(scale * 0.018)),
    )

    glow = alpha_layer(image.size)
    glow_draw = ImageDraw.Draw(glow)
    for nx, ny, color, radius in nodes:
        r = scale * radius * 1.8
        glow_draw.ellipse((nx - r, ny - r, nx + r, ny + r), fill=color[:3] + (80,))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=max(2, int(scale * 0.025))))
    image.alpha_composite(glow)

    for nx, ny, color, radius in nodes:
        r = scale * radius
        draw.ellipse((nx - r, ny - r, nx + r, ny + r), fill=color, outline=stroke, width=max(1, int(scale * 0.008)))


def draw_grid(draw: ImageDraw.ImageDraw, width: int, height: int, color: tuple[int, int, int, int]) -> None:
    step = 48
    for x in range(0, width + step, step):
        draw.line((x, 0, x, height), fill=color, width=1)
    for y in range(0, height + step, step):
        draw.line((0, y, width, y), fill=color, width=1)


def create_mark() -> None:
    image = Image.new("RGBA", (1024, 1024), INK)
    draw = ImageDraw.Draw(image)
    draw_grid(draw, 1024, 1024, (246, 244, 238, 22))
    draw.rounded_rectangle((72, 72, 952, 952), radius=78, outline=(246, 244, 238, 95), width=8)
    draw_network_mark(image, (138, 138, 886, 886), dark=True)
    image.save(BRAND_DIR / "logo-mark.png")


def create_wordmark() -> None:
    image = alpha_layer((1680, 520))
    mark = Image.open(BRAND_DIR / "logo-mark.png").resize((360, 360), Image.Resampling.LANCZOS)
    image.alpha_composite(mark, (32, 80))
    draw = ImageDraw.Draw(image)

    title = font(112, bold=True)
    meta = font(31)
    draw.text((450, 100), "NOUS", font=title, fill=INK)
    draw.text((450, 215), "RESEARCH", font=title, fill=INK)
    draw.line((454, 338, 1210, 338), fill=(13, 18, 22, 150), width=4)
    draw.text((456, 370), "OPEN SOURCE AI RESEARCH INDEX", font=meta, fill=(55, 64, 62, 255))
    draw.rectangle((1218, 338, 1268, 344), fill=GREEN)
    draw.rectangle((1284, 338, 1334, 344), fill=CYAN)
    image.save(BRAND_DIR / "logo-wordmark.png")


def create_favicon() -> None:
    favicon = Image.new("RGBA", (256, 256), INK)
    draw = ImageDraw.Draw(favicon)
    draw.rounded_rectangle((16, 16, 240, 240), radius=34, outline=(246, 244, 238, 85), width=3)
    draw_network_mark(favicon, (34, 34, 222, 222), dark=True)
    favicon.save(BRAND_DIR / "favicon.png")
    favicon.resize((180, 180), Image.Resampling.LANCZOS).save(BRAND_DIR / "apple-touch-icon.png")


def create_social_card() -> None:
    width, height = 1200, 630
    image = Image.new("RGBA", (width, height), PAPER)
    draw = ImageDraw.Draw(image)
    draw_grid(draw, width, height, (13, 18, 22, 16))
    draw.rectangle((0, 0, width, 18), fill=INK)
    draw.rectangle((0, height - 18, width, height), fill=INK)
    draw.rounded_rectangle((54, 54, width - 54, height - 54), radius=8, outline=(13, 18, 22, 120), width=3)

    panel = (690, 90, 1095, 495)
    draw.rectangle(panel, fill=INK)
    draw_network_mark(image, panel, dark=True)

    title = font(82, bold=True)
    subhead = font(34)
    micro = font(20)
    draw.text((90, 118), "NOUS", font=title, fill=INK)
    draw.text((90, 206), "RESEARCH", font=title, fill=INK)
    draw.rectangle((94, 312, 448, 322), fill=GREEN)
    draw.text((90, 352), "Open-source AI models,", font=subhead, fill=(34, 39, 40, 255))
    draw.text((90, 394), "research infrastructure,", font=subhead, fill=(34, 39, 40, 255))
    draw.text((90, 436), "and applied reasoning.", font=subhead, fill=(34, 39, 40, 255))
    draw.text((90, 515), "Independent keyword guide | nousresearch.lol", font=micro, fill=(72, 79, 76, 255))
    image.save(BRAND_DIR / "social-card.png")


def main() -> None:
    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    create_mark()
    create_wordmark()
    create_favicon()
    create_social_card()
    print(f"Brand assets generated in {BRAND_DIR}")


if __name__ == "__main__":
    main()
