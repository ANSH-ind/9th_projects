cimport cython
from libc.math cimport exp, sin, cos, log
import numpy as np
cimport numpy as cnp
from cython.parallel cimport prange

ctypedef fused dtype:
	float
	double


cdef void _kernel(dtype[:,::1] array, dtype base) noexcept nogil:

	cdef dtype div_term
	
	cdef Py_ssize_t row = array.shape[0]
	cdef Py_ssize_t col = array.shape[1]
	
	cdef Py_ssize_t i,z
	
	for i in prange(row,schedule='static'):
		div_term = exp(i*(-log(base)col))			
		for z in range(0, col, 2):
			array[i, z] = sin(z/div_term)
			array[i, z+1] = cos(z/div_term)

cdef void _procces_float_kernel(cnp.ndarray array, dtype base):
	cdef float[:,::1] float_array = array
	_kernel(float_array, base)

cdef void _procces_double_kernel(cnp.ndarray array, dtype base):
	cdef double[:,::1] double_array = array
	_kernel(double_array, base)

cpdef cnp.ndarray pos_encoding(cnp.ndarray array, int axis = -1, dtype base = 10000.0):
	cdef cnp.npy_intp* original_shape = array.shape
	cdef Py_ssize_t i
	ndim = array.ndim

	
	if axis >= ndim or axis < -ndim:
		raise ValueError(
    f"axis {axis} is out of bounds for array of dimension {array.ndim}"
    )
    
	if axis < 0:
		axis += ndim
	list_shape = []
	cdef Py_ssize_t j
	for i in range(ndim):
		list_shape.append(original_shape[i])
	
	if axis == array.ndim - 1 and array.flags["C_CONTIGUOUS"]:
		if array.dtype.num == cnp.NPY_FLOAT32:
			array = array.reshape(-1, array.shape[axis])
			_procces_float_kernel(array, base)
		elif array.dtype.num == cnp.NPY_FLOAT64:
			array = array.reshape(-1, array.shape[axis])
			_procces_double_kernel(array, base)
		else:
			raise TypeError(
			f"Unsupported dtype '{array.dtype}'."
		)
		array = array.reshape(tuple(list_shape))
		return array
	
	array = np.swapaxes(array, axis, -1)
	z = []
	for j in range(ndim):
		z.append(array.shape[j])
	
	if not array.flags["C_CONTIGUOUS"]:
		array = np.ascontiguousarray(array)
	
	array = array.reshape(-1, original_shape[axis])
	
	if array.dtype.num == cnp.NPY_FLOAT32:
		_procces_float_kernel(array)
	elif array.dtype.num == cnp.NPY_FLOAT64:
		_procces_double_kernel(array)
	else:
		raise TypeError(
        f"Unsupported dtype '{array.dtype}'."
    )
	
	array = array.reshape(tuple(z))
	array = np.swapaxes(array, -1, axis)
	return array
	