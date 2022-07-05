from setuptools import setup

setup(
    name="kancli",
    version='27.07.84',
    py_modules=['kancli'],
    install_requires=[
        'click',
        'requests',
        'logging',
        'tabulate'
    ],
    entry_points='''
        [console_scripts]
        kancli=kancli:cli
    ''',
)
