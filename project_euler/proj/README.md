# Project Euler Solutions

A Clojure library designed to solve Project Euler problems.

## Usage

To run a specific problem solution:

```bash
lein run <problem-number>
```

For example:

```bash
lein run 3  # Solves Project Euler problem 3
```

To list all available problems:

```bash
lein run
```

## Available Problems

Currently implemented problems:
- Problem 3
- Problem 4
- Problem 7
- Problem 9
- Problem 10
- Problem 12
- Problem 15
- Problem 16
- Problem 26
- Problem 28
- Problem 95
- Problem 361
- Problem 879

## Development

To add a new problem solution:
1. Create a new namespace under `src/proj/p<number>/core.clj`
2. Implement the `solve` function in that namespace
3. Add the namespace to the imports in `src/proj/core.clj`
4. Add the problem number to the `solve-problem` function in `src/proj/core.clj`

## License

Copyright © 2024 FIXME

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

This Source Code may also be made available under the following Secondary
Licenses when the conditions for such availability set forth in the Eclipse
Public License, v. 2.0 are satisfied: GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or (at your
option) any later version, with the GNU Classpath Exception which is available
at https://www.gnu.org/software/classpath/license.html.
