import os
import sys
import subprocess
from random import randint

output_video_width_in_pixels = 1920	# 480 is Twitter-friendly.
fps = 25
output_length = 60
input_videos = []
in_files = []
combined_file_bytes = b''
repeat_p_frames = 10
skip_frames = 50

print(in_files)

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
		combined_file_bytes += in_files[index].read()
		in_files[index].close()
		input_videos.append(name)

# fn = os.path.splitext(os.path.basename(input_videos[0]))[0]
fn = input("Enter output filename:")

output_dir   = 'moshed_videos/'
# make sure the output directory exists
if not os.path.exists(output_dir):
	os.mkdir(output_dir)

input_avi    = output_dir + 'datamoshing_input.avi'	# must be an AVI so i-frames can be located in binary file
output_avi   = output_dir + 'datamoshing_output.avi'
output_video = output_dir + 'moshed_' + fn + '.mp4'

out_file = open(output_avi, 'wb')


# 30306463 (ASCII 00dc) signals the end of a frame
frames = combined_file_bytes.split(bytes.fromhex('30306463'))

print("Number of frames: {}".format(len(frames)))

iframe = bytes.fromhex('0001B0')
count = 0

i_frame_yet = False
got_pframe = False
temp_frame = None
new_frame = False

for index, frame in enumerate(frames):
	# Leave first I-frame at start of video
	if  i_frame_yet == False:
		out_file.write(frame + bytes.fromhex('30306463'))
		if frame[5:8] == iframe:
			i_frame_yet = True
			print("Iframe detected. \n", index)
			count += 1

	# Skip all other I-frames		
	else:
		if frame[5:8] == iframe:
			print("Iframe skipped")
			new_frame = True
			continue

	# Swap collected p-frame here		
		if got_pframe == True and index == next_dump:	
			frame = temp_frame
			got_pframe = False
			print("Swap collected p-frame")
			for i in range(repeat_p_frames):
				out_file.write(frame + bytes.fromhex('30306463'))
			
	#Collect p-frame:
		if frame[5:8] != iframe and got_pframe == False and new_frame == True:
			temp_frame = frame
			got_pframe = True
			new_frame = False
			next_dump = index+skip_frames
			print("Collect p-frame")

		else:	
			out_file.write(frame + bytes.fromhex('30306463'))


print("Total iframes: {}".format(count))

out_file.close()

subprocess.run('ffmpeg.exe -loglevel error -y -i ' + output_avi + ' ' +
				' -crf 18 -pix_fmt yuv420p -vcodec libx264 -acodec aac -r ' + str(fps) + ' ' +
				' -vf "scale=' + str(output_video_width_in_pixels) + ':-2:flags=lanczos" ' + ' ' +
				output_video)

os.remove(output_avi)				

