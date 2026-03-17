# CMP 5006: Information Security - Homework 1

## Instructions

- Work in groups
- For submission, you will create a new branch of the class GitHub repository
- Each student must submit their homework as a pull request (PR) including all the artifacts
- In D2L you will include a link to your PR

## Topic: Foundations, Classical Ciphers, and Mathematical Underpinnings

### Section 1: Research - Historical & Advanced Classical Ciphers
Since we did not cover these in detail during lecture, research the following four topics to understand how they moved beyond simple substitution:

#### The Vigenère Cipher:
- Mechanism: Explain how the Vigenère Square (Tabula Recta) is used to encrypt a message using a keyword.
- Analysis: How does this polyalphabetic approach defend against basic frequency analysis?
- Breaking the Cipher: Briefly describe the Kasiski examination and how it determines keyword length.
#### The Hill Cipher:
- Mathematical Basis: This cipher is based on linear algebra. Explain how a plaintext block is converted into a vector and multiplied by a key matrix.
- Requirements: What specific mathematical requirements must the key matrix meet to ensure a message can be decrypted?
#### The Playfair Cipher:
- Mechanism: Explain the process of creating the $5 \times 5$ grid and the specific rules for encrypting a digraph (pair of letters).
- Historical Context: Research its use by British forces in WWI and WWII. Why was it considered "field-ready" compared to more complex systems?
#### The Enigma Machine:
- Rotor Logic: Explain the concept of the rotors and how they caused the substitution alphabet to change with every single keystroke.
- The Reflector: What was the purpose of the reflector in the Enigma's circuitry, and why did it mean a letter could never be encrypted as itself?
- The Plugboard: How did the plugboard (Steckerbrett) exponentially increase the number of possible configurations?

### Section 2: Mathematical Foundations
Show all your work for the following problems based on our class materials.

1. Modular Arithmetic: Find $x$ for the following:
    - $x \equiv 457 \pmod{13}$
    - $x \equiv -25 \pmod{7}$
2. The Euclidean Algorithm:
    - Calculate $\gcd(1160, 480)$ using the Euclidean Algorithm.
    - Use the Extended Euclidean Algorithm to find $x, y$ such that $1160x + 480y = \gcd(1160, 480)$.
3. Euler’s Totient Function: 
    - Calculate $\phi(21)$ and $\phi(17)$.
    - Calculate $\phi(360)$ using prime factorization.
4. Information Theory: A source produces $\{A, B, C, D\}$ with probabilities $P(A)=1/2$, $P(B)=1/4$, $P(C)=1/8$, and $P(D)=1/8$.
    - Calculate the Shannon Entropy $H(X)$.
5. Bayes' Theorem: An Intrusion Detection System (IDS) is designed to flag a "Brute Force" attack.
    - The probability of an actual attack is $P(A) = 0.001$.
    - If there is an attack, the IDS correctly flags it with a probability of $0.99$ (True Positive).
    - If there is no attack, the IDS incorrectly flags it with a probability of $0.01$ (False Positive).
    - Question: If the IDS flags an event, what is the probability that an actual attack is occurring? 

### Section 4: PicoCTF
Complete the assignment in PicoCTF platform. 
- Submit your Python scripts and the flags.
- For eaach problem you will attempt two different methods to solve. 