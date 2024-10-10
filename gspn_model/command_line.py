import errno
import os
import subprocess
import itertools
import sys
import multiprocessing
import shutil


def run_subprocess(queue, parameters, lock):
    try:
        subprocess.run(parameters, check=True)
        # Add any additional synchronization logic if needed
        with lock:
            queue.put(parameters)
    except subprocess.CalledProcessError as e:
        print(f"Error in subprocess {parameters}: {e}")


parameters = ['chload',
              'chparallel',
              'rch',
              'rendcall',
              'rfraud'
              ]
vals = {
    'chload': {
        'start': 5,
        'stop': 45,
        'step': 5
    },
    'chparallel': {
        'start': 3,
        'stop': 9,
        'step': 2
    },
    'rch': {
        'start': 7200,
        'stop': 28800,
        'step': 1800
    },
    'rendcall': {
        'start': 100,
        'stop': 3600,
        'step': 500

    },
    'rfraud': {
        'start': 30,
        'stop': 180,
        'step': 30
    },
}


if __name__ =='__main__':
    path = 'files/shared'
    model_name = 'Shared'
    pvals = {f'-{p}': list(range(vals[p]['start'], vals[p]['stop'] + vals[p]['step'], vals[p]['step'])) for p in parameters}
    pvals['-pfraud'] = [1, 3, 9, 19, 99]
    parameters.append('pfraud')
    subprocess_number = 10
    queue = multiprocessing.Queue()
    lock = multiprocessing.Lock()

    l = list(pvals.values())
    lvals = list(itertools.product(*l))
    numexec = 0
    numtot = len(lvals)
    processes = []

    for idx, val in enumerate(lvals):
        if idx == 30:
            print('fine')
            print(numexec)
            print(numtot)
            sys.exit()
        # creo il formato base del comando da lanciare
        s = ['./analysis.sh']
        dirname = f'{path}/execution'
        for z in zip(parameters, val):
            # aggiungo i parametri
            if z[0][0] == 'r':
                v = 1/z[1]
            else:
                v = z[1]
            s.extend([f'-{z[0]}',f'{v}'])
            dirname += f'_{z[0]}-{z[1]}'
        # creo cartella con risultati esecuzione
        try:
            os.mkdir(dirname)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass
        shutil.copyfile(f'{path}/{model_name}.net', f'{dirname}/{model_name}.net')
        shutil.copyfile(f'{path}/{model_name}.def', f'{dirname}/{model_name}.def')
        # raggruppo per subprocess_number
        s.extend(['-model', f'{dirname}/{model_name}'])
        print(f'eseguito comando {s}\n')
        process = multiprocessing.Process(target=run_subprocess, args=(queue, s, lock))
        processes.append(process)
        process.start()

        if (idx + 1) % subprocess_number == 0:
            numexec += subprocess_number
            print(f'eseguiti {subprocess_number} processi in parallelo... li sincronizzo\n')
            for process in processes:
                process.join()  # sincronizzo i processi
            subtask = []
            processes = []

    if numexec < numtot:
        for process in processes:
            process.join()  # sincronizzo i processi
        subtask = []
        processes = []
        print('esecuzione terminata\n')
# shellscript = subprocess.Popen(["shellscript.sh"], stdin=subprocess.PIPE)


# shellscript.stdin.write("yes\n")
# shellscript.stdin.close()
# returncode = shellscript.wait()
