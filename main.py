#	<Erno>
#	Note: Centers start at 4 and have a difference of 9 in the Kociemba 
#	notation i.e White center = 4 Red center = 13, 13-4=9
#	To detect cross:
#	<>	Go through each face and detect whether any face has a cross pattern
#		on them
#	<>	Assign a buffer with the face on which the cross was made
#	<>	Go to the faces surrounding it and decide whether or not the edges
#		are aligned

from turtle import delay

from bleak import BleakClient, BleakScanner, BleakGATTCharacteristic
import gancube
import asyncio
import magiccube
import serial
import time
import algorithms

full_moves = [
	[],
	[]
]
cross_moves = []
f2l_moves = []
OLL_moves = []
PLL_moves = []
#There are two cubes in this program; the visual of the smart cube and the visual of the smart cube
#The scrambled cube visual's only purpose is to be compared with the smart cube to make sure it is scrambled
visual = magiccube.Cube(3,"WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYY")
scrambled_cube = magiccube.Cube(3,"WWWWWWWWWOOOOOOOOOGGGGGGGGGRRRRRRRRRBBBBBBBBBYYYYYYYYY")
kociemba = ""
new_move = None
moves_recieved = 0
buffer = ""
scramble_array = []
global cross_solved
OLL_solved = False
cross_solved = False
cube_solved = False
f2l_solved = False
f2l_pair_WGR = False
f2l_pair_WBO = False 
f2l_pair_WBR = False 
f2l_pair_WGO = False
cube_scrambled = False
run_cfop_check = False
current_move = ""
buffer_x = 0
finish_session = False
timer_started = False
cube_calibrated = False
text_art = r"""    ______               
   / ____/________  ____ 
  / __/ / ___/ __ \/ __ \
 / /___/ /  / / / / /_/ /
/_____/_/  /_/ /_/\____/ 
                         """

comms = serial.Serial('COM5', 9600, timeout=1)
comms.reset_input_buffer()

def scramble_cube():
	global scramble
	global buffer_scramble
	global display_scramble
	global timer_started
	timer_started = False
	buffer_scramble = visual.generate_random_moves(num_steps=30)
	buffer_scramble = [str(m) for m in buffer_scramble]
	display_scramble = buffer_scramble.copy()
	for x in range(len(display_scramble)-2, -1, -1):
		if display_scramble[x] == display_scramble[x+1]:
			display_scramble.pop(x+1)
			if "'" in display_scramble[x]:
				display_scramble[x] = display_scramble[x].replace("'", "")
			display_scramble[x] = str(display_scramble[x]) + "2"
	buffer_scramble = display_scramble.copy()
	for x in range(len(buffer_scramble)-2, -1, -1):	
		if "2" in buffer_scramble[x]:
			buffer_scramble[x] = buffer_scramble[x].replace("2", "''")
			buffer_scramble.insert(x+1, buffer_scramble[x])
	scramble = " ".join(str(x) for x in display_scramble)
	scrambled_cube.rotate(scramble)
	scramble = " ".join(str(x) for x in display_scramble)

def detect_scrambling(move):
	global cube_scrambled
	global start_time
	global buffer_x
	global buffer_scramble
	global current_move
	if buffer_x == 0 and current_move == "":
		current_move = buffer_scramble[0]
	current_move = buffer_scramble[buffer_x]
	print("Scrambled cube state:")
	print(scrambled_cube)
	print(scramble)
	scrambled_cube_kociemba_state = scrambled_cube.get_kociemba_facelet_colors()
	visual_kociemba_state = visual.get_kociemba_facelet_colors()
	if visual_kociemba_state == scrambled_cube_kociemba_state:
		print("Cube has been scrambled")
		cube_scrambled = True
		start_time = time.perf_counter()
	else:
		cube_scrambled = False
		detect_incorrect_scrambling(move)
#		comms.write(b"Scrambling...\n")

def detect_incorrect_scrambling(move):
	global buffer_scramble
	global current_move
	global buffer_x
	if current_move == move:
		buffer_x += 1
		current_move = buffer_scramble[buffer_x]
	elif "''" in current_move:
		if "'" in move:
			if move.replace("'", "") == current_move.replace("''", ""):
				buffer_x += 1
				current_move = buffer_scramble[buffer_x]
		else:
			if move == current_move.replace("''", ""):
				buffer_x += 1
				current_move = buffer_scramble[buffer_x]
	else:
		print(f"Wrong move! {current_move}")

def serial_communication_protocol():
	if cube_solved:
		for x in range(len(full_moves[0])):
			buffer_serial = full_moves[0][x]
			buffer_serial = f"{buffer_serial}\n"
			comms.write(buffer_serial.encode("utf-8"))
			time.sleep(0.3)
		comms.close()
			

def record_move_history(move):
	global timer_started
	if cube_scrambled:
		if not timer_started:
			global start_time
			start_time = time.perf_counter()
			timer_started = True
		if not cross_solved:
			cross_moves.append(move)
		else:
			if not f2l_solved:
				f2l_moves.append(move)
			else:
				if not OLL_solved:
					OLL_moves.append(move)
				else:
					if not cube_solved:
						PLL_moves.append(move)

def CFOP():
	global cross_solved
	global cube_solved
	global f2l_solved
	global OLL_solved
	global f2l_pair_WGO
	global f2l_pair_WBO
	global f2l_pair_WBR
	global f2l_pair_WGR
	global OLL_state
	cube_solved = visual.is_done()
#	Currently only checks the White face
#	First adds the entire Kociemba notation to the Kociemba notation list
	buffer = visual.get_kociemba_facelet_colors()
	kociemba_notation = list(buffer)
	if kociemba_notation[4] == "W" and cross_solved == False:
		if kociemba_notation[1] == "W" and kociemba_notation[46] == "B" and cross_solved == False:
			if kociemba_notation[3] == "W" and kociemba_notation[37] == "O" and cross_solved == False:
				if kociemba_notation[5] == "W" and kociemba_notation[10] == "R" and cross_solved == False:
					if kociemba_notation[7] == "W" and kociemba_notation[19] == "G" and cross_solved == False:
						cross_solved = True
	if cross_solved:
		buffer = visual.get_kociemba_facelet_colors()
		kociemba_notation = list(buffer)
		if kociemba_notation[4] == "W":
	#		Checks for the WBO corner and BO edge and if it is aligned
			if f2l_pair_WBO == False:
				if kociemba_notation[0] == "W":
					if kociemba_notation[36] == "O":
						if kociemba_notation[47] == "B":
							if kociemba_notation[39] == "O" and kociemba_notation[50] == "B":
								f2l_pair_WBO = True
								f2l_moves.append("[f2l_pair_WBO solved]")
	#		Checks for the WBR corner and BR edge if it is aligned
			if f2l_pair_WBR == False:
				if kociemba_notation[2] == "W":
					if kociemba_notation[45] == "B":
						if kociemba_notation[11] == "R":
							if kociemba_notation[48] == "B" and kociemba_notation[14] == "R":
								f2l_pair_WBR = True
								f2l_moves.append("[f2l_pair_WBR solved]")
	#		Checks for the WGR corner and GR edge if it is aligned
			if f2l_pair_WGR == False:
				if kociemba_notation[8] == "W":
					if kociemba_notation[20] == "G":
						if kociemba_notation[9] == "R":
							if kociemba_notation[23] == "G" and kociemba_notation[12] == "R":
								f2l_pair_WGR = True
								f2l_moves.append("[f2l_pair_WGR solved]")
	#		Checks for the WGO corner and GO edge if it is aligned
			if f2l_pair_WGO == False:
				if kociemba_notation[6] == "W":
					if kociemba_notation[18] == "G":
						if kociemba_notation[38] == "O":
							if kociemba_notation[21] == "G" and kociemba_notation[41] == "O":
								f2l_pair_WGO = True
								f2l_moves.append("[f2l_pair_WGO solved]")
		if f2l_pair_WGR == True and f2l_pair_WBO == True and f2l_pair_WBR == True and f2l_pair_WGO == True:
			f2l_solved = True
			OLL_state = visual.get_kociemba_facelet_colors()
			solved_pieces = 0
			buffer = visual.get_kociemba_facelet_colors()
			kociemba_notation = list(buffer)
			for x in range(0, 9):
				piece = x + 27
				if kociemba_notation[piece] == "Y":
					solved_pieces += 1
			if solved_pieces == 9:
				OLL_solved = True
				global run_cfop_check
				if cube_solved:
					run_cfop_check = False
					global end_time
					global finish_session
					analyse_cube_solve()
					serial_communication_protocol()
					finish_session = True

def analyse_cube_solve():
	analysis = []
	end_time = time.perf_counter()
	print("Time:", str(end_time - start_time))
	print(f"Cross: ", " ".join(str(x) for x in cross_moves))
	print(f"F2L: ", " ".join(str(x) for x in f2l_moves))
	print(f"OLL: ", " ".join(str(x) for x in OLL_moves))
	print(f"PLL: ", " ".join(str(x) for x in PLL_moves))
#	Analyse cross solve to see if it is under 8 moves
	if len(cross_moves) <= 8:
		analysis.append(f"Well done! That cross solve was done in {len(cross_moves)} moves!")
	else:
		analysis.append("Cross solution is in more than 8 moves.")
#	Calculate average TPS (turns per second)
	tps = len(full_moves[0]) / (end_time - start_time)
	analysis.append(f"Average TPS: {tps}")
	for x in analysis:
		print(x)
	analysis.clear()

async def main():
	print("\033c", end="")
#	This finds the nearest Gan I3 smart cube and connects to them using BLE; 
#	This doesn't search for other smart cubes
	print("Searching for smart cubes to connect with...")
	devices = await BleakScanner.discover()
	for d in devices:
		if d.name and d.name.startswith("GAN"):
			print(f"<FOUND> {d.name} {d}")
			global cube
			cube = gancube.GanCube(d.address)
			cube.name = d.name
			cube.address = d.address
	async with BleakClient(cube.address, timeout=30.0) as client:
		cube_service = None
		for service in client.services:
			if service.uuid == cube.SERVICE_UUID:
				cube_service = service
				break
		read_chrct = None
		for chrct in cube_service.characteristics:
			if chrct.uuid == cube.CHRCT_UUID_READ:
				read_chrct = chrct
				print(f"Read characteristic: {read_chrct}")
				print("\033c", end="")
		async def handler(sender: BleakGATTCharacteristic, data: bytearray):
			global cube, full_moves
			data = [int(i) for i in data]
			dec = cube.decrypt(data)
			value = ''.join([bin(bt + 256)[3:] for bt in dec])
			if dec[0] == 208:
				exit()
			mode = int(value[0:4], 2)
			# Mode 1: Orientation
			if mode == 1:
				x_int = (dec[1] << 8) | dec[2]
				y_int = (dec[3] << 8) | dec[4]
				z_int = (dec[5] << 8) | dec[6]
				w_int = (dec[7] << 8) | dec[8]
				def int16_to_float(val):
					if val >= 32768:
						val -= 65536
					return val / 32768.0
				x = int16_to_float(x_int)
				y = int16_to_float(y_int)
				z = int16_to_float(z_int)
				w = int16_to_float(w_int)
				q = (x, y, z, w)
				rotm = [
					[1 - 2*(y**2 + z**2), 2*(x*y - z*w),     2*(x*z + y*w)],
					[2*(x*y + z*w),       1 - 2*(x**2 + z**2), 2*(y*z - x*w)],
					[2*(x*z - y*w),       2*(y*z + x*w),     1 - 2*(x**2 + y**2)]
				]
            # Mode 2: Moves
			elif mode == 2:
				global last_window
				if 'last_window' not in globals():
					last_window = []
				moves_map = ["U","U'","R","R'","F","F'","D","D'","L","L'","B","B'"]
				move_cnt = int(value[4:12], 2)
				curr_window = []
				for i in range(7):
					start = 12 + i*5
					end = start + 5
					if end > len(value):
						break
					m = int(value[start:end], 2)
					move = moves_map[m] if m < len(moves_map) else f"?({m})"
					curr_window.append(move)
				global new_move
				new_move = None
				if last_window:
					for i in range(len(curr_window)):
						if i >= len(last_window) or curr_window[i] != last_window[i]:
							new_move = curr_window[i]
							break
				else:
					new_move = curr_window[-1] if curr_window else None
#				When a move is registered from the smart cube, this snippet of code handles all the logic.
#				Not ideal, but I made it work. Any cleanup is appreciated
				if new_move:
					global cube_calibrated
					cube_calibrated = False
					global moves_recieved
					moves_recieved += 1
					if moves_recieved > 2:
						global run_cfop_check
						cube_calibrated = True
						record_move_history(new_move)
						visual.rotate(new_move)
						print("\033c", end="")
						print(visual)
						print(visual.get_kociemba_facelet_colors())
						if cube_scrambled:
							run_cfop_check = True
							full_moves[0].append(new_move)
							full_moves[1].append(time.perf_counter() - start_time)
						else:
							detect_scrambling(new_move)
				last_window = curr_window
		if read_chrct:
			await client.start_notify(read_chrct, handler)
			print(text_art)
			print("<Erno - Version 0.01>")
			print("Type 'help' for a list of commands.")
			prompt = input("> ")
			while True:
				if prompt.lower() == "start":
					if not cube_calibrated:
						print("Do a move and do it's inverse to calibrate the cube first.")
					scramble_cube()
					break
				elif prompt.lower() == "help":
					print("Available commands:")
					print("start - Start a new session and scramble the cube")
					print("help - Show this help message")
					prompt = input("> ")
				elif prompt.lower() == "clear":
					print("\033c", end="")
					prompt = input("> ")	
				else:
					print("Unknown command. Type 'help' for a list of commands.")
					prompt = input("> ")
			background_task = asyncio.create_task(run_task())
			while not finish_session:
				await asyncio.sleep(0.5)
			await client.stop_notify(read_chrct)
			background_task.cancel()
	
async def run_task():
	global run_cfop_check, finish_session
	while not finish_session:
		if run_cfop_check and cube_scrambled:
			CFOP()
		await asyncio.sleep(0.25)  # run 4 times per second
		if finish_session:
			break
asyncio.run(main())
