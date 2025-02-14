import os
import re
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch

# Constants
CACHE_DIR = "cache"
FONT_DIR = "assets/KOKU"
THUMBNAIL_SIZE = (1280, 720)
CIRCLE_SIZE = 400
CIRCLE_BORDER = 20
TEXT_X_POSITION = 565

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

def change_image_size(max_width, max_height, image):
    width_ratio = max_width / image.size[0]
    height_ratio = max_height / image.size[1]
    new_width = int(width_ratio * image.size[0])
    new_height = int(height_ratio * image.size[1])
    return image.resize((new_width, new_height))

def truncate_text(text):
    words = text.split(" ")
    line1, line2 = "", ""
    for word in words:
        if len(line1) + len(word) < 30:
            line1 += " " + word
        elif len(line2) + len(word) < 30:
            line2 += " " + word
    return line1.strip(), line2.strip()

def crop_center_circle(img, output_size, border, crop_scale=1.5):
    half_width, half_height = img.size[0] / 2, img.size[1] / 2
    larger_size = int(output_size * crop_scale)
    img = img.crop((
        half_width - larger_size / 2,
        half_height - larger_size / 2,
        half_width + larger_size / 2,
        half_height + larger_size / 2
    ))
    img = img.resize((output_size - 2 * border, output_size - 2 * border))
    final_img = Image.new("RGBA", (output_size, output_size), "white")
    mask = Image.new("L", (output_size - 2 * border, output_size - 2 * border), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, output_size - 2 * border, output_size - 2 * border), fill=255)
    final_img.paste(img, (border, border), mask)
    return final_img

async def get_thumb(videoid):
    cache_path = f"{CACHE_DIR}/{videoid}_v4.png"
    if os.path.isfile(cache_path):
        return cache_path

    url = f"https://www.youtube.com/watch?v={videoid}"
    results = VideosSearch(url, limit=1)
    for result in (await results.next())["result"]:
        title = result.get("title", "Unsupported Title")
        duration = result.get("duration", "Unknown Mins")
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        views = result.get("viewCount", {}).get("short", "Unknown Views")
        channel = result.get("channel", {}).get("name", "Unknown Channel")

    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                async with aiofiles.open(f"{CACHE_DIR}/thumb{videoid}.png", mode="wb") as f:
                    await f.write(await resp.read())

    youtube = Image.open(f"{CACHE_DIR}/thumb{videoid}.png")
    image = change_image_size(*THUMBNAIL_SIZE, youtube)
    background = image.convert("RGBA").filter(ImageFilter.BoxBlur(20))
    background = ImageEnhance.Brightness(background).enhance(0.6)
    draw = ImageDraw.Draw(background)

    # Load fonts
    font = ImageFont.truetype(f"{FONT_DIR}/font.ttf", 30)
    title_font = ImageFont.truetype(f"{FONT_DIR}/font3.ttf", 45)

    # Add circular thumbnail
    circle_thumbnail = crop_center_circle(youtube, CIRCLE_SIZE, CIRCLE_BORDER)
    background.paste(circle_thumbnail, (120, 160), circle_thumbnail)

    # Add text
    title1, title2 = truncate_text(title)
    draw.text((TEXT_X_POSITION, 180), title1, fill="white", font=title_font)
    draw.text((TEXT_X_POSITION, 230), title2, fill="white", font=title_font)
    draw.text((TEXT_X_POSITION, 320), f"{channel}  |  {views[:23]}", fill="white", font=font)

    # Add progress bar
    line_length = 580
    red_length = int(line_length * 0.6)
    draw.line([(TEXT_X_POSITION, 380), (TEXT_X_POSITION + red_length, 380)], fill="red", width=9)
    draw.line([(TEXT_X_POSITION + red_length, 380), (TEXT_X_POSITION + line_length, 380)], fill="white", width=8)
    draw.ellipse([(TEXT_X_POSITION + red_length - 10, 370), (TEXT_X_POSITION + red_length + 10, 390)], fill="red")

    # Add timestamps
    draw.text((TEXT_X_POSITION, 400), "00:00", fill="white", font=font)
    draw.text((1080, 400), duration, fill="white", font=font)

    # Add play icons
    play_icons = Image.open(f"{FONT_DIR}/play_icons.png").resize((580, 62))
    background.paste(play_icons, (TEXT_X_POSITION, 450), play_icons)

    # Save and clean up
    background.save(cache_path)
    os.remove(f"{CACHE_DIR}/thumb{videoid}.png")
    return cache_path
