try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
        name="ssa_baby_names",
        version="2.1",
        
        py_modules=["ssa_baby_names"],
        install_requires=["requests"],

        description="Python wrapper for the Social Security Administration's Popular Baby Names service",
        author="Miles Watkins",
        author_email="miles.w.watkins@gmail.com",

        url="https://github.com/mileswwatkins/ssa_baby_names",
        download_url="https://github.com/mileswwatkins/ssa_baby_names/tarball/2.1",
        keywords=["Social Security Administaration", "SSA", "baby names", "popular names", "names"]
        )
