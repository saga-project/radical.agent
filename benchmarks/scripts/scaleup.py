__author__    = "Ole Weidner"
__copyright__ = "Copyright 2013, Ole Weidner"
__license__   = "MIT"


""" Run this script to see how the agent behaves with increasing number 
    of cores / nodes to marshal. 

    We run this on stampede since it allows the largest core allocations on
    XSEDE. Details and queue names / limits can be found online:

    http://www.tacc.utexas.edu/user-services/user-guides/stampede-user-guide

    Without special request, the maximum number of cores is 4k (queue 'normal').
    With special access rights, it is possible to allocate 16k cores ('large').
"""

import os
import sys
import saga

EXPERIMENTPATH     = "%s" % os.getcwd()
PROCESSES_PER_NODE = 16 # each stampede node has 16 cores 
REPETITIONS        = 5  # repeat each experiment 5 times
CORE_CONFIG        = [64, 128, 256, 512, 1024, 2048, 3072, 4096]
QUEUE              = 'normal'
ALLOCATION         = 'TG-MCB090174'

# ----------------------------------------------------------------------------
#
def job_state_change_cb(src_obj, fire_on, value):
    print "  * Callback    : job state changed to '%s'" % value
    return True

# ----------------------------------------------------------------------------
#
def main():

    # iterate over all cores
    for cores in CORE_CONFIG:
        # repetitions
        for repetition in range(1, REPETITIONS+1):
            # create a working directory for this core/repetition tuple
            working_directory = "%s/%s-cores/rep-%s/" % (EXPERIMENTPATH, cores, repetition)
            if not os.path.exists(working_directory):
                os.makedirs(working_directory)
                print "Created new working directory '%s'" % working_directory
            else:
                print "Working directory '%s' exists. ABORTING." % working_directory
                return 1

            # create a workload input file in the working directory
            workload_filename = "%s/workload.json" % (working_directory)
            with open(workload_filename, 'w') as f:
                f.write("""
[
    {
     "type": "taskset", 
     "instances": %s, 
     "template": 
        {
        "type": "task", "id": "task-",   "executable": "/bin/sleep", "arguments": ["10"], "requirements": {"cores": 1}
        }
    }
]""" % str(cores*4)
                )

            # create a saga-job that launches a rhythmos-agent 
            try: 
                js = saga.job.Service("slurm://localhost")

                jd = saga.job.Description()
                jd.wall_time_limit   = 60 # minutes
                jd.total_cpu_count   = cores
                jd.working_directory = working_directory
               
                jd.queue             = QUEUE
                jd.project           = ALLOCATION
                jd.executable        = '/home1/00988/tg802352/software/bin/run-rhythmos-agent'
                jd.arguments         = ["--task-source=file://localhost//%s" % workload_filename , 
                                        "--task-results=file://localhost//%s/results.json" % working_directory,
                                        "--task-events=file://localhost//%s/events.json" % working_directory, 
                                        "--processes-per-node=%s" % PROCESSES_PER_NODE]
                jd.output            = "agent.out"
                jd.error             = "agent.err"

                # Create a new job from the job description
                rhythmos_instance = js.create_job(jd)

                # Now we can start our job.
                print "\nStarting Rhythmos Agent"
                rhythmos_instance.run()
                print "  * Job ID      : %s" % (rhythmos_instance.id)
                print "  * Job state   : %s" % (rhythmos_instance.state)
                # wait for our job to complete
                rhythmos_instance.wait()
                print "  * Job state   : %s" % (rhythmos_instance.state)

            except saga.SagaException, ex:
                # Catch all saga exceptions
                print "An exception occured: (%s) %s " % (ex.type, (str(ex)))
                print " \n*** Backtrace:\n %s" % ex.traceback
                rhythmos_instance.cancel()
                return 1

if __name__ == "__main__":
    sys.exit(main())
