from sly import Parser
from hoclex import HOCLexer
from hocast import *
from hocdot import DotCode
from hoccode import *
#debaez

class HOCParser(Parser):
	tokens = HOCLexer.tokens
	debugfile='parser.out'
	def __init__(self):
		self.errorStatus=False

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
		return

	@_('list NEWLINE')
	def list(self, p):
		if(self.errorStatus):
			return
		else:
			return p.list

	@_('list defn NEWLINE')
	def list(self, p):
		if(self.errorStatus):
			return
		else:
			if(p.list is None):
				return Listaprograma([p.defn])
			else:
				p.list.append(p.defn)
				return p.list

	@_('list assign NEWLINE')
	def list(self, p):
		if(self.errorStatus):
			return
		else:
			if(p.list is None):
				return Listaprograma([p.assign])
			else:
				p.list.append(p.assign)
				return p.list

	@_('list stmt NEWLINE')
	def list(self, p):
		if(self.errorStatus):
			return
		else:
			if(p.list is None):
				return Listaprograma([p.stmt])
			else:
				p.list.append(p.stmt)
				return p.list

	@_('list expr NEWLINE')
	def list(self, p):
		if(self.errorStatus):
			return
		else:
			if(p.list is None):
				return Listaprograma([p.expr])
			else:
				p.list.append(p.expr)
				return p.list

	@_('list error NEWLINE')
	def list(self, p):
		if(self.errorStatus):
			return
		else:
			if(p.list is None):
				return Listaprograma([p.error])
			else:
				p.list.append(p.error)
				return p.list

	
	'''
	type: INT | FOLAT | STRING

	'''

	@_('INT','FLOAT', 'STRING', 'VOID')
	def type(self, p):
		if (self.errorStatus):
			return
		else:
			return p[0]




	
	'''
	assign: ID '=' expr
		| ID ADDEQ expr
		| ID SUBEQ expr
		| ID MULEQ expr
		| ID DIVEQ expr
		| ID MODEQ expr
	;
	'''

	@_('ID ASSIGN expr', 'ID ADDEQ expr', 'ID SUBEQ expr', 'ID MULEQ expr', 'ID DIVEQ expr', 'ID MODEQ expr')
	def assign(self,p):
		if(self.errorStatus):
			return
		else:
			temp=Assign(p.ID, p[1], p.expr)
			temp.lineno=p.lineno
			return temp
			



	'''
	defn: FUNC procname  '(' ')' type stmt
		| PROC procname  '(' ')' type stmt
	;
	'''

	@_('FUNC procname LPAREN formalopt RPAREN type stmt')
	def defn(self, p):
		if(self.errorStatus):
			return
		else:
			return FuncDefn(p.procname, p.formalopt, p.type, p.stmt)

	@_('PROC procname  LPAREN formalopt RPAREN stmt')
	def defn(self, p):
		if(self.errorStatus):
			return
		else:
			return ProcDefn(p.procname, p.formalopt, p.stmt)

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
		if(self.errorStatus):
			return
		else:
			return p.expr

	@_('type ID')
	def stmt(self, p):
		if(self.errorStatus):
			return
		else:
			return TypeNode(p[0], p[1])
		

	@_('RETURN expr')
	def stmt(self, p):
		if(self.errorStatus):
			return
		else:
			temp=Retexp(p.expr)
			temp.lineno=p.lineno
			return temp

	@_('PROCEDURE begin LPAREN arglist RPAREN')
	def stmt(self, p):
		if(self.errorStatus):
			return
		else:
			return ProcArg(p.begin, p.arglist) 

	@_('PRINT prlist')
	def stmt(self, p):
		if(self.errorStatus):
			return
		else:
			return PrintPr(p.prlist)

	@_('WHILE LPAREN cond RPAREN stmt end')
	def stmt(self, p):
		if(self.errorStatus):
			return
		else:
			return WhileConst(p.cond, p.stmt, p.end)

	@_('FOR LPAREN cond SEMI cond SEMI cond RPAREN stmt end')
	def stmt(self, p):
		if(self.errorStatus):
			return
		else:
			return ForConst(p.cond0, p.cond1, p.cond2, p.stmt, p.end)

	@_('IF LPAREN cond RPAREN stmt end')
	def stmt(self, p):
		if(self.errorStatus):
			return
		else:
			return IfStmt(p.cond, p.stmt, p.end)

	@_('IF LPAREN cond RPAREN stmt end ELSE stmt end')
	def stmt(self, p):
		if(self.errorStatus):
			return
		else:
			return IfElsestmt(p[2], p[4], p[5], p[7], p[8])
		
	@_('LBRACKET stmtlist RBRACKET')
	def stmt(self, p):
		if(self.errorStatus):
			return
		else:
			return StmtBrack(p[1])

	

		'''
	cond: expr
	;
	'''

	@_('expr')
	def cond(self, p):
		if(self.errorStatus):
			return
		else:
			return p.expr


	'''
	begin: /*nothing*/
	;
	'''

	@_('')
	def begin(self, p):
		return

	'''
	end: /*nothing*/
	;
	'''

	@_('')
	def end(self, p):
		return

	'''
	stmtlist: /* nothing */
		   | stmtlist NEWLINE
		   | stmtlist stmt
	;
	'''


	@_('NEWLINE')
	def stmtlist(self, p):
		if(self.errorStatus):
			return
		else:
			return StmtLista([])
		

	@_('stmt')
	def stmtlist(self, p):
		if(self.errorStatus):
			return
		else:
			return StmtLista([p.stmt])

	@_('stmtlist NEWLINE')
	def stmtlist(self, p):
		if(self.errorStatus):
			return
		else:
			if(p.stmtlist is None):
				return StmtLista([])
			else:
				return p.stmtlist
		

	@_('stmtlist stmt')
	def stmtlist(self, p):
		if(self.errorStatus):
			return
		else:
			if(p.stmtlist is None):
				return StmtLista([p.stmt])
			else:
				p.stmtlist.appendStmtlists(p.stmt)
				return p.stmtlist
		
		
	'''
	expr: INTEGER
		| FLOATT
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
		if(self.errorStatus):
			return
		else:
			return p.INTEGER

	@_('FLOATT')
	def expr(self, p):
		if(self.errorStatus):
			return
		else:
			return p.FLOATT

	@_('ID')
	def expr(self, p):
		if(self.errorStatus):
			return
		else:
			return p.ID

	@_('ARG')
	def expr(self, p):
		if(self.errorStatus):
			return
		else:
			return p.ARG

	@_('assign')
	def expr(self, p):
		if(self.errorStatus):
			return
		else:
			return p.assign

	@_('FUNCTION begin LPAREN arglist RPAREN ')
	def expr(self, p):
		if(self.errorStatus):
			return
		else:
			return ExprFunc(p[1], p[3])

	@_('READ LPAREN ID RPAREN')
	def expr(self, p):
		if(self.errorStatus):
			return
		else:
			return ExprRead(p.ID)

	@_('ID LPAREN prlist RPAREN')
	def expr(self, p):
		if(self.errorStatus):
			return
		else:
			temp=ExprId(p.ID, p[2])
			temp.lineno=p.lineno
			return temp 

	@_('BLTIN LPAREN expr RPAREN')
	def expr(self, p):
		if(self.errorStatus):
			return
		else:
			return ExprBltin(p.BLTIN, p[2])

	@_('LPAREN expr RPAREN')
	def expr(self, p):
		if(self.errorStatus):
			return
		else:
			temp=ExprLparen(p[1])
			temp.lineno=p.lineno
			return temp 

	@_('expr PLUS expr', 'expr MINUS expr', 'expr TIMES expr', 'expr DIVIDE expr', 'expr MODULE expr', 'expr POWER expr')
	def expr(self, p):
		if(self.errorStatus):
			return
		else:
			temp=ExprSimbols(p[0], p[1], p[2])
			temp.lineno=p.lineno
			return temp

	@_('MINUS expr')
	def expr(self, p):
		if(self.errorStatus):
			return
		else:
			return ExprUnary(p[1])

	@_('expr GT expr', 'expr GE expr', 'expr LT expr', 'expr LE expr', 'expr EQ expr', 'expr NE expr', 'expr AND expr', 'expr OR expr')
	def expr(self, p):
		if(self.errorStatus):
			return
		else:
			temp=ExprComp(p[0], p[1], p[2])
			temp.lineno=p.lineno
			return temp	


	@_('NOT expr')
	def expr(self, p):
		if(self.errorStatus):
			return
		else:
			return DenyExpr(p[1])

	@_('INC ID', 'DEC ID')
	def expr(self, p):
		if(self.errorStatus):
			return
		else:
			return ExprIncDec(p[0], p[1])

	@_('ID INC', 'ID DEC')
	def expr(self, p):
		if(self.errorStatus):
			return
		else:
			return IncDecExpr(p[0], p[1])


	'''
	prlist:	  expr
		| STRINGG
		| prlist ',' expr
		| prlist ',' STRINGG
	;
	'''

	@_('expr')
	def prlist(self, p):
		if(self.errorStatus):
			return
		else:
			return PrList([p.expr],[])

	@_('STRINGG')
	def prlist(self, p):
		if(self.errorStatus):
			return
		else:
			return PrList([],[p.STRINGG])

	@_('prlist COMMA expr')
	def prlist(self, p):
		if(self.errorStatus):
			return
		else:
			if(p.prlist is None):
				return PrList([p.expr],[])
			else:
				p.prlist.appendExpr(p.expr)
				return p.prlist	

	@_('prlist COMMA STRINGG')
	def prlist(self, p):
		if(self.errorStatus):
			return
		else:
			if(p.prlist is None):
				return PrList([],[p.STRINGG])
			else:
				p.prlist.appendString(p.STRINGG)
				return p.prlist

	'''
	formals: ID
		| ID ',' formals

	;
	'''
	@_('empty')
	def formals(self, p):
		return

	@_('ID')
	def formals(self, p):
		if(self.errorStatus):
			return
		else:
			return p.ID

	@_('ID COMMA formals')
	def formals(self, p):
		if(self.errorStatus):
			return
		else:
			return FormalsList(p[0], p[2])

	'''
	formalss: ID
		| ID ',' formals

	;
	'''
	'''
	@_('ID')
	def formalss(self, p):
		if(self.errorStatus):
			return
		else:
			return Formal2sList(p[0])

	@_('ID COMMA formalss')
	def formalss(self, p):
		if(self.errorStatus):
			return
		else:
			return Formal2sList(p[0])
	'''
	


	@_('type ID')
	def formalsss(self, p):
		if(self.errorStatus):
			return
		else:
			return FormaltriplesList([str(p.type)+" "+str(p.ID)])

	@_('type ID COMMA formalsss')
	def formalsss(self, p):
		if(self.errorStatus):
			return
		else:
			if(p.formalsss is not None):
				p.formalsss.append(str(p.type)+" "+str(p.ID))
				return p.formalsss
			else: 
				return FormaltriplesList([str(p.type)+" "+str(p.ID)])
	'''
	formalopt: formals | formalss
	'''
	@_('formals')
	def formalopt(self,p):
		return p[0]

	@_('formalsss')
	def formalopt(self,p):
		return p[0]	


	'''
	procname: ID
		| FUNCTION
		| PROCEDURE

	;
	'''

	@_('ID')
	def procname(self, p):
		if(self.errorStatus):
			return
		else:
			return p.ID

	@_('FUNCTION')
	def procname(self, p):
		if(self.errorStatus):
			return
		else:
			return p.FUNCTION

	@_('PROCEDURE')
	def procname(self, p):
		if(self.errorStatus):
			return
		else:
			return p.PROCEDURE

	'''
	arglist:  /* nothing */
		| expr
		| arglist ',' expr
	;
	'''

	@_('empty')
	def arglist(self, p):
		return

	@_('expr')
	def arglist(self, p):
		if(self.errorStatus):
			return
		else:
			return p.expr

	@_('arglist COMMA expr')
	def arglist(self, p):
		if(self.errorStatus):
			return
		else:
			temp=ArglistExpr(p[0], p[2])
			temp.lineno=p.lineno
			return temp

	@_('')
	def empty(self, p):
		pass

	def error(self, p):
		self.errorStatus=True
		if p:
			print("Syntax error at {}, line {}, token {}".format(p.value, p.lineno, p.type))
		else:
			print("Error at EOF")
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
	if parser.errorStatus == True:
		print("error en codigo")
		return None
	else:
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
	dot=DotCode()
	code=GenerateCode()
	if(p == None):
		print("Este codigo tiene errores, no es posible construir el AST")
	else:
		#p.pprint()
		dot.visit(p)
		code.visit(p)
		for enum, i in enumerate(code.code):
			print(enum, i)
		
		#print(dot)