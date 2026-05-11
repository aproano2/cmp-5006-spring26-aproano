# Homework: Web Defense & Privacy Compliance



## 1. OWASP & CWE Mapping: 

Select three categories from the current OWASP Top 10. For each category:
1. Find one specific CWE (Common Weakness Enumeration) that falls under it.
2. Find one recent CVE (Common Vulnerabilities and Exposures) from 2025 or 2026 that exemplifies this weakness in a real-world application.

**Deliverable:** A table mapping Category to CWE to CVE with a 2-sentence summary of the CVE's impact.

## 2. The Ecuadorian Context: 
Research the Ley Orgánica de Protección de Datos Personales (LOPDP) of Ecuador. 
- Identify the eight data subject rights (Derechos del Titular) mentioned in the law.
- Briefly explain how the Superintendencia de Protección de Datos (the regulatory body) enforces these rights compared to the EU’s GDPR.

## 3. Hands-on Exploitation & Defense:

Log in to picoCTF and complete two "Web Exploitation" challenge of your choice (Recommended: Cookies, Inspect HTML, or SQLi-Lite).

**Deliverable:** A screenshot of the "Flag" and a brief "Write-up" explaining the logic you used to solve it.

## 4. WAF Deployment (DVWA):

- Use a local environment (Docker/VM) to run the Damn Vulnerable Web Application (DVWA).
- Attack: Set DVWA security to "Low" and successfully perform a Command Injection (e.g., getting the server to return whoami).
- Defense: Deploy a Web Application Firewall (WAF) such as ModSecurity (with Nginx/Apache) or an AWS WAF instance.
- Validation: Configure a rule to block semicolons ; or pipes | in HTTP arguments. Prove the attack is now blocked (403 Forbidden).

**Deliverable:** Screenshots of the successful attack (before) and the blocked request (after).

## 5. Design - The Privacy Engineering Task

You are designing a new Ecuadorian Fintech app called "QuitoCash" that allows users to send money via phone numbers. The app also uses AI to "predict" spending habits.

**Draft a Privacy Notice:** Create a 1-page Privacy Notice for QuitoCash. It must explicitly comply with both GDPR (for potential European users) and the Ecuadorian LOPDP. Ensure you include:
- The specific legal basis for processing (e.g., Consent, Legitimate Interest).
- How users can exercise their right to Portability and Opposition.
- A specific clause regarding the "Automated Decision Making" (the AI spending habit feature).

**Data Minimization:** List three specific data points the app might want to collect but should not collect under the principle of Data Minimization to remain compliant.