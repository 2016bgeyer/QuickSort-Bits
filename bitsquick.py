# My pseudocode for bits quick:
from random import randrange, randint
import os
import math
comparisons = 0
bitcounts = 0
bitcomparisons = 0
class Row():
	def __init__(self, bitlist, places = 0):
		self.bitlist = bitlist
		self.places = places
	
	def to_int(self, use_places = True):
		index = self.places if use_places else 0
		return list_to_int(self.bitlist[index:])

	def __str__(self):
		return str((self.bitlist, self.places, self.to_int(False)))
	
	def __repr__(self):
		return str(self.to_int(False)) # str((self.bitlist, self.places, self.to_int(False)))

def random_number(n_bits):
	return [randint(0, 1) for _ in range(0, n_bits)]

def get_data(n_runs, n_nums, n_bits):
	runs = []
	for i in range(n_runs):
		filename = f'data/{n_nums}_{n_bits}_{i}.txt'
		if not os.path.exists(filename): # if the file doesn't exist, generate it
			with open(filename, 'w+') as f:
				# arr = [random_number(n_bits) for _ in range(n_nums)]
				for _ in range(n_nums):
					f.write(str(random_number(n_bits)) + '\n')
		runs.append(read_bits(filename))
	return runs

def read_bits(filename):
	import json
	with open(filename, 'r') as f:
		lines = f.readlines()
		arr = [Row(json.loads(line[:-1])) for line in lines]
		return arr
	

def rotate_array_right(array, m):
	# rotate right by m places
	for row in array:
		row = rotate_row_right(row, m)
	return array

def rotate_row_right(row, m):
	# rotate right by m places
	# print(f'\nbeforerotate_row_right row: {row} -m: {-m}')
	
	row.places -= m
	# if row.places > n_bits or m > n_bits:
	# 	print(f'row: {row}')
	# 	print(f'm: {m}')

	# print(f'after rotate_row_right row: {row} -m: {-m}')
	return row

def rotate_row_left(row, m1):
	# rotate the row left m1 places
	# LM1 in the paper
	# if m1!=0:
	# 	print(f'beforerotate_row_left row: {row} m1: {m1}')
	
	row.places += m1
	# row.places = m1
	# if row.places > n_bits or m1 > n_bits:
	# 	print(f'row: {row}')
	# 	print(f'm1: {m1}')

	# if m1!=0:
	# 	print(f'after rotate_row_left row: {row} m1: {m1}')
	return row

def list_to_int(bitlist):
	result = 0
	for bit in bitlist:
		result = (result << 1) | bit
	return result


	
def row_less_than(a, b):
	global comparisons, n_bits, bitcomparisons
	comparisons += max(n_bits, n_bits - a.places)# only compare the unknown bits (upper bound of upper_comparisons)
	i = a.places
	a_bit = 0
	b_bit = 0
	bitcomparisons += 1
	while i < n_bits and a_bit == b_bit:
		a_bit = a.bitlist[i]
		b_bit = b.bitlist[i]
		bitcomparisons += 1
		i += 1

	bitcomparisons += 1
	estimated = a_bit <= b_bit
	first = a.to_int()
	second = b.to_int()
	actual = first <= second
	if estimated != actual:
		print(f'\nfirst: {first}')
		print(f'second: {second}')
		print(f'actual: {actual}')
		print(f'estimated: {estimated}')
		exit(0)
	return actual

def rejoin(less, x, more):
	joined = less + [x] + more
	return joined

def is_sorted(array):
	return all(array[i].to_int(False) <= array[i + 1].to_int(False) for i in range(len(array)-1))

def bitsquick(A, m):
	global bitcounts
	# The input m indicates how many bits each element of the
	# array A needs to be rotated to the right before the routine terminates,
	
	# Rm(A) (in the last line of the pseudocode) is the resulting array 
	# after these right-rotations.
	if len(A) <= 1:
		return rotate_array_right(A, m)
	A_less = []
	A_more = []
	
	rand_pivot_index = randrange(len(A))
	x = A[rand_pivot_index]	# pivot number/row
	# print(f'rand_pivot x: {x}')

	m1 = 0

	bitcounts += 1	# for either while comparison about to occur
	# print('bitcount')
	if x.bitlist[0] == 0:
		# m1 = 1
		while m1+1 < len(x.bitlist) and x.bitlist[m1+1] == 0:	# continue to first non-0 bit
			m1 += 1
			bitcounts += 1
			# print('bitcount')
		for index, y in enumerate(A):
			if index != rand_pivot_index:	# only consider rows that aren't the pivot
				if row_less_than(y, x):	# y < x
					y = rotate_row_left(y, m1)
					A_less.append(y) # union in the doc
				else:
					A_more.append(y) # union in the doc
		A_less = bitsquick(A_less, m1)
		A_more = bitsquick(A_more, 0)
		A = rejoin(A_less, x, A_more)
	else:
		# m1 = 1
		while m1+1 < len(x.bitlist) and x.bitlist[m1+1] == 1:	# continue to first non-1 bit
			m1 += 1
			bitcounts += 1
			# print('bitcount')
		for index, y in enumerate(A):
			if index != rand_pivot_index:	# only consider rows that aren't the pivot
				if row_less_than(y, x):	# y < x
					A_less.append(y) # union in the doc
				else:
					y = rotate_row_left(y, m1)
					A_more.append(y) # union in the doc
		A_less = bitsquick(A_less, 0)
		A_more = bitsquick(A_more, m1)
		A = rejoin(A_less, x, A_more)

	right_rotated_result = rotate_array_right(A, m)
	# print(f'right_rotated_result: {right_rotated_result}')
	return right_rotated_result


if __name__ == '__main__':
	
	# full_test = False
	# filename = 'QuickSort.txt' if full_test else 'small_test.txt'
	# f = open(filename, 'r')
	# bit_length = 14
	# arr = [Row(int_to_list(int(number_string), bit_length)) for number_string in f]

	n_runs = 20
	for n_nums in [5000]:
		for n_bits in [15]:
			twenty_runs = get_data(n_runs, n_nums, n_bits)

			total_comparisons = 0
			total_bitcounts = 0
			total_bitcomparisons = 0

			for arr in twenty_runs:
				comparisons = 0
				bitcounts = 0
				bitcomparisons = 0
				n = len(arr) 
				# print(f'n: {n}')
				# print(f'Unsorted array is: {arr}')

				sorted_arr = bitsquick(arr,0) 
				# print(f'# of Comparisons total: {comparisons}')
				# print(f'# of bitcounts: {bitcounts}')
				# print(f'Final array is: {sorted_arr}')
				if not is_sorted(sorted_arr):
					print('NOT SORTED: ', sorted_arr[:100])
				# print(f'The array is sorted: {is_sorted(sorted_arr)}')
				
				total_comparisons += comparisons
				total_bitcounts += bitcounts
				total_bitcomparisons += bitcomparisons
			
			print(f'\nn_nums: {n_nums}')
			print(f'n_bits: {n_bits}')

			print(f'Average comparisons: {total_comparisons/n_runs}')
			print(f'Average bitcounts: {total_bitcounts/n_runs}')
			print(f'Average bitcomparisons: {total_bitcomparisons/n_runs}')
			
			expected = (2 + 3/math.log(2)) * n *math.log(n) - n*13.9 + math.log2(n)
			print(f'Expected # of Comparisons: {expected}')