class DimensionError(Exception):
    def __init__(self,p,q):
        self.len1 = len(p)
        self.len2 = len(q)

    def __str__(self):
        return 'dimensions not equal: '+str(self.len1)+'<>'+str(self.len2)

def check_dim(a,b):
    if len(a) <> len(b):
        raise DimensionError(a,b)

def euclidean(p,q):
    """Euckidean distance finds the distance between two point in
       a multidimensional space.
    """
    check_dim(p,q)
    
    sum_sq = 0.0

    # add up the squared differences
    for i in range(len(p)):
        sum_sq+=(p[i]-q[i])**2

    # take square root
    return sum_sq**0.5

def pearson(x,y):
    """
    The Pearson correlation coefficient is a measure of how highly correlated
    two variables are. It is a value between 1 and -1, where 1 indicates that
    the variables are perfectly correlates, 0 indicates no correlation and -1
    means they are perfectly inverse correlated.
    """
    check_dim(x,y)

    n=len(x)
    vals=range(n)

    # simple sums
    sumx = sum([float(x[i]) for i in vals])
    sumy = sum([float(y[i]) for i in vals])

    # sum up the squares
    sumx_sq = sum([x[i]**2.0 for i in vals])
    sumy_sq = sum([y[i]**2.0 for i in vals])

    # sum up the products
    psum=sum([x[i]*y[i] for i in vals])

    # calculate Pearson score
    num = psum-(sumx*sumy/n)
    den = ((sumx_sq-pow(sumx,2)/n)*(sumy_sq-pow(sumy,2)/n))**.5
    if den==0: return 0

    r=num/den

    return r

def mean(x):
	return 1.0*(sum(x)/len(x))

def weightedmean(x,w):
    """
    The weighted mean is a type of average that has a weight for every
    observation being averaged.
    """
    check_dim(x,w)
    
    num = sum([x[i]*w[i] for i in range(len(w))])
    den = sum([w[i] for i in range(len(w))])

    return num/den

def tanimoto(a,b):
    """
    The Tanimoto coefficient is a measure of the similarity of two sets.
    """
    c = [v for v in a if v in b]
    return float(len(c))/(len(a)+len(b)-len(c))

def gini_impurity(l):
    """
    Gini impurity is a measure of how impure a set.
    """
    total=len(l)
    counts={}
    for item in l:
        counts.setdefault(item,0)
        counts[item]+=1

    imp=0
    for j in l:
        f1=float(counts[j])/total
        for k in l:
            if j==k: continue
            f2=float(counts[k])/total
            imp+=f1*f2
    return imp


def entropy(l):
    """
    Entropy is another way to see how mixed a set is. It comes from information
    theory, and it measures the amount of disorder in a set. Loosely defined,
    entropy is how surprising a randomly selected item from the set is.
    """
    from math import log
    log2=lambda x:log(x)/log(2)

    total=len(l)
    counts={}
    for item in l:
        counts.setdefault(item,0)
        counts[item]+=1

    ent=0
    for i in counts:
        p=float(counts[i])/total
        ent-=p*log2(p)
    return ent

def variance(vals):
    """
    Variance measures how much a list of numbers varies from the mean (average)
    value.It is frequently used in statistics to measure how large the
    difference are in a set of numbers.
    """
    mean=float(sum(vals))/len(vals)
    s=sum([(v-mean)**2 for v in vals])
    return s/len(vals)

def gaussian(dist,sigma=10.0):
    """
    The Gaussian function is the probability density function of the normal curve.
    """
    exp=math.e**(-dist**2/(2*sigma**2))
    return (1/(sigma*(2*math.pi)**.5))*exp

def dot_product(a,b):
    check_dim(a,b)
    return sum([a[i]*b[i] for i in range(len(a))])

def vector_len(a):
    """Calculate the size of a vector"""
    return sum([a[i] for i in range(len(a))])

def angle(a,b):
    from math import acos
    check_dim(a,b)
    dp=dot_product(a,b)
    la=vector_len(a)
    lb=vector_len(b)
    costheta=dp/(la*lb)
    return acos(costheta)

def least_squares(x,y):
    mean_x = mean(x)
    mean_y = mean(y)
    sxy = []
    dxq = []
    for index in range(0,len(x)):
        dx = x[index]-mean_x
        dy = y[index]-mean_y
        sxy += [dx*dy]
        dxq += [dx*dx]

    b1 = sum(sxy)/sum(dxq)
    b0 = mean_y - b1*mean_x
    return (b0, b1)

