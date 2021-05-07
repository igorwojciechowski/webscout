from setuptools import setup

setup(
    name='webscout',
    python_requires='>=3.5.0',
    version='0.1',
    description='Console tool for taking screenshots of given websites.',
    author='Igor Wojciechowski',
    author_email='igorxwojciechowski@gmail.com',
    install_requires=[
        'chromedriver==2.24.1',
        'jinja2==2.11.3',
        'requests==2.25.1',
        'selenium==3.141.0'
    ],
    package_data={
        'webscout.templates': [
            '*.j2'
        ]
    },
    packages=[
        'webscout',
        'templates'
    ],
    package_dir={
        'webscout': './webscout'
    },
    entry_points={
        'console_scripts': [
            'webscout = webscout:main'
        ]
    }
)
