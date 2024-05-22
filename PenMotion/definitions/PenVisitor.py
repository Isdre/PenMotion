from PenMotion.definitions.antlr.PenMotionParser import PenMotionParser
from antlr.PenMotionVisitor import PenMotionVisitor

from turtle import Turtle

class PenVisitor(PenMotionVisitor):
    def __init__(self,):
        self.pen = Turtle()
        self.pen.hideturtle()

    # Visit a parse tree produced by PenMotionParser#program.
    def visitProgram(self, ctx:PenMotionParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#line.
    def visitLine(self, ctx:PenMotionParser.LineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#command.
    def visitCommand(self, ctx:PenMotionParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#save.
    def visitSave(self, ctx:PenMotionParser.SaveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#function.
    def visitFunction(self, ctx:PenMotionParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#function_start.
    def visitFunction_start(self, ctx:PenMotionParser.Function_startContext):
        return self.visitChildren(ctx)


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
    def visitFunction_command(self, ctx:PenMotionParser.Function_commandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#function_end.
    def visitFunction_end(self, ctx:PenMotionParser.Function_endContext):
        return


    # Visit a parse tree produced by PenMotionParser#pagesize.
    def visitPagesize(self, ctx:PenMotionParser.PagesizeContext):

        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#set.
    def visitSet(self, ctx:PenMotionParser.SetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#home.
    def visitHome(self, ctx:PenMotionParser.HomeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#set_fun.
    def visitSet_fun(self, ctx:PenMotionParser.Set_funContext):
        return

    # Visit a parse tree produced by PenMotionParser#move.
    def visitMove(self, ctx:PenMotionParser.MoveContext):
        self.pen.right(ctx.getChild(0))
        self.pen.forward(ctx.getChild(1))

    # Visit a parse tree produced by PenMotionParser#repeat.
    def visitRepeat(self, ctx:PenMotionParser.RepeatContext):
        for _ in range(ctx.getChild(0)):
            self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#clear.
    def visitClear(self, ctx:PenMotionParser.ClearContext):
        self.pen.clear()


    # Visit a parse tree produced by PenMotionParser#call.
    def visitCall(self, ctx:PenMotionParser.CallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#call_arg.
    def visitCall_arg(self, ctx:PenMotionParser.Call_argContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PenMotionParser#comment.
    def visitComment(self, ctx:PenMotionParser.CommentContext):
        return self.visitChildren(ctx)