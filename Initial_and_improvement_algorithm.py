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

def improvement_algorithm(candidate_facility_number, point_amount, open_p_num_of_facs):
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

    def swap_facilities(opened_facilities, unopened_facilities, points):
        best_total_distance = calculate_total_distance(opened_facilities, points)
        best_opened_facilities = opened_facilities.copy()

        for i in range(len(opened_facilities)):
            for j in range(len(unopened_facilities)):
                new_opened_facilities = opened_facilities.copy()
                new_opened_facilities[i] = unopened_facilities[j]
                new_total_distance = calculate_total_distance(new_opened_facilities, points)

                if new_total_distance < best_total_distance:
                    best_total_distance = new_total_distance
                    best_opened_facilities = new_opened_facilities

        return best_opened_facilities

    def calculate_total_distance(facilities, points):
        total_distance = 0
        for point in points:
            min_dist = float('inf')
            for facility in facilities:
                dist = operator.distance_from(point.x, point.y, facility.x, facility.y)
                if dist < min_dist:
                    min_dist = dist
            total_distance += min_dist
        return total_distance

    best_opened_facilities = swap_facilities(opened_facilities, unopened_facilities, points)
    iterative_reassignment(points, best_opened_facilities)
    return best_opened_facilities, unopened_facilities, points

def measure_execution_time():
    problem_sizes = [
        (20, 5, 3),
        (40, 10, 4),
        (60, 15, 5),
        (80, 20, 6),
        (100, 25, 7),
        (150, 30, 8),
        (200, 35, 9),
        (250, 40, 10)
    ]

    execution_times_initial = []
    execution_times_improved = []

    for customer_amount, candidate_facility_amount, k_amount in problem_sizes:
        # Measure execution time for the initial algorithm
        start_time = time.time()
        opened_facilities, unopened_facilities, points = main(candidate_facility_amount, customer_amount, k_amount)
        end_time = time.time()
        execution_time_initial = end_time - start_time
        execution_times_initial.append(execution_time_initial)
        print(f"Initial Algorithm - Problem Size ({customer_amount}, {candidate_facility_amount}, {k_amount}) - Execution Time: {execution_time_initial:.4f} seconds")
        plot_facilities_and_points(opened_facilities, unopened_facilities, points, title=f"Initial Algorithm: {customer_amount}-{candidate_facility_amount}-{k_amount}")

        # Measure execution time for the improved algorithm
        start_time = time.time()
        best_opened_facilities, unopened_facilities, points = improvement_algorithm(candidate_facility_amount, customer_amount, k_amount)
        end_time = time.time()
        execution_time_improved = end_time - start_time
        execution_times_improved.append(execution_time_improved)
        print(f"Improved Algorithm - Problem Size ({customer_amount}, {candidate_facility_amount}, {k_amount}) - Execution Time: {execution_time_improved:.4f} seconds")
        plot_facilities_and_points(best_opened_facilities, unopened_facilities, points, title=f"Improved Algorithm: {customer_amount}-{candidate_facility_amount}-{k_amount}")

    # Plot execution time vs problem size for both initial and improved algorithms
    plot_execution_time_vs_problem_size(problem_sizes, execution_times_initial, execution_times_improved)

def plot_facilities_and_points(opened_facilities, unopened_facilities, points, title):
    colors = {}
    color_list = ['blue', 'red', 'green', 'purple', 'orange', 'cyan', 'pink', 'yellow', 'brown', 'linen']
    for i, fac in enumerate(opened_facilities):
        colors[fac.id] = color_list[i % len(color_list)]

    for fac in unopened_facilities:
        plt.scatter(fac.x, fac.y, c='black', marker='^')

    for fac in opened_facilities:
        plt.scatter(fac.x, fac.y, c=colors[fac.id], marker='^')

    for point in points:
        if hasattr(point, 'assigned_facility_id') and point.assigned_facility_id is not None:
            plt.scatter(point.x, point.y, c=colors[point.assigned_facility_id], marker='o')

    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title(title)
    plt.show()

def plot_execution_time_vs_problem_size(problem_sizes, execution_times_initial, execution_times_improved):
    problem_size_labels = [f"{c}-{f}-{k}" for c, f, k in problem_sizes]
    plt.figure(figsize=(10, 6))
    plt.plot(problem_size_labels, execution_times_initial, marker='o', label='Initial Algorithm')
    plt.plot(problem_size_labels, execution_times_improved, marker='o', label='Improved Algorithm')
    plt.xlabel('Problem Size (Customers-Candidate Facilities-K)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time vs Problem Size')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    measure_execution_time()
