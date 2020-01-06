# FizzBuzzLang
## The FizzBuzz Esoteric Programming Language
I firmly believe that most esoteric programming languages are the result of the affect of alcohol on the brains of carbon-based life forms. FizzBuzzLang is no different!

It's the language no one asked for, and never missed before it existed. But that didn't stop me creating it. Mainly because I dearly want a tech interview sometime, somewhere to go like this:

_Interviewer:_ Ok, can you write FizzBuzz for us?  
_Dev:_ Sure, what do you want me to write?  
_Interviewer:_ Ummmm…FizzBuzz?  
_Dev:_ Yes, but what? Hello World? An I/O example?  
_Interviewer:_ (look of confusion creeps across their face)

Ok, that might never happen, but (along with the whiskey I was drinking) it was enough to amuse me.

FizzBuzzLang is a Turing-complete programming language based on the classic interview challenge, FizzBuzz. It is possible to write FizzBuzz in FizzBuzzLang, but you run the risk of ending up in a very deep Turing-tarpit.

FizzBuzzLang is an imperative language, and each statement must be on its own line. <a href="https://raw.githubusercontent.com/lechien73/FizzBuzzLang/master/hello.fb" target="_blank">Here is an implementation of Hello World in FizzBuzzLang.</a>

It has just three keywords: FIZZ, BUZZ and FIZZBUZZ, and code is written as an Instruction Modification Parameter (IMP).

| IMP    | Mode Number | Meaning       |
|:-------|:-----------:|:--------------|
| FIZZ   | 1 | Data-space manipulation mode |
| BUZZ   | 2 |I/O mode |
| FIZZBUZZ | 3 | Flow control mode |

These are expanded below:

## Mode 1 - Data-space manipulation

FizzBuzzLang has an infinite (for very small values of infinite) data-space to work with.

### Movement through the data-space

We can move through the data-space using the following keywords:

| Keyword | Arguments |
|:--------|:----------|
| FIZZ    | FIZZ - move the pointer one step forwards in the data-space |
| FIZZ    | BUZZ - move the pointer one step backwards in the data-space |

So, `FIZZ FIZZ FIZZ` will move our data-space pointer one step forwards.

### Arithmetic

In mode 1, we can manipulate the data at the current pointer position:

| Keyword | Arguments | Optional Arguments |
|:--------|:----------|:-------------------|
| BUZZ    | FIZZ - addition | FIZZ or BUZZ - the names of stored locations |
| BUZZ    | BUZZ - subtraction | FIZZ or BUZZ - the names of stored locations |
| BUZZ    | FIZZBUZZ - modulus operation | FIZZ or BUZZ - the names of stored locations |

If the optional arguments are not supplied, then this keyword behaves as follows:

`FIZZ BUZZ FIZZ` increments the data at the current pointer position by one.
`FIZZ BUZZ BUZZ` decrements the data at the current pointer position by one.
`FIZZ BUZZ FIZZBUZZ` calculates the modulus of the value stored at the current pointer position and the position immediately preceding the current pointer and stores it in a location immediately following the current pointer position. So, if our data-space looks like this: `[10,7]` and the pointer is at `7`, here is how it would look after running the modulus operation: `[10,7,3]`

The optional arguments give the names of one of two stored locations in FizzBuzzLang.

### Stored locations

FizzBuzzLang has two storage locations, which allow you to store data-space addresses for later retrieval or arithmetic operations.

| Keyword   | Arguments     |
|:----------|:--------------|
| FIZZBUZZ  | FIZZ - store the current data-space address in the FIZZ storage location |
| FIZZBUZZ  | BUZZ - store the current data-space address in the BUZZ storage location |
| FIZZBUZZ  | FIZZBUZZ - move the data-space pointer to the address in either FIZZ or BUZZ |

Let's imagine that our data-space looks like this:

```
0000: 10
0001: 15
0002: 0
0003: 45 <
```
Our data-space pointer is at address 0003. The command `FIZZ FIZBUZZ FIZZ` will cause address 0003 to be stored in the FIZZ location.

If we want to jump to that location in the data-space, we can do so with the command: `FIZZ FIZZBUZZ FIZZBUZZ FIZZ`, which will cause the data-space pointer to move to the address stored in the `FIZZ` location.

Alternatively, we can use the location names in along with the arithmetic functions. So, as discussed `FIZZ BUZZ FIZZ` increments the data at the current pointer position by one. `FIZZ BUZZ FIZZ FIZZ` adds the value at location `FIZZ` to the value at the current data-space pointer. `FIZZ BUZZ FIZZBUZZ FIZZ` calculates the modulus of the value at location `FIZZ` and the value at the current data-set pointer and stores it in a location immediately following the current pointer position.

## Mode 2 - I/O

The `BUZZ` keyword selects mode 2, which handles input and output.

| Keyword | Optional Arguments | Meaning |
|:--------|:----------|:----------|
| FIZZ    | FIZZ or BUZZ | Outputs the number at the current data-space location or storage location |
| BUZZ    | FIZZ or BUZZ |Outputs the character representation of the number at the current location or storage location |
| FIZZBUZZ | | Accepts input of an integer, and stores it at the current data-space location |
| FIZZBUZZ | FIZZBUZZ | Allows input of a binary coded number, which is stored at the current data-space location |

FizzBuzzLang allows entry of a binary coded number to be stored at the current data-space location. The format of the number is FIZZ for 0 and BUZZ for 1. So, to store the binary number 1001000 (which is 72 in decimal), you would use the following code: `BUZZ FIZZBUZZ FIZZBUZZ BUZZ FIZZ FIZZ BUZZ FIZZ FIZZ FIZZ`

I/O example:

```
// requests input and stores it at the current location
BUZZ FIZZBUZZ
// prints out the number
BUZZ FIZZ
// prints out the ASCII representation of the number
BUZZ BUZZ
// end the program
FIZZBUZZ FIZZBUZZ
```

## Mode 3 - Flow Control

The `FIZZBUZZ` keyword selects mode 3, flow control mode.

| Keyword | Arguments | Meaning |
|:--------|:----------|:--------|
| FIZZ    | label name | Creates a label with the name given in the argument |
| BUZZ    | FIZZ + label name | Jump to label name if the current location value is not zero |
| BUZZ    | BUZZ + label name | Jump to label name if the current location value is zero |
| BUZZ    | FIZZBUZZ + label name | Jump to label name unconditionally |
| FIZZBUZZ | Ends the program |

The label name can contain anything you want, except whitespace characters. Convention (which I've just made up) says that it should be a combination of FIZZ and BUZZ

All programs must end with `FIZZBUZZ FIZZBUZZ`

Flow control example:

```
// set the current location value to 2
FIZZ BUZZ FIZZ
FIZZ BUZZ FIZZ
// create a label called FIZZBUZZBUZZ
FIZZBUZZ FIZZ FIZZBUZZBUZZ
// print the current location value
BUZZ FIZZ
// decrement the value at the current location by 1
FIZZ BUZZ BUZZ
// jump back to the label if the location value is not 0 else continue
FIZZBUZZ BUZZ FIZZ FIZZBUZZBUZZ
// end the program
FIZZBUZZ FIZZBUZZ
```

## General

FizzBuzzLang can be used to create complex(ish) programs. It can be used for loops, arithmetic, conditional branching and has rudimentary variable storage.

Any line not beginning with FIZZ, BUZZ or FIZZBUZZ is ignored, so it can be used to make an (ugly) polyglot.

The `fbi.py` file is a hacked-together FizzBuzzLang interpreter in Python. Use it as follows:

```python
from fbi import FizzBuzzLang

fb = FizzBuzzLang()

fb.run_file("filename.fb")
```

Bear in mind that the bits that should be working probably aren't - or work in unexpected ways. The bits that don't work will either just not work or not work spectacularly.

## Contributing

FizzBuzzLang is released under the GPL, which means you are encouraged to extend and modify the software. Personally, I really want you to! There is much left to implement, and I'd really like to see someone write an actual FizzBuzz implementation in FizzBuzzLang - or just see how complex we can get. I'd be interested to see if compact programs can be made.

_Matt Rudge, January 2020_
