from setuptools import find_packages, setup
from typing import List

hypen = '-e .'

def get_requirements(file_path:str) -> List[str]:

    '''this function will return the list of requirements'''

    requirements = []
    with open('requirements.txt','r') as file:
        requirements= file.readlines()
        requirements = [req.replace('\n',"") for req in requirements]

        if hypen in requirements:
            requirements.remove(hypen)

    return requirements




setup(
    name='ml_project',
    version= '0.0.1',
    author= 'Dip',
    author_email='nidermondol@gmail.com',
    packages= find_packages(),
    install_requires = get_requirements('requirements.txt')
)









