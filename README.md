# JoinOptimizationAlgorithm Description
This is a simple join optimization algorithm, JOA for short, for an RDBMS, implemented using Dynamic Programming, to find the lowest cost plan for a natural chain join query *Q* in terms of R<sub>0</sub>(A<sub>0</sub>, A<sub>1</sub>) &bowtie; R<sub>0</sub>(A<sub>1</sub>, A<sub>2</sub>) . . . R<sub>n−2</sub>(A<sub>n−2</sub>, A<sub>n−1</sub>) &bowtie; R<sub>n−1</sub>(A<sub>n−1</sub>, A<sub>n</sub>). The cost of a join plan is the sum of the estimated cardinalities of its intermediate node.

# Constraints
  - Fullness: Each relation appears only once.
  - Cartesian Product-free: Join two relations only when they share columns. 
  - Left-relation is smaller property: Relation with a smaller cardinality is always on the left.
 
# Usage
```bash
python main.py --query sample.in
```

# Example
### Sample Input
  - Line 1: an integer representing the number of relations R0, ..., Rn−1
  - Line 2: n cardinalities indicating the cardinality for each relation, separated by comma
  - Line 3: n-1 relations, suffixed by “R” which describe for each Ri, Ri+1 which one has a foreign key to the other
```bash
3
5,10,15
R1,R2
```

### Sample Output
The best plan is to join R<sub>0</sub> and R<sub>1</sub> first and get an estimated cardinality of 5, then join R<sub>2</sub> to attain a total cardinality of 5.
```bash
		         R0
	    JO(5)
		         R1
JO(5)
	    R2
```
