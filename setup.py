from setuptools import setup, find_packages

with open('README.rst') as file:
    long_description = file.read()

setup(name='gitlab_stats',
      version='1.2.1',
      description='CLI to get pipeline stats from gitlab API v4 using gitlab project ID',
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='gitlab pipeline stats build',
      url='https://github.com/Sylhare/gitlab_stats',
      author='sylhare',
      author_email='sylhare@outlook.com',
      license='MIT',
      packages=find_packages(exclude=['docs', 'dist', 'build']),
      include_package_data=True,
      install_requires=['requests'],
      tests_require=['pytest'],
      extras_require={
          'test': ['coverage', 'pytest'],
      },
      entry_points={
          'console_scripts': [
              'gitlab_stats = gitlab_stats.cli:main'
          ]
      })
