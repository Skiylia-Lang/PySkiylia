# Skiylia - Example code
Dynamically typed Object Oriented Program Language.

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

![GitHub](https://img.shields.io/github/license/SK1Y101/PySkiylia)
![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/SK1Y101/PySkiylia)
[![codecov](https://codecov.io/gh/SK1Y101/PySkiylia/branch/main/graph/badge.svg?token=DRJ67ZQA7M)](https://codecov.io/gh/SK1Y101/PySkiylia)
[![time tracker](https://wakatime.com/badge/github/SK1Y101/PySkiylia.svg?style=flat-square)](https://wakatime.com/badge/github/SK1Y101/PySkiylia)
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat)](#contributors)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

This repository folder contains examples of Skiylia-specific code, and (possibly) the equivalent in python.

## Releases

**PySkiylia: [Latest release]**

Support here: [issues]

## Sample Function code

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

## Sample Class structure

    ///This section contains a small snippet of Skiylia
    code that demonstrates class methods and properties///

    class Person:
      init(name, age):      //executed on initialisation
        self.name = name
        self.age = age

      hello():
        print("Hi there, I'm", self.name, ", and I'm", self.age)

      birthday():
        self.age = self.age + 1

    var John = Person("John", 24)
    John.hello()

    John.birthday()
    John.name = "Johnathon"
    John.hello()

    ///Hi there, I'm John, and I'm 24
       Hi there, I'm Johnathon, and I'm 25///


[Latest release]: https://github.com/SK1Y101/PySkiylia/releases
[issues]: https://github.com/SK1Y101/PySkiylia/issues
[folder]: https://github.com/SK1Y101/PySkiylia/ExampleCode
