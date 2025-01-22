import re

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def interpret(self, program):
        _, functions = program
        for func in functions:
            _, return_type, name, params, body, return_stmt = func
            self.functions[name] = (return_type, params, body, return_stmt)
        
        if 'main' in self.functions:
            self.call_function('main', [])
        else:
            raise RuntimeError("No 'main' function defined in the program.")

    def evaluate(self, node):
        if isinstance(node, tuple):
            if node[0] == 'float':
                return node[1]
            elif node[0] == 'int':
                return node[1]
            elif node[0] == 'func_call':
                func_name, args = node[1][0], [self.evaluate(arg) for arg in node[1][1]]
                return self.call_function(func_name, args)
            elif node[0] == 'var':
                if node[1] in self.variables:
                    return self.evaluate(self.variables[node[1]])
                else:
                    raise RuntimeError(f"Variable '{node[1]}' is not defined.")
            elif node[0] in ('+', '-', '*', '/'):
                left = self.evaluate(node[1])
                right = self.evaluate(node[2])
                if node[0] == '+':
                    return left + right
                elif node[0] == '-':
                    return left - right
                elif node[0] == '*':
                    return left * right
                elif node[0] == '/':
                    return left / right
            elif node[0] in ('==', '>', '<'):
                left = self.evaluate(node[1])
                right = self.evaluate(node[2])
                if node[0] == '==':
                    return left == right
                elif node[0] == '>':
                    return left > right
                elif node[0] == '<':
                    return left < right
        return node

    def execute(self, stmt):
        if stmt[0] == 'print':
            value = self.evaluate(stmt[1])
            while(isinstance(value, tuple)):
                value = self.evaluate(value)
            print(value)
        elif stmt[0] == 'assign':
            var_name = stmt[1]
            if var_name not in self.variables:
                raise RuntimeError(f"Variable '{var_name}' is not defined.")
            var_type = self.variables[var_name][0]
            value = self.evaluate(stmt[2])
            self.check_type(var_type, value)
            self.variables[var_name] = (var_type, self.evaluate(value))
        elif stmt[0] == 'declare':
            var_type, var_name = stmt[1], stmt[2]
            self.variables[var_name] = (var_type, 0 if var_type in ('int', 'float') else '\0')
        elif stmt[0] == 'declare_and_assign':
            var_type, var_name, value = stmt[1], stmt[2], self.evaluate(stmt[3])
            self.check_type(var_type, value)
            self.variables[var_name] = (var_type, self.evaluate(value))
        elif stmt[0] == 'if':
            condition = self.evaluate(stmt[1])
            if condition:
                for s in stmt[2]:
                    self.execute(s)
        elif stmt[0] == 'ifelse':
            condition = self.evaluate(stmt[1][1])
            if condition:
                for s in stmt[1][2]:
                    self.execute(s)
            else:
                for s in stmt[2][1]:
                    self.execute(s)
        elif stmt[0] == 'while':
            while self.evaluate(stmt[1]):
                for s in stmt[2]:
                    self.execute(s)
        elif stmt[0] == 'return':
            return self.evaluate(stmt[1])

    def call_function(self, name, args):
        if name not in self.functions:
            raise RuntimeError(f"Function '{name}' is not defined.")
        
        _, params, body, return_stmt = self.functions[name]
        
        if len(params) != len(args):
            raise RuntimeError(f"Function '{name}' expects {len(params)} arguments, but got {len(args)}.")
        
        local_variables = self.variables.copy()
        for (_, param_type, param_name), arg in zip(params, args):
            self.check_type(param_type, arg)
            self.variables[param_name] = arg

        for stmt in body:
            self.execute(stmt)
        
        return_value = self.execute(return_stmt)

        self.variables = local_variables

        return return_value
     
    def check_type(self, var_type, value):
        if var_type == 'int' and not isinstance(value, int):
            raise RuntimeError(f"Expected type 'int', but got {type(value).__name__}.")
        elif var_type == 'float' and not isinstance(value, (int, float)):
            raise RuntimeError(f"Expected type 'float', but got {type(value).__name__}.")
        elif var_type == 'char' and not isinstance(value, str):
            raise RuntimeError(f"Expected type 'char', but got {type(value).__name__}.")
