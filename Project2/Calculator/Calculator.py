a = float(input("Enter Number 1 : "))
b = float(input("Enter Number 2 : "))
o = input("Enter Operator (+, -, *, / , %) : ")

def cal(num1 , num2 , operator):
	if operator == "+":
		print(num1 + num2)
	elif operator == "-":
		print(num1 - num2)
	elif operator == "/":
		print(num1/num2)
	elif operator == "*":
		print(num1 * num2)
	elif operator == "%":
		print(num1 % num2)
	else : 
		print("Enter A Valid Operator")
	


cal(a , b , o)