from setuptools import find_packages, setup
from typing import List
# find_packages - find all the packages with in the directories


hypen_e_dot = "-e ."
def get_requirements(file_path:str)->List[str]:
    """
    Keyword arguments: path of requirements.txt
    Return: List of requirements 
    """
   
    with open(file_path,'r') as file:
        print("file",file)
        
        requirements = file.readlines()
        print("readed lines",requirements)
    requirements = [requirement.replace('\n','') for requirement in requirements if requirement !=hypen_e_dot]
    return requirements
        
        
setup(
    name = "mlops_learning",
    version="0.0.1",
    author="akeshkumar",
    author_email="akeshkumar65885@gmail.com",
    packages= find_packages(), # if we want any dir to be found as package we need to create __init__.py inside
                                # - this method search for folders having __init__.py and if is present in that dir, it consider it as package and build it
    requires= get_requirements("requirements.txt")
    
)
