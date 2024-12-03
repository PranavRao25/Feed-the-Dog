# from app.Layout import *
#
# class PriorityQueue:
# 	"""
# 		Min Heap Implementation
# 		Min Heap is a binary tree such that each internal node is at most the value of its childern
# 		If a node is stored at index k, its left child is at 2k+1 and right child at 2k+2
#
# 		Operations:
# 		1. getMin() - return the root of the tree O(1)
# 		2. Dequeue() - deletion of the minimum of the heap O(logN)
# 		3. Enqueue() - insertion into the heap O(logN)
# 	"""
#
# 	def __init__(self, maxsize: int, f: dict, root: Cell):
# 		self.__maxsize = maxsize
# 		self.__size = 1
# 		self.__front = 0
# 		self.__heap = [root]  # [0] * self.__maxsize
# 		self.compare_func = f
#
# 	def __parent(self, pos: int)->int:
# 		return pos//2
#
# 	def __leftChild(self, pos:int)->int:
# 		return 2*pos + 1
#
# 	def __rightChild(self, pos:int)->int:
# 		return 2*pos + 2
#
# 	def __isLeaf(self, pos:int)->bool:
# 		return pos > self.__size
#
# 	def __swap(self, pos1:int, pos2:int):
# 		self.__heap[pos1], self.__heap[pos2] = self.__heap[pos2], self.__heap[pos1]
#
# 	def __minHeapify(self, pos:int):
# 		if not self.__isLeaf(pos):  # inner node needed
# 			# if node is bigger than either of its childern
# 			if any(self.compare_func[self.__heap[pos]] >= self.compare_func[i] for i in (self.__heap[self.__leftChild(pos)], self.__heap[self.__rightChild(pos)])):
# 				if self.compare_func[self.__heap[self.__leftChild(pos)]] <= self.compare_func[self.__heap[self.__rightChild(pos)]]:
# 					# __swap with left
# 					self.__swap(pos, self.__leftChild(pos))
# 					self.__minHeapify(self.__leftChild(pos))
# 				else:
# 					# __swap with right
# 					self.__swap(pos, self.__rightChild(pos))
# 					self.__minHeapify(self.__rightChild(pos))
#
# 	def __minHeap(self):
# 		for pos in range(self.__size//2, 0, -1):
# 			self.__minHeapify(pos)
#
# 	def enqueue(self, cell:Cell):
# 		if self.__size >= self.__maxsize:
# 			raise MemoryError("Stack Overflow")
# 		self.__size += 1
# 		self.__heap.append(cell)  #[self.__size] = cell
#
# 		# maintain the min heap structure
# 		current = self.__size
# 		while self.compare_func[self.__heap[current]] <= self.compare_func[self.__heap[self.__parent(current)]]:
# 			self.__swap(current, self.__parent(current))
# 			current = self.__parent(current)
# 		self.__minHeap()
#
# 	def dequeue(self)->Cell:
# 		if self.__size == 0:
# 			raise MemoryError("Stack Empty")
#
# 		k = self.getMin()
# 		element = self.__heap.pop(self.__front)
# 		self.__heap.append(k)
# 		self.__size -= 1
# 		self.__minHeap()  # can be async
# 		return element
#
# 	def getMin(self)->Cell:
# 		return self.__heap[self.__front]
#
# 	def __len__(self)->int:
# 		return self.__size

class PriorityQueueBase:
	class _Item:
		__slots__ = '_key', '_value'

		def __init__(self, k, v):
			self._key, self._value = k, v

		def __lt__(self, other):
			return self._key < other._key

	def _is_empty(self):
		return len(self) == 0


class PriorityQueue(PriorityQueueBase):
	def __init__(self):
		self._data = []

	def _parent(self, j):
		return (j-1)//2

	def _left(self, j):
		return 2 * j + 1

	def _right(self, j):
		return 2 * j + 2

	def _has_left(self, j):
		return self._right(j) < len(self._data)

	def _has_right(self, j):
		return self._right(j) < len(self._data)

	def _swap(self, i, j):
		self._data[i], self._data[j] = self._data[j], self._data[i]

	def _upheap(self, j):
		parent = self._parent(j)
		if j > 0 and self._data[j] < self._data[parent]:
			self._swap(j, parent)
			self._upheap(parent)

	def _downheap(self, j):
		if self._has_left(j):
			left = self._left(j)
			small_child = left
			if self._has_right(j):
				right = self._right(j)
				if self._data[right] < self._data[left]:
					small_child = right
			if self._data[small_child] < self._data[j]:
				self._swap(j, small_child)
				self._downheap(small_child)

	def __len__(self):
		return len(self._data)

	def enqueue(self, key, value):
		self._data.append(self._Item(key, value))
		self._upheap(len(self._data)-1)

	def min(self):
		if self._is_empty():
			raise ValueError("Priority queue is empty.")
		item = self._data[0]
		return item._key, item._value

	def dequeue(self):
		if self._is_empty():
			raise ValueError("Priority queue is empty.")
		self._swap(0, len(self._data)-1)
		item = self._data.pop()
		self._downheap(0)
		return item._key, item._value
