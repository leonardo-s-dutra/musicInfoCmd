import os


def txt_to_list(file, number_of_lines):

	if not os.path.exists(file):
		print('Could not find file', "'"+file+"'", end = '\n\n')
		return -1

	try:
		with open(file) as f:

			lines = [line.replace('\n', '') for line in f.readlines()]

			if len(lines) < number_of_lines:
				print('Missing values in file', "'"+file+"'", end = '\n\n')
				return -1

			elif len(lines) > number_of_lines:
				print('Too many values in file', "'"+file+"'", end = '\n\n')
				return -1

			return lines

	except:
		print('Could not open file', "'"+file+"'", end = '\n\n')
		return -1


def check_arguments_number(arg, min, max):

	if len(arg) < min:
		print('Missing arguments!', end = '\n\n')
		return -1

	elif len(arg) > max:
		print('Too many arguments!', end = '\n\n')
		return -1

	else:
		return 0