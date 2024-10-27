import random
import os
from PIL import Image
from PIL import ImageFilter
import PIL

class ImageConvert:
    def __init__(self, imageFile):
        self.imageFile = imageFile
        self.outBW = os.path.join('images', 'bw', 'bwBackground.jpg')  # Ensure this is a valid path
        self.outBackground = os.path.join('images', 'green', 'treeReplace.png')  # Set the output path correctly
        # Use os.path.join for better path handling
        self.tree1 = os.path.join('assets', 'trees', 'topDownTree.png')
        self.tree2 = os.path.join('assets', 'trees', 'topDownTree2.png')

    def erode(self, cycles, image):
        for _ in range(cycles):
            image = image.filter(ImageFilter.MinFilter(3))
        return image

    def dilate(self, cycles, image):
        for _ in range(cycles):
            image = image.filter(ImageFilter.MaxFilter(3))
        return image

    def replaceImagePixels(self, image, size):
        # Load the main image and the image to paste
        main_image = image.convert("RGB")
        
        # Use a try-except to catch file loading errors
        try:
            replacement_image1 = Image.open(self.tree1).convert("RGB")
            replacement_image2 = Image.open(self.tree2).convert("RGB")
        except OSError as e:
            print(f"Error loading replacement images: {e}")
            return

        # Resize the replacement images
        replacement_images = [replacement_image1, replacement_image1, replacement_image1, replacement_image2, replacement_image2]
        for i in range(len(replacement_images)):
            replacement_images[i] = replacement_images[i].resize((size, size))

        # Get dimensions
        width, height = main_image.size
        modified_image = main_image.copy()

        def is_block_predominantly_black(image, x, y, block_size):
            black_pixel_count = sum(
                1 for j in range(block_size) for i in range(block_size)
                if y + j < height and x + i < width and image.getpixel((x + i, y + j)) == (0, 0, 0)
            )
            return black_pixel_count >= 1

        # Loop through the main image in blocks
        block_size = size // 2
        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                if is_block_predominantly_black(main_image, x, y, block_size):
                    modified_image.paste(random.choice(replacement_images), (x, y))

        # Save the modified image
        modified_image.save(self.outBackground)
        #modified_image.show()

    def convert_to_bw_segmentate(self, threshold=100):
        with Image.open(self.imageFile) as img_irl:
            img_irl_gray = img_irl.convert("L")
            img_irl_gray = img_irl_gray.resize((1200, 800))
            img_irl_threshold = img_irl_gray.point(lambda x: 255 if x > threshold else 0, '1')

        step_1 = self.erode(8, img_irl_threshold)
        step_2 = self.dilate(20, step_1)
        step_3 = self.erode(10, step_2)

        # Invert if mostly black
        if sum(1 for pixel in step_3.getdata() if pixel < 65) / float(len(step_3.getdata())) > 0.5:
            step_3 = PIL.ImageOps.invert(step_3)

        step_3.save(self.outBW)

        image = Image.open(self.outBW)
        pixels = list(image.getdata())

        path_colours = [(101, 68, 46), (128, 93, 73)]
        modified_pixels = []
        for i in range(0, len(pixels), 10):
            chunk = pixels[i:i + 10]
            path_colour = random.choice(path_colours)
            modified_chunk = [path_colour if pixel != 0 else (0, 0, 0) for pixel in chunk]
            modified_pixels.extend(modified_chunk)

        modified_image = Image.new("RGB", image.size)
        modified_image.putdata(modified_pixels)

        self.replaceImagePixels(modified_image, 24)
        #modified_image.show()


'''
# Example usage
trialImage = ImageConvert('images/irl/eightIRL.jpeg')
trialImage.convert_to_bw_segmentate()
'''