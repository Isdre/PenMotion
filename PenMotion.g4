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
    : 'save' string
    ;

function
    : function_start function_block
    ;

pagesize
    : 'pagesize' POSITIVE_NUMBER POSITIVE_NUMBER
    ;

set
    : 'set' set_fun
    ;

set_fun
    : 'penposition' POSITIVE_NUMBER POSITIVE_NUMBER
    | 'pensize' POSITIVE_NUMBER
    | 'penshape' string
    | 'penup'
    | 'pencolor' string
    | 'pendown'
    ;

move
    : 'move' INT INT
    ;

call
    : 'call' ID call_arg*
    ;

function_start
    : 'funcS' ID function_args EOL
    ;

function_args
    : ID*
    ;

function_block
    : (function_line? EOL)+ function_line? EOL function_end
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

call_arg
    : ID
    | ID_REVERSE
    | INT
    | string
    ;

comment
    : COMMENT
    ;

ID_REVERSE
    : '-' ID
    ;

ID
    : '_'?[a-zA-Z][a-zA-Z0-9_\-]*
    ;

string
    : '"' STRING '"'
    ;

STRING
    : (~('"' | '#'))*
    ;

INT
    : '-'? POSITIVE_NUMBER
    ;

POSITIVE_NUMBER
    : [0-9]+
    ;

COMMENT
    : '#' ~ [\r\n]*
    ;

EOL
    : [\r\n]+
    ;


WS
    : [ \t\r\n]+ -> skip
    ;
