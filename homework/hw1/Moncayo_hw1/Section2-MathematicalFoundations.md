### Section 2: Mathematical Foundations

- María Eulalia Moncayo 00326226
- Matías Jaramillo 00326063
- John Ochoa Abad 00345743

Show all your work for the following problems based on our class materials.

---

### 1. Modular Arithmetic: Find $x$ for the following:

- $x \equiv 457 \pmod{13}$

For this exercise it is necessary to remember the formula we reviewed in class to get the modular arithmetic of an operation. That formula starts from:

a = bq + x

Where:

- a: Numerator  
- b: Denominator  
- q: Quotient  
- x: Remainder  
- 0 ≤ x < b

### Apply the formula:

457 = 13q + x

Now divide:

457 / 13 = 35 with remainder 2

Because:

13 × 35 = 455

Substitute into the formula:

457 = 13(35) + 2

Therefore:

x ≡ 2

---

- $x \equiv -25 \pmod{7}$

We perform the same for this exercise

### Apply the formula:

-25 = 7q + x

Now divide:

-25 / 7 = -4 with remainder 3

Because:

7 × (-4) = -28

-25 - (-28) = 3

Substitute into the formula:

-25 = 7(-4) + 3

Therefore:

x ≡ 3

---

### 2. The Euclidean Algorithm:

- Calculate $\gcd(1160, 480)$ using the Euclidean Algorithm.

### The Euclidean Algorithm: Formula

The Euclidean Algorithm as shown in class is a method to find the greatest common divisor (gcd) of two integers. It is based on the following principle:

If a and b are integers with a > b > 0, then:

- gcd(a, b) = gcd(b, r)

where r is the remainder when a is divided by b.

The algorithm starts from the division algorithm formula:

a = b * q + r

Where:

- a = the larger number (numerator)  
- b = the smaller number (denominator)  
- q = quotient (integer part of the division)  
- r = remainder, satisfying 0 ≤ r < b  

The gcd of a and b is the same as the gcd of b and r:

gcd(a, b) = gcd(b, r)

We use the Euclidean Algorithm, as shown before

a = bq + r

- Step 1:

1160 = 480(2) + 200

- Step 2:

480 = 200(2) + 80

- Step 3:

200 = 80(2) + 40

- Step 4:

80 = 40(2) + 0

Since the remainder is now 0, the last non-zero remainder is the gcd.

Therefore:

gcd(1160, 480) = 40

---

- Use the Extended Euclidean Algorithm to find $x, y$ such that $1160x + 480y = \gcd(1160, 480)$.

We now find integers x and y such that:

1160x + 480y = gcd(1160, 480)

We already know:

gcd(1160, 480) = 40

Now we work backwards.

From Step 3:

40 = 200 - 80(2)

From Step 2:

80 = 480 - 200(2)

Substitute into the first equation:

40 = 200 - 2(480 - 200(2))

40 = 200 - 2(480) + 4(200)

40 = 5(200) - 2(480)

Now substitute Step 1:

200 = 1160 - 480(2)

40 = 5(1160 - 480(2)) - 2(480)

40 = 5(1160) - 10(480) - 2(480)

40 = 5(1160) - 12(480)

- Answer

gcd(1160, 480) = 40

Solution is:

x = 5  
y = -12  

Because:

1160(5) + 480(-12) = 40

---

### 3. Euler’s Totient Function: 

Euler’s Totient Function, denoted $\phi(n)$, counts the number of positive integers less than or equal to n that are coprime to n (i.e., integers that share no common divisors with n except 1).

- How to calculate $\phi(n)$

- Case 1: n is a prime number

If n is prime:

All numbers less than n are coprime with n

Therefore:

$\phi(p)$ = p - 1

Example: $\phi(17)$ = 17 - 1 = 16

- Case 2: n is a product of distinct primes

If n is the product of primes:

n = p1 * p2 * ... * pk

$\phi(n)$ = n * (1 - 1/p1) * (1 - 1/p2) * ... * (1 - 1/pk)

Factorize n into prime factors first

Apply the formula multiplying the terms

- Case 3: General formula for any n

Factorize n as:

n = p1^a1 * p2^a2 * ... * pk^ak

- Then:

$\phi(n)$ = n * (1 - 1/p1) * (1 - 1/p2) * ... * (1 - 1/pk)

- This works even if the primes repeat

---
 
- Calculate $\phi(21)$ and $\phi(17)$.

- Calculate $\phi(21)$

Step 1: Factorize 21

21 = 3 * 7

Step 2: Apply the formula

$\phi(21)$ = 21 * (1 - 1/3) * (1 - 1/7)

$\phi(21)$ = 21 * (2/3) * (6/7)

$\phi(21)$ = 21 * 12/21

$\phi(21)$ = 12

Result: $\phi(21)$ = 12

- Calculate $\phi(17)$

Step 1: Check if 17 is prime → Yes

Step 2: Apply prime formula

$\phi(17)$ = 17 - 1

$\phi(17)$ = 16

Result: $\phi(17)$ = 16

---

- Calculate $\phi(360)$ using prime factorization.

- Step 1: Factorize 360 into primes

360 = 2^3 * 3^2 * 5

- Step 2: Apply the formula

$\phi(360)$ = 360 * (1 - 1/2) * (1 - 1/3) * (1 - 1/5)

- Step 3: Calculate step by step

360 * (1/2) = 180

180 * (2/3) = 120

120 * (4/5) = 96

Result: $\phi(360)$ = 96

---

### 4. Information Theory: 

A source produces $\{A, B, C, D\}$ with probabilities $P(A)=1/2$, $P(B)=1/4$, $P(C)=1/8$, and $P(D)=1/8$.

- Calculate the Shannon Entropy $H(X)$.

Shannon Entropy measures the average uncertainty of a random variable as it was explained in class.  

It is denoted by H(X) and calculated using the formula:

H(X) = - Σ [ P(x) * log2(P(x)) ]

Where:

- X is the random variable  
- P(x) is the probability of outcome x  
- log2 is the logarithm base 2  
- Σ means sum over all possible outcomes  

Interpretation: 

- Higher entropy → more uncertainty  
- Lower entropy → more predictability

A source produces the symbols {A, B, C, D} with probabilities:

- P(A) = 1/2  
- P(B) = 1/4  
- P(C) = 1/8  
- P(D) = 1/8  

We need to calculate H(X).

- Step 1: Apply the formula

H(X) = - [ P(A)*log2(P(A)) + P(B)*log2(P(B)) + P(C)*log2(P(C)) + P(D)*log2(P(D)) ]

H(X) = - [ (1/2)*log2(1/2) + (1/4)*log2(1/4) + (1/8)*log2(1/8) + (1/8)*log2(1/8) ]

- (1/2) * log2(1/2) = (1/2) * (-1) = -1/2  
- (1/4) * log2(1/4) = (1/4) * (-2) = -1/2  
- (1/8) * log2(1/8) = (1/8) * (-3) = -3/8  
- (1/8) * log2(1/8) = (1/8) * (-3) = -3/8  

H(X) = - [ -1/2 -1/2 -3/8 -3/8 ]

Result -> H(X) = 1.75 bits

---

### 5. Bayes' Theorem: An Intrusion Detection System (IDS) is designed to flag a "Brute Force" attack.

- The probability of an actual attack is $P(A) = 0.001$.
- If there is an attack, the IDS correctly flags it with a probability of $0.99$ (True Positive).
- If there is no attack, the IDS incorrectly flags it with a probability of $0.01$ (False Positive).
- Question: If the IDS flags an event, what is the probability that an actual attack is occurring?

As it was checked in classes Bayes Theorem is a way to calculate conditional probabilities, the probability of an event A given that event B has occurred.  

The formula is:

- P(A | B) = ( P(B | A) * P(A) ) / P(B)

Where:

- P(A | B) = Probability of A given B 
- P(B | A) = Probability of B given A 
- P(A) = Probability of A
- P(B) = Total probability of B (can be calculated as: P(B) = P(B|A)*P(A) + P(B|¬A)*P(¬A))

Given:

- P(A) = 0.001 → Probability of an actual attack  
- P(Flag | A) = 0.99 → Probability IDS flags attack when attack occurs (True Positive)
- P(Flag | ¬A) = 0.01 → Probability IDS flags attack when there is no attack (False Positive)

- P(A | Flag) = ( P(Flag | A) * P(A) ) / P(Flag)

We substitute the known values

- P(A | Flag) = ( 0.99 * 0.001 ) / P(Flag)

We calculate P(Flag)

- P(Flag) = P(Flag | A) * P(A) + P(Flag|¬A)*P(¬A)

- P(¬A) = 1 - P(A) = 1 - 0.001 = 0.999

- P(Flag) = 0.99 * 0.001 + 0.01 * 0.999

- P(Flag) = 0.01098

We finally calculate the conditional probability

- P(A | Flag) = ( 0.99 * 0.001 ) / 0.01098

- Result -> P(A | Flag) = 0.0902 = 9.02% of probability that a real attack is happening if the IDS generates a flag
