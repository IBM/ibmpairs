## Contributing In General

You are very welcome to contribute to the open source repository of the IBM PAIRS Geoscope.
To contribute code or documentation, please submit a [pull request](https://github.com/IBM/ibmpairs/pulls).


### Proposing new features

If you would like to implement a new feature, please [raise an issue](https://github.com/IBM/ibmpairs/issues)
before sending a pull request so the feature can be discussed. This is to avoid
you wasting your valuable time working on a feature that the project developers
are not interested in accepting into the code base.


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
same approach - the [Developer's Certificate of Origin 1.1 (DCO)](https://github.com/hyperledger/fabric/blob/master/docs/source/DCO1.1.txt)
- that the Linux® Kernel [community](https://elinux.org/Developer_Certificate_Of_Origin)
uses to manage code contributions.

We simply ask that when submitting a patch for review, the developer must include
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
like `git-commit-template` with the DCO above, and run `git config commit.template git-commit-template`
once to have it as your default when running `git commmit ...`.


## Testing

We ask and expect you to write test cases for the contribution you make, because
it significantly helps to detect bugs while the project grows. Please place corresponding
code into the `tests` directory. Please make pull requests after your contribution
has passed all tests, only.

Right now, at least
```Bash
python tests/test_paw.py
```
has to pass without error.

## Coding style guidelines

When writing code please adopt the following coding style guidelines:
- try to well document your code, ideally with an approximate ratio 1:3 of documentation to code
- each function (of a class etc.) should have sufficient documentation on input, output,
  and how it processes information
- try to avoid having more than 80 characters of code per line
- it would be nice if you use ([VIM](http://vimdoc.sourceforge.net/htmldoc/fold.html)-style)
  text folding markers (`{{{` and `}}}`) to logically group
  your code

You can always take existing code as an example of good coding style.
