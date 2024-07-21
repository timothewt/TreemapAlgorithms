import json
from collections import deque
import tkinter as tk
from typing import Any

import numpy as np

from .node import Node


def rgb_to_hex(rgb: tuple[int, int, int]):
	"""Converts an RGB tuple to a hexadecimal color string.

	:param rgb: An RGB tuple (r, g, b) from 0 to 255
	:type rgb: tuple[int, int, int]
	:return: The corresponding hexadecimal color string
	:rtype: str
	"""
	return "#%02x%02x%02x" % rgb


def list_to_tree(labels: list[Any], values: np.ndarray) -> Node:
	"""Creates a binary tree from a list where each leaf is an item,
	and each non-leaf node holds the sum of its children values.

	An element in the queue is a tuple of a node and its children labels and values.

	:param labels: The items labels
	:type labels: list[Label]
	:param values: The values of the items
	:type values: np.ndarray
	:return: The root node of the binary tree
	:rtype: Node
	"""
	assert len(labels) == len(values), "Length of labels and values must be the same!"
	norm_values = values / np.sum(values)
	sorted_idx = np.argsort(-norm_values)
	labels = [labels[i] for i in sorted_idx]

	root = Node(None, np.sum(norm_values))
	queue = deque([(root, labels, norm_values[sorted_idx])])

	while queue:
		parent, labs, vals = queue.popleft()
		if len(vals) == 1:
			parent.label = labs[0]
			parent.value = vals[0]
			continue

		midpoint = np.sum(vals) / 2
		left_sum, idx = 0, 0
		while left_sum < midpoint and idx < len(vals) - 1:
			left_sum += vals[idx]
			idx += 1

		left = Node(None, left_sum)
		right = Node(None, np.sum(vals) - left_sum)
		parent.left, parent.right = left, right
		queue.extend([
			(left, labs[:idx], vals[:idx]),
			(right, labs[idx:], vals[idx:])
		])

	return root


def draw_layout(coords: dict[str, tuple[int, int, int, int]], w: int, h: int) -> None:
	"""Draws rectangles on a tkinter canvas based on the coordinates.

	:param coords: The dictionary of labels and their coordinates
	:type coords: dict[str, tuple[int, int, int, int]]
	:param w: The width of the canvas
	:type w: int
	:param h: The height of the canvas
	:type h: int
	"""
	root = tk.Tk()
	canvas = tk.Canvas(root, width=w, height=h)

	for label, (x0, y0, x1, y1) in coords.items():
		canvas.create_rectangle(x0, y0, x1, y1, fill=rgb_to_hex((np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))))
		canvas.create_text((x0 + x1) // 2, (y0 + y1) // 2, text=label, fill="white", font="Arial 20 bold")

	canvas.pack()
	root.mainloop()


def read_data(data_file_name: str) -> tuple[list[str], np.ndarray]:
	"""Reads the data from a JSON file.

	:param data_file_name: The name of the JSON file
	:type data_file_name: str
	:return: The labels and values from the JSON file
	:rtype: tuple[list[str], np.ndarray]
	"""
	with open(f"data/{data_file_name}", "r") as f:
		data = json.load(f)
		labels = list(data.keys())
		values = np.array(list(data.values()))
	return list_to_tree(labels, values)
