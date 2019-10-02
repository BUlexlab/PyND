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
3. Install `prun`, a tool that makes running shell commands from your python virtual environment easy.
   ```sh
   $ pip install prun
   ```

4. Clone this repository.
5. From the root directory of the repository, create a python virtual environment for the project in the `PyND/venv/` directory
    ```sh
    $ cd PyND
    $ python -m venv venv
    ```
    
6. Install the pynd package into your newly created virtual environment. From the `PyND` directory, run:
   ```sh
   $ prun pip install -e .
   ```
   Note: to support automated unit tests with `pytest` run instead `prun pip install -e .[dev]`

7. Install the [R](https://www.r-project.org/) packages 
[reticulate](https://cran.r-project.org/web/packages/reticulate/index.html), which allows 
you to run python from within an R session and pass objects back and forth between the two, and [here](https://github.com/jennybc/here_here) which makes using relative paths within an R project structure easier.
    ```r
    install.packages("reticulate")
    install.packages("here")
    ```

8. From R, `source()` the file `PyND\test.R`, using `chdir=TRUE`

   ```r
   source("PyND\test.R", chdir=TRUE)
   ```
   You should get some output like: 

> pynd.neighbors - 10-01 21:41:33 INFO    : starting word 1 of 100, "B_01_061"
> pynd.neighbors - 10-01 21:41:35 INFO    : .. 9.0% complete, 5.63 words/sec. Est. 0:00:16.16 (H:MM:SS.ms) remaining.
> pynd.neighbors - 10-01 21:41:35 INFO    : starting word 10 of 100, "G_02_26"
> pynd.neighbors - 10-01 21:41:36 INFO    : .. 19.0% complete, 6.19 words/sec. Est. 0:00:13.08 (H:MM:SS.ms) remaining.
> pynd.neighbors - 10-01 21:41:36 INFO    : starting word 20 of 100, "E_02_92"
> pynd.neighbors - 10-01 21:41:38 INFO    : .. 29.0% complete, 6.91 words/sec. Est. 0:00:10.27 (H:MM:SS.ms) remaining.
> pynd.neighbors - 10-01 21:41:38 INFO    : starting word 30 of 100, "H_02_20"
> pynd.neighbors - 10-01 21:41:39 INFO    : .. 39.0% complete, 7.45 words/sec. Est. 0:00:08.19 (H:MM:SS.ms) remaining.
> pynd.neighbors - 10-01 21:41:39 INFO    : starting word 40 of 100, "C_01_080"
> pynd.neighbors - 10-01 21:41:40 INFO    : .. 49.0% complete, 8.84 words/sec. Est. 0:00:05.77 (H:MM:SS.ms) remaining.
> pynd.neighbors - 10-01 21:41:40 INFO    : starting word 50 of 100, "A_01_003"
> pynd.neighbors - 10-01 21:41:41 INFO    : .. 59.0% complete, 10.76 words/sec. Est. 0:00:03.81 (H:MM:SS.ms) remaining.
> pynd.neighbors - 10-01 21:41:41 INFO    : starting word 60 of 100, "B_01_034"
> pynd.neighbors - 10-01 21:41:42 INFO    : .. 69.0% complete, 14.09 words/sec. Est. 0:00:02.20 (H:MM:SS.ms) remaining.
> pynd.neighbors - 10-01 21:41:42 INFO    : starting word 70 of 100, "J_02_071"
> pynd.neighbors - 10-01 21:41:42 INFO    : .. 79.0% complete, 20.41 words/sec. Est. 0:00:01.03 (H:MM:SS.ms) remaining.
> pynd.neighbors - 10-01 21:41:42 INFO    : starting word 80 of 100, "C_02_044"
> pynd.neighbors - 10-01 21:41:43 INFO    : .. 89.0% complete, 34.74 words/sec. Est. 0:00:00.32 (H:MM:SS.ms) remaining.
> pynd.neighbors - 10-01 21:41:43 INFO    : starting word 90 of 100, "D_02_021"
> pynd.neighbors - 10-01 21:41:43 INFO    : .. 99.0% complete, 89.79 words/sec. Est. 0:00:00.01 (H:MM:SS.ms) remaining.
> pynd.neighbors - 10-01 21:41:43 INFO    : starting word 100 of 100, "B_03_061"
> pynd.neighbors - 10-01 21:41:43 INFO    : completed 100 words in 0:00:09.67 (H:MM:SS.ms) (10.35 word/sec)
> pynd.neighbors - 10-01 21:41:43 INFO    : Wrote file /Users/nkc/PyND/output/foo-neighbors.csv
> pynd.neighbors - 10-01 21:41:43 INFO    : wrote file /Users/nkc/PyND/output/foo-nd.csv


