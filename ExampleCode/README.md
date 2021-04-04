# Skiylia - Example code
Dynamically typed Object Oriented Program Language.

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

![GitHub](https://img.shields.io/github/license/Skiylia-Lang/PySkiylia)
[![CodeFactor](https://www.codefactor.io/repository/github/skiylia-lang/pyskiylia/badge)](https://www.codefactor.io/repository/github/skiylia-lang/pyskiylia)
![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/Skiylia-Lang/PySkiylia)
[![codecov](https://codecov.io/gh/Skiylia-Lang/PySkiylia/branch/main/graph/badge.svg?token=DRJ67ZQA7M)](https://codecov.io/gh/Skiylia-Lang/PySkiylia)
[![time tracker](https://wakatime.com/badge/github/Skiylia-Lang/PySkiylia.svg?style=flat-square)](https://wakatime.com/badge/github/Skiylia-Lang/PySkiylia)

This repository folder contains examples of Skiylia-specific code, and (possibly) the equivalent in python.

**PySkiylia: [Latest release](../../releases)**

Open issues can be found here: [issues](../../issues)

To create an issue, be it a bug, question, feature request, or other, use this link here: [Open an issue](../../issues/new/choose)

# Skiylia

<img src="https://raw.githubusercontent.com/Skiylia-Lang/skiylia-lang.github.com/7a2533a517895c08b8aa52c32396c292a0563d49/Skiylia_Logo_text.svg" width=60%/>

Skiylia is dynamically typed, object oriented, and most importantly *interpreted*. While it may share many similarities with C derivatives, its heritage is definitely Pythonic.

The main directory housing the PySkiylia interpreter is [here](../../tree/main/PySkiylia). Within that directory is a separate document listing the most important syntax for Skiylia.

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
