import math
#define the cosin similarity function
def cosin_similarity(A,B):
    #find the dot product of 'A' and 'B' 
    dot = math.sumprod(A,B)
    #now find magnitude of 'A' and 'B'
    magnitude_a = math.sqrt(sum(a*a for a in A))
    magnitude_b = math.sqrt(sum(b*b for b in B))
    return dot/(magnitude_a*magnitude_b)

a = [1,2,3,4]
b = [1,2,3,4]
print(cosin_similarity(a,b))
#output become 1
