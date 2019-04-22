import os
import sys


# Python program for implementation of RR Scheduling

total_p_no = 16
total_time = 0
total_time_counted = 0
# proc is process list
proc = []
wait_time = 0
turnaround_time = 0

with open('input.txt') as f:
    # Getting the input for process
    for line in f:
            array = line.split()
            if (len(array) != 3):
                print ("wrong input format")
                exit()
            arrival, burst, remaining_time = int(array[1]), int(array[2]), int(array[1])
            proc.append([arrival, burst, remaining_time, 0])

    # total_time gets incremented with burst time of each process
    total_time += burst
time_quantum = 2
# Keep traversing in round robin manner until the total_time == 0
while total_time != 0:
    # traverse all the processes
    for i in range(len(proc)):
        # proc[i][2] here refers to remaining_time for each process i.e "i"
        if proc[i][2] <= time_quantum and proc[i][2] >= 0:
            total_time_counted += proc[i][2]
            total_time -= proc[i][2]
            # the process has completely ended here thus setting it's remaining time to 0.
            proc[i][2] = 0
        elif proc[i][2] > 0:
            # if process has not finished, decrementing it's remaining time by time_quantum
            proc[i][2] -= time_quantum
            total_time -= time_quantum
            total_time_counted += time_quantum
        if proc[i][2] == 0 and proc[i][3] != 1:
            # if remaining time of process is 0
            # and
            # individual waiting time of process has not been calculated i.e flag
            wait_time += total_time_counted - proc[i][0] - proc[i][1]
            turnaround_time += total_time_counted - proc[i][0]
            # flag is set to 1 once wait time is calculated
            proc[i][3] = 1
print("\nAvg Waiting Time is ", (wait_time * 1) / total_p_no)
print("Avg Turnaround Time is ", (turnaround_time * 1) / total_p_no)