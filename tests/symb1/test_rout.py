import time
import os, os.path
import pickle
import subprocess
import numpy
from nose.tools import ok_, nottest, with_setup

ahkab_path = "../../ahkab/ahkab.py"

def _run_test(ref_run=False):
	netlist = "rout.ckt"
	data_file = "rout" if not ref_run else "rout-ref"
	print "Running test... "
	start = time.time()
	proc = subprocess.Popen(["python", ahkab_path, "-v", "0", "-o", data_file, netlist])
	proc.communicate()
	stop = time.time()
	times = stop-start
	print "Done. The test took %f s" % times
	data = numpy.loadtxt(data_file+".tran")
	return data, times

def teardown_func():
	for f in ("rout.symbolic", ):
		os.remove(f)

@with_setup(None, teardown_func)
def test():
	ref_run = not os.path.isfile('rout-ref.tran')

	if not ref_run:
		res = numpy.loadtxt("colpitts-ref.tran")
	else:
		print "RUNNING REFERENCE RUN - INVALID TEST!"

	res_new, time_new = _run_test(ref_run)

	ok_(numpy.allclose(res_new, res, rtol=er, atol=ea), "Test colpitts FAILED")

if __name__ == '__main__':
	data = numpy.loadtxt("colpitts-ref.tran")
	
