import random
from bn import DiscreteBN

def prior_sample(bn: DiscreteBN, rng: random.Random):
    """
        Generate one full sample from the Bayesian network using prior sampling.

        Go through all variables in topological order.
        For each variable X, sample a value according to P(X | parents(X))
        using the already sampled values of its parents.

        Returns:
            dict[str, str]: A full assignment mapping each variable name to its sampled state.
                            Example: {"asia": "no", "tub": "no", "smoke": "yes", ...}
        """
    sample = {}
    for X in bn.topo_order:
        states = bn.states[X]
        probs = [bn.local_prob(X, s, sample) for s in states]
        r = rng.random()
        cum = 0.0
        for s, p in zip(states, probs):
            cum += p
            if r <= cum:
                sample[X] = s
                break
    return sample


def rejection_sampling(bn: DiscreteBN, query, evidence, N, rng):
    """
    Estimate the probability P(query_var = query_val | evidence) using rejection sampling.

    Algorithm outline:
      generate N samples and only keep those that match the evidence.
      Return the fraction of kept samples where the query is true.

    Parameters:
        bn (DiscreteBN): The Bayesian network object.
        query (tuple):  (variable_name, value) to estimate, e.g. ("either", "yes").
        evidence (dict): Observed variables, e.g. {"xray": "yes"}.
        N (int): Number of samples to generate.
        rng (random.Random): Random number generator instance.

    Returns:
        float: An estimate of P(query | evidence)
               If no samples match the evidence, you may return 0.
    """
    """TODO: implement this function"""

    raise NotImplementedError


def likelihood_weighting(bn: DiscreteBN, query, evidence, N, rng):
    """
    Estimate the probability P(query_var = query_val | evidence) using likelihood weighting.

    Algorithm outline:
      Generate N weighted samples where evidence variables are fixed
      to their observed values. Combine these weighted samples to
      estimate the conditional probability, making sure to normalize
      at the end.


    Parameters:
        bn (DiscreteBN): The Bayesian network object.
        query (tuple):  (variable_name, value) to estimate, e.g. ("either", "yes").
        evidence (dict): Observed variables, e.g. {"xray": "yes"}.
        N (int): Number of weighted samples to generate.
        rng (random.Random): Random number generator instance.

    Returns:
        float: An estimate of P(query | evidence)
               (Normalized weighted probability for the query variable being its target value.)
    """
    query_var, query_val = query

    # We'll keep weighted counts per value of the query variable
    counts = {v: 0.0 for v in bn.states[query_var]}

    # Found an algo online that was straightforward: https://www.geeksforgeeks.org/artificial-intelligence/likelihood-weighting-in-artificial-intelligence/
    # 1) Initialize / Repeat: generate N weighted samples
    for _ in range(N):
        sample = {}
        weight = 1.0

        # 2) Sample variables in topological order
        for var in bn.topo_order:
            parent_asg = {p: sample[p] for p in bn.parents[var]}

            if var in evidence:
                # observed: fix value and multiply weight by likelihood
                val = evidence[var]
                sample[var] = val
                prob = bn.local_prob(var, val, parent_asg)
                weight *= prob
            else:
                # not observed: sample from P(var | parents)
                values = bn.states[var]
                probs = [bn.local_prob(var, v, parent_asg) for v in values]

                r = rng.random()
                cum = 0.0
                chosen = values[-1]
                for v, p in zip(values, probs):
                    cum += p
                    if r <= cum:
                        chosen = v
                        break
                sample[var] = chosen

        # 3) Store the sample (accumulate weight for the query value)
        counts[sample[query_var]] += weight

    # 4) total weight
    total_weight = sum(counts.values())

    # 5) normalize to get P(query_var = query_val | evidence)
    if total_weight == 0.0:
        return 0.0
    return counts[query_val] / total_weight
