import setuptools

setuptools.setup(
    name="myenv",
    version="0.0.1",
    description="A small example package",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'pymysql',
        'scipy',
        'streamlit >=1.0',
        'compress_pickle',
        'hydralit_components>=1.0.7',
        'validators',
        'bokeh',
    ],
)
