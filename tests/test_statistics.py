from agent_workflow_comparative_eval import wilson_interval, paired_bootstrap_interval, paired_binary_deltas

def test_wilson_known_vector():
    assert wilson_interval(8,10)==[0.490162,0.943318]

def test_bootstrap_is_deterministic():
    a=paired_bootstrap_interval([1,-1,1,0,1],label="fixture",samples=1000)
    b=paired_bootstrap_interval([1,-1,1,0,1],label="fixture",samples=1000)
    assert a==b and a["n"]==5

def test_binary_deltas(): assert paired_binary_deltas([False,True],[True,False])==[1.0,-1.0]
