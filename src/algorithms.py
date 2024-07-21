from collections import deque
from typing import Any

from .node import Node


def slice_and_dice(tree: Node, w: int, h: int) -> dict[Any: tuple[int, int, int, int]]:
	"""Each node labeled "None" is assumed to be a non-leaf node.

	:param tree: Root node of the binary tree to be visualized
	:type tree: Node
	:param w: Width of the canvas
	:type w: int
	:param h: Height of the canvas
	:type h: int
	:return: Dictionary of labels and their corresponding coordinates (x0, y0, x1, y1)
	:rtype: dict[Label: tuple[int, int, int, int]]
	"""
	result = {}

	horizontal = True

	queue = deque([(2, 2, w, h, tree)])
	while queue:
		x0, y0, x1, y1, node = queue.popleft()
		if node.label:
			result[node.label] = x0, y0, x1, y1
			continue

		if horizontal:
			midpoint = int(x0 + (x1 - x0) * node.left.value/ node.value)
			queue.extend([
				(x0, y0, midpoint, y1, node.left),
				(midpoint, y0, x1, y1, node.right),
			])
		else:
			midpoint = int(y0 + (y1 - y0) * node.left.value / node.value)
			queue.extend([
				(x0, y0, x1, midpoint, node.left),
				(x0, midpoint, x1, y1, node.right),
			])

		horizontal = not horizontal

	return result
