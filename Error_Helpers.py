from scipy.stats import beta
from scipy.stats import binom
from scipy.stats import norm
from scipy.stats import t

def get_sigma(successes, n_trials):
    """
    Get normally distributed std errors
    """
    p = float(successes)/n_trials
    return math.sqrt(n_trials * p * (1 - p))/n_trials

def get_beta_confidence_interval(successes, trials, alpha=0.95):
    """
    Get confidence interval based on a beta distribution
    """
    dist = beta(successes+1, trials - successes + 1)
    return abs(dist.interval(alpha=alpha) - dist.mean())

def get_normally_distributed_binomial_confidence(successes, trials, alpha=0.95):
    """
    Use a normal distribution to approximate a binomial (k successes out of n trials)
    model. mean = succeses/trials, variance = n * p (1 - p). Find the confidence
    interval.
    """
    p = successes/float(trials)
    var = trials * p * (1 - p)
    dist = norm(p, math.sqrt(var))
    return abs(dist.interval(alpha=alpha) - dist.mean())

def get_2sample_2tail_ttest_pvalue(s1, n1, s2, n2):
    """
    Find p-value of 2-sample 2-tail t-test
    where we reject the null hypothesis of mean1 == mean2

    s1: successes of population 1
    n1: num trials of population 1
    s2: successes of population 2
    n2: num trials of population 2
    """
    p1 = s1/float(n1)
    p2 = s2/float(n2)
    var1 = p1*(1-p1)*n1
    var2 = p2*(1-p2)*n2
    SE = math.sqrt(var1/(n1*n1) + var2/(n2*n2))
    tstat = abs(p1 - p2)/float(SE)
    return (1 - t((n1-1)+(n2-1)).cdf(tstat))*2