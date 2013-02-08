from setuptools import setup, find_packages

setup(
    name='social',
    version='0.0.2',
    description='Django app for easily including a social content api.',
    author='MadeinHaus',
    author_email='cms-admin@madeinhaus.com',
    url='https://github.com/MadeInHaus/django-social',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['twython','gevent==0.13.8'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)