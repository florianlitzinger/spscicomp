import numpy 
import hmm.kernel.python

def random_sequence(A, B, pi, T, kernel=hmm.kernel.python):
    obs = kernel.random_sequence(A, B, pi, T)
    return obs

models = dict();

models['hmm_1'] =  (
    numpy.array(
        [[0.8, 0.2, 0.0],
         [0.0, 0.2, 0.8],
         [1.0, 0.0, 0.0]],
    ),
    numpy.array(
        [[1.0, 0.0],
         [0.0, 1.0],
         [0.0, 1.0]],
    ),
    numpy.array(
        [0.5, 0.5, 0.0],
    )
)
models['equi32'] = (
    numpy.array(
        [[ 0.333, 0.333, 0.333 ],
         [ 0.333, 0.333, 0.333 ],
         [ 0.333, 0.333, 0.333 ]], numpy.float32),
    numpy.array(
        [[ 0.5, 0.5 ],
         [ 0.5, 0.5 ],
         [ 0.5, 0.5 ]], numpy.float32),

    numpy.array([ 0.333, 0.333, 0.333 ], numpy.float32)
)
models['equi64'] = (
    numpy.array(
        [[ 0.333, 0.333, 0.333 ],
         [ 0.333, 0.333, 0.333 ],
         [ 0.333, 0.333, 0.333 ]], numpy.float64),

    numpy.array(
        [[ 0.5, 0.5 ],
         [ 0.5, 0.5 ],
         [ 0.5, 0.5 ]], numpy.float64),

    numpy.array([ 0.333, 0.333, 0.333 ], numpy.float64)
)
models['t2'] = (
    numpy.array(
        [[0.9, 0.05, 0.05],
         [0.1, 0.1, 0.9],
         [1.0, 0.0, 0.0]], numpy.float32),
    numpy.array(
        [[ 1.0,  0.0],
         [0., 1.0],
         [0., 1.0]], numpy.float32
    ),
    numpy.array(
        [0.333, 0.333, 0.333], numpy.float32
    ),
)
models['tbm1'] = (
	numpy.array(
		[[0.3, 0.3, 0.2, 0.1, 0.1],
		 [0.1, 0.3, 0.3, 0.2, 0.1],
		 [0.0, 0.1, 0.8, 0.1, 0.0],
		 [0.1, 0.2, 0.3, 0.3, 0.1],
		 [0.0, 0.0, 0.1, 0.3, 0.6]], numpy.float64),
	numpy.array(
		[[0.2, 0.2, 0.2, 0.4],
		 [1.0, 0.0, 0.0, 0.0],
		 [0.0, 0.2, 0.8, 0.0],
		 [0.0, 0.0, 0.0, 1.0],
		 [0.2, 0.8, 0.0, 0.0]], numpy.float64),
	numpy.array(
		[0.2, 0.2, 0.2, 0.2, 0.2],numpy.float64)
)

def get_models():
    return models

def compare_models(A1, B1, pi1, A2, B2, pi2, T, kernel=hmm.kernel.python):
    """ Give a measure for the similarity of two models."""
    obs = kernel.random_sequence(A2, B2, pi2, T)
    logprob1, _, _ = kernel.forward(A1, B1, pi1, obs)
    logprob2, _, _ = kernel.forward(A2, B2, pi2, obs)
    similarity1 = (logprob2 - logprob1) / float(T)
    obs = kernel.random_sequence(A1, B1, pi1, T)
    logprob1, _, _ = kernel.forward(A1, B1, pi1, obs)
    logprob2, _, _ = kernel.forward(A2, B2, pi2, obs)
    similarity2 = (logprob2 - logprob1) / float(T)
    return 0.5 * (similarity1 + similarity2)

def generate_startmodel(N, M, dtype=numpy.float64):
	A  = numpy.ones( (N,N), dtype=dtype)
	B  = numpy.ones( (N,M), dtype=dtype)
	pi = numpy.ones(  N   , dtype=dtype)

	for i in range(N):
		for j in range(N):
			if (i==j):
				A[i,j] = 0.8
			else:
				A[i,j] = 0.2 / float(N-1)

	#A /= float(N)
	B /= float(M)
	pi /= float(N)
	return (A, B, pi)