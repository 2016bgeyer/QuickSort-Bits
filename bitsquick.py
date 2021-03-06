# My pseudocode for bits quick:
from random import randrange, randint
import os
import math
max_comparisons = 0
bitcomparisons = 0
class Row():
	def __init__(self, bitlist, places = 0):
		self.bitlist = bitlist
		self.places = places	# places indicates the first unknown value index
	
	def __repr__(self):
		return str(list_to_int(self.bitlist))
		# return str((list_to_int(self.bitlist), self.bitlist, self.places))

def random_number(n_bits):
	return [randint(0, 1) for _ in range(0, n_bits)]

def get_data(n_runs, n_nums, n_bits):
	runs = []
	for i in range(n_runs):
		if not os.path.exists('data'): # if the data dir doesn't exist, generate it
			os.makedirs('data')
		filename = f'data/{n_nums}_{n_bits}_{i}.txt'
		if not os.path.exists(filename): # if the file doesn't exist, generate it
			with open(filename, 'w+') as f:
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
	row.places -= m
	return row

def rotate_row_left(row, m1):
	# rotate the row left m1 places
	# LM1 in the paper
	
	row.places += m1
	return row

def list_to_int(bitlist):
	result = 0
	for bit in bitlist:
		result = (result << 1) | bit
	return result


	
def row_less_than(a, b):
	global max_comparisons, n_bits, bitcomparisons
	max_comparisons += 1 # n_bits - a.places # only compare the unknown bits (upper bound of upper_comparisons)
	a_bit = 0
	b_bit = 0
	for i in range(a.places, n_bits):
		a_bit = a.bitlist[i]
		b_bit = b.bitlist[i]
		bitcomparisons += 1
		if a_bit != b_bit:
			break
 	# not counted as a separate comparison. They were already compared in the for loop
	# I am just redoing the computation instead of storing it for convenience
	return a_bit < b_bit

def rejoin(less, x, more):
	joined = less + [x] + more
	return joined

def is_sorted(array):
	return all(list_to_int(array[i].bitlist) <= list_to_int(array[i + 1].bitlist) for i in range(len(array)-1))

def bitsquick(A, m):
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
	
	m1 = 1
	if x.places < n_bits and x.bitlist[x.places] == 0:
		while x.places+m1 < n_bits and x.bitlist[x.places+m1] == 0:	# continue to first non-0 bit
			m1 += 1
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
		while x.places+m1 < n_bits and x.bitlist[x.places+m1] == 1:	# continue to first non-1 bit
			m1 += 1
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
	return right_rotated_result


if __name__ == '__main__':
	
	n_runs = 20
	for n_nums in [100, 1000, 10000, 20000]:
		for n_bits in [10, 15, 20]:
			all_runs = get_data(n_runs, n_nums, n_bits)

			total_max_comparisons = 0
			total_bitcomparisons = 0

			for arr in all_runs:
				max_comparisons = 0
				bitcomparisons = 0
				n = len(arr) 

				sorted_arr = bitsquick(arr,0) 
				# print(f'# of Comparisons total: {max_comparisons}')
				# print(f'Final array is: {sorted_arr}')
				if not is_sorted(sorted_arr):
					print('NOT SORTED: ', sorted_arr[:100])
				# print(f'The array is sorted: {is_sorted(sorted_arr)}')
				
				total_max_comparisons += max_comparisons
				total_bitcomparisons += bitcomparisons
			
			print(f'\nn_nums: {n_nums}')
			print(f'n_bits: {n_bits}')

			print(f'Average max_comparisons (worst case without bit saving): {total_max_comparisons/n_runs}')
			print(f'Average bitcomparisons: {total_bitcomparisons/n_runs}')
			
			expected = (2 + 3/math.log(2)) * n_nums *math.log(n_nums) - n_nums*13.9 + math.log2(n_nums)
			print(f'Expected # of Comparisons: {expected}')