from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='tunic',
    version='0.0.1',
    description='Thunderbird Usenet Newsgroup Import Converter',
    license='GNU',
    long_description=readme,
    author='vi',
    author_email='mail@v-i.dev',
    packages=['tunic'],
    install_requires=['pyinstaller'],
    scripts=['scripts/build']
)