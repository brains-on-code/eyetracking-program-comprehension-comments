import random

# the csv file should start a new line for each participant. Each line should contain the tasks for that participant.
# There are a total of 14 tasks. Each participant should do all tasks in one of the two variations (CM or CP).
# Each participant should do each task only once. The order of the tasks should be random.

# create a list of tasks
tasks = ['Task1', 'Task2', 'Task3', 'Task4', 'Task5', 'Task6', 'Task7', 'Task8', 'Task9', 'Task10', 'Task11', 'Task12']

# create a list of variations
variations = ['CM', 'CP']

globalTaskCount = {}


def main():
    # create a list of participants
    participants = []

    # ask user for number of participants
    num_participants = 20

    # loop through number of participants
    for i in range(num_participants):
        participant_tasks = []
        task_count = {'CM': 0, 'CP': 0}

        # loop through tasks
        for task in tasks:
            if task_count.get('CP', 0) < len(tasks)/2 and globalTaskCount.get(task + 'CP', 0) < num_participants/2:
                variation = 'CP'
                task_count['CP'] += 1
            elif task_count.get('CM', 0) < len(tasks)/2 and globalTaskCount.get(task + 'CM', 0) < num_participants/2:
                variation = 'CM'
                task_count['CM'] += 1
            else:
                variation = random.choice(variations)
                task_count[variation] += 1

            # create a task string
            task_string = task + variation
            if task_string in globalTaskCount:
                globalTaskCount[task_string] += 1
            else:
                globalTaskCount[task_string] = 1

            # add task string to participant tasks list
            participant_tasks.append(task_string)

        # add participant tasks list to participants list
        # shuffle tasks
        random.shuffle(participant_tasks)
        participants.append(participant_tasks)

    # print participants in console for testing with line breaks
    for participant in participants:
        print(participant)

    # print task count for each task (cp and cm)
    for task in tasks:
        print(task + 'CM: ' + str(globalTaskCount[task + 'CM']))
        print(task + 'CP: ' + str(globalTaskCount[task + 'CP']))

    # create a csv file
    with open('./imageCombinations.csv', 'w') as f:
        # loop through participants
        for participant in participants:
            # loop through participant tasks
            for task in participant:
                # write task to csv file
                if task == participant[-1]:
                    f.write(task + '\n')
                else:
                    f.write(task + ',')

if __name__ == '__main__':
    main()
