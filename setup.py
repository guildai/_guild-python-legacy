from setuptools import setup

setup(name="guild",
      packages=["guild"],
      version="0.2.dev0",
      install_requires=[
          "pyyaml",
          "werkzeug",
      ],
      author="TensorHub, Inc",
      email="garrett@guild.ai",
      license="Apache License, Version 2"
)
