---
title: Programming Constructs
subtitle: Unit 14 Assignment 1
---

# Variables

## What's a Variable?

To learn programming, we must first learn variables. These are perhaps the single most important part of software development as they're one of the simplest constructs which are used very commonly.

Variables store data and variables are able to change, hence the name Variable. These are used to store data inside of a program for short or long periods of time to remember some kind of information to be used later. They can be passed all the way from the start of a new program, or be used for a millisecond and then destroyed.

## Examples

### Defining an Integer

As we’re using C# for this basic programming tutorial, we will use the syntax of C#. The syntax of a programming language means how it looks and how its formatted, comparable to how Spanish or Czech has a ton of accents above letters, compared to English which evidently doesn’t. For the first example, let’s see how we define a variable:

```
int x = 1;
```

This variable declaration sets the key, or name, of x to be of the value 1. How is this 1 defined? Well, its stored inside of the program as a 32-bit long representation of a number which is defined by the int word (or keyword) which we used at the start of this example.

In essence, it sets x as a typical number equaling 1 inside of the program. To change this value, all that we have to do is something along the lines of:

```
x = 24;
```

All that this does is tell C# to change the existing value x to 24. It knows that x already exists because we haven’t added that keyword before, and it knows that the 24 value is valid as once C# finds the variable declaration, it knows that it’s set as an int datatype.

This is all variables are; there’s not much more to it!

### Defining a String

Using the same syntax, we can also define something called a string. These are a series of characters, such as the ones I’m writing now. Strings can have numbers inside of them, but the numbers aren’t considered actual numbers which can be added to or subtracted from for example.

Defining a new string variable is just as simple as a number:

```
string my_string = “Hello, World!”;
```

In certain languages, such as C#, allow you to also add other variables inside of strings. This is called “string concatenation” or “string formatting”. The same thing happens in other languages like Python, albeit slightly differently:

```
string new_string = $”HELLO {my_string) WORLD”;
```

This results in the overall string of “HELLO Hello, World! WORLD” being stored in memory.

### Defining a Float

Floats are almost the same as numbers to define but require some kind of decimal (.x) after it no matter what. Floats are numbers with these decimals on the end; allowing for more precise division and numbers than just whole numbers.

These do have a few disadvantages which won’t be mentioned in this tutorial, but keep in mind that it’s preferable to use integers if possible. This is how you define a float:

```
float my_float = 20.00;
```

This float can be used with other floats, you’ll need to cast (we’ll talk about this soon) the datatype to make it work with a normal integer:

```
float new_one = 4.52 / my_float;
```

### Defining a Boolean

Finally, for variables, we can try our luck creating boolean values.

Inside of computing, booleans are the most fundamental datatype. They can only be set to a true or false value, equivalent to a 1 or a 0 inside of low-level programming — these are called bits which you might have heard of before. To define this datatype, we use the same method as we did for integers:

```
bool am_i_cool = true;
```

# Converting Datatypes

As we learned in the previous section, datatypes are the things that tell C# what the data actually is. You can use these outsides of variables in other places which we’ll see soon. For now, let’s look at an example of changing a datatype to a different datatype — in this case a float, a number with decimals, to an int, the one which we saw before:

```
float y = 3.1415;
int z = (int)y;
```

So, as you’ve probably been able to guess, we’re first setting the value of this new y variable to 3.1415, the start of Pi. Something has changed here though, and that is the datatype defined for the variable. This makes y into a number which allows decimals on the end of it, in comparison to int values which do not.

Next up, we create a new variable yet again and set it as an integer. For the data value, we convert this previous y value (referenced by using the y key/name itself). To convert, we put the value we want to convert to in brackets before the name of the thing we want to convert as you can see. 

Sadly, converting this value into a value without any decimal places will cut anything off, removing data which may be needed. This will change the value from 3.1415 to just 3.

# Selection

Now that we’ve got all the basics of variables and datatypes out of the way, we can now look at Selection. This name is confusing for what this section describes, as what we’re doing is defining what’s called an if statement.

These statements create a branch inside of the program, which it will go to if a question is processed as true. To understand this, let’s see an example:

```
if(z > x) {
    // this might run!
}
```

The content inside of the wiggly brackets shown above will execute if z is greater than x, i.e. z > x. Anything inside of the normal brackets for this if statement is therefore part of the question. So what happens if this question comes out as false and the content we defined doesn’t run?

Well, if we put an extra else if statement tagged onto the end, we can define a second question which C# will ask and run a second piece of content. This looks like the following:

```
if (z > x { /* this might run! */ }
else if (true) { /* this might run if the other doesn’t! */ }
```

Please note that the first line is the same as the previous example, it’s just formatted differently as you can use both //-style comments and /**/-style comments, depending on what you’re trying to write and convey. If the first if question does execute, the second else if question won’t even be tested, it will just skip everything else in the statement.

The third and final part of an if statement is the else block. This part is quite simple as it doesn’t have a question to evaluate to see if it needs to run; instead only running if all the other questions evaluate to false; rendering nothing else available to run. For the completed example, this looks like the following:

```
if (z > x { /* this might run! */ }
else if (true) { /* this might run if the other doesn’t! */ }
else { /* this will run if nothing does! */ }
```

# Iteration

## Introduction

Another basic construct of software development is iteration. According to techopedia, iteration is defined as:

> Iteration, in the context of computer programming, is a process wherein a set of instructions or structures are repeated in a sequence a specified number of times or until a condition is met. When the first set of instructions is executed again, it is called an iteration. When a sequence of instructions is executed in a repeated manner, it is called a loop.

Basically, iteration is when a piece of code repeats and a loop is the place in which this repeats inside of the code.

## For Loops

Let’s see an example of this happening; we will define a new variable which will be created and then destroyed once the loop repeats. You can think of this like Groundhog Day works; everything inside of a loop is the same, but could be changed by external values changing inside or outside of the loop, causing the path to change via Selection which we’ve went over:

```
for(int i = 0; i < 10; i++) {
    string y = “hello there!”;
}
```

So this is a type of loop called a for loop, which:

1. Creates a variable to use inside of the loop
2. Checks a condition to see if the loop should still run
3. Allows you to add an expression to run at the end of the loop

These three conditions inside of the brackets combined allows us to do something like shown inside of the example; to create a new variable and tell it to only run for 10 iterations by making sure that it’s less, adding to it once each repetition of the loop finishes.

## Printing

To give better examples, we’re going to start to use a special item which allows us to output values from the code, this is called a print function. The function is the way we call it, and its a print function because it lets us output whatever we’d like because of the way this specific function is defined. An empty print functions look like the following for C#:

```
Console.WriteLine();
```

Inside of the brackets shown, we can add something to output, or print, so that we as developers can see that something works. This will be useful in the next section so we can see exactly what’s happening as a more in-depth example.

If you’d like, you can try putting variable names inside of these brackets for the examples we have gone over so far; just make sure to put this print function below where you’ve defined everything!

## While Loops

While loops are actually a bit simpler than the For Loops we went over before. All that these do is check if a condition is true or false. If it is true, then it runs the content inside of the loop. Once the loop finishes, it checks again and repeats, etc. This is very similar to if statements and are basically just one of them, but repeating. Here’s an example, using the print function as well:

```
while(true) {
    Console.WriteLine(“it’s running!”);
}
```

As true is always equal to the true output we need to run a while loop (true == true), this loop will actually run forever; unless the computer shuts down or the program is stopped. Try running this, it should output something like this in a black box which has popped up:

```
it’s running!
it’s running!
it’s running!
it’s running!
it’s running!
```

# Encapsulation

## Functions

Check back to the Printing section we saw before and note how the style of this looks — a set of characters before some brackets where you can define something in, which runs something more than just what you put into it.

This is a form of Encapsulation. A way to re-use code and expand code into more and more code without having to write it all in one part of your program. Instead of writing:

```
int x = 10;
int y = 20;
if(x < y && x == 10) {
    Console.WriteLine("it works!")
}
```

You can instead define a function for yourself and encapsulate the code, which you can reuse anywhere inside of your program at any time you want:

```
myFunction(10);
void myFunction(x) {
    int y = 20;
    if (x < y && x == 10) {
        Console.WriteLine("it works!");
    }
}
```

These two examples do exactly the same, but the latter allows you to put in whatever value for x you’d like whilst just reusing y, allowing you to easily customise the x value and print if it works while not having to copy and paste the whole if statement and the value for the aforementioned y variable.

## Namespaces

Inside of C#, there is also a component of writing code called name-spacing. This is a way to categorise code, allowing you to place different bits of code into different bits inside of the same file, or collection of different files containing your code.
This allows you to access places you otherwise wouldn’t be able to easily access; like if you had a lot of code in many files generally relating to cars, you’d have to do something like this to access a function for a Mercedes car:

```
cars/car_merc.cs.myFunction();
```

If you instead categorise everything inside of your cars/ directory which contains many files about cars, you could do this valid C# code to access the same Mercedes car function:

```
Car.Mercedes.myFunction();
```

You might notice that this looks quite similar to how our print function looked like, and that’s because the Console in the Console.WriteLine is actually an example of name-spacing. To make a new namespace to categorise these cars into, we can define it like:

```
namespace SampleNamespace
{
    class SampleClass {
        public void SampleMethod() {
            Console.WriteLine(
                "SampleMethod inside SampleNamespace");
        }
    }
}
```

Here were defining a new namespace called SampleNamespace with a class (don’t worry about this for now) called SampleClass, with a function inside of it — the function we are categorising inside of these groups for ease of use.

## Procedural

Procedural programming is an alternative to object orientated programming inside of the software development sphere. Both are abstract methodologies, themselves deriving from something called Imperative programming.

The difference between the two is that object orientated programming groups blocks of logic to discrete objects, which interact with other objects by taking them in as inputs, or returning them as outputs; or deriving themselves entirely from such objects. Instead of using objects to represent groups of logic, procedural programming takes a simpler approach: It represents important tasks as only namespaces and functions.

By doing this, it makes the categorisation of code simpler but it can have an impact with the quality and readability of the code, as you lose a way to group the code concisely in many cases. Because of this, both methodologies are used in conjunction as they derive from the same parent methodology and so naturally have a lot in common.

<!-- TODO: more -->
