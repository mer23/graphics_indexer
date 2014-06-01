import sys, os, pygame, ConfigParser
pygame.init()

IMAGES_PATH= "Skins/Default/Tiles/"
IMAGE_FILE_EXT= ".png"
AMOUNT_OF_IMAGES= 117
SAVED_SPRITES_LOGS_FILE= "graficos.ind"

###### OPTIONS ########
SOURCE_KEY= "source"
X_OFFSET_KEY= "offset_X"
Y_OFFSET_KEY= "offset_Y"
WIDTH_KEY= "width"
HEIGHT_KEY= "height"
DESC_KEY= "desc"
#######################
offset= 0,0 # used to set offset value for each sprite saved at logs file
DEFAULT_TILE_SIZE= 32
DEFAULT_IMAGE_SIZE= 1024, 256

SELECTED_TILE_COLOR= 0, 255, 18
BACKGROUND_COLOR= 0,0,0

current_img= 0
sprite_file_name= 1
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

	global offset
	offset= (DEFAULT_IMAGE_SIZE[1] - bottommost) / DEFAULT_TILE_SIZE , leftmost / DEFAULT_TILE_SIZE #offset is messured in tiles
	
	return pygame.transform.rotate(sprite, -90)


def save_sprite(description, file_name= None):
	global sprite_file_name

	if file_name is None:
		file_name= str(sprite_file_name)

	if parser.has_section(file_name):
		while True:		
			overwrite= raw_input("This name is already in use by another sprite from source image: " + parser.get(file_name, SOURCE_KEY) + IMAGE_FILE_EXT + ", desc: " + parser.get(file_name, DESC_KEY) + "." + "Do you want to overwrite it?(Y/N)")

			if overwrite.lower() == "y":
				pass

			elif overwrite.lower() == "n":
				return False

			else:
				print "Your answer wasn't understood."
				continue

			break

	sprite= sprite_generator(tiles_selected)

	pygame.image.save(sprite, file_name + IMAGE_FILE_EXT)

	############################ WRITE SPRITE LOGS ###############################
	parser.add_section(file_name) # add sprite header

	try: # add all key-value pairs for this sprite
		parser.set(file_name, SOURCE_KEY, str(current_img))
		parser.set(file_name, X_OFFSET_KEY, str(offset[0]))
		parser.set(file_name, Y_OFFSET_KEY, str(offset[1]))
		parser.set(file_name, WIDTH_KEY, str(sprite.get_width()))
		parser.set(file_name, HEIGHT_KEY, str(sprite.get_height()))
		parser.set(file_name, DESC_KEY, description)

	#section is added before the try so it's virtually impossible to reach the exception
	except ConfigParser.NoSectionError:
		print "FATAL: HOW DID WE GET HERE IF SECTION WAS JUST ADDED TO LOGS? \nError ocurred while trying to write logs for sprite " + str(sprite_file_name) + " from source image " + str(current_img) + IMAGE_FILE_EXT + "." 

	with open(SAVED_SPRITES_LOGS_FILE, "r+") as logs_file:
		parser.write(logs_file) # write everything to file
	###############################################################################

	print "Sprite file saved as " + file_name + IMAGE_FILE_EXT +". \n" + "You can continue highlighting tiles to compose a new sprite."

	if file_name == str(sprite_file_name):
		sprite_file_name += 1

	return True


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


def is_valid_source(string):
	try:
		return int(string) and int(string) > 0 and int (string) < AMOUNT_OF_IMAGES + 1
	except ValueError:
		return False

def is_valid_sprite_name(string):
	try:
		return int(string) and int(string) > 0
	except ValueError:
		return False

def display_commands():
	print "------------------------- USAGE -------------------------"
	print "* mark/unmark tile\t\t\tMOUSE CLICK"
	print "* load new source image\t\t\tN"
	print "* save selection under default name\tRETURN"
	print "* save selection under custom name\tS"
	print "* display sprite info\t\t\tI"
	print "* check sprite existence\t\tE"
	print "* delete sprite\t\t\t\tD"
	print "* program commands\t\t\tC"
	print "* close program\t\t\t\tESCAPE"
	print "---------------------------------------------------------"


def get_sprite_info(sprite_file_name):
	with open(SAVED_SPRITES_LOGS_FILE, "r") as logs_file:
		if parser.has_section(sprite_file_name):
			print "-------------------- " + sprite_file_name + IMAGE_FILE_EXT + " -------------------"
			print "Source image: " + IMAGES_PATH + parser.get(sprite_file_name, SOURCE_KEY) + IMAGE_FILE_EXT
			print "Offset (in tiles): (" + parser.get(sprite_file_name, X_OFFSET_KEY) + ", " + parser.get(sprite_file_name, Y_OFFSET_KEY) + ")"
			print "Width: " + parser.get(sprite_file_name, WIDTH_KEY) + " pixels"
			print "Height: " + parser.get(sprite_file_name, HEIGHT_KEY) + " pixels"
			print "Description: " + parser.get(sprite_file_name, DESC_KEY)
			print "----------------------------------------------//"
			return True

		return False


def delete_sprite(sprite_file_name):
	with open(SAVED_SPRITES_LOGS_FILE, "w") as logs_file:
		if parser.has_section(sprite_file_name):
			parser.remove_section(sprite_file_name) # deletes sprite from logs
			parser.write(logs_file) # update file

		if(os.path.exists(sprite_file_name + IMAGE_FILE_EXT)):	
			os.remove(sprite_file_name + IMAGE_FILE_EXT) #deletes sprite file
			return True

		return False


def sprite_exists(sprite): #if a tile exists it displays its info, if it doesn't it notifies so.
	global offset

	with open(SAVED_SPRITES_LOGS_FILE, "r") as logs_file:
		parser.readfp(logs_file)

		if not parser.sections(): return False

		for log in range (1, int(max(parser.sections())) + 1):
			log_name= str(log)
			if parser.has_section(log_name):
				if current_img == int( parser.get(log_name, SOURCE_KEY) ) and offset[0] == int( parser.get(log_name, X_OFFSET_KEY) ) and offset[1] == int( parser.get(log_name, Y_OFFSET_KEY) ):
					return get_sprite_info(log_name)

		return False



loadImages() # loads all images from given path
parser= ConfigParser.RawConfigParser()

#Sets sprite_file_name, which keeps track of the file names (numbers) already used. 
#Current value of sprite_file_name will be used as the name for next sprite saved.
with open(SAVED_SPRITES_LOGS_FILE, "r") as logs_file:
	parser.readfp(logs_file) #loads log file into this parser
	if parser.sections(): 
		sprite_file_name= int(max(parser.sections())) + 1 #sets sprite_file_name according to last sprite file saved in logs.

#main infinite loop
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

				if tiles_selected:
					while True:
						description= raw_input("Enter a brief description for this sprite: ")

						if save_sprite(description):
							tiles_selected= []
							draw_image(current_img)
							pygame.display.flip()

						break
				else: "You must select one or more tiles in order to build a sprite."


			if event.type == pygame.KEYUP and event.key == pygame.K_d:
				sprite_to_delete= raw_input("Enter number of sprite to delete: ")
				if delete_sprite(sprite_to_delete):
					print "File '" + str(sprite_to_delete) + IMAGE_FILE_EXT + "' was successfully deleted."
				else:
					print "File '" + str(sprite_to_delete) + IMAGE_FILE_EXT + "' doesn't exist."


			if event.type == pygame.KEYUP and event.key == pygame.K_i:
				sprite_requested= raw_input("Enter sprite number from which info is required: ")
				if not get_sprite_info(sprite_requested):
					print "Sprite doesn't exist."


			# closes current window and prompts user to pick another image
			if event.type == pygame.KEYUP and event.key == pygame.K_n:
				pygame.display.quit()
				image_selected= False
				current_img= 0

			if event.type == pygame.KEYUP and event.key == pygame.K_s:
				if tiles_selected:

					while True:
						file_name= raw_input("Enter a name to build sprite from current selection: ")
						if not is_valid_sprite_name(file_name):
							print "Name must be an positive integer."
							continue
						else: break

					description= raw_input("Enter a brief description for the sprite: ")

					if save_sprite(description, file_name):
						tiles_selected= []
						draw_image(current_img)
						pygame.display.flip()

				else: "You must select one or more tiles in order to build a sprite."


			if event.type == pygame.KEYUP and event.key == pygame.K_e:
				if tiles_selected:
					if not sprite_exists(sprite_generator(tiles_selected)):
						print "The sprite doesn't exist"
				else:
					print "No sprite is selected! You must select one or more tiles to check if the sprite they form already exists."


			if event.type == pygame.KEYUP and event.key == pygame.K_c:
				display_commands()
	
	else:
		image_number= raw_input("Enter image number (between 1 and " + str(AMOUNT_OF_IMAGES) + "): ")

		if(not is_valid_source(image_number)):
			print "The number you entered is invalid."
			continue

		current_img= int(image_number)
		screen = pygame.display.set_mode(DEFAULT_IMAGE_SIZE)
		screen.fill(BACKGROUND_COLOR)
		draw_image(current_img)
		pygame.display.flip()
		print "Select image tiles to shape a new sprite by clicking them.\nWhen you're done with selection press return.\nPress 'C' to display commands list."
		image_selected= True
		









