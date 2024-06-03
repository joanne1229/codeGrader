import ast

def parse_code(code):
    return ast.parse(code)

class ComplexityAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.complexity = "O(1)"
        self.nested_loops = []
        self.current_nesting = 0
        self.recursive = False
        self.logarithmic = False


    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        # Check for recursive calls
        if any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == node.name for n in ast.walk(node)):
            self.recursive = True

    def visit_For(self, node):
        self.current_nesting += 1
        self.generic_visit(node)
        self.nested_loops.append(self.current_nesting)
        self.current_nesting -= 1

    # def visit_While(self, node):
    #     self.current_nesting += 1
    #     self.generic_visit(node)
    #     self.nested_loops.append(self.current_nesting)
    #     self.current_nesting -= 1
    def visit_While(self, node):
        self.generic_visit(node)
        # Check for halving behavior in while loop conditions
        if isinstance(node.test, ast.Compare):
            left = node.test.left
            if isinstance(left, ast.BinOp) and isinstance(left.op, ast.FloorDiv) and isinstance(left.left, ast.BinOp):
                left_left = left.left
                if isinstance(left_left.op, ast.Add) and isinstance(left_left.right, ast.Num) and left_left.right.n == 1:
                    self.logarithmic = True

    def get_complexity(self):
        if not self.nested_loops:
            return "O(1)"
        
        # Calculate complexity from nested loops
        max_nesting = max(self.nested_loops, default=0)
        if max_nesting == 0:
            return "O(1)"
        
        complexity = "O(n"
        if max_nesting > 1:
            complexity += f"^{max_nesting}"
        complexity += ")"
        
        if self.recursive:
            complexity = f"T(n) = 2T(n/2) + {complexity}"  # Simple recurrence for divide-and-conquer
        
        return complexity

def analyze_complexity(code):
    tree = parse_code(code)
    analyzer = ComplexityAnalyzer()
    analyzer.visit(tree)
    return analyzer.get_complexity()
# def analyze_complexity(code):
#     tree = parse_code(code)
#     analyzer = ComplexityAnalyzer()
#     analyzer.visit(tree)
#     if analyzer.recursive:
#         return f"T(n) = 2T(n/2) + O(log n)"
#     elif analyzer.logarithmic:
#         return "O(log n)"
#     else:
#         return "O(1)"


# Example usage
code = """
def example_function(n):
    for i in range(n):
        for j in range(n):
            print(i, j)
    while n > 1:
        n = n // 2
"""

complexity = analyze_complexity(code)
print(f"Estimated Big O Complexity: {complexity}")
