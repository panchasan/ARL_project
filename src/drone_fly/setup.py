from setuptools import setup

package_name = 'drone_fly'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='chaneu',
    maintainer_email='chaneu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'publisher = drone_fly.publisher:main',
                'subscriber = drone_fly.subscriber:main',
        ],
    },
)


