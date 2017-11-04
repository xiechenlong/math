from sympy import *
import itertools
import time


num_variable = 3

variables = Matrix(list(symbols('x1:{}'.format(num_variable+1))))
variables_y = Matrix(list(symbols('y1:{}'.format(num_variable+1))))

matrix = []
for i in range(1,num_variable+1):
	matrix.append(list(symbols('a{}:{}'.format(i*10+1,i*10+num_variable+1))))

matrix = Matrix(matrix)

h_linear = matrix * variables
h_linear_y = matrix * variables_y

equation_2 = [variables[i] + h_linear[i]**3 - variables_y[i] - h_linear_y[i]**3 for i in range(0,num_variable)]
# print equation_2

z = symbols('z')
equation_3 = [1 - z*(variables[0] - variables_y[0])]
# print equation_3

for index, element in enumerate(h_linear):
	# print element
	h_linear[index] = element * element

# print 'variables: ',variables
# print 'matrix: ', matrix
# print 'h: ', h_linear

equation = []
equation_coeff = []

def k_order_principal_minor(matrix,k_rows,k):
	kopm = Matrix(k,k,[matrix[i,j] for i in k_rows for j in k_rows])
	return kopm.det()

# print k_order_principal_minor(matrix,[0,1],2)

def list_poly(h_linear,k_rows):
	poly = 1
	for i in k_rows:
		poly *= h_linear[i]
	return poly

# print list_poly(h_linear,[0,1])

def get(k,num_variable):
	balls = 2 * k
	boxes = num_variable
	rng = list(range(balls +1)) * boxes
	permutation = set(i for i in itertools.permutations(rng,boxes) if sum(i) == balls)
	return list(permutation)

# print get(2,2)

def get_n_equation(equation,equation_coeff,matrix,h_linear,num_variable):
	for k in range(0,num_variable-1):
		k_equation = 0
		for subset in itertools.combinations(range(0,num_variable), k+1):
			# print list(subset)
			k_equation += k_order_principal_minor(matrix,list(subset),k+1) * list_poly(h_linear,list(subset))
		equation.append(k_equation)

		k_equation = expand(k_equation)
		for coeff_variable in get(k+1,num_variable):
			variable = 1
			for index, i in enumerate(coeff_variable):
				variable *= variables[index]**i
			# print variable, k_equation.coeff(variable)
			equation_coeff.append(k_equation.coeff(variable))

	equation_coeff.append(matrix.det())

	return equation, equation_coeff

equation, equation_coeff = get_n_equation(equation,equation_coeff,matrix,h_linear,num_variable)
# print equation
# print len(equation_coeff)
# 2/3/4 ----------  4/22/130

all_equation = equation_coeff + equation_2 + equation_3

for index,e in enumerate(all_equation):
	all_equation[index] = poly(e)
print len(all_equation)

t = time.time()
print groebner(all_equation) == [1], time.time() - t

def test_grobner():
	x, y = symbols('x y')
	f = poly(x**2 - y)
	g = poly(x**3 - x)
	print groebner([f,g])
	print groebner([f,g]) == [f,g]
	print groebner([f,g]) == [f,x*y-x,y**2-y]

# test_grobner()

