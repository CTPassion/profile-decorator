<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
[![LinkedIn][linkedin-shield]][linkedin-url]
<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">profile-decorator</h3>

  <p align="center">
    Simplifies method profiling
  </p>
</div>


<!-- GETTING STARTED -->

### Prerequisites

There are no external dependancies, profiling is done using the standard library
package `CProfile`.

### Installation

Install the package
   ```sh
   pip install profile-decorator
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

Import the profile_me decorator:

```python
from profile_decorator import profile_me
```

For the default use, simply add it as a decorator to the function
you want to profile:
```python
@profile_me
def foo(bar):
    print("start")
    time.sleep(5)
    print("end")
```
This will return the profiled execution of foo when foo is called anywhere in your code.
By default, the profiling results are sorted by cumulative time, and only the top 50 are returned.

### Custom profiling
You can pass arguments to the decorator:
```python
@profile_me(n_rows=10, sort_by="time", output="file", filename="results")
def foo(bar):
    print("start")
    time.sleep(5)
    print("end")
```
This will return only the top 10 calls, sorted by time and then write them to a file rather than the stdout console, 
to do this you must provide a filename too.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the Apache Software License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Joshua Brumpton - ja.brumpton@gmail.com

Project Link: [github repo](https://github.com/CTPassion/profile_me/issues)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/joshua-brumpton-8a6bb619b/
