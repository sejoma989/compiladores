from sly import Parser
from analizlex import HOCLexer

class HOCParser(Parser):
    tokens = HOCLexer.tokens
	pass

	'''
	list:	  /* nothing */
		| list '\n'
		| list defn '\n'
		| list asgn '\n'
		| list stmt '\n'
		| list expr '\n'
		| list error '\n'
		;

	'''

	@_('empty')
	def list(self, p):
		pass

	@_('list "\n"')
	def list(self, p):
		pass

	@_('list defn "\n"')
	def list(self, p):
		pass

	@_('list asgn "\n"')
	def list(self, p):
		pass

	@_('list stmt "\n"')
	def list(self, p):
		pass

	@_('list expr "\n"')
	def list(self, p):
		pass

	@_('list error "\n"')
	def list(self, p):
		pass

	'''
	assign: VAR '=' expr
		| VAR ADDEQ expr
		| VAR SUBEQ expr
		| VAR MULEQ expr
		| VAR DIVEQ expr
		| VAR MODEQ expr
	;
	'''

	@_('VAR' '=' expr')
		def assign(self,p):
		pass

	@_('VAR' ADDEQ expr')
		def assign(self,p):
		pass

	@_('VAR' SUBEQ expr')
		def assign(self,p):
		pass

	@_('VAR' MULEQ expr')
		def assign(self,p):
		pass

	@_('VAR' DIVEQ expr')
		def assign(self,p):
		pass

	@_('VAR' MODEQ expr')
		def assign(self,p):
		pass

	'''
	defn: FUNC procname  '(' ')' stmt
		| PROC procname  '(' ')' stmt
	;
	'''

	@_('FUNC procname  '(' formals ')' stmt')
	def defn(self, p):
		pass

	@_('PROC procname  '(' formals ')' stmt')
	def defn(self, p):
		pass

    '''
    stmt: expr
    	| RETURN
    	| RETURN expr
    	| PROCEDURE begin '(' arglist ')'
    	| PRINT prlist
    	| while '(' cond ')' stmt end
    	| for '(' cond ';' cond ';' cond ')' stmt end
    	| if '(' cond ')' stmt end
    	| if '(' cond ')' stmt end ELSE stmt end
        | '{' stmtlist '}'
	;
    '''

    @_('expr')
	def stmt(self, p):
		pass

    @_('RETURN expr')
	def stmt(self, p):
		pass

    @_('PROCEDURE begin '(' arglist ')'')
	def stmt(self, p):
		pass

    @_('PRINT prlist')
	def stmt(self, p):
		pass

    @_('while '(' cond ')' stmt end ')
	def stmt(self, p):
		pass

    @_('for '(' cond ';' cond ';' cond ')' stmt end ')
	def stmt(self, p):
		pass

    @_('if '(' cond ')' stmt end ')
	def stmt(self, p):
		pass

    @_('if '(' cond ')' stmt end ELSE stmt end')
	def stmt(self, p):
		pass

    '''
    @(''{' stmtlist '}'')
	def stmt(self, p):
		pass
    '''


    '''
    while: WHILE
	   ;

    @('WHILE')
    def while(self, p):
        pass


    for: FOR
	   ;

    @('FOR')
    def for(self, p):
        pass


    if:	IF
	   ;

    @('IF')
    def if(self, p):
        pass
    '''

    def begin(self, p):
        pass
	;

    def end(self, p):
        pass
	;

    '''
    stmtlist: /* nothing */
	       | stmtlist '\n'
	       | stmtlist stmt
	;
    '''

    @_('')
    def stmtlist(self, p):
        pass

    @_('(stmtlist '\n')')
    def stmtlist(self, p):
        pass

    @_('stmtlist stmt')
    def stmtlist(self, p):
        pass

    '''
    expr:
    	| VAR
    	| asgn
    	| FUNCTION begin '(' arglist ')'
    	| READ '(' VAR ')'
    	| BLTIN '(' expr ')'
    	| '(' expr ')'
    	| expr '+' expr
    	| expr '-' expr
    	| expr '*' expr
    	| expr '/' expr
    	| expr '%' expr
    	| expr '^' expr
    	| '-' expr
    	| expr GT expr
    	| expr GE expr
    	| expr LT expr
    	| expr LE expr
    	| expr EQ expr
    	| expr NE expr
    	| expr AND expr
    	| expr OR expr
    	| NOT expr
    	| INC VAR
    	| DEC VAR
    	| VAR INC
    	| VAR DEC
	;
    '''

    @_(' ')
    def expr(self, p):
        pass

    @_('VAR')
    def expr(self, p):
        pass

    @_('asgn')
    def expr(self, p):
        pass

    @_(' FUNCTION begin '(' arglist ')' ')
    def expr(self, p):
        pass

    @_(' READ '(' VAR ')' ')
    def expr(self, p):
        pass

    @_(' BLTIN '(' expr ')' ')
    def expr(self, p):
        pass

    @_(' '(' expr ')' ')
    def expr(self, p):
        pass

    @_(' expr '+' expr')
    def expr(self, p):
        pass

    @_(' expr '-' expr ')
    def expr(self, p):
        pass

    @_(' expr '*' expr ')
    def expr(self, p):
        pass

    @_(' expr '/' expr')
    def expr(self, p):
        pass

    @_(' expr '%' expr')
    def expr(self, p):
        pass

    @_(' expr '^' expr')
    def expr(self, p):
        pass

    @_(' '-' expr ')
    def expr(self, p):
        pass

    @_(' expr GT expr')
    def expr(self, p):
        pass

    @_(' expr GE expr')
    def expr(self, p):
        pass

    @_(' expr LT expr')
    def expr(self, p):
        pass

    @_(' expr LE expr')
    def expr(self, p):
        pass

    @_(' expr EQ expr')
    def expr(self, p):
        pass

    @_(' expr NE expr')
    def expr(self, p):
        pass

    @_(' expr AND expr')
    def expr(self, p):
        pass

    @_(' expr OR expr')
    def expr(self, p):
        pass

    @_(' NOT expr')
    def expr(self, p):
        pass

    @_(' INC VAR')
    def expr(self, p):
        pass

    @_(' DEC VAR')
    def expr(self, p):
        pass

    @_(' VAR INC')
    def expr(self, p):
        pass

    @_(' VAR DEC')
    def expr(self, p):
        pass

    @_(' expr ')
    def prlist(self, p):
        pass

    '''
    prlist:	  expr
    	| STRING
    	| prlist ',' expr
    	| prlist ',' STRING
	;
    '''

    @_(' expr ')
    def prlist(self, p):
        pass

    @_(' STRING ')
    def prlist(self, p):
        pass

    @_(' prlist ',' expr ')
    def prlist(self, p):
        pass

    @_(' prlist ',' STRING ')
    def prlist(self, p):
        pass

    '''
    formals: VAR
    	| VAR ',' formals

    ;
    '''

    @_(' VAR ')
    def formals(self, p):
        pass

    @_(' VAR ',' formals ')
    def formals(self, p):
        pass

    '''
    procname: VAR
    	| FUNCTION
    	| PROCEDURE

    ;
    '''

    @_(' VAR ')
    def procname(self, p):
        pass

    @_(' FUNCTION ')
    def procname(self, p):
        pass

    @_(' PROCEDURE ')
    def procname(self, p):
        pass

    '''
    arglist:  /* nothing */
    	| expr
    	| arglist ',' expr
    ;
    '''

    @_(' ')
    def arglist(self, p):
        pass

    @_(' expr ')
    def arglist(self, p):
        pass

    @_(' arglist ',' expr ')
    def arglist(self, p):
        pass
	
if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()

    while True:
        try:
            text = input('calc > ')
            result = parser.parse(lexer.tokenize(text))
            print(result)
        except EOFError:
            break
