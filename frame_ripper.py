import os
import sys
import subprocess
import random

output_video_width_in_pixels = 1920	# 480 is Twitter-friendly.
fps = 25
output_length = 60
input_videos = []
in_files = []
combined_file_bytes = b''
repeat_p_frames = 10
skip_frames = 50

output_dir   = 'moshed_videos/'
# make sure the output directory exists
if not os.path.exists(output_dir):
	os.mkdir(output_dir)

input_avi    = output_dir + 'datamoshing_input.avi'	# must be an AVI so i-frames can be located in binary file
output_avi   = output_dir + 'datamoshing_output.avi'


if len(sys.argv) < 2:
	print("Please include a video to be datamoshed.")
	sys.exit()


for index, name in enumerate(sys.argv[1:]):
	if not os.path.isfile(sys.argv[index]):
		print("Couldn't find that video file. You might want to check the file name??")
		sys.exit()
	else:
		print(index, name)
		in_files.append(open(name,  'rb'))
		header_removed = in_files[index].read()
		combined_file_bytes += 
		in_files[index].close()
		input_videos.append(name)

frames = combined_file_bytes.split(bytes.fromhex('30306463'))
iframe = bytes.fromhex('0001B0')
pframe = bytes.fromhex('0001B6')




def probe_file(frames):
	iframe_cnt = 0
	pframe_cnt = 0
	bframe_cnt = 0
	for index, frame in enumerate(frames):
		if frame[5:8] == iframe:
			print("\nIframe")
			iframe_cnt += 1
		elif frame[5:8] == pframe:
			print("          pframe")
			pframe_cnt += 1
		else:
			print("                 bframe")
			bframe_cnt += 1
		print(frame[0:8])

def write_file(frames):
	fn = input("Enter output filename:")
	output_video = output_dir + 'moshed_' + fn + '.mp4'
	out_file = open(output_avi, 'wb')
	i_frame_yet = False
	write = False

	for index, frame in enumerate(frames):
		write = bool(random.getrandbits(1))
		if  i_frame_yet == False:
			out_file.write(frame + bytes.fromhex('30306463'))
			i_frame_yet = True

		if write:
			out_file.write(frame + bytes.fromhex('30306463'))

	out_file.close()

	subprocess.run('ffmpeg.exe -loglevel error -y -i ' + output_avi + ' ' +
					' -crf 18 -pix_fmt yuv420p -vcodec libx264 -acodec aac -r ' + str(fps) + ' ' +
					' -vf "scale=' + str(output_video_width_in_pixels) + ':-2:flags=lanczos" ' + ' ' +
					output_video)

	os.remove(output_avi)

funct = input("What would you like to do? Probe (p) or write (w) file? ")
if funct == 'w':
	write_file(frames)
elif funct	== 'p':
	probe_file(frames)
else:
	funct = input("What would you like to do? Probe (p) or write (w) file? ")

# fn = os.path.splitext(os.path.basename(input_videos[0]))[0]









# 30306463 (ASCII 00dc) signals the end of a frame





				

