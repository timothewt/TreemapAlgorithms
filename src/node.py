from __future__ import annotations

from collections import deque
from typing import Any


class Node:
	def __init__(self, label: Any, value: float, left: Node = None, right: Node = None):
		self.label = label
		self.value = value
		self.left = left
		self.right = right

	def __str__(self):
		result = ""
		queue = deque([(0, self)])
		while queue:
			depth, node = queue.popleft()
			result += (depth - 1) * "\t" + (depth > 0) * "|-" + f"{node.label} ({node.value})\n"
			if node.right:
				queue.appendleft(
					(depth + 1, node.right)
				)
			if node.left:
				queue.appendleft(
					(depth + 1, node.left)
				)
		return result
