from setuptools import find_packages, setup

package_name = 'egitim_ortam'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Mavi Gölge Yazılım Ekibi',
    maintainer_email='mavigolge@example.com',
    description='Yer tutucu paket: CI zincirinin çalıştığını doğrular.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={'console_scripts': []},
)
