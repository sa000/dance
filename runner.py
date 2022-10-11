from model import run_inference, draw_prediction_on_image, movenet, init_crop_region, determine_crop_region
from grader import create_slope_matrices, calculate_angles, get_grade_angles
from util.helpers import generate_videos_side_by_side, generated_graded_video
from util.video import Video
import tensorflow as tf
import numpy as np 

#Movement lighting model is 0.5x faster than thunder model
from PIL import Image
INPUT_DIR, OUTPUT_DIR = 'input', 'output'

print("Loading Information")
base_video = 'anm'
instructor_path = f'{INPUT_DIR}/instructor_{base_video}.gif'
student_path = f'{INPUT_DIR}/student_{base_video}.gif'

instructor_video = Video(instructor_path)
instructor_video.generate_keypoints()
instructor_video.save_output(f'{OUTPUT_DIR}/instructor_labeled_{base_video}.gif')


student_video = Video(student_path)
student_video.generate_keypoints()
student_video.save_output(f'{OUTPUT_DIR}/student_labeled_{base_video}.gif')

generate_videos_side_by_side(instructor_video.output_video, student_video.output_video, f'{OUTPUT_DIR}/side_by_side_labeled_{base_video}.gif')


#Grading System
print("Performing Grading")
slopes_instructor = create_slope_matrices(instructor_video.keypoints)
slopes_student = create_slope_matrices(student_video.keypoints)
num_frames = max(len(slopes_instructor), len(slopes_student))
angles = [calculate_angles(slopes_instructor[i], slopes_student[i]) for i in range(num_frames)]
angle_grades = [np.round(get_grade_angles(angle_matrix),2) for angle_matrix in angles]

print("Finished Grading")

print("Generating Grading Video")
im = Image.open(f'{OUTPUT_DIR}/side_by_side_labeled_{base_video}.gif')
generated_graded_video(im, angle_grades, base_video)
print("Finished Vidoe Generation")

