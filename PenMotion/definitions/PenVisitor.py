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

    # Override the visitChildren method to set the self.arg_dict attribute
    def visitChildren(self, node):
        result = self.defaultResult()
        if node is None:
            return result
        for child in node.getChildren():
            childResult = child.accept(self)
            result = self.aggregateResult(result, childResult)
        return result

    # Visit a parse tree produced by PenMotionParser#program.
    def visitProgram(self, ctx:PenMotionParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#line.
    def visitLine(self, ctx:PenMotionParser.LineContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PenMotionParser#save.
    def visitSave(self, ctx: PenMotionParser.SaveContext):
        filename = ctx.getChild(1).getText()  # get the filename
        cv = self.pen.getscreen().getcanvas()  # get the turtle's canvas
        if self.arg_dict is not None and filename in self.arg_dict.keys():
            filename = self.arg_dict[filename]

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
            self.visitChildren(block)  # visit the command with the argument values

    # Visit a parse tree produced by PenMotionParser#function_args.
    def visitFunction_args(self, ctx:PenMotionParser.Function_argsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#function_block.
    def visitFunction_block(self, ctx:PenMotionParser.Function_blockContext,arg_dict=None):
        
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#function_line.
    def visitFunction_line(self, ctx:PenMotionParser.Function_lineContext,arg_dict=None):
        
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PenMotionParser#function_command.
    def visitFunction_command(self, ctx: PenMotionParser.Function_commandContext):
        if ctx.set_():
            return self.visitSet(ctx.set_())
        elif ctx.pagesize():
            return self.visitPagesize(ctx.pagesize(),)
        elif ctx.move():
            return self.visitMove(ctx.move())
        elif ctx.call():
            return self.visitCall(ctx.call())
        elif ctx.save():
            return self.visitSave(ctx.save())
        elif ctx.repeat():
            return self.visitRepeat(ctx.repeat())
        elif ctx.clear():
            return self.visitClear(ctx.clear())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#pagesize.
    def visitPagesize(self, ctx:PenMotionParser.PagesizeContext):
        width = ctx.getChild(1).getText()  # get the width
        height = ctx.getChild(2).getText()  # get the height
        if self.arg_dict is not None and width in self.arg_dict.keys() and height in self.arg_dict.keys():  # if color is a function argument
            width = self.arg_dict[width]
            height = self.arg_dict[height]
        self.pen.getscreen().screensize(int(width), int(height))
        self.pen.getscreen().setworldcoordinates(0, 0, int(width), int(height))
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PenMotionParser#set.
    def visitSet(self, ctx: PenMotionParser.SetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PenMotionParser#set_fun.
    def visitSet_fun(self, ctx: PenMotionParser.Set_funContext):
        match ctx.getChild(0).getText():
            case 'penposition':
                x = ctx.getChild(1).getText() # get the x-coordinate
                y = ctx.getChild(2).getText()  # get the y-coordinate
                self.pen.penup()
                if self.arg_dict is not None and x in self.arg_dict.keys() and y in self.arg_dict.keys():  # if color is a function argument
                    x = self.arg_dict[x]
                    y = self.arg_dict[y]
                self.pen.goto(int(x), int(y))  # set the pen position
                self.pen.pendown()
            case 'pensize':
                size = ctx.getChild(1).getText()  # get the pen size
                if self.arg_dict is not None and size in self.arg_dict.keys():  # if color is a function argument
                    size = self.arg_dict[size]
                self.pen.pensize(int(size))  # set the pen size
            case 'pencolor':
                color = ctx.getChild(1).getText() # get the pen color
                if self.arg_dict is not None and color in self.arg_dict.keys():  # if color is a function argument
                    color = self.arg_dict[color]  # resolve the function argument
                self.pen.pencolor(color.strip('"')) # set the pen color
            case 'penshape':
                shape = ctx.getChild(1).getText() # get the pen shape
                if self.arg_dict is not None and shape in self.arg_dict.keys():  # if color is a function argument
                    shape = self.arg_dict[shape]  # resolve the function argument
                self.pen.shape(shape.strip('"'))  # set the pen shape
            case 'penup':
                self.pen.penup()  # lift the pen up
            case 'pendown':
                self.pen.pendown()  # put the pen down
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PenMotionParser#move.
    def visitMove(self, ctx: PenMotionParser.MoveContext):
        x = ctx.getChild(1).getText() # get the x-coordinate
        y = ctx.getChild(2).getText() # get the y-coordinate

        if x in self.arg_dict.keys() or x[1:] in self.arg_dict.keys():
            if x[0] == '-':
                x = -1 * int(self.arg_dict[x[1:]])
            else: x = self.arg_dict[x]

        if y in self.arg_dict.keys() or y[1:] in self.arg_dict.keys():
            if y[0] == '-':
                y = -1 * int(self.arg_dict[y[1:]])
            else:
                y = self.arg_dict[y]
        current_x = self.pen.xcor()  # get the current x-coordinate
        current_y = self.pen.ycor()  # get the current y-coordinate
        self.pen.setpos(current_x + int(x), current_y + int(y))  # move the pen by y units vertically
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PenMotionParser#repeat.
    def visitRepeat(self, ctx: PenMotionParser.RepeatContext):
        repetitions = ctx.getChild(1).getText() # get the number of repetitions
        if repetitions in self.arg_dict.keys():
            repetitions = self.arg_dict[repetitions]

        if repetitions[1:] in self.arg_dict.keys():
            repetitions = -1 * int(self.arg_dict[repetitions[1:]])

        command = ctx.function_command()  # get the command to be repeated
        for _ in range(int(repetitions)):  # repeat the command the specified number of times
            self.visitChildren(command)


    # Visit a parse tree produced by PenMotionParser#clear.
    def visitClear(self, ctx:PenMotionParser.ClearContext):
        self.pen.clear()
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
