# Artificial Intelligence - Report 2 

**Name:** Siebe Mees

**Student number:** s0222485


## Bayesian Networks (BN)

## Q2: Exact Calculation

**Task:**  
Compute the exact probability of:  
 P(either=yes | xray=yes)

using the conditional probability tables from the appendix in the assignment.

### 2.1 In general:
$P(either = value \mid xray = yes) ∝  Σ_{smoke} Σ_{asia} Σ_{lung} Σ_{tub}$
   $P(either = value, xray = yes, smoke, asia, lung, tub)$

Using the factorization of the Asia network:
$P(either, xray, smoke, asia, lung, tub)= P(asia) \cdot P(tub \mid asia) \cdot P(smoke) \cdot P(lung \mid smoke)\cdot P(either \mid lung, tub) \cdot P(xray \mid either)$
### 2.1 Compute required prior probabilities
#### 2.1.1 P(lung = yes) and P(lung = no)
$P(lung = yes) = P(lung = yes \mid smoke = yes) \cdot P(smoke = yes) + P(lung = yes \mid smoke = no) \cdot P(smoke = no)$
$= 0.10 \cdot 0.5 + 0.01 \cdot 0.5 = 0.055$

$P(lung = no) = 1 − 0.055 = 0.945$

#### 2.1.2 P(tub = yes) and P(tub = no)
$P(tub = yes) = P(tub = yes \mid asia = yes) \cdot P(asia = yes+ P(tub = yes \mid asia = no) \cdot P(asia = no)$
$= 0.05 \cdot 0.01 + 0.01 \cdot 0.99 = 0.0104$

$P(tub = no) = 1 − 0.0104 = 0.9896$

#### 2.1.3 P(either = yes)
“either = yes” is true if lung = yes OR tub = yes:

$ P(either = yes) = 1 − P(lung = no, tub = no)$
$= 1 − (0.945 \cdot 0.9896) = 1 − 0.935172 = 0.064828$

$P(either = no) = 0.935172$

### 2.2 Include the xray evidence
From the CPT:
$P(xray = yes \mid either = yes) = 0.98$
$P(xray = yes \mid either = no) = 0.05$

Compute unnormalized values:
$P(either = yes, xray = yes)$
$= 0.064828 \cdot 0.98 = 0.06353144$

$ P(either = no, xray = yes)$
$= 0.935172 \cdot 0.05 = 0.04675860$

### 2.3 Normalize the distribution
$P(either = yes \mid xray = yes) = \dfrac{P(either = yes, xray = yes)} {P(either = yes, xray = yes) + P(either = no, xray = yes)}$

$ = \dfrac{0.06353144}{0.06353144 + 0.04675860} = \dfrac{0.06353144}{0.11029004} ≈ 0.5760$

**Exact Value:**  
P(either=yes | xray=yes) = 0,5760

**Comparison:**  
From the likelihood weighting experiment (10 runs × 5000 samples): 
```
Estimated P(either=yes | xray=yes) = 0.583341
```
Difference: 0.5833 - 0.5760 = 0.0073 (about 0.7%)
which is within normal Monte Carlo variance. 

The sampling estimate closely matches the exact probability derived from the CPTs.

---

## Q3: Exact with Extra Evidence

**Task:**  
Compute the exact probability  
P(either=yes | xray=yes, tub=yes).

**Derivation:**  

In the Asia network, the node **either** is defined as:

- either = yes if lung = yes or tub = yes,
- either = no only if lung = no and tub = no.

This is encoded in the conditional probability table:

- For any values of `lung`:
    $P(\text{either} = \text{no} \mid \text{tub} = \text{yes}, \text{lung}) = 0,$
    $P(\text{either} = \text{yes} \mid \text{tub} = \text{yes}, \text{lung}) = 1.$

So as soon as we know tub = yes, we **already know with certainty** that either = yes, regardless of the `xray` outcome.

Formally:
$P(\text{either} = \text{no}, \text{tub} = \text{yes}, \dots) = 0$

for all combinations of the other variables. Hence:

$P(\text{either} = \text{no} \mid \text{xray} = \text{yes}, \text{tub} = \text{yes}) = 0$

and therefore

$P(\text{either} = \text{yes} \mid \text{xray} = \text{yes}, \text{tub} = \text{yes}) = 1.$

The extra evidence xray = yes does not change this: the moment we observe tub = yes, `either` must be `yes` in this model.

**Exact Value:**  
P(either=yes | xray=yes, tub=yes) = 1

Verified using a sampling method (likelihood weighting), even 1 sample was enought and gave us the same answer as lets say 5000 samples.


---

## Q4: D-Separation

**Task:**  
Determine whether each conditional independence statement holds in the Asia network.  
If it does not hold, list at least one active path.

| Statement                        | Independent? | Active Path (if any)        |
|----------------------------------|--------------|-----------------------------|
| (a) asia ⟂ xray                  | False        | asia → tub → either → xray  |
| (b) tub ⟂ smoke \| either        | False        | tub → either ← lung ← smoke |
| (c) tub ⟂ bronc                  | True         | -                           |
| (d) tub ⟂ bronc \| dysp          | False        | tub → either → dysp ← bronc |
| (e) tub ⟂ bronc \| smoke, either | True         | -                           |

---

## References

- [BNLearn Asia network](https://www.bnlearn.com/bnrepository/discrete-small.html#asia)  
