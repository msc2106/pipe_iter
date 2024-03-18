import setuptools 

with open("README.md", "r") as fh: 
	description = fh.read() 

setuptools.setup( 
	name="pipe-iter", 
	version="0.1", 
	author="Mark Cohen", 
	author_email="mark.simon.cohen@gmail.com", 
	packages=["pipe-iter"], 
	description="A package to allow chaining of functional operations on iterators, modeled on Rust's iterator syntax", 
	long_description=description, 
	long_description_content_type="text/markdown", 
	url="https://github.com/msc2106/pipe_iter", 
	license='MIT', 
	python_requires='>=3.9', 
	install_requires=[] 
) 
