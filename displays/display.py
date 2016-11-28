#!/usr/bin/python
# coding: UTF-8

# Abstract Base class to provide display primitives
# Written by: Ron Ritchey
import sys, copy, math, abc

class widget:
	__metaclass__ = abc.ABCMeta

	def __init__(self, rows, columns):
		self.rows = rows
		self.columns = columns


	# Widgets
	@abc.abstractmethod
	def text(msg, (x,y) = (0,0), (h,w)=(0,0), do=Null, fontpkg=Null, varwidth = False, just='left', vjust='top'):
		# Input
		# 	msg (unicode) -- msg to display
		#	(x,y) (integer tuple) -- Coordinates to place the message within display object
		#	(h,w) (integer tuple) -- Bounds of the rectangle that message will be written into.  If set to 0, no restriction on size.
		#	do (display object) -- If provided, the message will be placed within the provided display object
		#	fontpkg (font object) -- The font that the message should be rendered in.
		#	varwidth (bool) -- Whether the font should be displaced monospaced or variable
		#	just (unicode) -- Determines how to justify the text horizontally.  Allowed values [ 'left','right','center' ]
		#	vjust (unicode) -- Determines how to justify the text vertically.  Allowed values [ 'top', 'bottom', 'center' ]
		# Returns
		#	display object.  Will create a new one just large enought to hold the message if do is Null.
		return

	@abc.abstractmethod
	def image(file, (x,y)=(0,0), (h,w)=(0,0), do=Null)
		# Input
		#	file (unicode) -- filename of file to retrieve image from.  Must be located within the images directory.
		#	(x,y) (integer tuple) -- Coordinates to place the image within display object
		#	(h,w) (integer tuple) -- Bounds of the rectangle that image will be written into.  If set to 0, no restriction on size.
		#	do (display object) -- If provided, the image will be placed within the provided display object
		# Returns
		#	display object.  Will create a new one just large enought to hold the image if do is Null.
		return

	@abc.abstractmethod
	def progressbar(value, range, size, style, (x,y)=(0,0), do=Null)
		# Input
		#	value (numeric) -- Value of the variable showing progress.
		#	range (numeric tuple) -- Range of possible values.  Used to calculate percentage complete.
		#	size (number tuple) -- width and height to draw progress boundary
		#	style (unicode) -- Sets the style of the progress bar.  Allowed values [ 'rounded', 'square' ]
		#	(x,y) (integer tuple) -- Coordinates to place the progress bar within display object
		#	do (display object) -- If provided, the image will be placed within the provided display object
		# Returns
		#	display object.  Will create a new one just large enought to hold the image if do is Null.
		return

	@abc.abstractmethod
	def line( (x0,y0,x1,y1), (x,y)=(0,0), width=1, do=Null)
		# Input
		#	(x0,y0, x1, y1) (integer quad tuple) -- Points to draw a line between.
		#	(x,y) (integer tuple) -- Coordinates to place the image within display object
		#	width (integer) -- number of pixels/blocks wide the line should be drawn
		#	do (display object) -- If provided, the image will be placed within the provided display object
		# Returns
		#	display object.  Will create a new one just large enought to hold the image if do is Null.
		return

	@abc.abstractmethod
	def rectangle( (x0,y0,x1,y1), width=1, do=Null)
		# Input
		#	(x0,y0, x1, y1) (integer quad tuple) -- Upper left and lower right corners of the rectangle.
		#	width (integer) -- number of pixels/blocks wide the lines of the rectangle should be drawn
		#	do (display object) -- If provided, the image will be placed within the provided display object
		# Returns
		#	display object.  Will create a new one just large enought to hold the image if do is Null.
		return

	@abc.abstractmethod
	def rectangle( (x0,y0,x1,y1), width=1, do=Null)
		# Input
		#	(x0,y0, x1, y1) (integer quad tuple) -- Upper left and lower right corners of the rectangle.
		#	width (integer) -- number of pixels/blocks wide the lines of the rectangle should be drawn
		#	do (display object) -- If provided, the image will be placed within the provided display object
		# Returns
		#	display object.  Will create a new one just large enought to hold the image if do is Null.
		return


# def set(image,x,y,val):
# 	# Sets pixel at x,y to value
# 	# x is the distance in pixels from the top of the buffer (not the number of bytes)
#
# 	# Figure out what byte we are in
# 	bx = int(x/8) # Byte we are in
# 	bo = x % 8	# Offset within the byte
#
# 	# Add byte at coordinates if needed
# 	try:
# 		newval = buffer[(bx,y)]
# 	except KeyError:
# 		buffer[(bx,y)] = 0
# 		newval = 0
#
# 	newval = buffer[(bx,y)]
# 	if val:
# 		newval |= 1 << bo # Set bit
# 	else:
# 		newval = ~(1<<bo)&0xFFFF&newval # Clear bit
# 	buffer[(bx,y)] = newval

# def get(buffer,x,y):
# 	# Get current value of pixel at coordinates x,y
#
# 	bx = int(x/8)
# 	bo = x % 8
#
# 	try:
# 		vb = buffer[(bx,y)]
# 	except KeyError:
# 		return 0
#
# 	if vb & (1<<bo):
# 		return 1
# 	else:
# 		return 0

# def getbuffer(buffer,x,y,height,width):
# 	# Return buffer that is referenced from coordinates starting x,y and is the size of height,width
# 	# x,y - coordinates of the upper left portion of the display
# 	# height,width - size of the display buffer to Return
#
# 	retval = { }
#
# 	for i in range (0, width):
# 		for j in range(0, height):
# 			val = get(buffer,x+j, y+i)
# 			set(retval,j,i,val)
#
# 	return retval
def invertbits(byte):
	# Assumes 8 bit value
	if byte < 0 | byte > 255:
		raise ValueError
	retval = 0
	for i in range(0,8):
		if byte & 1:
			retval |= 1
		byte = byte >> 1
		retval = retval << 1
	retval = retval >> 1
	return retval

def getframe(image,x,y,width,height):
	# Returns an array of arrays
	# [
	#   [ ], # Array of bytes for line 0
	#   [ ]  # Array of bytes for line 1
	#				 ...
	#   [ ]  # Array of bytes for line n
	# ]

	# Select portion of image to work with
	img = image.crop( (x,y, width, height) )


	width, height = img.size
	bheight = int(math.ceil(height / 8.0))
	imgdata = list(img.getdata())


	retval = []	# The variable to hold the return value (an array of byte arrays)
	retline = [0]*width # Line to hold the first byte of image data
	bh = 0 # Used to determine when we've consumed a byte worth of the line

	# Perform a horizontal iteration of the image data
	for i in range(0,height):
		for j in range(0,width):
			# if the value is true then mask a bit into the byte within retline
			if imgdata[(i*width)+j]:
				try:
					retline[j] |= 1<<bh
				except IndexError as e:
					# WTF
					print "width = {0}".format(width)
					raise e
		# If we've written a full byte, start a new retline
		bh += 1
		if bh == 8: # We reached a byte boundary
			bh = 0
			retval.append(retline)
			retline = [0]*width
	if bh > 0:
		retval.append(retline)

	return retval

def scrollbuffer(image, direction=u'left', distance=1):
	direction = direction.lower()

	# Save region to be overwritten
	# Move body
	# Restore region to cleared space

	width, height = image.size

	if direction == u'left':
		region = image.crop((0,0, distance, height))
		body = image.crop((distance,0, width, height))
		image.paste(body, (0,0))
		image.paste(region, ((width-distance),0) )
	elif direction == u'right':
		region = image.crop((width-distance,0, width, height))
		body = image.crop((0,0, width-distance, height))
		image.paste(body, (distance,0) )
		image.paste(region, (0,0) )
	elif direction == u'up':
		region = image.crop((0,0, width, distance))
		body = image.crop((0,distance, width, height))
		image.paste(body, (0,0) )
		image.paste(region, (0,height-distance) )
	elif direction == u'down':
		region = image.crop((0,height-distance, width, height))
		body = image.crop((0,0, width, height-distance))
		image.paste(body, (0,distance) )
		image.paste(region, (0,0) )


def show(bytebuffer,width, height):

	for i in range(0,height):
		for k in range(0,8):
				for j in range(0,width):
					mask = 1 << k
					if bytebuffer[i][j]&mask:
						sys.stdout.write('*')
						sys.stdout.flush()
					else:
						sys.stdout.write(' ')
						sys.stdout.flush()
				print ''

def clear(image,x,y,width,height):
	draw = ImageDraw.Draw(image)
	draw.rectangle((x,y, x+width-1, y+height-1),0)

def msgwidth(msg, fontpkg, varwidth=False):
 	(fx, fy) = fontpkg['size']
 	retval = [ ]
 	clp = 0 # Current line pixel used count

	for c in msg:
		if c == u'\n':
			if clp == 0:
				retval.append(0)
			else:
				retval.append(clp-1)
			clp = 0
			continue

		if varwidth:
			try:
				clp += fontpkg[ord(c)].width+1
			except:
				clp += fontpkg[ord('?')].width+1
		else:
			clp += fx+1
	retval.append(clp-1)
	return retval

 # 	for c in msg:
 # 		if c == u'\n':
 # 			retval.append(clp-1)
 # 			clp = 0
 # 			continue
	#
 # 		bytearray = copy.copy(fontpkg[ord(c)])
 # 		if varwidth and ord(c) != 0x20: # if variable width requested and char is not a space
 # 			try:
 # 				# Trim left
 # 				while bytearray[0] == 0:
 # 					del bytearray[0]
 # 				# Trim right
 # 				for i in range(len(bytearray)-1,0,-1):
 # 					if bytearray[i] == 0:
 # 						del bytearray[i]
 # 			except IndexError:
 # 				# bytearray for this character was empty
 # 				pass
	#
 # 		for val in bytearray:
 # 			clp += 1
 # 		# Add pixel wide gap between characters
 # 		clp += 1
 # 	retval.append(clp-1)
	#
 # 	return retval

def line(image,x0, y0, x1, y1, color=1):
	draw = ImageDraw.Draw(image)
	draw.line((x0,y0,x1,y1),color)

def message(image,msg,x,y,fontpkg,varwidth = False, just='left', height=0, width=0):

	(fx,fy) = fontpkg['size']
	cx = x
	cy = y

	for c in msg:

		# If newline, move y to next line (based upon font height) and return x to beginning of line
		if c == u'\n':
			cy = cy + fy
			cx = x
			continue

		try:
			charimg = fontpkg[ord(c)]
		except KeyError:
			# Requested character does not exist in font.  Replace with '?'
			charimg = fontpkg[ord('?')]

		# if varwidth and ord(c) != 0x20: # if variable width requested and char is not a space
		# 	try:
		# 		# Trim left
		# 		while bytearray[0] == 0:
		# 			del bytearray[0]
		# 		# Trim right
		# 		for i in range(len(bytearray)-1,0,-1):
		# 			if bytearray[i] == 0:
		# 				del bytearray[i]
		# 	except IndexError:
		# 		# bytearray for this character was empty
		# 		pass

		# # Place character bitmap into frame buffer
		# for val in bytearray:
		# 	cy = y
		# 	for i in range(0,fy):
		# 		# Test bit
		# 		tb = 1
		# 		if val & (1<<i):
		# 			tv = 1
		# 		else:
		# 			tv = 0
		# 		image.putpixel((cx,cy),tv)
		# 		cy += 1
		# 	cx += 1
		#
		# # Add pixel wide gap between characters
		# cy = y
		# for i in range(0,fy):
		# 	image.putpixel((cx,cy),0)
		# 	cy += 1
		# cx += 1

		# Adjust charimg if varwidth is False
		if not varwidth:
			offset = (fx-charimg.width)/2
			charimg = copy.copy(charimg).crop( (-offset,0,fx-offset,fy) )

		# Paste character into frame
		image.paste(charimg, (cx,cy))

		# Erase space between characters
		clear(image,cx+charimg.width,cy,1,fy)

		# Move to next character position
		if varwidth:
			cx += charimg.width+1
		else:
			cx += fx+1