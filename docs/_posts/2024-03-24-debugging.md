---
title: Debugging
---

I've just finished my implementation of problem 4 from chapter 2.1 in The Art of Computer Programming.  I learned a few things about using the MDK while doing this, including using the debugger and invoking Scheme inside the interactive VM.  I've reorganized my approach to the script slightly, separating the scenarios from the test runner so that I can load the scenarios in the VM while still being able to run them as a series from the test runner.  I've also included the test output this time for easier review later if I should ever come back to this.

Also I've refined my test runner a bit, with a super simple pattern where I have a scenario function that sets up data and returns a lambda to validate the results separately after running a solution program.  I think this should be a time saver.  I've updated the template files accordingly.

ADDENDUM: After reviewing the test outputs I realized I had not actually properly implemented the solution!  I've amended the solution.  Going forward I should probably not be counting on manual verification, as I am apparently just terrible at doing that reliably.