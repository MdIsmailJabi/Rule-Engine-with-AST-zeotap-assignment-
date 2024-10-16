from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value

rules_db = []

def create_rule(rule_string: str) -> Node:
    if "AND" in rule_string:
        left = Node("operand", value="age > 30")
        right = Node("operand", value="salary > 50000")
        return Node("operator", left=left, right=right)  # AND operator
    elif "OR" in rule_string:
        left = Node("operand", value="age < 25")
        right = Node("operand", value="department = 'Marketing'")
        return Node("operator", left=left, right=right)  # OR operator
    else:
        raise ValueError("Invalid rule string.")

def evaluate_rule(ast_root: Node, data: dict) -> bool:
    if ast_root.type == "operand":
        if ">" in ast_root.value:
            field, value = ast_root.value.split(" > ")
            return data[field] > int(value)
        elif "=" in ast_root.value:
            field, value = ast_root.value.split(" = ")
            return data[field] == value.strip("'")
    elif ast_root.type == "operator":
        left_result = evaluate_rule(ast_root.left, data)
        right_result = evaluate_rule(ast_root.right, data)
        if ast_root.value == "AND":
            return left_result and right_result
        elif ast_root.value == "OR":
            return left_result or right_result
    return False

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Rule Engine API!"}

class RuleRequest(BaseModel):
    rule_string: str

class EvaluationRequest(BaseModel):
    data: dict

@app.post("/create_rule/")
def create_rule_endpoint(request: RuleRequest):
    try:
        rule = create_rule(request.rule_string)
        rules_db.append(request.rule_string)
        return {"message": "Rule created successfully", "ast": str(rule)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating rule: {str(e)}")

@app.post("/evaluate_rule/")
def evaluate_rule_endpoint(request: EvaluationRequest):
    if not rules_db:
        raise HTTPException(status_code=404, detail="No rules found.")
    
    ast_root = create_rule(rules_db[0])  # Use the first rule for evaluation
    result = evaluate_rule(ast_root, request.data)
    return {"result": result}
