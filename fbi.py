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

class FizzBuzzLang(object):
    """
    The main class. Assume all methods are private except for run_file
    """
    def __init__(self, *, debug=False):
        self.stack = [0]
        self.sp = 0
        self.stored_sp1 = 0
        self.stored_sp2 = 0
        self.ip = 0
        self.labels = {}
        self.debug = debug
   
    def parse_tokens(self, line):
        mode = 0
        submode = 0
        args = []
        line = line.split(" ")
        if line[0] == "FIZZ":
            mode = 1
        elif line[0] == "BUZZ":
            mode = 2
        elif line[0] == "FIZZBUZZ":
            mode = 3
        if line[1].rstrip() == "FIZZ":
            submode = 1
        elif line[1].rstrip() == "BUZZ":
            submode = 2
        elif line[1].rstrip() == "FIZZBUZZ":
            submode = 3
        if len(line) >= 3:
            for arg in line[2:]:
                args.append(arg.rstrip())
        return mode, submode, args
    
    def op_stack(self, submode, args):
        if submode == 1:
            if args[0] == "FIZZ":
                self.sp += 1
                if len(self.stack) == self.sp:
                    self.stack.append(0)
            elif args[0] == "BUZZ":
                self.sp = self.sp - 1 if self.sp > 0 else 0
            elif args[0] == "FIZZBUZZ":
                self.sp += 1
                if len(self.stack) == self.sp:
                    self.stack.append(self.stack[self.sp-1])
                else:
                    self.stack[self.sp] = self.stack[self.sp-1]
        
        elif submode == 2:
            locargs = True if len(args) > 1 else False
            if locargs:
                stored_loc = self.stored_sp1 if args[1] == "FIZZ" else self.stored_sp2
            if args[0] == "FIZZ":
                self.stack[self.sp] = self.stack[self.sp] + self.stack[stored_loc] if locargs else self.stack[self.sp] + 1
            elif args[0] == "BUZZ":
                self.stack[self.sp] = self.stack[self.sp] - self.stack[stored_loc] if locargs else self.stack[self.sp] - 1
            elif args[0] == "FIZZBUZZ":
                if self.sp + 1 == len(self.stack):
                    self.stack.append(0)
                if locargs:
                    self.stack[self.sp + 1] = self.stack[self.sp] % self.stack[stored_loc]
                else:
                    self.stack[self.sp + 1] = 0 if self.stack[self.sp] == 0 else self.stack[self.sp] % self.stack[self.sp - 1]
                self.sp += 1                   

        elif submode == 3:
            if args[0] == "FIZZ":
                self.stored_sp1 = self.sp
            elif args[0] == "BUZZ":
                self.stored_sp2 = self.sp
            elif args[0] == "FIZZBUZZ":
                self.sp = self.stored_sp1 if args[1] == "FIZZ" else self.stored_sp2

        return
    
    def op_io(self, submode):
        if submode == 1:
            print(self.stack[self.sp])
        elif submode == 2:
            print(chr(self.stack[self.sp]), end="")
        elif submode == 3:
            inputnum = 0
            try:
                inputnum = int(input("> "))       
            except ValueError:
                print("Error: Must be an integer!")
                return
            self.stack[self.sp] = inputnum
        
        return

    def op_flow(self, submode, args):
        if submode == 1:
            if args[0] not in self.labels:
                self.labels[args[0]] = self.ip
            self.ip += 1
        elif submode == 2:
            if args[1] not in self.labels:
                print("Error: label does not exist!")
                return
            if (args[0] == "FIZZ" and self.stack[self.sp] != 0) or \
               (args[0] == "BUZZ" and self.stack[self.sp] == 0) or \
               (args[0] == "FIZZBUZZ"):
                self.ip = self.labels[args[1]]
            else:
                self.ip += 1

        if submode == 3:
            return 0
    
    def run_file(self, filename):
        """
        Opens the file, parses the tokens and attempts to
        execute it in FizzBuzzLang
        """

        with open(filename) as prog:
            code = prog.readlines()

        while True:
            if self.ip == len(code):
                print("Error: Expected statement")
                break

            mode, submode, args = self.parse_tokens(code[self.ip])
            if mode == 1:
                self.op_stack(submode, args)
                self.ip += 1
            elif mode == 2:
                self.op_io(submode)
                self.ip += 1
            elif mode == 3:
                bv = self.op_flow(submode, args)
                if bv == 0:
                    break
            else:
                self.ip += 1

            if self.debug:
                print(self.labels, self.stored_sp1, self.stored_sp2)
                print(mode, submode, args)
                print(self.stack, self.sp, self.ip)
