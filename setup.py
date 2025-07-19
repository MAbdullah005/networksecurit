'''
the setup.py file is an esianltial part of packaging and
distributing python project . it is used bu setup tools
(or distutiles in older python version) to define the configration
of your project  such as meta data ,dependenies and more

'''
from setuptools import find_packages,setup
from typing import List
# find_packages: when ever the is a __init__.py file in folder the parent folder
#  become package for project so we can deliver
# setup: setup the meta data
def get_requirement()-> list[str]:
    # this function return a list of requrirment.txt
    requirement_lst:List[str]=[]
    try:
      with open('requirements.txt','r') as f:
         # read lien from dfile
         lines=f.readlines()
         # process each line
         for line in lines:
            requirement=line.strip()
            ## ignore the empty line and -e .
            if requirement and requirement!='-e .':
               requirement_lst.append(requirement)
    except FileNotFoundError as e:
       print("requirmeet.txt is not found")

    return requirement_lst


setup(
   name="NetworkSecuritys",
   version=1.0,
   author="Abdullah Ali",
   author_email="abdullahaliofc@gmail.com",
   packages=find_packages(),
   install_requires=get_requirement()
)               