from src import slice_and_dice, read_data, draw_layout


def main(data_file_name: str = "data.json", w: int = 1280, h: int = 720) -> None:
	"""Main loop. Reads the data from a json files, uses a Treemap algorithm
	and displays it in a window.

	:param data_file_name: The name of the data file
	:type data_file_name: str
	:param w: The window width
	:type w: int
	:param h: The window height
	:type h: int
	"""

	tree = read_data(data_file_name)
	coords = slice_and_dice(tree, w, h)
	draw_layout(coords, w, h)


if __name__ == "__main__":
	main()
