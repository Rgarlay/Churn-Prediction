from setuptools import setup, find_packages





def get_packages()-> list:
    try:
        packages = []
        with open('req.txt','r') as file:
            lines = file.readlines()
        for line in lines:
            line = line.strip()
            if '-e .' not in line:
                packages.append(line)
    except Exception as e:
        print(e)
    return packages

setup(
    name =  'Retail Project',
    Author = 'Ravi Garlay',
    version = '0.0.1',
    email = 'ravigarlay@outlook.com',
    description='MLOps',
    packages = find_packages(),
    install_packages = get_packages()
)