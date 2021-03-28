# Skiylia - Interpreter
Dynamically typed Object Oriented Program Language.

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

![GitHub](https://img.shields.io/github/license/Skiylia/PySkiylia)
![Snyk Vulnerabilities for GitHub Repo](https://img.shields.io/snyk/vulnerabilities/github/Skiylia/PySkiylia)
[![codecov](https://codecov.io/gh/Skiylia/PySkiylia/branch/main/graph/badge.svg?token=DRJ67ZQA7M)](https://codecov.io/gh/Skiylia/PySkiylia)
[![time tracker](https://wakatime.com/badge/github/Skiylia/PySkiylia.svg?style=flat-square)](https://wakatime.com/badge/github/Skiylia/PySkiylia)

**PySkiylia: [Latest release](../releases)**

Open issues can be found here: [issues](../issues)

To create an issue, be it a bug, question, feature request, or other, use this link here: [Open an issue](../issues/new/choose)

# Skiylia

Skiylia is dynamically typed, object oriented, and most importantly *interpreted*. While it may share many similarities with C derivatives, its heritage is definitely Pythonic.

The main directory housing the PySkiylia interpreter is [here](../tree/main/PySkiylia). Within that directory is a separate document listing the most important syntax for Skiylia.

# Syntax overview

While there will definitely be a more exhaustive look into the exact syntactic structure and feature-set of Skiylia, a subset of it's important features are listed below.

## Comments

Line comments in Skiylia begin with '//', terminating with line breaks
```skiylia
// This is a Skiylia comment.
```

Multi-line comments begin and end with '///' clusters
```skiylia
/// This is a multi-line comment.
    It is particularly helpful for longer explanations.
    Of course, it can be used on a single line as well! ///
```

While it is common practice to align all multi-line comments with matching whitespace, it is by no means a requirement.

## Keywords

These are all of the words reserved for Skiylia functions, and cannot be used for variable names, class names, or the like.

```skiylia
and break continue class def do else false for if not
null or return self super true var when where while xor
```
*note: 'elif' is also a reserved word, but as of PySkiylia-0.7.1 has not been implemented.*

## Primitives

Primitives, also called native, external, or foreign functions are accessible to Skiylia but implemented in the host language (in this case, Python)

```skiylia
abs bool clock float floor int integer mod pow print
round sqrt str string
```

## Code structure

Much like Python, Skiylia code is divided into 'blocks' of equivalent indentation. All statements of greater indentation have access to the variables and functions in the blocks with lower indentation.

```skiylia
def function(b):
  // This line is within the function block.
  var a = "hello"

  if b ~~~ a:
    // This line is inside the function, and the 'if' statement block
    print(a, "and", b, "have the same type!")

  /// This line is not a part of the 'if' block,
      but is in the function block. ///
  return a

// This line is not within the function block.
```

Additionally, statements cannot appear adjacent to each-other. Instead, they are separated by newlines ('/n'), as opposed to C-like languages, which allow the use of semi-colons to condense statements onto single lines.

```skiylia
print("hi") print("hello world!")

/// This will cause an error, as the two
    print functions share the same line. ///
```

### Indentation rules

Some keywords, such as 'break' and 'return', act as block terminators, where indentation *must* decrease following them.

```skiylia
def testFunction(a):
  if a == "test":
    return true
    print("function input was not equal to 'test'.")

/// That final print function is at the same indentation level
    as the preceding return statement.
    This will cause an indentation error. ///
```

This is in contrast to the colon, which requires the indentation level to increase. Colons are always found following conditionals, control-flow structures, function definitions, and class definitions.

```skiylia
def testFunction(a):
  if a == "test":
  return true
  print("function input was not equal to 'test'.")

/// In this example, not only is the print statement at the
    same indentation level as the immediately preceding return,
    but the return itself is not indented relative to the
    conditional before it!
    This will cause two seperate indentation errors. ///
```

Colons cannot be placed anywhere in a Skiylia script, even if following the correct indentation rules. As mentioned above, conditionals, control-flow structures, function definitions, and class definitions (The group of which is imaginatively named 'Colon-terminated statements') are the only objects in Skiylia where a following colon is permitted.

```skiylia
def testFunction(a):
  if a == "test":
    print("function input was equal to 'test'."):
      return
  print("Test")

/// The indentation on the return is techincally correct,
    as it increases following a colon.
    This will still throw an error however, as the print
    function is not a colon-terminated statement. ///
```

The three examples above illustrate the indentation errors that can arise from mistyped code. Other languages get around this by denoting code blocks with curly braces '{ }', and allowing semi-colons to separate statements, but Skiylia aims to be slightly more human readable.

```skiylia
def testFunction(a):
  if a == "test":
    print("function input was equal to 'test'.")
    return
  print("Test")

/// Now we have well behaving indentation.
    Doesn't that look lovely?
    Plus, there's not an indentation error in sight! ///
```

### Exceptions to the rules

Of course, as with most languages, there do exist some exceptions. In Skiylia, this is the case where a colon-terminated statement is followed by a single expression.

Due to the colon acting as an implicit indentation marker, that expression can be written without a newline, without throwing an error.

```skiylia
if a == true: print("'a' was true!")
else: print("'a' was false!")

/// This script will not throw an indentation error,
    as the print function is a single statement. ///
```

As of PySkiylia-0.7.1, following implicit indentation with explicit indentation does not throw an error. In future versions, this may not be the case, and writing code as shown below is *highly* discouraged.
```skiylia
if a == true: print("'a' was true!")
  print("In fact, the value of 'a' was", a)
else: print("'a' was false!")

/// This will also not throw an error (for now).
    It does, of course, looks very ugly, so most
    people would avoid writing it anyway. ///
```

## Closing remarks

Now you know the most important basics of Skiylia, so grab that interpreter and give it a whirl! Just remember that the language is still evolving, and it's entirely possible that things written above may be modified or removed in future versions.

Thanks for reading this far, happy coding!
