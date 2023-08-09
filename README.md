# dnamic

DNA microscopy code base

DNA microscopy is a new technology development program to achieve spatio-genetic imaging without the use of specialized machinery.

## Setup w/ python 2.7 (original version):
```
conda create --name dnamic python=2.7
conda activate dnamic
conda install -c conda-forge numpy biopython scipy numba
```

## Convert to python3:
Install [`2to3`](https://docs.python.org/3/library/2to3.html)
```
pip install 2to3
```

Convert with `2to3`, putting the new files 
```
2to3 -n -w -o ./py3 py/ 
```