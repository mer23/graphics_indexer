import sys, pygame
pygame.init()

IMAGES_PATH= "Skins/Default/Tiles/"
IMAGE_FILE_EXT= ".png"
AMOUNT_OF_IMAGES= 117

DEFAULT_TILE_SIZE= 32
DEFAULT_IMAGE_SIZE= 1024, 256

SELECTED_TILE_COLOR= 0, 255, 18
BACKGROUND_COLOR= 0,0,0

current_img= 0
image_selected= False

images= []
tiles_selected= []

def loadImages():
	for image in range (AMOUNT_OF_IMAGES):
		images.append( pygame.transform.rotate(pygame.image.load(IMAGES_PATH + str(image + 1) + IMAGE_FILE_EXT), 90) ) #png files naming starts from 1

def sprite_generator(tile_list):
	leftmost= tile_list[0].left #leftmost tile edge
	topmost= tile_list[0].top #topmost tile edge
	rightmost= tile_list[0].right #rightmost tile edge
	bottommost= tile_list[0].bottom #bottommost tile edge

	for tile in tile_list:
		if tile.left < leftmost: leftmost= tile.left
		if tile.top < topmost: topmost= tile.top
		if tile.right > rightmost: rightmost= tile.right
		if tile.bottom > bottommost: bottommost= tile.bottom

	sprite= pygame.Surface( (rightmost - leftmost , bottommost - topmost) ) # creates a new surface with proper size
	sprite.fill(BACKGROUND_COLOR)

	for tile in tile_list:
		area_at_tile= pygame.Rect(tile.left - leftmost, tile.top - topmost, tile.width, tile.height)
		sprite.blit(images[current_img - 1].subsurface(tile), area_at_tile)
	
	return pygame.transform.rotate(sprite, -90)


def rectangle_from_click(pos):
	topleft_x = pos[0] - (pos[0] % DEFAULT_TILE_SIZE)
	topleft_y = pos[1] - (pos[1] % DEFAULT_TILE_SIZE)
	return pygame.Rect(topleft_x, topleft_y, DEFAULT_TILE_SIZE, DEFAULT_TILE_SIZE)



def highlight_tile(tile, mark): #highlights (or unmarks) selected tile
	if mark:
		pygame.draw.rect(screen, SELECTED_TILE_COLOR, pygame.Rect(tile.x, tile.y, tile.width+1, tile.height+1), 1)
	else:
		draw_image(current_img)
		for tile in tiles_selected:
			highlight_tile(tile, True)


def draw_image(image_id):
	screen.blit(images[image_id - 1], (0, 0) )


def is_valid(string):
	try:
		return int(string) and int(string) > 0 and int (string) < 118
	except ValueError:
		return False


loadImages() # loads all images from given path


while True:

	if (image_selected):
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
				sys.exit()		

			#adds the clicked tile to list and highlights it (or the opposite if it was already selected)
			if event.type == pygame.MOUSEBUTTONUP:
				tile= rectangle_from_click(pygame.mouse.get_pos())
				if tile not in tiles_selected:
					tiles_selected.append(tile)
					highlight_tile(tile, True)
				else:
					tiles_selected.remove(tile)
					highlight_tile(tile, False)

				pygame.display.flip()

			if event.type == pygame.KEYUP and event.key == pygame.K_RETURN: # Sends selected tiles to the new image generator.
				file_name= raw_input("Enter this Sprite's file name, without file extension: ")
				pygame.image.save(sprite_generator(tiles_selected), file_name + IMAGE_FILE_EXT)
				tiles_selected= []
				draw_image(current_img)
				print "Sprite file saved, you can start selecting tiles to compose a new one."
				pygame.display.flip()

			# closes current window and prompts user to pick another image
			if event.type == pygame.KEYUP and event.key == pygame.K_n:
				pygame.display.quit()
				image_selected= False
				current_img= 0
	
	else:
		image_number= raw_input("Enter image number (between 1 and " + str(AMOUNT_OF_IMAGES) + "): ")

		if(not is_valid(image_number)):
			print "The number you entered is invalid."
			continue

		current_img= int(image_number)
		screen = pygame.display.set_mode(DEFAULT_IMAGE_SIZE)
		screen.fill(BACKGROUND_COLOR)
		draw_image(current_img)
		pygame.display.flip()
		print "Select the slots to shape the new image by clicking them.\nWhen you're done with selection press return.\nTo select a new image press the 'n' key."
		image_selected= True
		









