class Node:
    def __init__(self, type, left=None, right=None, value=None):
        self.type = type  # "operator" or "operand"
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value})"


def create_rule(rule_string):
    """Parse a rule string into an AST."""
    import ast
    tree = ast.parse(rule_string, mode='eval')
    return _build_ast(tree.body)


def _build_ast(node):
    """Recursively build AST nodes from Python's AST."""
    if isinstance(node, ast.BoolOp):  # AND / OR operator
        op = "AND" if isinstance(node.op, ast.And) else "OR"
        return Node("operator", _build_ast(node.values[0]), _build_ast(node.values[1]), op)
    elif isinstance(node, ast.Compare):  # Comparisons like age > 30
        left = node.left.id
        op = node.ops[0].__class__.__name__
        value = node.comparators[0].n if isinstance(node.comparators[0], ast.Constant) else None
        return Node("operand", value=f"{left} {op} {value}")
    else:
        raise ValueError("Unsupported rule format.")


def evaluate_rule(ast_node, data):
    """Evaluate the AST against the provided user data."""
    if ast_node.type == "operator":
        left_result = evaluate_rule(ast_node.left, data)
        right_result = evaluate_rule(ast_node.right, data)
        if ast_node.value == "AND":
            return left_result and right_result
        elif ast_node.value == "OR":
            return left_result or right_result
    elif ast_node.type == "operand":
        field, operator, value = ast_node.value.split()
        value = int(value)  # Assuming integer comparison
        if operator == "Gt":
            return data.get(field) > value
        elif operator == "Lt":
            return data.get(field) < value
    return False
