
parser grammar evaql_parser;

options {
	tokenVocab=evaql_lexer;
}

// Top Level Description

root
    : sqlStatements? MINUSMINUS? EOF
    ;

sqlStatements
    : (sqlStatement MINUSMINUS? SEMI | emptyStatement)*
    (sqlStatement (MINUSMINUS? SEMI)? | emptyStatement)
    ;

sqlStatement
    : ddlStatement | dmlStatement | utilityStatement
    ;

emptyStatement
    : SEMI
    ;

ddlStatement
    : createDatabase | createTable | createIndex | createUdf
    | dropDatabase | dropTable | dropIndex
    ;

dmlStatement
    : selectStatement | insertStatement | updateStatement
    | deleteStatement | loadStatement | uploadStatement
    ;

utilityStatement
    : simpleDescribeStatement | helpStatement
    ;

// Data Definition Language

//    Create statements

createDatabase
    : CREATE DATABASE
      ifNotExists? uid
    ;

createIndex
    : CREATE
      INDEX uid indexType?
      ON tableName indexColumnNames
    ;

createTable
    : CREATE TABLE
      ifNotExists?
      tableName createDefinitions                                  #columnCreateTable
    ;

// Create UDFs
createUdf
    : CREATE UDF
      ifNotExists?
      udfName
      INPUT  createDefinitions
      OUTPUT createDefinitions
      TYPE   udfType
      IMPL   udfImpl
    ;


// details
udfName
    : uid
    ;

udfType
    : uid
    ;

udfImpl
    : stringLiteral
    ;

indexType
    : USING (BTREE | HASH)
    ;

createDefinitions
    : '(' createDefinition (',' createDefinition)* ')'
    ;

createDefinition
    : uid columnDefinition                                          #columnDeclaration
    | indexColumnDefinition                                         #indexDeclaration
    ;

columnDefinition
    : dataType columnConstraint*
    ;

columnConstraint
    : nullNotnull                                                   #nullColumnConstraint
    | DEFAULT defaultValue                                          #defaultColumnConstraint
    | PRIMARY? KEY                                                  #primaryKeyColumnConstraint
    | UNIQUE KEY?                                                   #uniqueKeyColumnConstraint
    ;

indexColumnDefinition
    : INDEX uid? indexType?
      indexColumnNames                                              #simpleIndexDeclaration
    ;

//    Drop statements

dropDatabase
    : DROP DATABASE ifExists? uid
    ;

dropIndex
    : DROP INDEX
      uid ON tableName
    ;

dropTable
    : DROP TABLE ifExists?
      tables
    ;

// Data Manipulation Language

//    Primary DML Statements

deleteStatement
    : singleDeleteStatement
    ;

insertStatement
    : INSERT
      INTO? tableName
      (
        ('(' columns=uidList ')')? insertStatementValue
      )
    ;

selectStatement
    : querySpecification                                            #simpleSelect
    | left=selectStatement UNION unionAll=ALL? right=selectStatement   #unionSelect
    ;

updateStatement
    : singleUpdateStatement
    ;

loadStatement
    : LOAD DATA
      INFILE fileName
      INTO tableName
    ;

uploadStatement
    : UPLOAD
      PATH fileName
      BLOB videoBlob
    ;

fileName
    : stringLiteral
    ;

videoBlob
    : stringLiteral
    ;

// details

insertStatementValue
    : selectStatement
    | insertFormat=(VALUES | VALUE)
      '(' expressionsWithDefaults ')'
        (',' '(' expressionsWithDefaults ')')*
    ;

updatedElement
    : fullColumnName '=' (expression | DEFAULT)
    ;


//    Detailed DML Statements

singleDeleteStatement
    : DELETE
    FROM tableName
      (WHERE expression)?
      orderByClause? (LIMIT decimalLiteral)?
    ;

singleUpdateStatement
    : UPDATE tableName (AS? uid)?
      SET updatedElement (',' updatedElement)*
      (WHERE expression)? orderByClause? limitClause?
    ;

// details

orderByClause
    : ORDER BY orderByExpression (',' orderByExpression)*
    ;

orderByExpression
    : expression order=(ASC | DESC)?
    ;

tableSources
    : tableSource (',' tableSource)*
    ;

tableSource
    : tableSourceItemWithSample joinPart*                #tableSourceBase
    ;

tableSourceItemWithSample
    : tableSourceItem sampleClause?
    ;

tableSourceItem
    : tableName                                  #atomTableItem
    | (
      selectStatement |
      LR_BRACKET selectStatement RR_BRACKET
      )                                                            #subqueryTableItem
    ;

sampleClause
    : SAMPLE decimalLiteral
    ;


joinPart
    : JOIN tableSourceItemWithSample
      (
        ON expression
        | USING '(' uidList ')'
      )?                                                            #innerJoin
    ;

//    Select Statement's Details

queryExpression
    : '(' querySpecification ')'
    | '(' queryExpression ')'
    ;

querySpecification
    : SELECT selectElements
      fromClause orderByClause? limitClause?
      errorBoundsExpression? confidenceLevelExpression?
    ;

// details

selectElements
    : (star='*' | selectElement ) (',' selectElement)*
    ;

selectElement
    : fullId '.' '*'                                                #selectStarElement
    | fullColumnName (AS? uid)?                                     #selectColumnElement
    | functionCall (AS? uid)?                                       #selectFunctionElement
    | (LOCAL_ID VAR_ASSIGN)? expression (AS? uid)?                  #selectExpressionElement
    ;

fromClause
    : FROM tableSources
      (WHERE whereExpr=expression)?
      (
        GROUP BY
        groupByItem (',' groupByItem)*
      )?
      (HAVING havingExpr=expression)?
    ;

groupByItem
    : expression order=(ASC | DESC)?
    ;

limitClause
    : LIMIT
    (
      (offset=decimalLiteral ',')? limit=decimalLiteral
      | limit=decimalLiteral OFFSET offset=decimalLiteral
    )
    ;

errorBoundsExpression
	: ERROR_BOUNDS REAL_LITERAL
	;

confidenceLevelExpression
	: CONFIDENCE_LEVEL REAL_LITERAL
	;

//    Other administrative statements

shutdownStatement
    : SHUTDOWN
    ;

// Utility Statements


simpleDescribeStatement
    : DESCRIBE tableName
    ;

helpStatement
    : HELP STRING_LITERAL
    ;

// Common Clauses

//    DB Objects

fullId
    : uid (DOT_ID | '.' uid)?
    ;

tableName
    : fullId
    ;

fullColumnName
    : uid (dottedId dottedId? )?
    ;

indexColumnName
    : uid ('(' decimalLiteral ')')? sortType=(ASC | DESC)?
    ;

userName
    : STRING_USER_NAME | ID;

uuidSet
    : decimalLiteral '-' decimalLiteral '-' decimalLiteral
      '-' decimalLiteral '-' decimalLiteral
      (':' decimalLiteral '-' decimalLiteral)+
    ;

uid
    : simpleId
    //| DOUBLE_QUOTE_ID
    | REVERSE_QUOTE_ID
    ;

simpleId
    : ID
    ;

dottedId
    : DOT_ID
    | '.' uid
    ;


//    Literals

decimalLiteral
    : DECIMAL_LITERAL | ZERO_DECIMAL | ONE_DECIMAL | TWO_DECIMAL | ANYDIM
    ;

stringLiteral
    : STRING_LITERAL
    ;

booleanLiteral
    : TRUE | FALSE;

nullNotnull
    : NOT? (NULL_LITERAL | NULL_SPEC_LITERAL)
    ;

arrayLiteral
    : LR_SQ_BRACKET  constant (',' constant)* RR_SQ_BRACKET
    | LR_SQ_BRACKET RR_SQ_BRACKET
    ;

constant
    : stringLiteral | decimalLiteral
    | '-' decimalLiteral
    | booleanLiteral
    | REAL_LITERAL
    | NOT? nullLiteral=(NULL_LITERAL | NULL_SPEC_LITERAL)
    | arrayLiteral
    ;


//    Data Types

arrayType
    : INT8 | UINT8 | INT16 | INT32 | INT64
    | UNICODE | BOOL
    | FLOAT32 | FLOAT64 | DECIMAL
    | STR | DATETIME | ANYTYPE
    ;

dataType
    : BOOLEAN                                         #simpleDataType
    | TEXT lengthOneDimension?                        #dimensionDataType
    | INTEGER UNSIGNED?                               #integerDataType
    | FLOAT lengthTwoDimension? UNSIGNED?             #dimensionDataType
    | NDARRAY arrayType? lengthDimensionList?         #arrayDataType
    | ANYTYPE                                         #anyDataType
    ;

lengthOneDimension
    : '(' decimalLiteral ')'
    ;

lengthTwoDimension
    : '(' decimalLiteral ',' decimalLiteral ')'
    ;

lengthDimensionList
    : '(' ( decimalLiteral  ',')* decimalLiteral ')'
    ;

//    Common Lists

uidList
    : uid (',' uid)*
    ;

tables
    : tableName (',' tableName)*
    ;

indexColumnNames
    : '(' indexColumnName (',' indexColumnName)* ')'
    ;

expressions
    : expression (',' expression)*
    ;

expressionsWithDefaults
    : expressionOrDefault (',' expressionOrDefault)*
    ;


//    Common Expressions

defaultValue
    : NULL_LITERAL
    | constant
    ;

expressionOrDefault
    : expression | DEFAULT
    ;

ifExists
    : IF EXISTS;

ifNotExists
    : IF NOT EXISTS;


//    Functions

functionCall
    : udfFunction                                              #udfFunctionCall
    | aggregateWindowedFunction                                #aggregateFunctionCall
    ;

udfFunction
    : simpleId '(' functionArgs ')' dottedId?
    ;


aggregateWindowedFunction
    : (AVG | MAX | MIN | SUM)
      '(' aggregator=(ALL | DISTINCT)? functionArg ')'
    | COUNT '(' (starArg='*' | aggregator=ALL? functionArg) ')'
    ;

functionArgs
    : (constant | fullColumnName | functionCall | expression)
    (
      ','
      (constant | fullColumnName | functionCall | expression)
    )*
    ;

functionArg
    : constant | fullColumnName | functionCall | expression
    ;


//    Expressions, predicates

// Simplified approach for expression
expression
    : notOperator=(NOT | '!') expression                            #notExpression
    | expression logicalOperator expression                         #logicalExpression
    | predicate IS NOT? testValue=(TRUE | FALSE | UNKNOWN)          #isExpression
    | predicate                                                     #predicateExpression
    ;

predicate
    : predicate NOT? IN '(' (selectStatement | expressions) ')'     #inPredicate
    | predicate IS nullNotnull                                      #isNullPredicate
    | left=predicate comparisonOperator right=predicate             #binaryComparisonPredicate
    | predicate comparisonOperator
      quantifier=(ALL | ANY | SOME) '(' selectStatement ')'         #subqueryComparisonPredicate
    | predicate NOT? LIKE predicate (STRING_LITERAL)?               #likePredicate
    | (LOCAL_ID VAR_ASSIGN)? expressionAtom                         #expressionAtomPredicate
    ;


// Add in ASTVisitor nullNotnull in constant
expressionAtom
    : constant                                                      #constantExpressionAtom
    | fullColumnName                                                #fullColumnNameExpressionAtom
    | functionCall                                                  #functionCallExpressionAtom
    | unaryOperator expressionAtom                                  #unaryExpressionAtom
    | '(' expression (',' expression)* ')'                          #nestedExpressionAtom
    | '(' selectStatement ')'                                       #subqueryExpessionAtom
    | left=expressionAtom bitOperator right=expressionAtom          #bitExpressionAtom
    | left=expressionAtom mathOperator right=expressionAtom         #mathExpressionAtom
    ;

unaryOperator
    : '!' | '~' | '+' | '-' | NOT
    ;

comparisonOperator
    : '=' | '>' | '<' | '<' '=' | '>' '='
    | '<' '>' | '!' '=' | '<' '=' '>'
    | '@' '>' | '<' '@'
    ;

logicalOperator
    : AND | '&' '&' | XOR | OR | '|' '|'
    ;

bitOperator
    : '<' '<' | '>' '>' | '&' | '^' | '|'
    ;

mathOperator
    : '*' | '/' | '%' | DIV | MOD | '+' | '-' | '--'
    ;
