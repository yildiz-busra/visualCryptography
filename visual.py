from PIL import Image
import random

def generate_shares(input):
    img = Image.open(input).convert('1')
    width, height = img.size
    share1 = Image.new('1', (width * 2, height * 2))
    share2 = Image.new('1', (width * 2, height * 2))

    pixels = img.load()
    pixels_share1 = share1.load()
    pixels_share2 = share2.load()

    for x in range(width):
        for y in range(height):
            pixel = pixels[x, y]           
            random_bit = random.randint(0, 1) # random bit to decide the pattern

            if pixel == 255: 
                if random_bit == 0:
                    # pattern 1
                    pixels_share1[x * 2, y * 2] = 255
                    pixels_share1[x * 2 + 1, y * 2] = 0
                    pixels_share1[x * 2, y * 2 + 1] = 0
                    pixels_share1[x * 2 + 1, y * 2 + 1] = 255

                    pixels_share2[x * 2, y * 2] = 255
                    pixels_share2[x * 2 + 1, y * 2] = 0
                    pixels_share2[x * 2, y * 2 + 1] = 0
                    pixels_share2[x * 2 + 1, y * 2 + 1] = 255
                else:
                    # pattern 2
                    pixels_share1[x * 2, y * 2] = 0
                    pixels_share1[x * 2 + 1, y * 2] = 255
                    pixels_share1[x * 2, y * 2 + 1] = 255
                    pixels_share1[x * 2 + 1, y * 2 + 1] = 0

                    pixels_share2[x * 2, y * 2] = 0
                    pixels_share2[x * 2 + 1, y * 2] = 255
                    pixels_share2[x * 2, y * 2 + 1] = 255
                    pixels_share2[x * 2 + 1, y * 2 + 1] = 0

            elif pixel == 0:  
                if random_bit == 0:
                    # pattern 1
                    pixels_share1[x * 2, y * 2] = 255
                    pixels_share1[x * 2 + 1, y * 2] = 0
                    pixels_share1[x * 2, y * 2 + 1] = 0
                    pixels_share1[x * 2 + 1, y * 2 + 1] = 255

                    pixels_share2[x * 2, y * 2] = 0
                    pixels_share2[x * 2 + 1, y * 2] = 255
                    pixels_share2[x * 2, y * 2 + 1] = 255
                    pixels_share2[x * 2 + 1, y * 2 + 1] = 0
                else:
                    # pattern 2
                    pixels_share1[x * 2, y * 2] = 0
                    pixels_share1[x * 2 + 1, y * 2] = 255
                    pixels_share1[x * 2, y * 2 + 1] = 255
                    pixels_share1[x * 2 + 1, y * 2 + 1] = 0

                    pixels_share2[x * 2, y * 2] = 255
                    pixels_share2[x * 2 + 1, y * 2] = 0
                    pixels_share2[x * 2, y * 2 + 1] = 0
                    pixels_share2[x * 2 + 1, y * 2 + 1] = 255

    share1.save("share1.png")
    share2.save("share2.png")
    print("Shares saved as 'share1.png' and 'share2.png'.")

def overlay_shares(share1, share2, output):
    share1 = Image.open(share1)
    share2 = Image.open(share2)
    assert share1.size == share2.size, "Shares must be the same size."
    result = Image.new('1', share1.size)

    pixels_share1 = share1.load()
    pixels_share2 = share2.load()
    pixels_result = result.load()

    width, height = share1.size
    for x in range(width):
        for y in range(height):
            pixels_result[x, y] = pixels_share1[x, y] & pixels_share2[x, y]

    result.save(output)
    print(f"Overlayed image saved as '{output}'.")

generate_shares("input.png") 
overlay_shares("share1.png", "share2.png", "output.png")
