from setuptools import setup, find_packages

setup(
    name='social',
    version='0.3.3',
    description='Django app for easily including a social content api.',
    author='MadeinHaus',
    author_email='cms-admin@madeinhaus.com',
    url='https://github.com/MadeInHaus/django-social',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['twython', 'gevent==0.13.8', 'celery==3.0.12',
                      'django-celery==3.0.11', 'feedparser==5.1.3',
                      'beautifulsoup4==4.1.3', 'requests==1.2.3', 'django-taggit==0.12.2',],
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
