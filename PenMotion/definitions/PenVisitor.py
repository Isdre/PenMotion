import pyautogui
import tkinter as tk

from PenMotion.definitions.antlr.PenMotionParser import PenMotionParser
from PenMotion.definitions.antlr.PenMotionVisitor import PenMotionVisitor

import os

from turtle import Turtle

class PenVisitor(PenMotionVisitor):
    def __init__(self,):
        self.pen = Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.getscreen().setworldcoordinates(0, 0, 800, 800)
        self.functions = {}
        self.arg_dict = {}
        self.inFunction = False

    def checkIfIsIdentifier(self, identifier:str) -> bool:
        if identifier in self.arg_dict.keys():
            return self.arg_dict[identifier]
        elif identifier[1:] in self.arg_dict.keys() and identifier[0] == '-':
            return str(-1 * int(self.arg_dict[identifier[1:]]))
        return None
    # Visit a parse tree produced by PenMotionParser#program.
    def visitProgram(self, ctx:PenMotionParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#line.
    def visitLine(self, ctx:PenMotionParser.LineContext):
        self.inFunction = False
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PenMotionParser#save.
    def visitSave(self, ctx: PenMotionParser.SaveContext):
        filename = ctx.getChild(1).getText()  # get the filename
        cv = self.pen.getscreen().getcanvas()  # get the turtle's canvas
        if self.inFunction:
            v = self.checkIfIsIdentifier(filename)
            if v is not None:
                filename = v

        # get the coordinates of the turtle window
        x = cv.winfo_rootx()
        y = cv.winfo_rooty()
        x1 = x + cv.winfo_width()
        y1 = y + cv.winfo_height()

        # take a screenshot of the turtle window
        img = pyautogui.screenshot(region=(x, y, x1 - x, y1 - y))

        # save the screenshot as a PNG file
        img.save(filename.strip('"'))  # replace with '.jpg' for JPG format

    # Visit a parse tree produced by PenMotionParser#function.
    def visitFunction(self, ctx: PenMotionParser.FunctionContext):
        function_name = ctx.identifier().getText()  # get the function name
        function_args_ctx = ctx.function_args()
        function_args = [arg.getText() for arg in function_args_ctx.identifier()] if function_args_ctx else []  # get the function arguments
        block = ctx.function_block() # get the function commands
        self.functions[function_name] = (function_args, block)  # store the function arguments and commands

    # Visit a parse tree produced by PenMotionParser#call.
    def visitCall(self, ctx: PenMotionParser.CallContext):
        function_name = ctx.identifier().getText()  # get the function name
        if function_name in self.functions:  # if the function exists
            function_args, block = self.functions[function_name]  # get the function arguments and commands
            call_args_ctx = ctx.call_arg()  # get the call arguments context
            call_args = [
                arg.getText() if not isinstance(arg, PenMotionParser.IdentifierContext) else self.arg_dict[arg.getText()] for
                arg in call_args_ctx]  # resolve the call arguments
            self.arg_dict = dict(zip(function_args, call_args))  # create a dictionary of argument values
            self.inFunction = True
            self.visitChildren(block)  # visit the command with the argument values

    # Visit a parse tree produced by PenMotionParser#pagesize.
    def visitPagesize(self, ctx:PenMotionParser.PagesizeContext):
        width = ctx.getChild(1).getText()  # get the width
        height = ctx.getChild(2).getText()  # get the height
        if self.inFunction:
            w = self.checkIfIsIdentifier(width)
            h = self.checkIfIsIdentifier(height)
            if w is not None:
                width = w
            if h is not None:
                height = h
        self.pen.getscreen().screensize(int(width), int(height))
        self.pen.getscreen().setworldcoordinates(0, 0, int(width), int(height))

    # Visit a parse tree produced by PenMotionParser#set.
    def visitSet(self, ctx: PenMotionParser.SetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PenMotionParser#set_fun.
    def visitSet_fun(self, ctx: PenMotionParser.Set_funContext):
        match ctx.getChild(0).getText():
            case 'penposition':
                x = ctx.getChild(1).getText() # get the x-coordinate
                y = ctx.getChild(2).getText()  # get the y-coordinate
                if self.inFunction:
                    v = self.checkIfIsIdentifier(x)
                    if v is not None:
                        x = v
                    v = self.checkIfIsIdentifier(y)
                    if v is not None:
                        y = v
                self.pen.penup()
                self.pen.goto(int(x), int(y))  # set the pen position
                self.pen.pendown()
            case 'pensize':
                size = ctx.getChild(1).getText()  # get the pen size
                if self.inFunction:
                    v = self.checkIfIsIdentifier(size)
                    if v is not None:
                        size = v
                self.pen.pensize(int(size))  # set the pen size
            case 'pencolor':
                color = ctx.getChild(1).getText() # get the pen color
                if self.inFunction:
                    v = self.checkIfIsIdentifier(color)
                    if v is not None:
                        color = v
                self.pen.pencolor(color.strip('"')) # set the pen color
            case 'penshape':
                shape = ctx.getChild(1).getText() # get the pen shape
                if self.inFunction:
                    v = self.checkIfIsIdentifier(shape)
                    if v is not None:
                        shape = v
                self.pen.shape(shape.strip('"'))  # set the pen shape
            case 'penup':
                self.pen.penup()  # lift the pen up
            case 'pendown':
                self.pen.pendown()  # put the pen down

    # Visit a parse tree produced by PenMotionParser#move.
    def visitMove(self, ctx: PenMotionParser.MoveContext):
        x = ctx.getChild(1).getText() # get the x-coordinate
        y = ctx.getChild(2).getText() # get the y-coordinate

        if self.inFunction:
            v = self.checkIfIsIdentifier(x)
            if v is not None:
                x = v
            v = self.checkIfIsIdentifier(y)
            if v is not None:
                y = v

        current_x = self.pen.xcor()  # get the current x-coordinate
        current_y = self.pen.ycor()  # get the current y-coordinate
        self.pen.setpos(current_x + int(x), current_y + int(y))  # move the pen by y units vertically

    # Visit a parse tree produced by PenMotionParser#repeat.
    def visitRepeat(self, ctx: PenMotionParser.RepeatContext):
        repetitions = ctx.getChild(1).getText() # get the number of repetitions

        if self.inFunction:
            v = self.checkIfIsIdentifier(repetitions)
            if v is not None:
                repetitions = v

        command = ctx.function_command()  # get the command to be repeated
        for _ in range(int(repetitions)):  # repeat the command the specified number of times
            self.visitChildren(command)


    # Visit a parse tree produced by PenMotionParser#clear.
    def visitClear(self, ctx:PenMotionParser.ClearContext):
        self.pen.clear()


    # Visit a parse tree produced by PenMotionParser#function_args.
    def visitFunction_args(self, ctx:PenMotionParser.Function_argsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#function_block.
    def visitFunction_block(self, ctx:PenMotionParser.Function_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#function_line.
    def visitFunction_line(self, ctx:PenMotionParser.Function_lineContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PenMotionParser#function_command.
    def visitFunction_command(self, ctx: PenMotionParser.Function_commandContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PenMotionParser#call_arg.
    def visitCall_arg(self, ctx:PenMotionParser.Call_argContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#comment.
    def visitComment(self, ctx:PenMotionParser.CommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#identifier.
    def visitIdentifier(self, ctx:PenMotionParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#int.
    def visitInt(self, ctx:PenMotionParser.IntContext):
        return self.visitChildren(ctx)
