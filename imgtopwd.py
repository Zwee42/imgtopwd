#!/usr/bin/env python3

import sys
import hashlib
from PIL import Image
import argparse

def parse_flags(argv):
    
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    length = 16
    seed = None
    image_path = None

    p = argparse.ArgumentParser(
        prog="imgtopwd",
        description="Generate a deterministic password from an image."
    )

    p.add_argument("-i", "--image", type=str, help="Path to the image file")
    p.add_argument("-l", type=int, default=16, help="Specify the length of the generated password")
    p.add_argument("-s", action="store_true", help="Allow special characters in the password")
    p.add_argument("--seed", type=str, help="Use the provided text as seed instead of image data")

    args = p.parse_args(argv[1:])

    length = args.l
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    if args.s:
        chars += "!@#$%^&*()-_=+[]{}|;:',.<>?/"
    seed = args.seed or ""
    image_path = args.image

    return image_path,length, chars, seed

def hash_to_pwd(text, length, chars):
    digest = hashlib.sha256(text.encode()).hexdigest()
    pwd_chars = [chars[int(digest[i:i+2], 16) % len(chars)] for i in range(0, len(digest), 2)]
    return ''.join(pwd_chars)[:length]


def image_to_text(img_path):
    try:
        with Image.open(img_path) as img:
            img = img.convert("RGB")
            pixels = img.getdata()
            chars = [(r + g + b) // 3 for (r, g, b) in pixels]
            return ''.join(chr((val % 94) + 33) for val in chars)
    except Exception as e:
        sys.exit(f"Error reading image: {e}")

def main():
    image_path, length, chars, seed = parse_flags(sys.argv)
    if not image_path:
        sys.exit("Image path is required. Use -i or --image to specify the image file.")
    text = image_to_text(image_path)
    password = hash_to_pwd(seed + text, length, chars)
    print(f"Generated password: \n{password}")

if __name__ == '__main__':
    main()