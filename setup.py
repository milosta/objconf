from setuptools import setup, find_packages

test_dependencies = [
    'pytest',
    'flake8',
]
extras = {
    'tests': test_dependencies,
}

setup(
    name='objconf',
    version='0.3.0',
    description='Object configuration for Python projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/milosta/objconf',

    author='Miloslav Stanek',
    author_email='milostanek@gmail.com',

    packages=find_packages(exclude=['docs', 'tests']),
    python_requires='>=3.6',
    install_requires=[
        'pyaml',
    ],
    tests_require=test_dependencies,
    extras_require=extras,
)
