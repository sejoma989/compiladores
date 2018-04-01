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

	@('FUNC procname  '(' formals ')' stmt')
	def defn(self, p):
		pass

	@('PROC procname  '(' formals ')' stmt')
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

    @('expr')
	def stmt(self, p):
		pass

	@('RETURN expr')
	def stmt(self, p):
		pass

    @('PROCEDURE begin '(' arglist ')'')
	def stmt(self, p):
		pass

	@('PRINT prlist	')
	def stmt(self, p):
		pass

    @('while '(' cond ')' stmt end ')
	def stmt(self, p):
		pass

    @('for '(' cond ';' cond ';' cond ')' stmt end ')
	def stmt(self, p):
		pass

    @('if '(' cond ')' stmt end ')
	def stmt(self, p):
		pass

	@('if '(' cond ')' stmt end ELSE stmt end')
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

    @('')
    def stmtlist(self, p):
        pass

    @('(stmtlist '\n')')
    def stmtlist(self, p):
        pass

    @('stmtlist stmt')
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

    @(' ')
    def expr(self, p):
        pass

    @('VAR')
    def expr(self, p):
        pass

    @('asgn')
    def expr(self, p):
        pass

    @(' FUNCTION begin '(' arglist ')' ')
    def expr(self, p):
        pass

    @(' READ '(' VAR ')' ')
    def expr(self, p):
        pass

    @(' BLTIN '(' expr ')' ')
    def expr(self, p):
        pass

    @(' '(' expr ')' ')
    def expr(self, p):
        pass

    @(' expr '+' expr')
    def expr(self, p):
        passexpr AND expr

    @(' expr '-' expr ')
    def expr(self, p):
        pass

    @(' expr '*' expr ')
    def expr(self, p):
        pass

    @(' expr '/' expr')
    def expr(self, p):
        pass

    @(' expr '%' expr')
    def expr(self, p):
        pass

    @(' expr '^' expr')
    def expr(self, p):
        pass

    @(' '-' expr ')
    def expr(self, p):
        pass

    @(' expr GT expr')
    def expr(self, p):
        pass

    @(' expr GE expr')
    def expr(self, p):
        pass

    @(' expr LT expr')
    def expr(self, p):
        pass

    @(' expr LE expr')
    def expr(self, p):
        pass

    @(' expr EQ expr')
    def expr(self, p):
        pass

    @(' expr NE expr')
    def expr(self, p):
        pass

    @(' expr AND expr')
    def expr(self, p):
        pass

    @(' expr OR expr')
    def expr(self, p):
        pass

    @(' NOT expr')
    def expr(self, p):
        pass

    @(' INC VAR')
    def expr(self, p):
        pass

    @(' DEC VAR')
    def expr(self, p):
        pass

    @(' VAR INC')
    def expr(self, p):
        pass

    @(' VAR DEC')
    def expr(self, p):
        pass

    @(' expr ')
    def prlist(self, p):
        pass

    '''
    prlist:	  expr
    	| STRING
    	| prlist ',' expr
    	| prlist ',' STRING
	;
    '''

    @(' expr ')
    def prlist(self, p):
        pass

    @(' STRING ')
    def prlist(self, p):
        pass

    @(' prlist ',' expr ')
    def prlist(self, p):
        pass

    @(' prlist ',' STRING ')
    def prlist(self, p):
        pass

    '''
    formals: VAR
    	| VAR ',' formals

    ;
    '''

    @(' VAR ')
    def formals(self, p):
        pass

    @(' VAR ',' formals ')
    def formals(self, p):
        pass

    '''
    procname: VAR
    	| FUNCTION
    	| PROCEDURE

    ;
    '''

    @(' VAR ')
    def procname(self, p):
        pass

    @(' FUNCTION ')
    def procname(self, p):
        pass

    @(' PROCEDURE ')
    def procname(self, p):
        pass

    '''
    arglist:  /* nothing */
    	| expr
    	| arglist ',' expr
    ;
    '''

    @(' ')
    def arglist(self, p):
        pass

    @(' expr ')
    def arglist(self, p):
        pass

    @(' arglist ',' expr ')
    def arglist(self, p):
        pass
