#import sys 

#print(sys.executable) 

import random 

import PIL 

PIL.__version__ 

 

from PIL import Image 

from PIL import ImageFilter 

 

 

def erode(cycles, image): 

    for _ in range(cycles): 

            image = image.filter(ImageFilter.MinFilter(3)) 

    return image 

 

 

def dilate(cycles, image): 

    for _ in range(cycles): 

            image = image.filter(ImageFilter.MaxFilter(3)) 

    return image 

 

 

def replaceImagePixels(image,size): 

 

    # Load the main image and the image to paste 

    main_image = image.convert("RGB")  

    replacement_image1 = Image.open("topDownTree.png").convert("RGB") 

    replacement_image2 = Image.open("topDownTree2.png").convert("RGB")  

 

    # Ensure the replacement image is the right size (20x20 pixels) 

     

    replacement_images = [replacement_image1,replacement_image1,replacement_image1,replacement_image2,replacement_image2] 

     

    for i in range(len(replacement_images)): 

        replacement_images[i] = replacement_images[i].resize((size, size)) 

 

    # Get dimensions 

    width, height = main_image.size 

 

    # Create a new image to hold the result 

    modified_image = main_image.copy() 

 

    def is_block_predominantly_black(image, x, y, block_size): 

        black_pixel_count = 0 

        #total_pixels = block_size * block_size 

     

        for j in range(block_size): 

            for i in range(block_size): 

                if y + j < height and x + i < width: 

                    pixel = image.getpixel((x + i, y + j)) 

                    if pixel == (0, 0, 0): 

                        black_pixel_count += 1 

     

        if black_pixel_count >= 1: 

            return True 

        else: 

            return False 

     

    # Loop through the main image in blocks of 20x20 pixels 

    block_size = size//2 

    for y in range(0, height, block_size): 

        for x in range(0, width, block_size): 

            # Check if the current block is black 

            if is_block_predominantly_black(main_image, x, y, block_size): 

                #print(f"Block at ({x}, {y}) is black. Pasting replacement image.") 

                # Paste the replacement image if the block is black 

                modified_image.paste(random.choice(replacement_images), (x, y)) 

            #else: 

                #print(f"Block at ({x}, {y}) is not black.") 

                 

 

    # Save or display the modified image 

    irlTreeReplacement = "treeReplace.png".format(i) 

    modified_image.save(irlTreeReplacement) 

    modified_image.show() 

 

 

 

def convert_to_bw_segmentate(input_image_path, output_image_path, modded,threshold = 100): 

 

    #irltrial = "irlTrial3.jpg" 

 

    with Image.open(input_image_path) as img_irl: 

        img_irl_gray = img_irl.convert("L") 

        new_width  = 1200 

        new_height = 800 

        img_irl_gray = img_irl_gray.resize((new_width, new_height)) 

        #img_irl_gray.save(irlOgScaled) 

 

        img_irl_threshold = img_irl_gray.point(lambda x: 255 if x > threshold else 0, '1') 

 

 

    ####### segmentation ###### 

 

    step_1 = erode(8, img_irl_threshold) 

    #step_1.show() 

     

    step_2 = dilate(20, step_1) 

    #step_2.show() 

 

    step_3 = erode(10, step_2) 

    #step_3.show() 

 

     

    pixels = step_3.getdata()    

     

    #pixels = step_3.getdata()      # get the pixels as a flattened sequence 

    black_thresh = 65 

    nblack = 0 

    for pixel in pixels: 

        if pixel < black_thresh: 

            nblack += 1 

    n = len(pixels) 

 

    if (nblack / float(n)) > 0.5: 

        #print("mostly black - reverse") 

        step_3 = PIL.ImageOps.invert(step_3) 

      

 

     

    step_3.save(output_image_path) 

    

 

    image = Image.open(output_image_path) 

 

    #Access the pixel data of the image 

    pixels = list(image.getdata()) 

    #print(pixels) 

 

 

    path_colours = [(101, 68, 46),  (128, 93, 73)] 

 

 

    #Create a new list of pixel values with the new color 

    modified_pixels = [] 

    for i in range(0, len(pixels), 10): 

        chunk = pixels[i:i + 10]  # Get a chunk of 20 pixels 

        #new_colour = random.choice(new_colours) 

        path_colour = random.choice(path_colours) 

        # Change the color of the chunk if the pixels are not white 

        modified_chunk = [path_colour if pixel !=  0 else (0,0,0) for pixel in chunk] 

        modified_pixels.extend(modified_chunk)  # Add modified chunk to the result 

 

    # modified_pixels now contains the modified pixels 

 

 

    #Create a new image with the modified pixel values 

    modified_image = Image.new("RGB", image.size) 

    modified_image.putdata(modified_pixels) 

 

    #Save the modified image to a file 

 

    #modified_image.save(modded) 

    replaceImagePixels(modified_image,24)   

 

    #Display the modified image 

    #modified_image.show() 

     

''' 

for i in range(2,3): 

    #print(i) 

    into =  'irlTrial{}.jpg'.format(i) 

    outto = 'irlTrialBW{}.jpg'.format(i) 

    modded = 'irlModified{}.jpg'.format(i) 

    #irlOgScaled = 'irlOgScaled{}.jpg'.format(i) 

    convert_to_bw_segmentate(into,outto,modded) 

''' 

 

into =  'irlTrial{}.jpg'.format(i) 

outto = 'irlTrialBW{}.jpg'.format(i) 

modded = 'irlModified{}.jpg'.format(i) 

    #irlOgScaled = 'irlOgScaled{}.jpg'.format(i) 

convert_to_bw_segmentate(into,outto,modded)