## Contributing

You are very welcome to contribute to the open source repository of the IBM Environmental Intelligence: Geospatial APIs SDK (ibmpairs).
To contribute code or documentation, please submit a [pull request](https://github.com/IBM/ibmpairs/pulls).


### Setting up your development environment

To obtain all required Python module, simply run
```Bash
pip install -r requirements.txt
pip install -r requirements-development.txt
```
from the base of this repo.


### Proposing new features

If you would like to implement a new feature, please [raise an issue](https://github.com/IBM/ibmpairs/issues)
before sending a pull request so the feature can be discussed.


### Fixing bugs

If you would like to fix a bug, please [raise an issue](https://github.com/IBM/ibmpairs/issues)
before sending a pull request so it can be tracked.


### Merge approval

The project maintainers use LGTM (Looks Good To Me) in comments on the code
review to indicate acceptance. A change requires LGTMs from one of the
maintainers of each component affected.

For a list of the maintainers, see the [MAINTAINERS.md](MAINTAINERS.md) page.


## Legal

Each source file must include a license header for the [BSD-Clause-3](https://opensource.org/licenses/BSD-3-Clause)
Software License. Using the SPDX format is the simplest approach.
e.g.

```Python
# Copyright <years> <holder> All Rights Reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
```

We have tried to make it as easy as possible to make contributions. This
applies to how we handle the legal aspects of contribution. We use the
same approach - the [Developer's Certificate of Origin 1.1 (DCO)](https://github.com/hyperledger/fabric/blob/master/docs/source/DCO1.1.txt) - that
the Linux® Kernel [community](https://elinux.org/Developer_Certificate_Of_Origin)
uses to manage code contributions.

We simply assert that when submitting a patch for review, the developer must include
a sign-off statement in the commit message.

Here is an example Signed-off-by line, which indicates that the submitter accepts
the DCO linked above:
```
Signed-off-by: Your Name <your@mail.org>
```

You can include this automatically when you commit a change to your
local git repository using the following command:
```Bash
git commit -s
```
Alternatively/in addition you can have a template for your commit text in a file
like `git-commit-template` with the DCO above. Then run `git config commit.template git-commit-template`
to have it as your default when running `git commit ...`.


## Testing

We ask and expect you to write test cases for the contribution you make, because
it significantly helps to detect bugs while the project grows. Please place corresponding
code into the `tests` directory. Please make pull requests after your contribution
has passed all tests, only.

Please make sure
```Bash
pytest
```
passes without error. Note, there is a set of environment variables such as
`PAW_TESTS_REAL_CONNECT`, `PAW_TESTS_PAIRS_PASSWORD_FILE_NAME`, `PAW_TESTS_PAIRS_USER`,
etc. which can be employed to configure the test suite at runtime.


## Coding style guidelines

When writing code please adopt the following coding style guidelines:
- Try to well document your code, ideally with an approximate ratio 1:3 of documentation to code.
- Each function (of a class etc.) should have sufficient documentation on input, output, exceptions
  and how it processes information. The goal is to have all documentation required for
  the API in code such that [Sphinx](https://documentation-style-guide-sphinx.readthedocs.io/en/latest/style-guide.html)
  can automatically generate documentation. An example:
  ```Python
  def numbers_2_string(numbers):
      """
      This is a one-liner summarising the function.

      And here comes more details.

      :param numbers:       list of random numbers to convert to string
      :type numbers:        [float]
      :returns:             the user given numbers, concatenated by space
      :rtype:               str
      :raises Exception:    if given input cannot be interpreted
                            if the input is not an iterable
      """
      # check that all elements in input are floating point numbers
      if not all(
        [
            isinstance(num, float)
            for num in numbers
        ]
      ):
          raise Exception("Sorry, input contains non-floating point elements.")

      # return space-concatenated numbers
      return ' '.join(numbers)
  ```
  *note*: This example also incorporates other aspects mentioned below
- Try to reserve one line for each argument of a function/class (call), e.g. instead
  of
  ```Python
  funct(arg1, arg2, arg3=default1, argum4=default2, ...)
  ```
  this is preferred:
  ```Python
  funct(
    arg1,
    arg2,
    arg3    = default1,
    argum4  = default2,
    ...
  )
  ```
  Similarly, it holds for dictionaries:
  ```Python
  {
    "key1": [
        {
            "subkey1": "val1",
            "subkey2": "val2",
            ...
        }
    ],
    "key2":  122.2,
    ...
  }
  ```
  instead of
  ```Python
  {"key1":[{"subkey1":"val1","subkey2":"val2",...}],"key2":122.2,...}
  ```
- For indentation, please use 4 simple space characters,
- Try to avoid having more than 80 characters of code per line
- Please choose descriptive names for variables, e.g. for quantities with physical
  units we tend to include the unit in the name, some examples:

  | variable example        | description                                                                    |
  |-------------------------|--------------------------------------------------------------------------------|
  | `time_start_running_sec`   | simple variable   |
  | `PingServer`            | class instance having fist character upper case                                |
  | `MAX_TIME_THESHOLD_MS`  | a global constant with units miliseconds                                       |
  | `time_service_response` | a function name                                                                |

  *note*: This way the code becomes more human readable (documentation of variable by name).

You can always take existing code as an example of good coding style.
