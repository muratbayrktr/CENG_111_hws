import math
import random
from evaluator import get_data  # get_data() will come from this import
general_data = get_data()
# retrieving all the get_data
M_ROW = general_data[0]  # number of rows, M <= 100
N_COLUMN = general_data[1]  # number of columns , N <= 100
D = general_data[2]  # distance threshold for infectivity
K = general_data[3]  # k constant for calculating infectivity probability
Lambda = general_data[4]  # constant for calculating mask defend value
mu = general_data[5]  # constant for calculating movement directionality probability
universal_state = general_data[6]  # it returns list of lists, universal_state,namely datas of individuals by order

def new_move():
	global M_ROW
	global N_COLUMN
	global D
	global K
	global Lambda
	global mu
	global universal_state
	# calculating new movements
	new_movements = calculate_new_movement(universal_state, mu, M_ROW, N_COLUMN)
	# updating universal state accordingly
	index = 0
	for i in new_movements:
		# (x,y) update
		universal_state[index][0] = i[0]
		# direction update
		universal_state[index][1] = i[1]
		# index update
		index += 1
	# deleting index variable
	del index
	post_spread_states = calculate_infection_state(universal_state, K, Lambda, D)
	for i in post_spread_states:
		universal_state[i][3] = 'infected'
	print(universal_state)
	return universal_state


# calculating infection state
def calculate_infection_state(individuals, kappa, Lambda, distance_threshold):
	states = []
	for i in range(len(individuals)):
		x = individuals[i][0][0]
		y = individuals[i][0][1]
		mask_state = individuals[i][2]
		infection_state = individuals[i][3]
		for j in range(i + 1, len(individuals)):
			second_x = individuals[j][0][0]
			second_y = individuals[j][0][1]
			second_mask_state = individuals[j][2]
			second_infection_state = individuals[j][3]
			distance_i_j = math.sqrt((abs(x - second_x)) ** 2 + (abs(y - second_y)) ** 2)
			if infection_state == second_infection_state:
				continue
			elif distance_i_j <= distance_threshold:
				masked_count = 0
				if mask_state == 'masked':
					masked_count += 1
				if second_mask_state == 'masked':
					masked_count += 1
				constant = kappa / (distance_i_j ** 2)
				infection_probability = min(1, constant) / (Lambda ** masked_count)
				inf = ['infected', 'notinfected']
				new_state = random.choices(inf, weights=(infection_probability, 1 - infection_probability))[0]
				if new_state == 'infected':
					states.append(i)
					states.append(j)
	return states # returning states as lists


# calculating new movements
def calculate_new_movement(states, MU, M, N):
	# Probabilities for movements
	p_forward = MU * 1 / 2
	p_forward_left = MU * 1 / 8
	p_forward_right = MU * 1 / 8
	p_left = (1 / 2) * (1 - MU - MU ** 2)
	p_right = (1 / 2) * (1 - MU - MU ** 2)
	p_backward_left = (MU ** 2) * (2 / 5)
	p_backward_right = (MU ** 2) * (2 / 5)
	p_backward = (MU ** 2) * (1 / 5)
	direction_weights = (
	p_forward, p_forward_right, p_right, p_backward_right, p_backward, p_backward_left, p_left, p_forward_left)

	list_of_moves = []
	coordinates = []
	for k in states:
		coordinates.append(k[0])
	count = 0
	for i in states:
		x = i[0][0]
		y = i[0][1]
		direction = i[1]
		if direction == 0:  # done
			forward = ((x, y + 1), 0)
			forward_right = ((x - 1, y + 1), 1)
			right = ((x - 1, y), 2)
			backward_right = ((x - 1, y - 1), 3)
			backward = ((x, y - 1), 4)
			backward_left = ((x + 1, y - 1), 5)
			left = ((x + 1, y), 6)
			forward_left = ((x + 1, y + 1), 7)
		elif direction == 1:  # done
			forward = ((x - 1, y + 1), 1)
			forward_right = ((x - 1, y), 2)
			right = ((x - 1, y - 1), 3)
			backward_right = ((x, y - 1), 4)
			backward = ((x + 1, y - 1), 5)
			backward_left = ((x + 1, y), 6)
			left = ((x + 1, y + 1), 7)
			forward_left = ((x, y + 1), 0)
		elif direction == 2:  # done
			forward = ((x - 1, y), 2)
			forward_right = ((x - 1, y - 1), 3)
			right = ((x, y - 1), 4)
			backward_right = ((x + 1, y - 1), 5)
			backward = ((x + 1, y), 6)
			backward_left = ((x + 1, y + 1), 7)
			left = ((x, y + 1), 0)
			forward_left = ((x - 1, y + 1), 1)
		elif direction == 3:  # done
			forward = ((x - 1, y - 1), 3)
			forward_right = ((x, y - 1), 4)
			right = ((x + 1, y - 1), 5)
			backward_right = ((x + 1, y), 6)
			backward = ((x + 1, y + 1), 7)
			backward_left = ((x, y + 1), 0)
			left = ((x - 1, y + 1), 1)
			forward_left = ((x - 1, y), 2)
		elif direction == 4:  # done
			forward = ((x, y - 1), 4)
			forward_right = ((x + 1, y - 1), 5)
			right = ((x + 1, y), 6)
			backward_right = ((x + 1, y + 1), 7)
			backward = ((x, y + 1), 0)
			backward_left = ((x - 1, y + 1), 1)
			left = ((x - 1, y), 2)
			forward_left = ((x - 1, y - 1), 3)
		elif direction == 5:  # done
			forward = ((x + 1, y - 1), 5)
			forward_right = ((x + 1, y), 6)
			right = ((x + 1, y + 1), 7)
			backward_right = ((x, y + 1), 0)
			backward = ((x - 1, y + 1), 1)
			backward_left = ((x - 1, y), 2)
			left = ((x - 1, y - 1), 3)
			forward_left = ((x, y - 1), 4)
		elif direction == 6:  # done
			forward = ((x + 1, y), 6)
			forward_right = ((x + 1, y + 1), 7)
			right = ((x, y + 1), 0)
			backward_right = ((x - 1, y + 1), 1)
			backward = ((x - 1, y), 2)
			backward_left = ((x - 1, y - 1), 3)
			left = ((x, y - 1), 4)
			forward_left = ((x + 1, y - 1), 5)
		elif direction == 7:  # done
			forward = ((x + 1, y + 1), 7)
			forward_right = ((x, y + 1), 0)
			right = ((x - 1, y + 1), 1)
			backward_right = ((x - 1, y), 2)
			backward = ((x - 1, y - 1), 3)
			backward_left = ((x, y - 1), 4)
			left = ((x + 1, y - 1), 5)
			forward_left = ((x + 1, y), 6)

		probable_moves = [forward, forward_right, right, backward_right, backward, backward_left, left, forward_left]
		move = random.choices(probable_moves, weights=direction_weights, k=1)[0]
		move_coordinates = move[0]
		if move_coordinates in coordinates or move_coordinates[0] >= N or move_coordinates[1] >= M or move_coordinates[
			0] < 0 or move_coordinates[1] < 0:
			list_of_moves.append(((x, y), direction))  # if it is occupied, return old x,y,direction
		else:
			coordinates[count] = move[0]  # if no occupancy, add to coordinates list and
			list_of_moves.append(move)  # add to return list
		count += 1
	return list_of_moves
