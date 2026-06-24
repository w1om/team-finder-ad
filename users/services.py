import random
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw


def generate_default_avatar(user):
    bg_color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
    image = Image.new("RGB", (200, 200), color=bg_color)
    draw = ImageDraw.Draw(image)

    letter = user.first_name[0].upper() if user.first_name else (user.email[0].upper() if user.email else "U")
    draw.text((90, 90), letter, fill=(255, 255, 255))

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    file_name = f"avatar_{user.email}.png"
    user.avatar.save(file_name, ContentFile(buffer.getvalue()), save=True)
