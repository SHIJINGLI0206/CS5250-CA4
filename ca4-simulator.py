'''
CS5250 Assignment 4, Scheduling policies simulator

Input file:
    input.txt
Output files:
    FCFS.txt
    RR.txt
    SRTF.txt
    SJF.txt
'''

import sys
input_file = 'input.txt'


class Process:
    last_scheduled_time = 0
    def __init__(self, id, arrive_time, burst_time):
        self.id = id
        self.arrive_time = arrive_time
        self.burst_time = burst_time
        self.burst_time_next = 0
        self.last_burst_time = 0

    #for printing purpose
    def __repr__(self):
        return ('[id %d : arrival_time %d,  burst_time %d]'%(self.id, self.arrive_time, self.burst_time))

def FCFS_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    waiting_time = 0
    for p in process_list:
        if current_time < p.arrive_time:
            current_time = p.arrive_time
        schedule.append((current_time,p.id))
        waiting_time += (current_time - p.arrive_time)
        current_time = current_time + p.burst_time
    average_waiting_time = waiting_time/float(len(process_list))
    return schedule, average_waiting_time

#Input: process_list, time_quantum (Positive Integer)
#Output_1 : Schedule list contains pairs of (time_stamp, proccess_id) indicating the time switching to that proccess_id
#Output_2 : Average Waiting Time


def RR_scheduling(process_list, time_quantum):
    # store the (switching time, proccess_id) pair
    schedule = []
    current_time = 0
    len_process = len(process_list)
    waiting_time = [0 for i in range(len_process)]
    burst_time_remaining = [process.burst_time for process in process_list]

    while True:
        is_done = 0
        for i in range(len_process):
            if current_time < process_list[i].arrive_time:
                continue
            if burst_time_remaining[i] > 0:
                schedule.append((current_time,process_list[i].id))
                print('schedule',schedule)
                exec_time = process_list[i].burst_time - burst_time_remaining[i]
                waiting_time[i] = (current_time - exec_time - process_list[i].arrive_time)
                print('waittime: ', waiting_time)
                if process_list[i].burst_time > time_quantum:
                    current_time = current_time + time_quantum
                    burst_time_remaining[i] = burst_time_remaining[i] - time_quantum
                else:
                    current_time += burst_time_remaining[i]
                    burst_time_remaining[i] = 0
            else:
                is_done += 1

        if is_done == len_process:
            break
    average_waiting_time = sum(waiting_time)/float(len_process)
    return schedule, average_waiting_time


def SRTF_scheduling(process_list):
    #store the (switching time, proccess_id) pair
    schedule = []
    old_idx = -1
    current_time = 0
    len_process = len(process_list)
    waiting_time = [0 for i in range(len_process)]
    burst_time_remaining = [process.burst_time for process in process_list]

    while sum(burst_time_remaining) > 0:
        burst_min = min(br for(br, p) in zip(burst_time_remaining, process_list) if br > 0 and
                        p.arrive_time <= current_time)
        idx = burst_time_remaining.index(burst_min)
        p_min = process_list[idx]

        if idx != old_idx:
            schedule.append((current_time,p_min.id))
            print('schedule:: ', schedule)
            old_idx = idx
        exec_time = process_list[idx].burst_time - burst_time_remaining[idx]
        waiting_time[idx] = (current_time - exec_time - process_list[idx].arrive_time)
        burst_time_remaining[idx] -= 1
        current_time += 1
    average_waiting_time = sum(waiting_time)/float(len_process)
    return schedule, average_waiting_time


def SJF_scheduling(process_list, alpha):
    #store the (switching time, proccess_id) pair
    schedule = []


    current_time = 0
    #  data structure:
    #  { pid : [predicted_burst_time, last_burst_time] }
    process_predicted = {}
    queued_process = [p for p in process_list]
    len_process = len(process_list)
    waiting_time = [0 for _ in range(len_process)]
    burst_time_remaining = [process.burst_time for process in process_list]

    pmax = 0
    while pmax >=0:
        print(queued_process[0].burst_time_next)
        pmax = max(p.burst_time_next for p in queued_process)
        q = 0
        for i in range(len(queued_process)):
            if queued_process[i].burst_time_next >=0:
                if queued_process[i].arrive_time <= current_time:
                    q += 1
                    if len(process_predicted) > 0 and queued_process[i].id in process_predicted.keys():
                        process_predicted[queued_process[i].id] = [alpha * process_predicted[queued_process[i].id][0] +
                                                                  (1 - alpha) * process_predicted[queued_process[i].id][1],
                                                                  queued_process[i].burst_time ]
                    else:
                        print(queued_process[i].id)
                        # initial value for T1 is 5
                        process_predicted[queued_process[i].id] = [5, queued_process[i].burst_time]
                    queued_process[i].burst_time_next = process_predicted[queued_process[i].id][0]
                    print("i, next",(i,queued_process[i].burst_time_next))
                elif queued_process[i].arrive_time > current_time and q == 0:
                    q = 1
                    current_time = queued_process[i].arrive_time
                    process_predicted[queued_process[i].id] = [alpha * process_predicted[queued_process[i].id][0] +
                                                               (1 - alpha) * process_predicted[queued_process[i].id][1],
                                                               queued_process[i].burst_time]
                    queued_process[i].burst_time_next = process_predicted[queued_process[i].id][0]





        for k in range(q):
            idx = -1
            pred_proc_burst_min = None #queued_process[0]
            for j,p in enumerate(queued_process):
                if p.burst_time_next > 0 :
                    if idx == -1 or pred_proc_burst_min == None or pred_proc_burst_min.burst_time_next > p.burst_time_next:
                        pred_proc_burst_min = p
                        idx = j
            queued_process[idx].burst_time_next = -1

            schedule.append((current_time,pred_proc_burst_min.id))
            print('schedule: ', schedule)
            waiting_time[idx] += (current_time - pred_proc_burst_min.arrive_time)
            print('wating time: ',(idx,waiting_time[idx]))
            current_time = current_time + pred_proc_burst_min.burst_time
            #queued_process[i].burst_time_next = -1
                #queued_process.remove(pred_proc_burst_min)

    average_waiting_time = sum(waiting_time)/float(len(process_list))
    return schedule, average_waiting_time


def read_input():
    result = []
    with open(input_file) as f:
        for line in f:
            array = line.split()
            if (len(array) != 3):
                print ("wrong input format")
                exit()
            result.append(Process(int(array[0]),int(array[1]),int(array[2])))
    return result


def write_output(file_name, schedule, avg_waiting_time):
    with open(file_name,'w') as f:
        for item in schedule:
            f.write(str(item) + '\n')
        f.write('average waiting time %.2f \n'%(avg_waiting_time))


def main(argv):
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)

    print("simulating FCFS ----")
    FCFS_schedule, FCFS_avg_waiting_time = FCFS_scheduling(process_list)
    write_output('FCFS.txt', FCFS_schedule, FCFS_avg_waiting_time )

    print("simulating RR ----")
    RR_schedule, RR_avg_waiting_time = RR_scheduling(process_list,time_quantum = 2)
    write_output('RR.txt', RR_schedule, RR_avg_waiting_time )

    print ("simulating SRTF ----")
    SRTF_schedule, SRTF_avg_waiting_time = SRTF_scheduling(process_list)
    write_output('SRTF.txt', SRTF_schedule, SRTF_avg_waiting_time )

    print ("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time = SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

if __name__ == '__main__':
    #main(sys.argv[1:])
    process_list = read_input()
    print ("printing input ----")
    for process in process_list:
        print (process)

    print("simulating SJF ----")
    SJF_schedule, SJF_avg_waiting_time = SJF_scheduling(process_list, alpha = 0.5)
    write_output('SJF.txt', SJF_schedule, SJF_avg_waiting_time )

