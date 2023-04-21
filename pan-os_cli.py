"""

pan-os_cli v1.0 [20230421]

Script to repeat CLI commands on PAN-OS over SSH

by Terence LEE <telee.hk@gmail.com>

https://github.com/telee0/pan_scripts
https://pexpect.readthedocs.io/en/stable/index.html

"""

import json
import os
import re
import time
import traceback
from datetime import datetime
from os import makedirs

import paramiko
from paramiko_expect import SSHClientInteraction

from cli import cf, cli, metrics

verbose, debug = True, False


def collect_data():
    hostname = cf['hostname']
    username = cf['username']
    password = cf['password']
    prompt = cf['prompt']

    iterations = cf['iterations']
    time_delay = cf['time_delay']
    time_interval = cf['time_interval']

    cli_timeout = cf['cli_timeout']

    client = None

    # SSH to login
    #
    try:
        # Create a new SSH client object
        client = paramiko.SSHClient()

        # Set SSH key parameters to auto accept unknown hosts
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(hostname=hostname, username=username, password=password)
    except Exception as e:
        print("go:", e)
        client.close()
        return

    output = []

    try:
        with SSHClientInteraction(client, timeout=10, display=False) as interact:
            print(f"-- sleep for {time_delay} seconds..")
            time.sleep(max(3, time_delay))  # wait for at least 3 seconds
            interact.send("")
            for i in range(iterations):
                for c in cli:
                    if verbose:
                        t = datetime.now().strftime('%H:%M:%S')
                        print(f"[{i:02d} {t}] c =", c)

                    command, count, timeout = c[0], 1, cli_timeout

                    c_len = len(c)
                    if c_len >= 2:
                        count = max(count, c[1])  # make sure at least once
                        if c_len >= 3:
                            timeout = min(timeout, c[2])  # if 0 no_prompt = True
                    no_prompt = False
                    if timeout <= 0:
                        no_prompt = True
                    for j in range(count):  # repeat_count of each command
                        if not no_prompt:
                            interact.expect([prompt], timeout=timeout)
                        interact.send(command)
                        output.append(interact.current_output_clean)
                if i < iterations - 1:
                    print(f"-- sleep for {time_interval} seconds..")
                    time.sleep(time_interval)

            # check here for more use cases
            #
            # https://github.com/fgimian/paramiko-expect/blob/master/examples/paramiko_expect-demo.py

            command = 'exit'
            interact.send("")
            interact.expect([prompt])
            interact.send(command)
            output.append(interact.current_output_clean)

        if debug:
            print("\n".join(output))

    except Exception as e:
        print(e)
        traceback.print_exc()
    finally:
        client.close()

    return output


def write_data(data, stats=None):

    target_dir = './'
    t = datetime.now().strftime('%Y%m%d%H%M')
    ddhhmm = t[6:12]

    job_dir = cf['job_dir'].format(ddhhmm)

    # prepare the directory structure for job files
    #
    makedirs(job_dir, exist_ok=True)
    os.chdir(job_dir)

    cnf_file = cf['cnf_file'].format(ddhhmm)
    cli_file = cf['cli_file'].format(ddhhmm)
    sta_file = cf['sta_file'].format(ddhhmm)

    if verbose:
        # print(json.dumps(data, indent=4))
        pass

    file = target_dir + cnf_file
    with open(file, 'a') as f:
        f.write(json.dumps({'cf': cf, 'cli': cli, 'metrics': metrics}, indent=4))
        if verbose:
            print(f"-- generate config file {file}")

    file = target_dir + cli_file
    with open(file, 'a') as f:
        f.write("\n".join(data))
        if verbose:
            print(f"-- generate output file {file}")

    file = target_dir + sta_file
    with open(file, 'a') as f:
        f.write(json.dumps(stats, indent=4))
        if verbose:
            print(f"-- generate stats file {file}")


def analyze(data):

    output = {}

    results = {}
    for key in metrics.keys():
        pattern = metrics[key]
        results[key] = []
        for i, text in enumerate(data):
            matches = re.findall(pattern, text)
            if matches:
                for m in matches:
                    results[key].append(m)
                    break  # skip the rest of the matches
                if debug:
                    print("matches:", matches)
            if debug:
                print(f"{i} - text =", text)
                print("-" * 80)
        if len(results[key]) == 0:  # delete empty matches from the results
            del results[key]

    for key in results.keys():
        v_0 = float(results[key][0])
        s = {
            'min': v_0, 'max': v_0,
            'ave': 0,
            'cnt': len(results[key])
        }
        for v_i in results[key]:
            value = float(v_i)
            s['min'] = min(s['min'], value)
            s['max'] = max(s['max'], value)
            s['ave'] += value
        s['ave'] /= s['cnt']
        print()
        print(f"{key}:", results[key])
        print(f"stats:", s)
        output[key] = s

    return output


if __name__ == '__main__':
    data_ = collect_data()
    stats_ = analyze(data_)
    write_data(data_, stats_)
