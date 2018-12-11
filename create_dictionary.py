class Item_Dictionary:
	def __init__(self,byte_list, index):
		self.byte_list = byte_list
		self.index = index
		self.counter = 0
		self.size = len(byte_list)

		if index == 0:
			self.transitions = {}
		else:
			self.transitions = {}

	def is_item(self,byte_list):
		return ((byte_list > self.byte_list) - (byte_list < self.byte_list)) == 0;

	def can_split(self):
		return self.size > 1

	def split(self,index):
		item = Item_Dictionary(self.byte_list[self.size/2:], index)
		item.counter = self.counter
		item.transitions = self.transitions;
		self.transitions = {}
		self.transitions[ item.index ] = item.counter
		self.size = self.size/2
		return item

	def increment(self, index ):
		self.counter += 1

		if not index in self.transitions:
			self.transitions[index] = 0

		self.transitions[ index ] += 1

	def remove_index(self, index_to_delete, index_to_receive ):
		if not index_to_delete in self.transitions:
			self.transitions[ index_to_delete ] = 0

		if not index_to_receive in self.transitions:
			self.transitions[ index_to_receive ] = 0

		self.transitions[ index_to_receive ] += self.transitions[ index_to_delete ]
		del self.transitions[ index_to_delete ]


class Dictionary_Builder:
	def __init__(self,max_items,max_size ):
		self.dictionary = []
		self.max_items = max_items
		self.current_max_size = max_size
		self.current_min_size = max_size
		self.previous = 0
		self.counter = 0

	def add_item(self, item):
		self.dictionary.append( item )
		self.counter += 1

	def add(self,byte_list):

		if not self.dictionary:
			item_dictionary = Item_Dictionary(byte_list, self.counter )
			self.add_item( item_dictionary )
			self.previous = 0
			return

		index = self.in_dictionary(byte_list)

		if index != -1:
			self.dictionary[ self.previous ].increment( index )
			return

		new_index = len(self.dictionary)
		item_dictionary = Item_Dictionary(byte_list, self.counter )
		self.add_item( item_dictionary )

		self.dictionary[ self.previous ].increment( new_index )

		while len(self.dictionary) > self.max_items:
			print("LEN "+str(len(self.dictionary))+" mxi"+str(self.max_items)+"Spliting" )
			self.split_process()


		item_max = max(self.dictionary, key=lambda item: item.size )
		self.current_max_size = item_max.size;

		print("MAx size"+str(self.current_max_size ) )
		item_min = min(self.dictionary, key=lambda item: item.size )
		self.current_min_size = item_min.size
		print("Min size"+str(self.current_min_size))


	def in_dictionary(self, byte_list):
		for i in self.dictionary:
			if i.is_item( byte_list ):
				return i.index

		return -1


	def split_process(self):

		max_size = max(self.dictionary, key=lambda item: item.size )
		self.current_max_size = max_size;

		list_candidates = filter(lambda x: x.size == max_size, self.dictionary )
		list_candidates.sort(key=lambda x: x.counter)

		self.dictionary.sort(key=lambda e: e.index)

		item_to_split = list_candidates[0];
		new_item = item_to_split.split( self.counter )
		self.add_item( new_item )

		if self.previous == item_to_split.index:
			self.previous = new_item.index


		self.search_and_remove_item( item_to_split )
		self.search_and_remove_item( new_item )


	#new item is gonna be romoved
	def search_and_remove_item(self, new_item):
		old_item = None
		for index,value in enumerate(self.dictionary):
			if index != new_item.index:
				if value.is_item( new_item.byte_list):
					old_item = value
					break

		if old_item is not None:
			for item in self.dictionary:
				item.remove_index( new_item.index, old_item.index )

			if self.previous == new_item.index:
				self.previous = old_item.index

	def continue_reading(self, byte_list):
		if len( byte_list ) < self.current_max_size:
			if len(byte_list) < self.current_min_size:
				return True

			for i in self.dictionary:
				if ((i>byte_list)-(i<byte_list)) == 0:
					return False

			return True

		return False

	def printx(self):
		elements = []
		for i in self.dictionary:
			i.byte_list.append( "trans = "+str( i.counter ) )
			elements.append( i.byte_list )

		print( elements )


if __name__ == "__main__":

	byte_list = [ 0, 0, 0, 0, 0, 0, 0, 1, 0, 0,1, 2, 3, 4, 0, 0, 2,0,2 ,0, 2, 0, 0, 0, 0, 0, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 2, 3, 4, 5]
	print( byte_list )

	dic = Dictionary_Builder( 256, 4 )
	current = []

	while byte_list:
		current.append( byte_list.pop(0) )
		if not dic.continue_reading( current ):
			print("Adding "+str(current) )
			dic.add( current )
			current = []

	if current:
		dic.add( current )

	dic.printx()
