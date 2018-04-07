from sly import Parser
from analizlex import HOCLexer

#debaez

class HOCParser(Parser):
	tokens = HOCLexer.tokens

	precedence = (
		('right', 'ASSIGN', 'ADDEQ', 'SUBEQ', 'MULEQ', 'DIVEQ', 'MODEQ'),
		('left', 'OR'),
		('left', 'AND'),
		('left', 'GT', 'GE', 'LT', 'LE', 'EQ', 'NE', 'RETURN'),
		('left', 'PLUS', 'MINUS'),
		('left', 'TIMES', 'DIVIDE', 'MODULE'),
		('left', 'NOT', 'INC', 'DEC'),
		('right', 'POWER')
	)

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

	@_('list NEWLINE')
	def list(self, p):
		pass

	@_('list defn NEWLINE')
	def list(self, p):
		pass

	@_('list assign NEWLINE')
	def list(self, p):
		pass

	@_('list stmt NEWLINE')
	def list(self, p):
		pass

	@_('list expr NEWLINE')
	def list(self, p):
		pass

	@_('list error NEWLINE')
	def list(self, p):
		pass

	'''
	assign: ID '=' expr
		| ID ADDEQ expr
		| ID SUBEQ expr
		| ID MULEQ expr
		| ID DIVEQ expr
		| ID MODEQ expr
	;
	'''

	@_('ID ASSIGN expr')
	def assign(self,p):
		pass

	@_('ID ADDEQ expr')
	def assign(self,p):
		pass

	@_('ID SUBEQ expr')
	def assign(self,p):
		pass

	@_('ID MULEQ expr')
	def assign(self,p):
		pass

	@_('ID DIVEQ expr')
	def assign(self,p):
		pass

	@_('ID MODEQ expr')
	def assign(self,p):
		pass

	'''
	defn: FUNC procname  '(' ')' stmt
		| PROC procname  '(' ')' stmt
	;
	'''

	@_('FUNC procname LPAREN formals RPAREN stmt')
	def defn(self, p):
		pass

	@_('PROC procname  LPAREN formals RPAREN stmt')
	def defn(self, p):
		pass

	'''
	stmt: expr
		| RETURN
		| RETURN expr
		| PROCEDURE begin '(' arglist ')'
		| PRINT prlist
		| WHILE '(' cond ')' stmt end
		| FOR '(' cond SEMI cond SEMI cond ')' stmt end
		| IF '(' cond ')' stmt end
		| IF '(' cond ')' stmt end ELSE stmt end
		| LBRACKET stmtlist RBRACKET
	;
	'''

	@_('expr')
	def stmt(self, p):
		pass

	@_('RETURN expr')
	def stmt(self, p):
		pass

	@_('PROCEDURE begin LPAREN arglist RPAREN')
	def stmt(self, p):
		pass

	@_('PRINT prlist')
	def stmt(self, p):
		pass

	@_('WHILE LPAREN cond RPAREN stmt end ')
	def stmt(self, p):
		pass

	@_('FOR LPAREN cond SEMI cond SEMI cond RPAREN stmt end ')
	def stmt(self, p):
		pass

	@_('IF LPAREN cond RPAREN stmt end ')
	def stmt(self, p):
		pass

	@_('IF LPAREN cond RPAREN stmt end ELSE stmt end')
	def stmt(self, p):
		pass

	@_('LBRACKET stmtlist RBRACKET')
	def stmt(self, p):
		pass



	'''
	cond: expr
	;
	'''

	@_('expr')
	def cond(self, p):
		pass


	'''
	begin: /*nothing*/
	;
	'''

	@_('')
	def begin(self, p):
		pass

	'''
	end: /*nothing*/
	;
	'''

	@_('')
	def end(self, p):
		pass

	'''
	stmtlist: /* nothing */
		   | stmtlist NEWLINE
		   | stmtlist stmt
	;
	'''

	@_('empty')
	def stmtlist(self, p):
		pass

	@_('stmtlist NEWLINE ')
	def stmtlist(self, p):
		pass

	@_('stmtlist stmt')
	def stmtlist(self, p):
		pass

	'''
	expr: INTEGER
		| FLOAT
		| ID
		| ARG
		| asgn
		| FUNCTION begin '(' arglist ')'
		| READ '(' ID ')'
		| ID '(' formals ')'
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
		| INC ID
		| DEC ID
		| ID INC
		| ID DEC
	;
	'''

	@_('INTEGER')
	def expr(self, p):
		pass

	@_('FLOAT')
	def expr(self, p):
		pass

	@_('ID')
	def expr(self, p):
		pass

	@_('ARG')
	def expr(self, p):
		pass

	@_('assign')
	def expr(self, p):
		pass

	@_('FUNCTION begin LPAREN arglist RPAREN ')
	def expr(self, p):
		pass

	@_('READ LPAREN ID RPAREN')
	def expr(self, p):
		pass

	@_('ID LPAREN prlist RPAREN')
	def expr(self, p):
		pass

	@_('BLTIN LPAREN expr RPAREN')
	def expr(self, p):
		pass

	@_('LPAREN expr RPAREN')
	def expr(self, p):
		pass

	@_('expr PLUS expr')
	def expr(self, p):
		pass

	@_('expr MINUS expr')
	def expr(self, p):
		pass

	@_(' expr TIMES expr')
	def expr(self, p):
		pass

	@_('expr DIVIDE expr')
	def expr(self, p):
		pass

	@_('expr MODULE expr')
	def expr(self, p):
		pass

	@_('expr POWER expr')
	def expr(self, p):
		pass

	@_('MINUS expr')
	def expr(self, p):
		pass

	@_('expr GT expr')
	def expr(self, p):
		pass

	@_('expr GE expr')
	def expr(self, p):
		pass

	@_('expr LT expr')
	def expr(self, p):
		pass

	@_('expr LE expr')
	def expr(self, p):
		pass

	@_('expr EQ expr')
	def expr(self, p):
		pass

	@_('expr NE expr')
	def expr(self, p):
		pass

	@_('expr AND expr')
	def expr(self, p):
		pass

	@_('expr OR expr')
	def expr(self, p):
		pass

	@_('NOT expr')
	def expr(self, p):
		pass

	@_('INC ID')
	def expr(self, p):
		pass

	@_('DEC ID')
	def expr(self, p):
		pass

	@_('ID INC')
	def expr(self, p):
		pass

	@_('ID DEC')
	def expr(self, p):
		pass

	'''
	prlist:	  expr
		| STRING
		| prlist ',' expr
		| prlist ',' STRING
	;
	'''

	@_('expr')
	def prlist(self, p):
		pass

	@_('STRING')
	def prlist(self, p):
		pass

	@_('prlist COMMA expr')
	def prlist(self, p):
		pass

	@_('prlist COMMA STRING')
	def prlist(self, p):
		pass

	'''
	formals: ID
		| ID ',' formals

	;
	'''
	@_('empty')
	def formals(self, p):
		pass

	@_('ID')
	def formals(self, p):
		pass

	@_('ID COMMA formals')
	def formals(self, p):
		pass

	'''
	procname: ID
		| FUNCTION
		| PROCEDURE

	;
	'''

	@_('ID')
	def procname(self, p):
		pass

	@_('FUNCTION')
	def procname(self, p):
		pass

	@_('PROCEDURE')
	def procname(self, p):
		pass

	'''
	arglist:  /* nothing */
		| expr
		| arglist ',' expr
	;
	'''

	@_('empty')
	def arglist(self, p):
		pass

	@_('expr')
	def arglist(self, p):
		pass

	@_('arglist COMMA expr')
	def arglist(self, p):
		pass

	@_('')
	def empty(self, p):
		pass

	def error(self, p):
		self.errorStatus=True
		print("Syntax error at {}, line {}, token {}".format(p.value, p.lineno, p.type))
		#if p:
		#	print("Syntax error at {}, line {}, token {}".format(p.value, p.lineno, p.type))
			# Just discard the token or tell the parser it's okay.
		#	self.errok()
		#else:
		#	print("Syntax error at EOF")
		pass

def parse(data, debug=0):
	#print(parser.error)
	p = parser.parse(lexer.tokenize(data))
	#print(parser.errorStatus)
	#if parser.errorStatus:
	#	print("error en codigo")
	#	return None
	print("sin errores\n") 
	return p

if __name__ == '__main__':
	import sys
	lexer = HOCLexer()
	parser = HOCParser()

	if(len(sys.argv)!=2):#Verifica la cantidad de argumentos a la hora de compilar si no son 2. "py 'fichero.py' 'archivo'"
		sys.stderr.write('Usage: "{}" "filename"\n'.format(sys.argv[0]))#permite que al al compilar indique que debe de darse el archivo de la forma python.exe "fichero.py" "Archivo a abrir, como un simple print"
		raise SystemExit(1)#termina el programa
	file= open(sys.argv[1]).read()
	p=parse(file)

