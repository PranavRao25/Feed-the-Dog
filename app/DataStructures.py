class PriorityQueue:
	"""
		Min Heap Implementation
		Min Heap is a binary tree such that each internal node is at most the value of its childern
		If a node is stored at index k, its left child is at 2k+1 and right child at 2k+2

		Operations:
		1. getMin() - return the root of the tree O(1)
		2. Dequeue() - deletion of the minimum of the heap O(logN)
		3. Enqueue() - insertion into the heap O(logN)
	"""

	def __init__(self, maxsize, f, root):
		self.__maxsize = maxsize
		self.__size = 0
		self.__front = 0
		self.__heap = [root]  # [0] * self.__maxsize
		self.compare_func = f

	def __parent(self, pos):
		return pos//2

	def __leftChild(self, pos):
		return 2*pos + 1

	def __rightChild(self, pos):
		return 2*pos + 2

	def __isLeaf(self, pos):
		return pos > self.__size

	def __swap(self, pos1, pos2):
		self.__heap[pos1], self.__heap[pos2] = self.__heap[pos2], self.__heap[pos1]

	def __minHeapify(self, pos):
		if not self.__isLeaf(pos):  # inner node needed
			# if node is bigger than either of its childern
			if any(self.__compare_func(self.__heap[pos]) >= self.__compare_func(i) for i in (self.__heap[self.__leftChild(pos)], self.__heap[self.__rightChild(pos)])):
				if self.__compare_func(self.__heap[self.__leftChild(pos)]) <= self.__compare_func(self.__heap[self.__rightChild(pos)]):
					# __swap with left
					self.__swap(pos, self.__leftChild(pos))
					self.__minHeapify(self.__leftChild(pos))
				else:
					# __swap with right
					self.__swap(pos, self.__rightChild(pos))
					self.__minHeapify(self.__rightChild(pos))

	def __minHeap(self):
		for pos in range(self.__size//2, 0, -1):
			self.__minHeapify(pos)

	def enqueue(self, cell):
		if self.__size >= self.__maxsize:
			raise MemoryError("Stack Overflow")
		self.__size += 1
		self.__heap.append(cell)  #[self.__size] = cell

		# maintain the min heap structure
		current = self.__size
		while self.__compare_func(self.__heap[current]) <= self.__compare_func(self.__heap[self.__parent(current)]):
			self.__swap(current, self.__parent(current))
			current = self.__parent(current)
		self.__minHeap()

	def dequeue(self):
		if self.__size == 0:
			raise MemoryError("Stack Empty")

		element = self.__heap.pop(self.__front)
		self.__heap[self.__front] = self.__heap[self.__size]
		self.__size -= 1
		self.__minHeap()  # can be async
		return element

	def getMin(self):
		return self.__heap[self.__front]

	def __len__(self):
		return self.__size