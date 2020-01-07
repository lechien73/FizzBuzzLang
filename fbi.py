"""
    FizzBuzzLang Interpreter
    Copyright (C) 2020 Matt Rudge (mrudge@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


class FBSyntaxError(SyntaxError):
    def __init__(self, line, filename="", linenum=1, token="", expected=""):
        error = f"Expected {expected} token but got '{token}'"
        colnum = line.index(token) + 1
        super().__init__(error, (filename, linenum, colnum, line))


class FizzBuzzLang:
    """
    The main class. All methods are private except for run_file
    """
    def __init__(self, *, debug=False):
        self.stack = [0]
        self.sp = 0
        self.stored_sp1 = 0
        self.stored_sp2 = 0
        self.ip = 0
        self.labels = {}
        self.debug = debug

    def _parse_tokens(self, line, file, linenum):
        """Parse a single line into tokens

        The only permitted non-code lines are "//" comments and whitespace
        """
        if line.strip().startswith("//") or not line.strip():
            return 0, 0, []

        tokens = line.split()

        mode = {"FIZZ": 1, "BUZZ": 2, "FIZZBUZZ": 3}.get(tokens[0])
        if not mode:
            raise FBSyntaxError(line, file, linenum, tokens[0], "mode")

        submode = {"FIZZ": 1, "BUZZ": 2, "FIZZBUZZ": 3}.get(tokens[1])
        if not submode:
            raise FBSyntaxError(line, file, linenum, tokens[1], "submode")

        args = tokens[2:]
        for i, arg in enumerate(args):
            is_label = mode == 3 and submode in (1, 2) and i == len(args)-1
            if not is_label and arg not in ("FIZZ", "BUZZ", "FIZZBUZZ"):
                raise FBSyntaxError(line, file, linenum, arg, "argument")

        return mode, submode, args

    def _op_stack(self, submode, args):
        """Execute a Data-space manipulation operation
        """
        if submode == 1:
            if args[0] == "FIZZ":
                self.sp += 1
                if len(self.stack) == self.sp:
                    self.stack.append(0)
            elif args[0] == "BUZZ":
                self.sp = max(self.sp - 1, 0)
            elif args[0] == "FIZZBUZZ":
                self.sp += 1
                if len(self.stack) == self.sp:
                    self.stack.append(self.stack[self.sp-1])
                else:
                    self.stack[self.sp] = self.stack[self.sp-1]

        elif submode == 2:
            locargs = len(args) > 1
            if locargs:
                if args[1] == "FIZZ":
                    stored_loc = self.stored_sp1
                else:
                    stored_loc = self.stored_sp2
            if args[0] == "FIZZ":
                if locargs:
                    self.stack[self.sp] += self.stack[stored_loc]
                else:
                    self.stack[self.sp] += 1
            elif args[0] == "BUZZ":
                if locargs:
                    self.stack[self.sp] -= self.stack[stored_loc]
                else:
                    self.stack[self.sp] -= 1
            elif args[0] == "FIZZBUZZ":
                if self.sp + 1 == len(self.stack):
                    self.stack.append(0)
                if locargs:
                    divisor = self.stack[stored_loc]
                else:
                    divisor = self.stack[self.sp - 1]
                self.stack[self.sp + 1] = self.stack[self.sp] % divisor
                self.sp += 1

        elif submode == 3:
            if args[0] == "FIZZ":
                self.stored_sp1 = self.sp
            elif args[0] == "BUZZ":
                self.stored_sp2 = self.sp
            elif args[0] == "FIZZBUZZ":
                if args[1] == "FIZZ":
                    self.sp = self.stored_sp1
                else:
                    self.sp = self.stored_sp2

    def _op_io(self, submode, args):
        """Execute an Input/Output operation
        """
        stored_loc = self.sp
        locargs = len(args) > 1
        if locargs:
            if args[1] == "FIZZ":
                stored_loc = self.stored_sp1
            else:
                stored_loc = self.stored_sp2
        if submode == 1:
            print(self.stack[stored_loc])
        elif submode == 2:
            print(chr(self.stack[stored_loc]), end="")
        elif submode == 3:
            if locargs and args[0] == "FIZZBUZZ":
                varnum = "".join("0" if fb == "FIZZ" else "1"
                                 for fb in args[1:])
                self.stack[self.sp] = int(varnum, 2)
            else:
                try:
                    self.stack[self.sp] = int(input("> "))
                except ValueError:
                    print("Error: Must be an integer!")

    def _op_flow(self, submode, args):
        """Execute a Flow Control operation
        """
        if submode == 1:
            if args[0] not in self.labels:
                self.labels[args[0]] = self.ip
            self.ip += 1
        elif submode == 2:
            if args[1] not in self.labels:
                print("Error: label does not exist!")
                return
            jump = (args[0] == "FIZZ" and self.stack[self.sp] != 0 or
                    args[0] == "BUZZ" and self.stack[self.sp] == 0 or
                    args[0] == "FIZZBUZZ")
            if jump:
                self.ip = self.labels[args[1]]
            else:
                self.ip += 1

        if submode == 3:
            return 0

    def run_file(self, filename):
        """Parse the FizzBuzzLang script and attempt to execute it
        """

        with open(filename) as prog:
            code = prog.readlines()

        while True:
            if self.ip == len(code):
                print("Error: Expected statement")
                break

            mode, submode, args = self._parse_tokens(
                code[self.ip], filename, self.ip)
            if mode == 1:
                self._op_stack(submode, args)
                self.ip += 1
            elif mode == 2:
                self._op_io(submode, args)
                self.ip += 1
            elif mode == 3:
                bv = self._op_flow(submode, args)
                if bv == 0:
                    break
            else:
                self.ip += 1

            if self.debug:
                print(self.labels, self.stored_sp1, self.stored_sp2)
                print(mode, submode, args)
                print(self.stack, self.sp, self.ip)
