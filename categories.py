import random
from PIL import Image
from database import *

def generate_random_color():
    color = '#{:06x}'.format(random.randint(0, 0xFFFFFF))
    return color

def extract_dominant_color(image_loc):
    image = Image.open(image_loc)
    dominant_color = image.getpixel((0, 0))
    color = '#{:02x}{:02x}{:02x}'.format(*dominant_color)
    return color

def darken_color(color, factor=0.8):
    r, g, b = color[1:3], color[3:5], color[5:7]  # Extract RGB values from the color string
    r, g, b = int(r, 16), int(g, 16), int(b, 16)  # Convert RGB values to integers
    r, g, b = int(r * factor), int(g * factor), int(b * factor)  # Darken the RGB values
    dark_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)  # Convert back to color string
    return dark_color

def get_categories_data():
    q = "SELECT genre,image_loc FROM songs where privacy='public' and status='approved' group by genre"
    genres = select(q)
    q = "SELECT language,image_loc FROM songs where privacy='public' and status='approved' group by language"
    languages = select(q)
    categories_data = []
    
    for genre in genres:
        genre_name = genre['genre'].capitalize()
        image = genre['image_loc']
        color = extract_dominant_color('static/' + image)
        dark_color = darken_color(color)
        genre_with_color = {
            'content_name': genre_name,
            'category_type': 'genre',
            'color': dark_color,
            'image': image
        }
        categories_data.append(genre_with_color)

    for language in languages:
        language_name = language['language'].capitalize()
        image = language['image_loc']
        color = extract_dominant_color('static/' + image)
        dark_color = darken_color(color)
        language_with_color = {
            'content_name': language_name,
            'category_type': 'language',
            'color': dark_color,
            'image': image
        }
        categories_data.append(language_with_color)

    return categories_data
