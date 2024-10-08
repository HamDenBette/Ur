import pygame
import math
from datetime import datetime

pygame.init()
screen_size = (640, 640)  # Make the window square for a better circular fit
screen = pygame.display.set_mode(screen_size)
font = pygame.font.SysFont(None, 50)
screen.fill((255, 255, 255))

# Dynamically set the clock size to fit the window
clock_radius = min(screen_size) // 2 - 20  # A bit smaller than half of the window
center = (screen_size[0] // 2, screen_size[1] // 2)  # Center of the screen

black = (0, 0, 0)
white = (255, 255, 255)

# Roman numerals for the clock face
roman_numerals = ["XII", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]

# Load the image using pygame's image loader
image_url = 'beer.jpg'  # Replace this with your local path
background_image = pygame.image.load(image_url)

# Scale the image to fit the clock size
background_image = pygame.transform.scale(background_image, (clock_radius * 2, clock_radius * 2))

def draw_clock_face():
    # Draw clock border
    pygame.draw.circle(screen, black, center, clock_radius, 10)
    
    # Draw Roman numerals
    numeral_radius = clock_radius - 50  # Distance from center for the numerals
    for i, numeral in enumerate(roman_numerals):
        angle = math.radians(360 / 12 * i - 90)  # Adjust to make 12 at the top
        x = center[0] + numeral_radius * math.cos(angle) - 20  # Offset for center alignment
        y = center[1] + numeral_radius * math.sin(angle) - 20  # Offset for center alignment
        text = font.render(numeral, True, black)
        screen.blit(text, (x, y))

def create_image_mask():
    # Create a mask surface the size of the screen with alpha channel
    mask = pygame.Surface((clock_radius * 2, clock_radius * 2), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 0))  # Fill it with transparent color

    # Draw a filled white circle in the mask surface
    pygame.draw.circle(mask, (255, 255, 255), (clock_radius, clock_radius), clock_radius)

    return mask

while True:
    # Clear the screen
    screen.fill(white)

    # Get current time and date
    now = datetime.now()
    s = now.second
    m = now.minute
    h = now.hour % 12
    day = now.day
    month = now.month
    year = now.year

    # Calculate the height of the portion of the image to draw
    fill_percentage = s / 60  # Percentage of the minute that has passed
    image_height = int(clock_radius * 2 * fill_percentage)  # Height to draw based on percentage

    # Create a mask for the clock face
    mask = create_image_mask()

    # Create a temporary surface for the clock image
    temp_surface = pygame.Surface((clock_radius * 2, clock_radius * 2), pygame.SRCALPHA)
    temp_surface.blit(background_image, (0, clock_radius * 2 - image_height))

    # Apply the mask on the temporary surface
    temp_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    # Draw the masked image centered on the screen
    screen.blit(temp_surface, (center[0] - clock_radius, center[1] - clock_radius))

    # Draw clock face on top of the image
    draw_clock_face()

    # Set hand lengths based on clock radius
    radius_s = int(clock_radius * 0.9)  # Seconds hand
    radius_m = int(clock_radius * 0.75)  # Minutes hand
    radius_h = int(clock_radius * 0.5)  # Hours hand
    start_position = (screen_size[0] // 2, screen_size[1] // 2)

    # Draw seconds hand
    angle_s = 360 / 60 * s - 90  # Adjusted to make 12 o'clock the top (clockwise movement)
    end_offset = [radius_s * math.cos(math.radians(angle_s)), radius_s * math.sin(math.radians(angle_s))]
    end_position = (start_position[0] + end_offset[0], start_position[1] + end_offset[1])
    pygame.draw.line(screen, (0, 0, 0), start_position, end_position, 3)

    # Draw minutes hand
    angle_m = 360 / 60 * m - 90 + (6 * s / 60)  # Adjusted to start from 12 o'clock (clockwise)
    end_offset = [radius_m * math.cos(math.radians(angle_m)), radius_m * math.sin(math.radians(angle_m))]
    end_position = (start_position[0] + end_offset[0], start_position[1] + end_offset[1])
    pygame.draw.line(screen, (0, 0, 0), start_position, end_position, 5)

    # Draw hours hand
    angle_h = 360 / 12 * (h + m / 60) - 90  # Adjusted to make 12 o'clock the top (clockwise)
    end_offset = [radius_h * math.cos(math.radians(angle_h)), radius_h * math.sin(math.radians(angle_h))]
    end_position = (start_position[0] + end_offset[0], start_position[1] + end_offset[1])
    pygame.draw.line(screen, (0, 0, 0), start_position, end_position, 7)

    # Reposition the digital clock slightly below the center
    digital_clock_pos = (center[0] - 80, center[1] + clock_radius // 2 + -40)
    text_time = font.render(f'{now.strftime("%H:%M:%S")}', True, (255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (digital_clock_pos[0] - 20, digital_clock_pos[1] - 15, 180, 60))
    screen.blit(text_time, digital_clock_pos)

    # Render the date
    date_text = font.render(f'{day}/{month}/{year}', True, (255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (digital_clock_pos[0] - 20, digital_clock_pos[1] - 263, 195, 60))
    screen.blit(date_text, (digital_clock_pos[0], digital_clock_pos[1] - 250))  # Adjust position as needed

    # Clock "teeth" hour
    for marker_angle in range(0, 360, 30):
        start_offset = [295 * math.cos(math.radians(marker_angle)), 295 * math.sin(math.radians(marker_angle))]
        end_offset = [(295 - 20) * math.cos(math.radians(marker_angle)),
                  (295 - 20) * math.sin(math.radians(marker_angle))]
        line_start = (start_position[0] + start_offset[0], start_position[1] + start_offset[1])
        line_end1 = (start_position[0] + end_offset[0], start_position[1] + end_offset[1])
        pygame.draw.line(screen, (0, 0, 0), line_start, line_end1, 4)
    
    # Clock "teeth" min
    for marker_angle1 in range(0, 360, 6):
        start_offset1 = [295 * math.cos(math.radians(marker_angle1)), 295 * math.sin(math.radians(marker_angle1))]
        end_offset1 = [(295 - 10) * math.cos(math.radians(marker_angle1)),
                  (295 - 10) * math.sin(math.radians(marker_angle1))]
        line_start1 = (start_position[0] + start_offset1[0], start_position[1] + start_offset1[1])
        line_end2 = (start_position[0] + end_offset1[0], start_position[1] + end_offset1[1])
        pygame.draw.line(screen, (0, 0, 0), line_start1, line_end2, 2)

    # Update display
    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
