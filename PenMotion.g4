grammar PenMotion;

program
    : (line? EOL+)+ line? EOF
    ;

line
    : command comment?
    | comment
    ;

command
    : pagesize
    | function
    | set
    | move
    | call
    | save
    ;

save
    : 'save' (STRING|ID)
    ;

function
    : function_start function_block
    ;

function_start
    : 'funcS' ID function_args EOL
    ;

function_args
    : ID*
    ;

function_block
    : (function_line? EOL)+ function_end
    ;

function_line
    : function_command comment?
    | comment
    ;

function_command
    : set
    | move
    | call
    | save
    ;

function_end
    : 'funcE'
    ;

pagesize
    : 'pagesize' INT INT
    ;

set
    : 'set' set_fun
    ;

set_fun
    : 'penposition' (INT|ID|ID_REVERSE) (INT|ID|ID_REVERSE)
    | 'pensize' (INT|ID|ID_REVERSE)
    | 'penshape' (STRING|ID)
    | 'pencolor' (STRING|ID)
    | 'penup'
    | 'pendown'
    ;

move
    : 'move' (INT|ID|ID_REVERSE) (INT|ID|ID_REVERSE)
    ;

call
    : 'call' ID call_arg*
    ;

call_arg
    : ID
    | ID_REVERSE
    | INT
    | STRING
    ;

comment
    : COMMENT
    ;

ID_REVERSE
    : '-' ID
    ;

ID
    : '_'? [a-zA-Z] [a-zA-Z0-9_\-]*
    ;

INT
    : '-'? NUMBER
    ;

NUMBER
    : [0-9]+
    ;

STRING
    : '"' (~('"'))* '"'
    ;


COMMENT
    : '#' ~ [\r\n]*
    ;

EOL
    : [\r\n]+
    ;


WS
    : [ \t]+ -> skip
    ;
