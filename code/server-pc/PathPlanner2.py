# Just a dummy trial to make the path traversal from scratch

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import math
threshold = 10

class PathPlanning:

    def __init__(self, centre_of_tracking:tuple):
        self.lane_1 = centre_of_tracking[0]
        self.lane_2 = centre_of_tracking[1]
        self.track = None
        self.centre_of_tracking = centre_of_tracking
        self.l_or_r = None
        self.reset = False
        self.start = (0,0)


    def lane_assist(self, current_x:int, current_y:int, classes, bboxes, goal_pos):

        if self.check_obstacles(classes):
            action = self.obstacle_avoidance(classes, bboxes, goal_pos)
            if action is not None:
                return action
            
    
        self.track = (current_x, current_y)
        # print(f"Track: {self.track[0]} Centre of Tracking: {self.centre_of_tracking[0]} {self.centre_of_tracking[1]}")
        if self.centre_of_tracking[0] > self.track[0]:
            return 'l'
        
        if self.centre_of_tracking[1] < self.track[0]:
            return 'r'

        if self.reset == True:
            self.l_or_r = None
            self.reset = False


    def obstacle_avoidance(self, classes, bboxes, goal_pos):
        obstacles = []
        for clas, bbox in zip(classes, bboxes):
            if clas != 'person':
                obstacles.append((int((bbox[0]+bbox[2])/2), int((bbox[1]+bbox[3])/2)))
        if obstacles:
            force_field_vector = self.calculate_force_field(obstacles, goal)
            force_field_angle = self.calculate_force_field_angle(force_field_vector)
            force_field_angle_degrees = math.degrees(force_field_angle)

            if force_field_angle_degrees < 90:
                return 'r', force_field_angle_degrees
            
            if force_field_angle_degrees > 90:
                return 'l', force_field_angle_degrees

    def check_obstacles(self, classes):
        flag = False
        for clas in classes:
            if clas != 'person':
                flag = True
        return flag
    def calculate_force_field(self, obstacles, goal):
        # Initialize total force field vector
        total_force_field = [0, 0]

        # Iterate through each obstacle
        for obstacle in obstacles:
            # Step 1: Calculate the vector from obstacle to goal
            vector_to_goal = (goal[0] - obstacle[0], goal[1] - obstacle[1])

            # Step 2: Normalize the vector
            magnitude = math.sqrt(vector_to_goal[0]**2 + vector_to_goal[1]**2)
            unit_vector = (vector_to_goal[0] / magnitude, vector_to_goal[1] / magnitude)

            # Step 3: Invert the vector
            inverted_vector = (unit_vector[0], unit_vector[1])

            # Add the force field contribution from this obstacle to the total force field
            total_force_field[0] += inverted_vector[0]
            total_force_field[1] += inverted_vector[1]

        return total_force_field

    def calculate_force_field_angle(self,force_field_vector):
        # Calculate the angle
        angle = math.atan2(force_field_vector[1], force_field_vector[0])

        return angle

    def plot_force_field(self, obstacles, goal, force_field_vector):
        # Plot obstacles
        for obstacle in obstacles:
            plt.plot(obstacle[0], obstacle[1], 'ro')  # Red circles for obstacles

        # Plot goal
        plt.plot(goal[0], goal[1], 'go')  # Green circle for goal

        # Plot force field vector
        plt.quiver(*self.start, force_field_vector[0], force_field_vector[1], angles='xy', scale_units='xy', scale=1, color='b')

        # Set plot limits
        plt.xlim(-1, 6)
        plt.ylim(-1, 8)

        # Add labels and title
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Force Field Visualization')

        # Show plot
        plt.grid()
        plt.show()

    def draw_filled_rectangles(self, image, bboxes, classes, scores, colors=None):
        """
        Draw filled rectangles around bounding boxes on the image.

        Args:
        - image (numpy.ndarray): Input image.
        - bboxes (list): List of bounding boxes in the format [[x1, y1, x2, y2], ...].
        - classes (list): List of class labels corresponding to each bounding box.
        - scores (list): List of confidence scores corresponding to each bounding box.
        - colors (list, optional): List of BGR colors for drawing rectangles. If not provided, random colors will be used.

        Returns:
        - numpy.ndarray: Image with filled rectangles drawn.
        """
        for bbox, class_label, score in zip(bboxes, classes, scores):
            if class_label != 'person':
                x1, y1, x2, y2 = map(int, bbox)

                if colors is None:
                    color = (int(class_label * 12.5), int(score * 255), int((1 - score) * 255))
                else:
                    color = colors[class_label]

                cv.rectangle(image, (x1, y1), (x2, y2), color, cv.FILLED)
                
                text = f"{class_label}: {score:.2f}"
                cv.putText(image, text, (x1, y1 - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)

        return image
        
if __name__ == "__main__":


    pathplanner = PathPlanning((0,0))
    # Example usage
    obstacles = [(1, 2), (3, 4), (4,5)]  # Coordinates of multiple obstacles
    
    goal = (-1,7)
    force_field_vector = pathplanner.calculate_force_field(obstacles, goal)
    print("Total force field vector:", force_field_vector)

    # Calculate the angle
    force_field_angle = pathplanner.calculate_force_field_angle(force_field_vector)
    print("Force field angle (radians):", force_field_angle)

    # Convert radians to degrees if needed
    force_field_angle_degrees = math.degrees(force_field_angle)
    print("Force field angle (degrees):", force_field_angle_degrees)

    # Plot the force field
    pathplanner.plot_force_field(obstacles, goal, force_field_vector)

    # ref_frame = cv.imread(r"C:\Users\ROHIT FRANCIS\Downloads\Test1 (2).jpg")
    # pathplanner = PathPlanning(ref_frame)
    # feed = cv.imread(r"C:\Users\ROHIT FRANCIS\Downloads\Test3.jpg")
    # cv.imshow("", ref_frame)
    # cv.imshow(" ", feed)
    # cv.waitKey(0)
    # pathplanner.lane_assist(feed)

    # cam = cv.VideoCapture(0)

    # ret, ref_frame = cam.read()
    # # if ret:
    # pathplanner = PathPlanning(ref_frame)

    # while True:

    #     ret, frame = cam.read()
        
    #     mask = pathplanner.lane_assist(frame)

    #     if cv.waitKey(1) == ord('q'):
    #         break

    #     cv.imshow('feed', frame)
    #     cv.imshow("mask", mask)
    #     pathplanner.ref_frame = frame