from setuptools import setup, find_packages

setup(
    name='ai_website_builder',
    version='1.0.0',
    description='AI-Powered Website Builder with Multilingual Code Generation using Flask and MongoDB',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(include=['utils']),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-PyMongo',
        'Flask-Bcrypt',
        'Flask-Login',
        'python-dotenv',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
