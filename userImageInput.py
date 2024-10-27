import pygame
import tkinter as tk
from tkinter import filedialog

# Function to open file dialog to load an image
def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select an Image", 
                                            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    return file_path

# Initialize Pygame
pygame.init()
X = 600
Y = 600
scrn = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Image Loader and Saver')

# Colors
button_color = (0, 128, 255)
button_hover_color = (0, 255, 255)
text_color = (255, 255, 255)

# Button dimensions
load_button_rect = pygame.Rect(100, 250, 200, 50)
save_button_rect = pygame.Rect(300, 250, 200, 50)

# Variable to hold the loaded image
loaded_image = None

# Specify the save location and filename
save_location = 'images\irl\loadedImage.png'  # Change this path as needed

# Main loop
status = True

while status:
    scrn.fill((0, 0, 0))  # Clear the screen

    # Draw the Load Image button
    if load_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(scrn, button_hover_color, load_button_rect)
    else:
        pygame.draw.rect(scrn, button_color, load_button_rect)

    # Draw the Save Image button only if an image is loaded
    if loaded_image:
        if save_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(scrn, button_hover_color, save_button_rect)
        else:
            pygame.draw.rect(scrn, button_color, save_button_rect)

        # Draw button text for Save Image
        save_text = pygame.font.Font(None, 36).render('Save Image', True, text_color)
        save_text_rect = save_text.get_rect(center=save_button_rect.center)
        scrn.blit(save_text, save_text_rect)

    # Draw button text for Load Image
    load_text = pygame.font.Font(None, 36).render('Load Image', True, text_color)
    load_text_rect = load_text.get_rect(center=load_button_rect.center)
    scrn.blit(load_text, load_text_rect)

    # Display loaded image if available
    #if loaded_image:
     #   scrn.blit(loaded_image, (0, 0))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and load_button_rect.collidepoint(event.pos):
                # Open file dialog and load image
                root = tk.Tk()
                root.withdraw()  # Hide the root window
                file_path = open_file_dialog()
                if file_path:
                    try:
                        loaded_image = pygame.image.load(file_path).convert()
                    except pygame.error:
                        print("Error loading image.")
            elif event.button == 1 and loaded_image and save_button_rect.collidepoint(event.pos):
                # Save the loaded image to the specified location
                pygame.image.save(loaded_image, save_location)  # Save the image
                print(f"Image saved to: {save_location}")

# Deactivate Pygame
pygame.quit()
