import numpy as np
from PIL import Image

def to_binary_image(image_path):
    """Convert the image to a binary (black & white) image."""
    img = Image.open(image_path).convert("1")  # Convert to black and white
    return np.array(img)

def generate_shares_3outof3(binary_image):
    """Generate three shares from the binary image using a 3-out-of-3 visual cryptography scheme."""
    height, width = binary_image.shape
    share1 = np.zeros((height, width), dtype=np.uint8)
    share2 = np.zeros((height, width), dtype=np.uint8)
    share3 = np.zeros((height, width), dtype=np.uint8)
    
    for i in range(height):
        for j in range(width):
            if binary_image[i, j] == 0:  # Black pixel in the original image
                # Randomly split black pixel into three shares
                shares = np.random.choice([0, 0, 0, 1, 1, 1], 3, replace=False)
                np.random.shuffle(shares)
                share1[i, j], share2[i, j], share3[i, j] = shares
            else:  # White pixel in the original image
                # Randomly split white pixel into three shares
                shares = np.random.choice([0, 1, 1], 3, replace=False)
                np.random.shuffle(shares)
                share1[i, j], share2[i, j], share3[i, j] = shares
    return share1, share2, share3

def save_share(share, file_name):
    """Save a share as an image file."""
    img = Image.fromarray(share * 255)  # Convert binary (0/1) to black (0) and white (255)
    img.save(file_name)

def combine_shares(share1, share2, share3):
    """Combine three shares using a majority rule to reveal the original image."""
    combined = np.zeros_like(share1)
    height, width = share1.shape
    for i in range(height):
        for j in range(width):
            # Majority rule: if at least 2 shares have the pixel as 1, it's white (1)
            combined[i, j] = 1 if (share1[i, j] + share2[i, j] + share3[i, j]) >= 2 else 0
    Image.fromarray(combined * 255).save('snippet\output.png')  # Save the combined image


# Main Execution
if __name__ == "__main__":
    # Load and process the image
    img_path = 'input.png'  # Replace with your image path
    binary_img = to_binary_image(img_path)

    # Generate shares
    share1, share2, share3 = generate_shares_3outof3(binary_img)

    # Save shares as images
    save_share(share1, 'snippet\share1.png')
    save_share(share2, 'snippet\share2.png')
    save_share(share3, 'snippet\share3.png')

    # Combine shares to reveal the original image
    combined_image = combine_shares(share1, share2, share3)
    Image.fromarray(combined_image * 255).show()
