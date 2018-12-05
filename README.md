# PyND
Python module for calculating neighborhood density

## Getting Started
1. Be sure you have [Python](https://www.python.org/) installed. From a shell session, 
run `python --version`.  The output should look something like what is shown below. 
This package was developed against Python 3.6, though it may work with newer versions
of python.

    ```sh
    $ python --version
    Python 3.6.6
    ```
2. Check that `pip` is installed for the version of Python you intend on using. 
From a shell session, run `pip --version`. The output should look something like 
what is shown below. It's critical that the python version shown at the end of the line 
matches the one above.

    ```sh
    $ pip --version
    pip 18.1 from c:\...python\python36\lib\site-packages\pip (python 3.6)
    ```

3. Check that `pipenv` is installed. From a shell session, run `pipenv --version`.
The output should be something like: 
    ```sh
    $ pipenv --version
    pipenv, version 2018.10.13
    ```
    If pipenv is not installed, install it using pip by running `pip install pipenv`, 
then check that the installation was successful by running `pipenv --version`

4. Clone this repository.
5. From the root directory of the repository, create a virtual environment with `pipenv`
    ```sh
    $ cd PyND
    $ pipenv shell
    ```
6. Install the [R](https://www.r-project.org/) package 
[reticulate](https://cran.r-project.org/web/packages/reticulate/index.html), which allows 
you to run python from within an R session and pass objects back and forth between the two.
    ```r
    install.packages("reticulate")
    ```
7. From R, `source()` the file `PyND\Test.R`
