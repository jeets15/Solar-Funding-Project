from setuptools import setup

setup(
    packages=['solar_offset'],
    include_package_data=True,
    install_requires=[
        'flask',
        'python-dotenv',
        'google-api-python-client',
        'email-validator'
    ]
)
