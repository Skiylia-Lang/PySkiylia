# PySkiylia
Dynamically typed Object Oriented Programming Language.

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

![GitHub](https://img.shields.io/github/license/Skiylia-Lang/PySkiylia)
![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/Skiylia-Lang/PySkiylia)
[![codecov](https://codecov.io/gh/Skiylia-Lang/PySkiylia/branch/main/graph/badge.svg?token=DRJ67ZQA7M)](https://codecov.io/gh/Skiylia-Lang/PySkiylia)
[![time tracker](https://wakatime.com/badge/github/Skiylia-Lang/PySkiylia.svg)](https://wakatime.com/badge/github/Skiylia-Lang/PySkiylia)
![GitHub language count](https://img.shields.io/github/languages/count/Skiylia-Lang/PySkiylia)
![GitHub top language](https://img.shields.io/github/languages/top/Skiylia-Lang/PySkiylia)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Skiylia-Lang/PySkiylia)
![Lines of code](https://img.shields.io/tokei/lines/github.com/Skiylia-Lang/PySkiylia)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat)](#contributors)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Releases

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Skiylia-Lang/PySkiylia?include_prereleases)
![GitHub commits since latest release (by date including pre-releases)](https://img.shields.io/github/commits-since/Skiylia-Lang/PySkiylia/latest/develop?include_prereleases)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/Skiylia-Lang/PySkiylia)
![GitHub milestone](https://img.shields.io/github/milestones/progress/Skiylia-Lang/PySkiylia/1)
![GitHub milestones](https://img.shields.io/github/milestones/open/Skiylia-Lang/PySkiylia)
![GitHub issues](https://img.shields.io/github/issues-raw/Skiylia-Lang/PySkiylia)
![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/Skiylia-Lang/PySkiylia)
![GitHub last commit](https://img.shields.io/github/last-commit/Skiylia-Lang/PySkiylia)

**PySkiylia: [Latest release](PySkiylia/releases)**

Open issues can be found here: [issues](PySkiylia/issues)

To create an issue, be it a bug, question, feature request, or other, use this link here: [Open an issue](PySkiylia/issues/new/choose)

# Skiylia

Skiylia is dynamically typed, object oriented, and most importantly *interpreted*. While it may share many similarities with C derivatives, its heritage is definitely Pythonic.

The main directory housing the PySkiylia interpreter is [here](PySkiylia/tree/main/PySkiylia). Within that directory is a separate document listing the most important syntax for Skiylia.

## Sample code

```skiylia
///This section contains a small snippet of Skiylia
code that calculates the factorial of a number///

def factorial(n):
  if int(n) != n:
    return null   //can't compute factorial of a float this way
  if n < 2:
    return 1
  return n * factorial(n - 1)   //recursion that makes this work

var num = 6
print("The factorial of", num, "is", factorial(num))

//output: The factorial of 6 is 720
```

Within this [folder](PySkiylia/tree/main/ExampleCode) is a collection of code examples that have been used to test the project. While not exhaustive by any means, they should cover the basics. Feel free to play around and get a feel for the language!

Who knows, at some point in the future there may even be a link to a Skiylia tutorial. It's certainly an idea in the works.

## Running Skiylia

Under the [Latest release] you'll find the most up to date version of PySkiylia, containing all the python sub-modules. Running PySkiylia.py from the command line will open the interpreter in REPL mode, while passing a .skiy file as a second argument will allow execution of said script.

## Contributing

Any contributions made are absolutely welcome. Checkout the issues area for any outstanding problems, or to file your own!

Forking this repository is an excellent way to contribute to the code that makes this interpreter tick. Open a pull request (preferably to the develop branch) if you have anything to add, and it'll be looked over.

# Acknowledgements

I, [Jack](https://github.com/SK1Y101), definitely couldn't have created PySkiylia without any outside sources.

I owe a huge debt to Bob Nystrom and his excellent book, [Crafting Interpreters](https://craftinginterpreters.com/). Not only did he give me true inspiration to develop Skiylia, but also provided cleanly documented concepts and a delightful read. If there is *anyone* that hasn't yet read his implementation of Lox from cover to cover, I would thoroughly recommend doing so.

## Tools

 - The interpreter was written in [Python](https://www.python.org/) 3.8, and can be ran on any machine with it installed.
 - [Mergify](https://mergify.io/) has been automatically managing all of the repository branches.
 - [All-contributors](https://allcontributors.org/) has been managing the contributors section.
 - [Snyk](https://snyk.io/) has been monitoring for security concerns.
 - [Release-drafter](https://github.com/release-drafter/release-drafter) has been compiling all pull requests into changelogs on each draft release, massively expediating the process.
 - And while we don't have an dependencies (yet?) [Dependabot](https://dependabot.com/) has been keeping in the shadows.

## Contributors

All the people who have contributed ([emoji key](https://allcontributors.org/docs/en/emoji-key)):
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/SK1Y101"><img src="https://avatars.githubusercontent.com/u/8695579?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jack Lloyd-Walters</b></sub></a><br /><a href="https://github.com/Skiylia-Lang/PySkiylia/commits?author=SK1Y101" title="Code">💻</a> <a href="https://github.com/Skiylia-Lang/PySkiylia/pulls?q=is%3Apr+reviewed-by%3ASK1Y101" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/SK2Y202"><img src="https://avatars.githubusercontent.com/u/81203841?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jack Lloyd-Walters</b></sub></a><br /><a href="https://github.com/Skiylia-Lang/PySkiylia/pulls?q=is%3Apr+reviewed-by%3ASK2Y202" title="Reviewed Pull Requests">👀</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://allcontributors.org) specification.
