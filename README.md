# PySkiylia
Dynamically typed Object Oriented Programming Language.

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

![GitHub](https://img.shields.io/github/license/SK1Y101/PySkiylia)
![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/SK1Y101/PySkiylia)
[![codecov](https://codecov.io/gh/SK1Y101/PySkiylia/branch/main/graph/badge.svg?token=DRJ67ZQA7M)](https://codecov.io/gh/SK1Y101/PySkiylia)
[![time tracker](https://wakatime.com/badge/github/SK1Y101/PySkiylia.svg?style=flat-square)](https://wakatime.com/badge/github/SK1Y101/PySkiylia)
![GitHub language count](https://img.shields.io/github/languages/count/SK1Y101/PySkiylia)
![GitHub top language](https://img.shields.io/github/languages/top/SK1Y101/PySkiylia)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/SK1Y101/PySkiylia)
![Lines of code](https://img.shields.io/tokei/lines/github.com/SK1Y101/PySkiylia)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat)](#contributors)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Releases

![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/SK1Y101/PySkiylia?include_prereleases)
![GitHub commits since latest release (by date including pre-releases)](https://img.shields.io/github/commits-since/SK1Y101/PySkiylia/latest/develop?include_prereleases)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/SK1Y101/PySkiylia)
![GitHub milestone](https://img.shields.io/github/milestones/progress/SK1Y101/PySkiylia/1)
![GitHub milestones](https://img.shields.io/github/milestones/open/SK1Y101/PySkiylia)
![GitHub issues](https://img.shields.io/github/issues-raw/SK1Y101/PySkiylia)
![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/SK1Y101/PySkiylia)
![GitHub last commit](https://img.shields.io/github/last-commit/SK1Y101/PySkiylia)

**PySkiylia: [Latest release]**

Support here: [issues]

# Skiylia

Skiylia is dynamically typed, object oriented, and most importantly *interpreted*. While it may share many similarities with C derivatives, its heritage is definitely Pythonic.

To that end, Skiylia is most aptly described as a Python-C# hybrid.

##

## Sample code

    ///This section contains a small snippet of Skiylia
    code that calculates the factorial of a number///

    def factorial(n):
        if int(n) != n:
            return null   //can't compute factorial of a float this way
        if x < 2:
            return 1
        return x * factorial(n - 1)   //recursion that makes this work

    var num = 6
    print("The factorial of", num, "is", factorial(num))

    //output: The factorial of 6 is 720

Within this [folder] is a collection of code examples that have been used to test the project. While not exhaustive by any means, they should cover the basics. Feel free to play around and get a feel for the language!

## Contributing

Any contributions made are absolutely welcome. Checkout the issues area for any outstanding problems, or to file your own!

Forking this repository is an excellent way to contribute to the code that makes this interpreter tick. Open a pull request (preferably to the develop branch) if you have anything to add, and it'll be looked over.

# Acknowledgements

I, [Jack](https://github.com/SK1Y101), definitely couldn't have created PySkiylia without any outside sources.

I owe a huge debt to Bob Nystrom and his excellent book, [Crafting Interpreters]. Not only did he give me true inspiration to develop Skiylia, but also provided cleanly documented concepts and a delightful read. If there is *anyone* that hasn't yet read his implementation of Lox from cover to cover, I would thoroughly recommend doing so.

## Tools

Languages: [Python] (of course)


## Contributors

All the people who have contributed ([emoji key](https://allcontributors.org/docs/en/emoji-key)):
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/SK1Y101"><img src="https://avatars.githubusercontent.com/u/8695579?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jack Lloyd-Walters</b></sub></a><br /><a href="https://github.com/SK1Y101/PySkiylia/commits?author=SK1Y101" title="Code">💻</a> <a href="https://github.com/SK1Y101/PySkiylia/pulls?q=is%3Apr+reviewed-by%3ASK1Y101" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/SK2Y202"><img src="https://avatars.githubusercontent.com/u/81203841?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jack Lloyd-Walters</b></sub></a><br /><a href="https://github.com/SK1Y101/PySkiylia/pulls?q=is%3Apr+reviewed-by%3ASK2Y202" title="Reviewed Pull Requests">👀</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://allcontributors.org) specification.

[Latest release]: https://github.com/SK1Y101/PySkiylia/releases
[issues]: https://github.com/SK1Y101/PySkiylia/issues
[folder]: https://github.com/SK1Y101/PySkiylia/tree/main/ExampleCode
[Crafting Interpreters]: https://craftinginterpreters.com/
