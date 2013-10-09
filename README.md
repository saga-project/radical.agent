Package radical.agent
=====================

The radical.agent package provides a stand-alone pilot job agent.


Installation
------------

You can install the latest radical.agent directly from [PyPi](https://pypi.python.org/pypi/radical.agent/):

    pip install --upgrade radical.agent

You can also install the latest development version (which might be broken)
from GitHub directly:

    pip install -e git://github.com/saga-project/radical.agent.git#egg=radical.agent

Command-Line Invocation
-----------------------

While radical.agents are meant to be deployed automatically by a pilot provisioning mechanism, they can be used independently. In this _usage mode_ they pretty much behave like an _original_ Pilot Job, i.e., providing late-binding on a single HPC system. 

The agent executable (which is installed via the `radical.agent` package) is invoked on the command line. The `--help` option shows the command-line options:

```bash
radical-agent --help
Usage: radical-agent [options]

Options:
  -h, --help            show this help message and exit
  -t URL, --task-source=URL
                        Specifies the location where to pull the tasks from.
  -r URL, --task-results=URL
                        Specifies the location where to publish the task
                        results. [default: file:///dev/stdout]
  -e URL, --task-events=URL
                        Specifies the location where to publish the task
                        events. [default: file:///dev/stdout]
  -m URL, --task-metrics=URL
                        Specifies the location where to publish task metrics.
  -l URL, --agent-logs=URL
                        Specifies the location where to publish agent log
                        data. [default: file:///dev/stderr]

  Execution Options:
    These options control task execution

    -w DIRECTORY, --workdir=DIRECTORY
                        Specifies the working directory for the agent.
                        [default: .]
    --processes-per-node=COUNT
                        Maximum number of processes to run concurrently on a
                        node. [default: number of cores per node]
    --detect-node-failure
                        Try to detect erratic node behavior and move tasks
                        away from faulty nodes. [default: disabled]
```

The idea is that each input channel (task source) and output channel (results, events, metrics, log) can be controlled and redirected independently. The underlying implementation is adaptor-based, similar to SAGA. 

Currently a set of file-based adaptors exist - they support both physical files as well as STOUT and STDERR. The adaptors use JSON as the file-format for input and output.

### A Simple Example

Let's run a couple of tasks! 

With the file-based task-source adaptor, you have to define your tasks as a JSON file. It's pretty straight forward, the only odd part is that you have to define an 'id' for each task. That's because the agent itself doesn't manage task ids since they are usually specific to the backend / workload manager. The example input file uses integers, but task ids can be random strings - the only requirement is that they are unique.

As a first _experiment_, put the following into a file and save it as `input.json`:

```json
[
  {"type":"task", "id":"1",   "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}},
  {"type":"task", "id":"2",   "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}},
  {"type":"task", "id":"3",   "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}},
  {"type":"task", "id":"4",   "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}},
  {"type":"task", "id":"5",   "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}},
  {"type":"task", "id":"6",   "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}},
  {"type":"task", "id":"7",   "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}},
  {"type":"task", "id":"8",   "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}},
  {"type":"task", "id":"9",   "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}},
  {"type":"task", "id":"10",  "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}},
  {"type":"task", "id":"11",  "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}},
  {"type":"task", "id":"12",  "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}},
  {"type":"task", "id":"13",  "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}},
  {"type":"task", "id":"14",  "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}},
  {"type":"task", "id":"15",  "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}},
  {"type":"task", "id":"16",  "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}}
]
```

Alternatively, you can define a task set instead of individual tasks. A task set is described by a template task and the number of tasks instances you want to generated:

```
[
  {
    "type":"taskset", 
    "instances": 16, 
    "template": 
    {
      "type":"task", "id": "set_1-task_",   "executable": "/bin/hostname", "arguments": ["-f"], "requirements": {"cores": 1}
    }
  }
]
```

Next, invoke the agent to execute the workload:

```bash
radical-agent --task-source=file:////`pwd`/input.json  --task-results=file:////`pwd`/results.json
```

You will see the agent starting to work, executing the tasks from `input.json`. Events will show up on the console, since --task-events=file:///dev/stdout is the default:

```json
{"timestamp": "2013-07-11 10:03:52.707306", "value": "RUNNING", "type": "event", "event": "STATECHANGE", "task_id": "1"}
{"timestamp": "2013-07-11 10:03:52.709479", "value": "RUNNING", "type": "event", "event": "STATECHANGE", "task_id": "2"}
```

Results will end up in a file called `results.json`. The result set for each task looks like this:

```json
{"cmdline": "/usr/local/bin/mpirun -np 1 -host localhost /bin/hostname  -f ", "working_directory": "/Users/oweidner/Projects/RHYTHMOS/radical.agent/task-16", "stderr": "/Users/oweidner/Projects/RHYTHMOS/radical.agent/task-16/STDERR", "task_id": "16", "stdout": "/Users/oweidner/Projects/RHYTHMOS/radical.agent/task-16/STDOUT", "execution_location": ["localhost"], "start_time": "2013-07-11 10:03:54.763593", "type": "result", "exit_code": 0, "stop_time": "2013-07-11 10:03:55.768100"}
```

If no working directory is defined for a task, radical.agent creates a subdirectory `task-<task_id>` in the agent's working directory (can be controlled via `--workdir=`). Note that radical.agent will fail if you invoke the same command line a second time since the task-* directories already exist.

radical.agent can (or at least tries to) detect the number of cores and nodes that are available for execution. It can also detect things like MPI. So if you, for example, run the above example on an 8-core system, you will see that radical.agent processes the tasks in batches of 8. Future versions will allow to change that behavior, but that's still work in progress.

**On a Cluster**

You can try to launch a radical.agent via PBS to see how it can marshal multiple nodes. Wrapping everything in a simple PBS script (here for india.futuregrid.org) is sufficient.

```bash
#PBS
#PBS -N radical
#PBS -e radical.err 
#PBS -o radical.out 
#PBS -l nodes=2:ppn=1 
#PBS -q batch

source /N/u/oweidner/radical/bin/activate

radical-agent \
-w /N/u/oweidner/tmp/ \
-t file:///N/u/oweidner/16_bfast_tasks.json \
-r file:///N/u/oweidner/tmp/results.json \
-e file:///N/u/oweidner/tmp/events.json
```

If you look at the results file, you will see that half of the tasks executed on one node and the other half on another node: 

```json
{"task_id": "1", ..., "execution_location": ["i60"], ...}
{"task_id": "2", ..., "execution_location": ["i62"], ...}
```