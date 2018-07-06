
import pydotplus as pgv
import hocast as ast
import re

class DotCode(ast.NodeVisitor):
	'''
	Clase Node Visitor que crea secuencia de instrucciones Dot
	'''
	
	def __init__(self):
		super(DotCode, self).__init__()
		self.errorStatus=False
		# Secuencia para los nombres de nodos
		self.id = 0
		
		# Stack para retornar nodos procesados
		self.stack = []
		
		# Inicializacion del grafo para Dot
		self.dot = pgv.Dot('AST', graph_type='digraph')  
		
		self.dot.set_node_defaults(shape='box', color='lightgray', style='filled')
		self.dot.set_edge_defaults(arrowhead='none')

		#Control de chequeo de variables
		self.InFuncDefn=False 			#Bandera para saber si se está en el visitante FuncDef
		self.InAssign=False 			#Bandera para saber si se está en el visitante Assign
		self.InRetex=False 				#Bandera para saber si se está en el visitante Retex
		self.InExprSimbols=False 		#Bandera para saber si se está en el visitante ExprSimbols
		self.InPrList=False 			#Bandera para saber si se está en el visitante PrList
		self.InExpId=False 	 			#Bandera para saber si se está en el visitante ExprId
		self.IsDeffined=False 			#Bandera para saber si en un llamado a una función, ésta ha sido definida
		self.DatFuncDic={}				#Diccionario para guardar los datos locales con su respectivo
		self.DatGlobDic={}				#Diccionario para guardar los datos globales con su respectivo tipo
		self.TipoFuncDic={}				#Diccionario para guardar el nombre de la función con su respectivo tipo
		self.ExprSimbols=[]				#Lista para guardar las operaciones que se realizan en el programa
		self.ExprComp=[]				#Lista para guardar las comparaciones que se realizan en el programa
		self.tempExprComp1=" "			#Variable temporal usada para comparar tipos en el visitante de comparación
		self.tempExprComp2=" "			#Variable temporal usada para comparar tipos en el visitante de comparación
		self.nombrefuncion=" "			#Variable que almacena el nombre de la función
		self.nombrefuncionenExprId=" "	#Variable que almacena el nombre de una función que está siendo llamada
	def __repr__(self):
		return self.dot.to_string()
	
	def new_node(self, node, label=None, shape='box', color="lightgray"):
		'''
		Crea una variable temporal como nombre del nodo
		'''
		if label is None:
			label = node.__class__.__name__#le entrega al label, es decir nombre el label
		
		self.id += 1
		
		return pgv.Node('n{}'.format(self.id), label=label, shape=shape, color=color)


	def visit_Listaprograma(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):

			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item, 'diamond')
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))

		#print(self.DatGlobDic)
		#print(self.TipoFuncDic)
		
	def visit_FuncDefn(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.InFuncDefn=True
		self.TipoFuncion=node.type
		self.nombrefuncion=node.procname
		for field in getattr(node, "_fields"):
			
			value = getattr(node, field, None)

			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))
		
		#print(self.DatFuncDic)
		self.nombrefuncion=""
		self.DatFuncDic={}
		self.InFuncDefn=False
		self.TipoFuncion=""
		self.stack.append(target)


	def visit_FormaltriplesList(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):
			
			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					self.DatFuncDic[item.split()[1]]=item.split()[0]
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item, 'diamond')
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))

		self.TipoFuncDic[self.nombrefuncion]=[self.TipoFuncion,len(self.DatFuncDic)]
		self.stack.append(target)


	def visit_Assign(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.InAssign=True
		for field in getattr(node, "_fields"):

			value = getattr(node, field, None)
			#print("Field: ", field)
			#print("Value: ", value)
			if (field == "ID"): 
				if self.InFuncDefn:

					if value not in self.DatFuncDic:	
						print("Error Semantico!!! En la linea", node.lineno, "La variable ",value," no está definida.")
				else:
					if value not in self.DatGlobDic:
						print("Error semantico!!! En la linea", node.lineno, "La variable ",value," no está definida.")

			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))

		self.InAssign=False
		self.stack.append(target)	

	def visit_ExprSimbols(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.InExprSimbols=True
		for field in getattr(node, "_fields"):

			value = getattr(node, field, None)
			for i in [3]:
				self.ExprSimbols.append(value)
			if isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))

		temp0=re.search('((\d*\.\d+)|(\d+\.\d*)|([1-9]e\d+))(e[-+]?\d+)?', str(self.ExprSimbols[0]))
		temp2=re.search('((\d*\.\d+)|(\d+\.\d*)|([1-9]e\d+))(e[-+]?\d+)?', str(self.ExprSimbols[2]))
		if self.InFuncDefn:
			if(self.ExprSimbols[1] == "+" or self.ExprSimbols[1] == "-" or self.ExprSimbols[1] == "*" or self.ExprSimbols[1] == "/" or self.ExprSimbols[1] == "%"):
				if self.ExprSimbols[0] in self.DatFuncDic or str.isdigit(str(self.ExprSimbols[0])) or temp0 is not None:
					for item in self.DatFuncDic:
						if item == self.ExprSimbols[0]:
							if self.DatFuncDic.get(item) == "string":
								print("Error semantico!!! En la linea", node.lineno, "La variable ",self.ExprSimbols[0]," es de un tipo incompatible con la operación.")
				else:
					print("Error semantico!!! En la linea",node.lineno,"La variable ",self.ExprSimbols[0]," no está definida.")

				if self.ExprSimbols[2] in self.DatFuncDic or str.isdigit(str(self.ExprSimbols[2])) or temp2 is not None:
					for item in self.DatFuncDic:
						if item == self.ExprSimbols[2]:
							if self.DatFuncDic.get(item) == "string":
								print("Error semantico!!! En la linea",node.lineno,"La variable ",self.ExprSimbols[2]," es de un tipo incompatible con la operación.")
				else:
					print("Error semantico!!! En la linea", node.lineno, "La variable ",self.ExprSimbols[2]," no está definida.")
				
		else:
			if(self.ExprSimbols[1] == "+" or self.ExprSimbols[1] == "-" or self.ExprSimbols[1] == "*" or self.ExprSimbols[1] == "/" or self.ExprSimbols[1] == "%"):
				if self.ExprSimbols[0] in self.DatGlobDic or str.isdigit(str(self.ExprSimbols[0])):
					for item in self.DatGlobDic:
						if item == self.ExprSimbols[0]:
							if self.DatGlobDic.get(item) == "string":
								print("Error semantico!!! En la linea", node.lineno, "La variable ",self.ExprSimbols[0]," es de un tipo incompatible con la operación.")
				else:
					print("Error semantico!!! En la linea", node.lineno, "La variable ",self.ExprSimbols[0]," no está definida.")

				if self.ExprSimbols[2] in self.DatGlobDic or str.isdigit(str(self.ExprSimbols[2])):
					for item in self.DatGlobDic:
						if item == self.ExprSimbols[2]:
							if self.DatGlobDic.get(item) == "string":
								print("Error semantico!!! En la linea", node.lineno, "La variable ",self.ExprSimbols[2]," es de un tipo incompatible con la operación.")
				else:
					print("Error semantico!!! En la linea",node.lineno,"La variable ",self.ExprSimbols[2]," no está definida.")

		
		if self.InRetex and not self.InPrList:
			if(self.ExprSimbols[1] == "+" or self.ExprSimbols[1] == "-" or self.ExprSimbols[1] == "*" or self.ExprSimbols[1] == "/" or self.ExprSimbols[1] == "%"):
				if not (self.DatFuncDic.get(self.ExprSimbols[0])==self.TipoFuncion and self.DatFuncDic.get(self.ExprSimbols[2])==self.TipoFuncion):
					if self.TipoFuncion == "int":
						if not (self.DatFuncDic.get(self.ExprSimbols[0])=="int" and str.isdigit(str(self.ExprSimbols[2]))):
							if not ((self.DatFuncDic.get(self.ExprSimbols[2])=="int" and str.isdigit(str(self.ExprSimbols[0])))):
								print("Error semantico!!!En la linea",node.lineno,"Está intentando devolver un tipo de dato inválido en la función",self.nombrefuncion)
					if self.TipoFuncion == "float":
						if not (self.DatFuncDic.get(self.ExprSimbols[0])=="float" and temp2 is not None):
							if not (self.DatFuncDic.get(self.ExprSimbols[2])=="float" and temp0 is not None):
								print("Error semantico!!!En la linea",node.lineno,"Está intentando devolver un tipo de dato inválido en la función",self.nombrefuncion)
					if self.TipoFuncion == "string":
						if not (self.DatFuncDic.get(self.ExprSimbols[0])==self.TipoFuncion and self.DatFuncDic.get(self.ExprSimbols[2])==self.TipoFuncion):
							print("Error semantico!!!En la linea",node.lineno,"Está intentando devolver un tipo de dato inválido en la función",self.nombrefuncion)


		self.InExprSimbols=False
		self.ExprSimbols=[]
		self.stack.append(target)


	def visit_ExprComp(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):

			value = getattr(node, field, None)
			for i in [3]:
				self.ExprComp.append(value)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item, 'diamond')
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
			elif isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))

		
		if (self.ExprComp[1] == "||" or self.ExprComp[1] == "&&" or self.ExprComp[1] == "<=" or self.ExprComp[1] == ">=" or self.ExprComp[1] == "==" or self.ExprComp[1] == "!=" or self.ExprComp[1] == "<" or self.ExprComp[1] == ">" or self.ExprComp[1] == "!"):
			if self.InFuncDefn:
				if self.ExprComp[0] in self.DatFuncDic:
					for item in self.DatFuncDic:
						if item == self.ExprComp[0]:
							self.tempExprComp1 = self.DatFuncDic.get(item)
				if str.isdigit(str(self.ExprComp[0])):
					self.tempExprComp1 = "int"

				if self.ExprComp[2] in self.DatFuncDic:
					for item in self.DatFuncDic:
						if item == self.ExprComp[2]:
							self.tempExprComp2 = self.DatFuncDic.get(item)
				if str.isdigit(str(self.ExprComp[2])):
					self.tempExprComp2 = "int"
				if not ((self.tempExprComp1 == "int" or self.tempExprComp1 == "float") and (self.tempExprComp2 == "int" or self.tempExprComp2 == "float")):
					if not((self.tempExprComp1 == "string") and (self.tempExprComp2 == "string")):
						print("Error semantico!!!En la linea",node.lineno," Está intentando comparar tipos de datos incompatibles")
			else:
				if self.ExprComp[0] in self.DatGlobDic:
					for item in self.DatGlobDic:
						if item == self.ExprComp[0]:
							self.tempExprComp1 = self.DatGlobDic.get(item)
				if str.isdigit(str(self.ExprComp[0])):
					self.tempExprComp1 = "int"

				if self.ExprComp[2] in self.DatGlobDic:
					for item in self.DatGlobDic:
						if item == self.ExprComp[2]:
							self.tempExprComp2 = self.DatGlobDic.get(item)
				if str.isdigit(str(self.ExprComp[2])):
					self.tempExprComp2 = "int"
				if not ((self.tempExprComp1 == "int" or self.tempExprComp1 == "float") and (self.tempExprComp2 == "int" or self.tempExprComp2 == "float")):
					if not((self.tempExprComp1 == "string") and (self.tempExprComp2 == "string")):
						print("Error semantico!!!En la linea",node.lineno," Está intentando comparar tipos de datos incompatibles")



		self.ExprComp=[]
		self.stack.append(target)	


	def visit_Retexp(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.InRetex=True

		if not self.InFuncDefn:
			print("Error semantico!!!En la linea",node.lineno," No se puede retornar un valor por fuera de una función.")


		for field in getattr(node, "_fields"):

			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item, 'diamond')
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
			elif isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				if value in self.DatFuncDic:
					if not((self.DatFuncDic.get(value) == self.TipoFuncion)):
						print("Error!!! Está intentando devolver un tipo de dato inválido en la función",self.nombrefuncion)
				if str.isdigit(str(value)) and self.TipoFuncion == "string":
					print("Error semantico!!!En la linea",node.lineno," Está intentando devolver un tipo de dato inválido en la función",self.nombrefuncion)
				if str.isdigit(str(value)) and self.TipoFuncion == "float":
					print("Error semantico!!!En la linea",node.lineno," Está intentando devolver un tipo de dato inválido en la función",self.nombrefuncion)
				temp=re.search('((\d*\.\d+)|(\d+\.\d*)|([1-9]e\d+))(e[-+]?\d+)?', str(value))
				if (temp is not None and self.TipoFuncion == "int"):
					print("Error semantico!!!En la linea",node.lineno,"Está intentando devolver un tipo de dato inválido en la función",self.nombrefuncion)

				
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))

		self.InRetex=False
		self.stack.append(target)

	def visit_ExprId(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.InExpId=True




		for field in getattr(node, "_fields"):

			value = getattr(node, field, None)
			if field == "ID":
				self.nombrefuncionenExprId=value

				if self.nombrefuncionenExprId in self.TipoFuncDic:
					self.IsDeffined=True
				else:
					print("Error!! La función",self.nombrefuncionenExprId,"no ha sido definida.")
			if self.InRetex:
				if field == "ID":
					if not (value in self.TipoFuncDic):
						print("Error semantico!!!En la linea",node.lineno,"Está intentando retornar una función (", value ,") que no está definida")
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item, 'diamond')
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
			elif isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))

		self.IsDeffined=False
		self.InExpId=False
		self.stack.append(target)


	def visit_PrList(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		self.InPrList=True
		numparam=len(node.exprs)+len(node.strings)

		#________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
		if self.IsDeffined:
			numparamreal=self.TipoFuncDic.get(self.nombrefuncionenExprId)[1]
			if not (numparam==numparamreal):
					print("Error!!! La función",self.nombrefuncionenExprId,"requiere",numparamreal,"parametros, y está recibiendo",numparam)
			
		
		for field in getattr(node, "_fields"):

			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item, 'diamond')
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
			elif isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))

		self.InPrList=False
		self.stack.append(target)


	def visit_TypeNode(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)

		if not self.InFuncDefn:
			self.DatGlobDic[node.ID]=node.typ
		for field in getattr(node, "_fields"):

			value = getattr(node, field, None)
			
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item, 'diamond')
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
			elif isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))

		self.stack.append(target)

	def visit_ExprLparen(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):

			value = getattr(node, field, None)
			temp=re.search('((\d*\.\d+)|(\d+\.\d*)|([1-9]e\d+))(e[-+]?\d+)?', str(value))
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item, 'diamond')
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
			elif isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				if self.InRetex:
					if value in self.DatFuncDic:
						if not (self.DatFuncDic.get(value)==self.TipoFuncion):
							print("Error semantico!!!En la linea",node.lineno,"Está intentando devolver un tipo de dato inválido en la función",self.nombrefuncion)
					elif str.isdigit(str(value)):
						if not (self.TipoFuncion=="int"):
							print("Error semantico!!!En la linea",node.lineno,"Está intentando devolver un tipo de dato inválido en la función",self.nombrefuncion)	
					elif temp is not None:
						if not(self.TipoFuncion=="float"):
							print("Error semantico!!!En la linea",node.lineno,"Está intentando devolver un tipo de dato inválido en la función",self.nombrefuncion)	
					else:
						print("Error semantico!!! En la linea",node.lineno,"La variable ",value," no está definida.")
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))

		self.stack.append(target)

	

	def generic_visit(self, node):
		target = self.new_node(node)
		self.dot.add_node(target)
		for field in getattr(node, "_fields"):

			value = getattr(node, field, None)
			if isinstance(value, list):
				for item in value:
					if isinstance(item, ast.AST):
						self.visit(item)
						self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
					elif(item is not None):#caso de ramas
						targetHijo = self.new_node(None, item, 'diamond')
						self.dot.add_node(targetHijo)
						self.dot.add_edge(pgv.Edge(target, targetHijo))
			elif isinstance(value, ast.AST):
				self.visit(value)
				self.dot.add_edge(pgv.Edge(target, self.stack.pop()))
			elif(value is not None):#ramas...
				targetHijo = self.new_node(None, value, 'diamond')
				self.dot.add_node(targetHijo)
				self.dot.add_edge(pgv.Edge(target, targetHijo))

		self.stack.append(target)