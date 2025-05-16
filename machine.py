
class Rotor:
	def __init__(self, num):
		self.num = num
		self.rotate_state = 0

		split_point = int(batch_o[num*2])
		mode = int(batch_o[num*2+1])
		table = origin_table[split_point:] + origin_table[:split_point]

		if mode:
			self.table = ''
			for s in range(13):
				self.table += table[s] + table[s+13]
		else:
			self.table = table

	def replace(self, index):
		# 按照自己的替换表执行一次字母替换
		#
		# 返回替换的字符的数字位置

		index = (index + self.rotate_state) % 26
		letter = self.table[index]
		index = (ord(letter) - 97 - self.rotate_state) % 26

		return index

	def reverse_replace(self, index):
		# 按照自己的替换表执行一次反向字母替换
		#
		# 返回替换的字符的数字位置

		index = (index + self.rotate_state) % 26
		letter = chr(97+index)
		index = (self.table.find(letter) - self.rotate_state) % 26

		return index

class ReflectBoard(Rotor):
	def __init__(self, num):
		super().__init__(num)

	def reflect(self, index):
		# 这将会变换输入的字母并反射回转子

		letter = chr(97+index)
		index = self.table.find(letter)

		if index % 2:
			letter = self.table[index-1]
		else:
			letter = self.table[index+1]
		index = ord(letter) - 97

		return index

class Keyboard:
	def __init__(self):
		s = sum([int(s) for s in batch_o]) 
		if s % 2:
			t = origin_table
			self.table = ''.join([t[s]+t[s+13] for s in range(0,12,2)])
		else:
			self.table = origin_table[6:19]

	def in_put(self, letter):
		# 输入字母变换后输出

		letter = self.exchange(letter)
		index = ord(letter) - 97
		index = transform(index)
		letter = chr(97+index)
		letter = self.exchange(letter)

		return letter

	def exchange(self, letter):
		# 模拟接线板的功能，交换六对字母

		if letter in self.table:
			index = self.table.find(letter)
			if index % 2:
				letter = self.table[index-1]
			else:
				letter = self.table[index+1]

		return letter

def transform(index):
	# 将字母依次通过转子的变换然后输出

	for rotor in rotor_group:
		index = rotor.replace(index)
	index = reflect_board.reflect(index)
	for rotor in rotor_group[::-1]:
		index = rotor.reverse_replace(index)

	return index

origin_table = 'bimrqvdwhsnozgfpjaxeytulkc'
batch_o = '30714091'

rotor_group = []
for s in range(3):
	s = Rotor(s)
	rotor_group.append(s)
reflect_board = ReflectBoard(len(rotor_group))
keyboard = Keyboard()
