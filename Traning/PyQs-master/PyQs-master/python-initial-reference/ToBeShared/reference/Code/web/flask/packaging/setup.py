from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    #Please keep in mind that you have to list subpackages explicitly. 
    #If you want setuptools to lookup the packages for you automatically
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)