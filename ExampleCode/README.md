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

```skiylia
///This section contains a small snippet of Skiylia
code that calculates the Tribonacci numbers///

def Trib(n):
  var a = 0
  var b = 0
  var c = 1
  var out = 0
  for var x when x<n do x++:
    out = a + b + c
    c = b
    b = a
    a = out
  return out

for var x when x<=10:
  print(Trib(x))

//0, 1, 1, 2, 4, 7, 13, 24, 44, 81, 149
```

## Sample Class structure

```skiylia
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

class John(Person):
  birthday():
    super.birthday()
    print("I hate getting older")

var John = Person("John", 24)
John.hello()

John.birthday()
John.name = "Johnathon"
John.hello()

///Hi there, I'm John, and I'm 24
   I hate getting older
   Hi there, I'm Johnathon, and I'm 25///
```

[Latest release]: https://github.com/SK1Y101/PySkiylia/releases
[issues]: https://github.com/SK1Y101/PySkiylia/issues
[folder]: https://github.com/SK1Y101/PySkiylia/ExampleCode
