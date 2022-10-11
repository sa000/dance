
import numpy as np
import tensorflow as tf
from typing import Tuple
from math import degrees, atan

NUM_JOINTS = 17
def angle(slope1: float, slope2: float) -> float:
    '''
    Calculates the angle between two slopes
    '''
    angle = degrees(atan((slope2-slope1)/(1+(slope2*slope1))))
    return angle


#calculate the angle between every slope in each slopes matrix
def calculate_angles(slopes1, slopes2):
    '''
    Calculates the angle between every slope in each slopes matrix
    '''
    angles = np.zeros((NUM_JOINTS,NUM_JOINTS))
    for i in range(17):
        for j in range(i+1,NUM_JOINTS):
            angles[i,j] = abs(angle(slopes1[i,j], slopes2[i,j]))
    print("Finished Calculating Angles")
    return angles
    
def create_slope_matrices(keypoints_list: np.ndarray ) -> np.ndarray:
    '''
    Creates a distance matrix from the keypoints
    arg:
        keypoints_list; np.ndarray of shape (1,1,17,3). Contains 17 joins with a tuple of x,y position and score. See the model for more information
    return:
        slopes (np.ndarray). Array of slope matrices that contain slopes between each join
    '''
    slopes = []

    for keypoints in keypoints_list:
        coordinates = keypoints[0,0,:,0:2]
        x, y = coordinates[:,0], coordinates[:,1]

        #Create a 17x17 distance matrix with 0
        slope = np.zeros((NUM_JOINTS,NUM_JOINTS))
        #for each pair of coordinates, calcualte the slope and intercept and set it to the distance matrix
        for i in range(17):
            for j in range(i+1,NUM_JOINTS):
                m, b = np.polyfit([x[i], x[j]],[y[i], y[j]], 1) 
                slope[i,j] = m
        slopes.append(slope)
    print("Finished creating distance matrix")
    return np.stack(slopes)

def get_grade_angles(matrix):
    '''
    Since this is a symmetric matrix, we only need to look at the upper triangle.
    Get the avergage of all the angles as a grade. (Maybe median is better metric)
    Grading metric can be re-evaluated here

    return: 
        grade: float
    '''
    grade = abs(matrix[np.triu_indices_from(matrix, k=1)].mean())
    return grade


