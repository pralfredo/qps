"""
Pramithas Upreti
12/01/2022
CS152B
Final Project
collection.py

This is an additional functions module primarily for creating the graphs.
But, it also has functions utilized in the Tkinter graphics in main.py.
It also has the constant class that incorporates all the constant values required for our simulation.
This constant class is used in mechanics.py for quantum calculations.
The functions class is also used in graphing for manipulating the functions entered by the user.

This module is only a collection of functions and classes, so there is no point in running it.
"""

#import statements
import numpy as np
from sympy import lambdify, abc, latex
from sympy.parsing.sympy_parser import parse_expr

class VariableNotFoundError(Exception):
    """This class is the variable not found error."""

    def __str__(self) -> None:
        """Print this exception."""
        return "Variable not found"


def rectangle(x):
    """Rectangle function that is essentially the simulation space"""
    try:
        #uses numpy array
        return np.array([1.0 if (x_i < 0.5 and x_i > -0.5) else 0 for x_i in x])
    except:
        return 1.0 if (x < 0.5 and x > -0.5) else 0.


# Dictionary of modules and user defined functions. Used for lambdify from sympy to parse input.
module_list = ["numpy", {"rect":rectangle}]


def multiplies_var(main_var, arb_var, expression):
    """This function checks to see if an arbitrary variable multiplies a sub expression that contains the main variable.
    If it does, return True else False."""
    arg_list = []
    for arg1 in expression.args:
        if arg1.has(main_var): 
            arg_list.append(arg1) 
            for arg2 in expression.args:
                if ((arg2 is arb_var or (arg2.is_Pow and arg2.has(arb_var))) and expression.has(arg1*arg2)):
                    return True
    return any([multiplies_var(main_var, arb_var, arg) for arg in arg_list if (arg is not main_var)])


def noise(x):
    """This is the noise function that will be used by other modules to parse values"""
    if isinstance(x, np.ndarray):
        #uses numpy array
        return np.array([2.0*np.random.rand() - 1.0 for _ in range(len(x))])
    else:
        return 2.0*np.random.rand() - 1.0


def scales(x, scales_val):
    """This method scales x back into a boundary if it exceeds it."""
    absmaxposval = np.abs(np.amax(x))
    absmaxnegval = np.abs(np.amin(x))
    if (absmaxposval > scales_val or absmaxnegval > scales_val):
        x = scales_val*x/absmaxposval if absmaxposval > absmaxnegval else scales_val*x/absmaxnegval
    return x


def rescales_array(x_prime, x, y):
    """This method, when given an array x that maps to an array y, and array x that is transformed to x_prime, applies this same transform to y."""
    y_prime = np.zeros([len(x)])
    contains_value = np.zeros([len(x)], np.int32)
    for i in range(len(x)):
        index = 0
        min_val = abs(x[i] - x_prime[0])
        for j in range(1, len(x_prime)):
            if abs(x[i] - x_prime[j]) < min_val:
                index = j
                min_val = abs(x[i] - x_prime[j])
        if min_val < (x[1] - x[0]):
            if contains_value[index] == 0:
                y_prime[index] = y[i]
                contains_value[index] = 1
            else:
                contains_value[index] += 1
                y_prime[index] = (y[i]/contains_value[index]+ y_prime[index]*(contains_value[index] - 1.0)/contains_value[index])
    i = 0
    while i < len(y_prime):
        if (i + 1 < len(y_prime) and contains_value[i+1] == 0):
            j = i + 1
            while (contains_value[j] == 0 and j < len(y_prime) - 1):
                j += 1
            for k in range(i+1, j):
                y_prime[k] = y_prime[i] + ((k - i)/(j - i))*(y_prime[j] - y_prime[i])
            i = j - 1
        i += 1
    return y_prime


def change_array(x_array, y_array, x, y, gradual=True):
    """Given a location x that maps to a value y, and an array x_array which maps to array y_array, find the closest element in x_array to x. 
    Then, change its corresponding element in y_array with y."""
    if (x < x_array[0]) or (x > x_array[-1]):
        return y_array
    closest_index = np.argmin(np.abs(x_array - x))
    y_array[closest_index] = y
    n = 1
    if len(x_array) > 100:
        n = 4 if gradual else 3
    if (closest_index - n >= -1 and 
        closest_index + n <= len(x_array)):
        for i in range(n):
            if i < n - 1:
                y_array[closest_index+i] = y
                y_array[closest_index-i] = y
            elif i == n - 1:
                if gradual:
                    y_array[closest_index+i] = (y + y_array[closest_index+i])/2.0
                    y_array[closest_index-i] = (y + y_array[closest_index-i])/2.0
                else:
                    y_array[closest_index+i] = y
                    y_array[closest_index-i] = y
    return y_array


class Function:
    """This function class is of the form y = f(x; a, b, c...) that helps us manipulate and parse functions"""
    module_list = ["numpy", {"rect": rectangle, "noise": noise}]

    def __init__(self, function_name, param):
        """The is the initializer. The parameter must be a string representation of a function, and it needs to be at least a function of x."""
        if isinstance(param, str):
            #returns one expression
            param = parse_expr(param)
        if function_name == "x":
            function_name = "1.0*x"
        #returns one expression
        self._symbolic_func = parse_expr(function_name)
        symbol_set = self._symbolic_func.free_symbols
        if abc.k in symbol_set:
            #returns one expression
            k_param = parse_expr("k_param")
            self._symbolic_func = self._symbolic_func.subs(abc.k, k_param)
            symbol_set = self._symbolic_func.free_symbols
        symbol_list = list(symbol_set)
        if param not in symbol_list:
            raise VariableNotFoundError
        #changes the formatting of symbols
        self.latex_repr = latex(self._symbolic_func)
        symbol_list.remove(param)
        self.parameters = symbol_list
        var_list = [param]
        var_list.extend(symbol_list)
        self.symbols = var_list
        #tranforms sympy(lambda) expressions into python expressions
        self._lambda_func = lambdify(self.symbols, self._symbolic_func, modules=self.module_list)


    def __call__(self, x, *args):
        """This method calls this class as if it were a function."""
        if args == ():
            kwargs = self.get_default_values()
            args = (kwargs[s] for s in kwargs)
        return self._lambda_func(x, *args)


    def __str__(self):
        """This method is the string representation of the function"""
        return str(self._symbolic_func)


    def multiply_latex_string(self, var):
        """The string is multiplied as per the symbols in this method"""
        #returns one expression
        var = parse_expr(var)
        expression = var*self._symbolic_func
        #changes the formatting of symbols
        return latex(expression)


    def get_default_values(self):
        """This method gets a dict of the suggested default values for each parameter used in this function."""
        return {s:float(multiplies_var(self.symbols[0], s, self._symbolic_func)) for s in self.parameters}


    def get_enumerated_default_values(self):
        """This method gets an enumerated dict of the suggested default values for each parameter used in this function."""
        return {i: [s, float(multiplies_var(self.symbols[0], s, self._symbolic_func))] for i, s in enumerate(self.parameters)}


    def get_tupled_default_values(self):
        """This method gets the suggested default values as a tuple."""
        enum_defaults = self.get_enumerated_default_values()
        return tuple([enum_defaults[i][1] for i in range(len(self.parameters))])


    def add_function(function_name, new_function) -> None:
        """This method adds a function to the module"""
        Function.module_list[1][function_name] = new_function


class constant:
    """This class is essentially the parent class for almost all other classes.
    It includes the fundamental constant, including mass, hbar, e, dx, dt etc
    It also includes some other random constants needed for graphing"""

    def __init__(self):
        """This method initializes the constants"""
        # Mass
        self.m = 1.      
         # Reduced Planck constant        
        self.hbar = 1.  
        # Charge        
        self.e = 1.   
        # Initial position           
        self.x0 = -0.5    
        # The Length of the box       
        self.L = 1.  
        # Number of spatial steps           
        self.N = 512       
        # Space stepsize      
        self.dx = self.L/self.N  
        # Time stepsize
        self.dt = 0.00001        
        # scales 
        self._scales = (128/self.N)*5e5


    def _get_constant(self):
        """Return the constant"""
        return self.m, self.hbar, self.e, self.L, self.N, self.dx, self.dt