#define PY_ARRAY_UNIQUE_SYMBOL cool_ARRAY_API
#define NO_IMPORT_ARRAY

#include <stdio.h>
#include <stdlib.h>

#include "Python.h"
#include "math.h"
#include "numpy/arrayobject.h"

/* Needs to be compiled as C files because of the Naming problem in Namespace */
#ifdef __cplusplus 
extern "C" {  
#endif 

/*
    Calculate the new centers in the received block.
*/
int closest_center(double point_data[], PyArrayObject *centers, int cluster_size, int dimension)
{
    /* Given the centers and one point and return which center is nearest to the point */
    int i, j;
    double min_distance = 1E100;
    double distance;
    int min_index = 0;  
    for (i = 0; i < cluster_size; i++)
    {
        distance = 0;
        for (j = 0; j < dimension; j++)
        {
            distance += pow(point_data[j] - (*(double*)PyArray_GETPTR2(centers, i, j)), 2);
        }
        if (distance <= min_distance)
        {
            min_distance = distance;
            min_index = i;
        }
    }
    return min_index;
}
  
PyObject* kmeans_chunk_center(PyArrayObject *data, PyArrayObject *centers, PyObject *data_assigns)
{
    /* Record the nearest center of each point and renew the centers with the points near one given center. */
    int cluster_size, dimension, chunk_size;
    cluster_size = *(int *)PyArray_DIMS(centers);
    dimension = PyArray_DIM(centers, 1);
    chunk_size = *(int *)PyArray_DIMS(data);
    int *centers_counter = (int *)malloc(sizeof(int) * cluster_size);
    double *new_centers = (double *)malloc(sizeof(double) * cluster_size * dimension);
    int i, j;
    int closest_center_index;
    double* point_data[dimension];

    for (i = 0; i < cluster_size; i++)
    {
	    (*(centers_counter + i)) = 0;
    }

    for (i = 0; i < cluster_size * dimension; i++)
    {
	    (*(new_centers + i)) = 0;
    }

    for (i = 0; i < chunk_size; i++)
    {
        for (j = 0; j < dimension; j++)
        {
            point_data[j] = (double*)PyArray_GETPTR2(data, i, j);
        }
        closest_center_index = closest_center((*point_data), centers, cluster_size, dimension);
        PyList_SetItem(data_assigns, i, PyInt_FromLong(closest_center_index));
        (*(centers_counter + closest_center_index))++;
        for (j = 0; j < dimension; j++)
        {
            (*(new_centers + closest_center_index * dimension + j)) += (*point_data[j]);
        }
    }

    for (i = 0; i < cluster_size; i++)
    {
        if (*(centers_counter + i) == 0)
        {
            for (j = 0; j < dimension; j++)
            {
                (*(new_centers + i * dimension + j)) = (*(double*)PyArray_GETPTR2(centers, i, j));
            }
        }
        else
        {
            for (j=0; j < dimension; j++)
            {
                (*(new_centers + i * dimension + j)) /= (*(centers_counter + i));
            }
        }
    }

    PyObject* return_new_centers;
    npy_intp dims[2] = {cluster_size, dimension};
    return_new_centers = PyArray_SimpleNew(2, dims, NPY_DOUBLE);
    void *arr_data = PyArray_DATA((PyArrayObject*)return_new_centers);
    memcpy(arr_data, new_centers, PyArray_ITEMSIZE((PyArrayObject*) return_new_centers) * cluster_size * dimension);
    /* Need to copy the data of the malloced buffer to the PyObject
       since the malloced buffer will disappear after the C extension is called. */
    free(centers_counter);
    free(new_centers);
    return (PyObject*) return_new_centers;
}

#ifdef __cplusplus  
} 
#endif 
