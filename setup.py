import setuptools

requires = [
    "flake8 > 7.0.0",
]

flake8_entry_point = "flake8.extension"

setuptools.setup(
    name="flake8_six_compatablity_plugin",
    license="MIT",
    version="1.0.0",
    python_requires='>3.2.0',
    description="Flake8 Extension to ensure six compatability",
    author="ShakedAp",
    url="https://github.com/ShakedAp/flake8_six_plugin",
    packages=setuptools.find_packages(),
    install_requires=requires,
    entry_points={
        flake8_entry_point: [
            'SIX = flake8_six_compatablity_plugin.flake8_plugin:SixCompatibilityPlugin',
        ],
    },
    classifiers=[
        "Framework :: Flake8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
)