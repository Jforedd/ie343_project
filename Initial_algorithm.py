import random
import matplotlib.pyplot as plt
import time
from Facility import Facility
from Point import Point
from Operators import Operators

def main(candidate_facility_number, point_amount, open_p_num_of_facs):
    operator = Operators()

    facs_coordinates = operator.create_distance_matrix(candidate_facility_number, 2)
    points_coordinates = operator.create_distance_matrix(point_amount, 2)
    facs = [Facility(i, facs_coordinates[i][0], facs_coordinates[i][1], 20 * random.random() + 50) for i in range(candidate_facility_number)]
    points = [Point(i, points_coordinates[i][0], points_coordinates[i][1], 2 * random.random() + 1) for i in range(point_amount)]
    distance_matrix = operator.distance_matrix(facs, points)
    
    opened_facilities = []
    unopened_facilities = facs.copy()
    unassigned_points = points.copy()

    total_distance = 0
    min_value = float('inf')
    index_of = 0
    previous_min = -1
    max_val = 0

    for y in range(len(facs)):
        total_distance = sum(distance_matrix[y])
        if max_val < total_distance:
            max_val = total_distance
    min_value = max_val + 1

    for _ in range(open_p_num_of_facs):
        for y in range(len(facs)):
            total_distance = sum(distance_matrix[y])
            if total_distance < min_value and facs[y] not in opened_facilities:
                min_value = total_distance
                index_of = y
        opened_facilities.append(facs[index_of])
        unopened_facilities.remove(facs[index_of])
        min_value = max_val + 1

    for point in points:
        min_dist = float('inf')
        nearest_facility = None
        for facility in opened_facilities:
            dist = operator.distance_from(point.x, point.y, facility.x, facility.y)
            if dist < min_dist:
                min_dist = dist
                nearest_facility = facility
        point.assigned_facility_id = nearest_facility.id

    def reassign_points(points, opened_facilities):
        for point in points:
            min_dist = float('inf')
            nearest_facility = None
            for facility in opened_facilities:
                dist = operator.distance_from(point.x, point.y, facility.x, facility.y)
                if dist < min_dist:
                    min_dist = dist
                    nearest_facility = facility
            point.assigned_facility_id = nearest_facility.id

    def iterative_reassignment(points, opened_facilities, iterations=10):
        for _ in range(iterations):
            reassign_points(points, opened_facilities)

    iterative_reassignment(points, opened_facilities)
    return opened_facilities, unopened_facilities, points
