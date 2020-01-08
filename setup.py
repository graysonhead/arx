import setuptools

setuptools.setup(
    name='arx',
    use_scm_verion=True,
    setup_requires=['setuptools_scm'],
    author='Grayson Head',
    author_email='grayson@graysonhead.net',
    url='https://github.com/graysonhead/arx',
    packages=setuptools.find_packages(),
    license='GPL V3',
    install_requires=[
        'toml>=0.10.0',
        'paramiko>=2.7.1',
        'pylxd>=2.2.10',
        'needystates>=0.3.0'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    project_urls={
        'Source': 'https://github.com/graysonhead/arx',
        'Bug Reports': 'https://github.com/graysonhead/arx/issues',
        # 'Documentation': 'https://runcible.readthedocs.io/en/latest/index.html',
        # 'Gitter': 'https://gitter.im/runcible_project/community'
    },
    python_requires='>=3.5, <4',
    entry_points={}
)