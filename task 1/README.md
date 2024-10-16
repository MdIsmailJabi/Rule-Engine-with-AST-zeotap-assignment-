
# Rule Engine with AST

## Overview
This is a simple 3-tier rule engine application that uses an Abstract Syntax Tree (AST) to represent and evaluate user eligibility rules.

## Features
- Create rules dynamically and store them in a database.
- Evaluate JSON data against stored rules.
- Simple API built with FastAPI.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/rule-engine-ast.git
   cd rule-engine-ast

Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
uvicorn main:app --reload
Test the API:

POST /create_rule/: Create a new rule.
POST /evaluate_rule/: Evaluate data against the rule.
Example Rule
java
Copy code
((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)
