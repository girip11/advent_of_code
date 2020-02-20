# Puzzle 1 Approaches

## Approach 1

* Parse each claim to get the rectangle coordinates
* For every unique pair of rectangle, find the intersecting points and add those points to a set.
* Length of the set gives the output
* Compute Complexity - O(n^2) where n is the number of claims.
* Memory complexity - O(i) - where i is the total number of intersecting points

## Approach 2

* Parse each claim to get the rectangle coordinates
* For each rectangle, keep adding its coordinates to a hash with the claim ID as the value.
* Iterate through the hash to find out all the points with >= 2 claims
* Compute complexity - O(n) - where n is the number of claims.
* Memory complexity - O(i) - where i is the total number of points on all the rectangles. (Ignoring the space used for storing the claim ids)

## Approach 3 (Difference in data structures used Array over Hash)

This approach is a slight modification to the approach 2 (implementation wise) which could improve on memory usage, since the count of the points is what is required.

* Parse each claim to get the rectangle coordinates.
* Get the minimum and maximum row and column from all of the claims/rectangle.
* Using these values initialize an array or size [(max_row - min_row) + 1, (max_col - min_col) + 1].
* For each rectangle, map its coordinates to the array position and add a count to value in the index pointed to by the coordinates.
* Iterate through the array to find out all the values >= 2
* Compute complexity - O(n) - where n is the number of claims.
* Memory complexity - O(i) - where i is the total number of points on all the rectangles
