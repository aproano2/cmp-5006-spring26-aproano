# **Homework 2: Securing the "AutoDrive" Firmware Pipeline**

**Scenario:** You are a Security Engineer at *AutoDrive*, a company that manages thousands of self-driving cars. You must ensure that when the company sends a software update (firmware) to a car, it is genuine, hasn't been tampered with, and cannot be intercepted by competitors.

### **Part 1: RSA Key Generation (The Mechanics)**
Before a car leaves the factory, it generates its own RSA key pair to communicate securely with AutoDrive HQ.

1.  **Manual Calculation:** Assume a simplified RSA setup where the car chooses two small primes: $p = 11$ and $q = 13$.
    * Generate the public and private keys
    * Verify that they can be used for encryption and decryption
2.  **Implementation Logic:** Why is it computationally impossible for a hacker to find $d$ if they only know $n$ and $e$ in a real-world 2048-bit system?

### **Part 2: Cryptographic Hashes (Integrity Check)**
The firmware file is 2GB. We don't want to sign the entire file because it is too slow.

1.  **The Avalanche Effect:** If you change exactly **one bit** in the 2GB firmware file and run it through SHA-256 again, how much of the resulting hash should change? Why is this property important for detecting a "Man-in-the-Middle" attack?
2.  **Collision Resistance:** Explain what a "Collision" is in hashing. If a hacker finds a way to make a malicious "Virus.bin" have the same SHA-256 hash as the "Update.bin," why does this break the entire security of the car?

### **Part 3: Digital Certificates (The Chain of Trust)**
AutoDrive HQ doesn't just send its public key to the car via a text file; it uses a **Digital Certificate**.

1.  **Research Task:** Research the **Certificate Signing Request (CSR)** process. List the four main pieces of information that AutoDrive HQ must send to a Certificate Authority (CA) to get a signed X.509 certificate.
2.  **Validation:** When the car receives the HQ's certificate, it needs to verify it. What specific "Root Certificate" must be pre-installed on the car's computer at the factory for this to work?

### **Part 4: Digital Signatures (Authentication)**
To prove the update is official, AutoDrive HQ "signs" the update.

1.  **The Workflow:** Describe the process of creating the signature.
    * What is hashed?
    * Which key (HQ Public or HQ Private) is used to encrypt the hash?
2.  **Non-Repudiation:** If a faulty update causes a car to crash, AutoDrive might try to claim they never sent that specific update. How does the use of a **Digital Signature** provide legal "Non-repudiation" in this case?

---

### **Part 5: System Design Challenge**
**The Task:** Design a "Secure Update Protocol" for the car. Draw a flow diagram or provide a numbered list showing the interaction between **AutoDrive HQ** and the **Vehicle**.

Your design must use a **Hybrid System** (Asymmetric for keys, Symmetric for the 2GB file) and satisfy these five requirements:

| Requirement | How your design achieves it |
| :--- | :--- |
| **1. Secure Key Exchange** | How does the car get the AES "Session Key" from HQ? |
| **2. Confidentiality** | How do you ensure a competitor cannot "sniff" the firmware code? |
| **3. Integrity** | How does the car know the file wasn't corrupted during the download? |
| **4. Authentication** | How does the car know the update is from HQ and not a "Spoofed" server? |
| **5. Non-Repudiation** | How do we prove HQ is the one who authorized this specific version? |

