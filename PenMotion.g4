grammar PenMotion;

program
    : (line? EOL+)+ line? EOF
    ;

line
    : (function|function_command) comment?
    | comment
    ;

save
    : 'save' (STRING|identifier)
    ;

function
    : 'funcS' identifier function_args? EOL function_block 'funcE'
    ;

function_args
    : (identifier', ')* identifier
    ;

function_block
    : (function_line? EOL)+
    ;

function_line
    : function_command comment?
    | comment
    ;

function_command
    : set
    | pagesize
    | move
    | call
    | save
    | repeat
    | clear
    ;

pagesize
    : 'pagesize' (int|identifier) (int|identifier)
    ;

set
    : 'set' set_fun
    ;

set_fun
    : 'penposition' (int|identifier) (int|identifier)
    | 'pensize' (int|identifier)
    | 'penshape' (STRING|identifier)
    | 'pencolor' (STRING|identifier)
    | 'penup'
    | 'pendown'
    ;

move
    : 'move' (int|identifier) (int|identifier)
    ;

repeat
    : 'repeat' (int|identifier) function_command
    ;

clear
    : 'clear'
    ;

call
    : 'call' identifier call_arg*
    ;

call_arg
    : identifier
    | int
    | STRING
    ;

comment
    : COMMENT
    ;



identifier
    : '-'?ID
    ;

ID
    : '_'? [a-zA-Z] [a-zA-Z0-9_\-]*
    ;

int
    : INT
    ;

INT
    : '-'? NUMBER
    ;

NUMBER
    : [0-9]+
    ;

STRING
    : '"'(~('"'))+'"'
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
