from tkinter import filedialog as fd

def request_filename():
    filetypes = (
        ('image files', ['*.png', '*.jpeg', '*.jpg']),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        # initialdir='/',
        filetypes=filetypes)

    # filename = "/Users/LucasTong/Desktop/temp/badge.jpg"

    return filename

def rgb2ryb(r, g, b):
	t = type(r)

	# Remove the whiteness from the color.
	w = float(min(r, g, b))
	r = float(r) - w
	g = float(g) - w
	b = float(b) - w

	mg = max(r, g, b)

	# Get the yellow out of the red+green.
	y = min(r, g)
	r -= y
	g -= y

	# If this unfortunate conversion combines blue and green, then cut each in half to preserve the value's maximum range.
	if b and g:
		b /= 2.0
		g /= 2.0

	# Redistribute the remaining green.
	y += g
	b += g

	# Normalize to values.
	my = max(r, y, b)
	if my:
		n = mg / my
		r *= n
		y *= n
		b *= n

	# Add the white back in.
	r += w
	y += w
	b += w

	# And return back the ryb typed accordingly.
	return t(r), t(y), t(b)