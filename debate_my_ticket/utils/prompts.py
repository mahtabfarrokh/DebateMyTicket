PRO_PAYMENT_PROMPT = """You are a legal assistant arguing in favor of paying the ticket. 
Consider the following information:
- Ticket details: {ticket_info}
- Local laws: {local_laws}
- Social context: {social_context}
- Previous debate: {previous_debate}

Your task is to argue why the ticket should be paid. Keep your response under 100 words.
If you believe the ticket should be paid, start your response with "CONCEDE: " followed by your reasoning.
Otherwise, provide your argument."""

ANTI_PAYMENT_PROMPT = """You are a legal assistant arguing against paying the ticket.
Consider the following information:
- Ticket details: {ticket_info}
- Local laws: {local_laws}
- Social context: {social_context}
- Previous debate: {previous_debate}

Your task is to argue why the ticket should be challenged. Keep your response under 100 words.
If you believe the ticket should be challenged, start your response with "CONCEDE: " followed by your reasoning.
Otherwise, provide your argument."""

TICKET_VALIDATION_PROMPT = """Analyze the following ticket information for potential legal issues:
{ticket_info}

Check for:
1. Missing required signatures
2. Date inconsistencies
3. Incorrect formatting
4. Missing required fields
5. Other potential legal flaws

Provide a list of any issues found."""

INFO_EXTRACTION_PROMPT = """Extract the following information from the ticket text:
{ticket_text}

Required fields:
1. Ticket number
2. City
3. Address
4. Violation description/code
5. Date and time
6. Officer information
7. Fine amount

Format the output as a JSON object.""" 