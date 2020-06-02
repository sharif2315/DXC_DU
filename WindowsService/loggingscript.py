import logging
logpath = r'C:\Users\sahmed243\Documents\WebDevelopment\Python\Scripts\DU_Github\DXC_DU\WindowsService\test.log'
logging.basicConfig(filename=logpath, level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s')

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y

num_1 = 20
num_2 = 10

add_result = add(num_1, num_2)
logging.info('Add: {} + {} = {}'.format(num_1, num_2, add_result))

sub_result = add(num_1, num_2)
logging.info('Sub: {} + {} = {}'.format(num_1, num_2, sub_result))

mul_result = add(num_1, num_2)
logging.info('Mul: {} + {} = {}'.format(num_1, num_2, mul_result))

div_result = add(num_1, num_2)
logging.info('Div: {} + {} = {}'.format(num_1, num_2, div_result))
