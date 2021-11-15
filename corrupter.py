factor = 5
start_effect = 200
output_directory = 'corrupted_videos'


import os
import argparse
import random
import sys
import datetime

def quit_if_no_video_file(video_file):
	if not os.path.isfile(video_file):
		raise argparse.ArgumentTypeError("Couldn't find {}. You might want to check the file name??".format(video_file))
	else:
		return(video_file)

# make sure the output directory exists
def confirm_output_directory(output_directory):
	if not os.path.exists(output_directory): os.mkdir(output_directory)

	return(output_directory)


parser = argparse.ArgumentParser()


parser.add_argument('input_video', 										type=quit_if_no_video_file, 	help="File to be moshed")
parser.add_argument('--factor',        	default = factor, 			type=float, 					help="Time the video starts on the original footage's timeline. Trims preceding footage.")
parser.add_argument('--start_effect',	default = start_effect, 		type=int, 					help="Time the effect starts on the trimmed footage's timeline. The output video can be much longer.")
parser.add_argument('--output_dir',     default = output_directory, 	type=confirm_output_directory, 	help="Output directory")

locals().update( parser.parse_args().__dict__.items() )

in_file  = open(input_video,  'rb')


file_bytes = bytearray(in_file.read())
s = ""


for i in range(start_effect):
	s+=chr(file_bytes[i])
	
print(s)

factor = factor * 0.000001
n = int((len(file_bytes)-start_effect)*factor)

date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
file_name = os.path.splitext( os.path.basename(input_video) )[0]
output_video = os.path.join(output_dir, 'corrupted-{}_{}_{}.mp4'.format(n, file_name, date))
out_file = open(output_video, 'wb')

print(len(file_bytes), n)

end_effect = len(file_bytes)
for i in range(n):
	PosA = random.randint(start_effect, end_effect)
	PosB = random.randint(start_effect, end_effect)
	tmp = file_bytes[PosA]
	file_bytes[PosA] = file_bytes[PosB]
	file_bytes[PosB] = tmp

out_file.write(file_bytes)
in_file.close()
out_file.close()

