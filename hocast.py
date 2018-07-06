# hocast.py
# -*- coding: utf-8 -*-
'''
Objetos Arbol de Sintaxis Abstracto (AST - Abstract Syntax Tree).

Este archivo define las clases para los diferentes tipos de nodos del
árbol de sintaxis abstracto.  Durante el análisis sintático, se debe 
crear estos nodos y conectarlos.  En general, usted tendrá diferentes
nodos AST para cada tipo de regla gramatical.  Algunos ejemplos de
nodos AST pueden ser encontrados al comienzo del archivo.  Usted deberá
añadir más.
'''

# NO MODIFICAR
class AST(object):
        '''
        Clase base para todos los nodos del AST.  Cada nodo se espera 
        definir el atributo _fields el cual enumera los nombres de los
        atributos almacenados.  El método a continuación __init__() toma
        argumentos posicionales y los asigna a los campos apropiados.
        Cualquier argumento adicional especificado como keywords son 
        también asignados.
        '''
        _fields = []
        def __init__(self,*args,**kwargs):
                assert len(args) == len(self._fields)
                for name,value in zip(self._fields,args):
                        setattr(self,name,value)
                # Asigna argumentos adicionales (keywords) si se suministran
                for name,value in kwargs.items():
                        setattr(self,name,value)
                self.lineno=0
        def __repr__(self):
                return self.__class__.__name__

        def pprint(self):
                for depth, node in flatten(self):
                        print("%s%s" % (" "*(4*depth),node))

def validate_fields(**fields):
        def validator(cls):
                old_init = cls.__init__
                def __init__(self, *args, **kwargs):
                        old_init(self, *args, **kwargs)
                        for field,expected_type in fields.items():
                                assert isinstance(getattr(self, field), expected_type)
                cls.__init__ = __init__
                return cls
        return validator

# ----------------------------------------------------------------------
# Nodos AST especificos
#
# Para cada nodo es necesario definir una clase y añadir la especificación
# del apropiado _fields = [] que indique que campos deben ser almacenados.
# A modo de ejemplo, para un operador binario es posible almacenar el
# operador, la expresión izquierda y derecha, como esto:
# 
#    class Binop(AST):
#        _fields = ['op','left','right']
# ----------------------------------------------------------------------

# Nodos del arbol


@validate_fields(stmts=list)
class Listaprograma(AST):
        _fields=["stmts"]
        def append(self, stmt):
                self.stmts.append(stmt)

class Assign(AST):
        _fields=["ID", "simbolo", "expr"]

class FuncDefn(AST):
        _fields=["procname", "formals", "type", "stmt"]

class ProcDefn(AST):
        _fields=["procname", "formals", "stmt"]

class Retexp(AST):
        _fields=["expr"]

class TypeNode(AST):
        _fields=["typ", "ID"]

class ProcArg(AST):
        _fields=["begin", "arglist"]

class PrintPr(AST):
        _fields=["prlist"] 

class WhileConst(AST):
        _fields=["cond", "stmt", "end"]

class ForConst(AST):
        _fields=["cond1", "cond2", "cond3", "stmt", "end"]

class IfStmt(AST):
        _fields=["cond", "stmt", "end"]

class IfElsestmt(AST):
        _fields=["cond", "stmt", "end", "stmt2", "end2"]

class StmtBrack(AST):
        _fields=["stmtlist"]

@validate_fields(stmts=list)
class StmtLista(AST):
        _fields=["stmts"]
        def appendStmtlists(self, stmt):
                self.stmts.append(stmt)

class ExprFunc(AST):
        _fields=["begin", "arglist"]

class ExprRead(AST):
        _fields=["ID"]

class ExprId(AST):
        _fields=["ID", "prlist"]

class ExprBltin(AST):
        _fields=["BLTIN", "expr"]

class ExprLparen(AST):
        _fields=["expr"]

class ExprSimbols(AST):
        _fields=["expr1", "simbolo","expr"]

class ExprUnary(AST):
        _fields=["expr"]

class ExprComp(AST):
        _fields=["expr1", "simboloComp", "expr"]

class DenyExpr(AST):
        _fields=["expr"]

class ExprIncDec(AST):
        _fields=["Incremental", "ID"]

class IncDecExpr(AST):
        _fields=["ID", "Incremental"]

@validate_fields(exprs=list, strings=list)
class PrList(AST):
        _fields=["exprs", "strings"]
        def appendExpr(self, expr):
                self.exprs.append(expr)
        def appendString(self, string):
                self.strings.append(string)

class FormalsList(AST):
        _fields=["IDformal", "formals"]

class Formal2sList(AST):
        _fields=["IDformal2s"]

@validate_fields(IDnTypeList=list)
class FormaltriplesList(AST):
        _fields=["IDnTypeList"]
        def append(self, IDType):
                self.IDnTypeList.append(IDType)

@validate_fields(arglists=list)
class ArglistExpr(AST):
        _fields=["arglistas", "expr"]
        def append(self, arglist):
                self.arglists.append(arglist)




# ----------------------------------------------------------------------
#                  NO MODIFIQUE NADA AQUI ABAJO
# ----------------------------------------------------------------------

# Las clase siguientes para visitar y reescribir el AST son tomadas
# desde el módulo ast de python .

# NO MODIFIQUE
class NodeVisitor(object):
        '''
        Clase para visitar nodos del árbol de sintaxis.  Se modeló a partir
        de una clase similar en la librería estándar ast.NodeVisitor.  Para
        cada nodo, el método visit(node) llama un método visit_NodeName(node)
        el cual debe ser implementado en la subclase.  El método genérico
        generic_visit() es llamado para todos los nodos donde no hay coincidencia
        con el método visit_NodeName().

        Es es un ejemplo de un visitante que examina operadores binarios:

                class VisitOps(NodeVisitor):
                        visit_Binop(self,node):
                                print("Operador binario", node.op)
                                self.visit(node.left)
                                self.visit(node.right)
                        visit_Unaryop(self,node):
                                print("Operador unario", node.op)
                                self.visit(node.expr)

                tree = parse(txt)
                VisitOps().visit(tree)
        '''
        def visit(self,node):
                '''
                Ejecuta un método de la forma visit_NodeName(node) donde
                NodeName es el nombre de la clase de un nodo particular.
                '''
                if node:
                        method = 'visit_' + node.__class__.__name__
                        visitor = getattr(self, method, self.generic_visit)
                        return visitor(node)
                else:
                        return None

        def generic_visit(self,node):
                '''
                Método ejecutado si no se encuentra médodo aplicable visit_.
                Este examina el nodo para ver si tiene _fields, es una lista,
                o puede ser recorrido completamente.
                '''
                for field in getattr(node,"_fields"):
                        value = getattr(node,field,None)
                        if isinstance(value, list):
                                for item in value:
                                        if isinstance(item,AST):
                                                self.visit(item)
                        elif isinstance(value, AST):
                                self.visit(value)

# NO MODIFICAR
class NodeTransformer(NodeVisitor):
        '''
        Clase que permite que los nodos del arbol de sintraxis sean 
        reemplazados/reescritos.  Esto es determinado por el valor retornado
        de varias funciones visit_().  Si el valor retornado es None, un
        nodo es borrado. Si se retorna otro valor, reemplaza el nodo
        original.

        El uso principal de esta clase es en el código que deseamos aplicar
        transformaciones al arbol de sintaxis.  Por ejemplo, ciertas optimizaciones
        del compilador o ciertas reescrituras de pasos anteriores a la generación
        de código.
        '''
        def generic_visit(self,node):
                for field in getattr(node,"_fields"):
                        value = getattr(node,field,None)
                        if isinstance(value,list):
                                newvalues = []
                                for item in value:
                                        if isinstance(item,AST):
                                                newnode = self.visit(item)
                                                if newnode is not None:
                                                        newvalues.append(newnode)
                                        else:
                                                newvalues.append(n)
                                value[:] = newvalues
                        elif isinstance(value,AST):
                                newnode = self.visit(value)
                                if newnode is None:
                                        delattr(node,field)
                                else:
                                        setattr(node,field,newnode)
                return node

# NO MODIFICAR
def flatten(top):
        '''
        Aplana el arbol de sintaxis dentro de una lista para efectos
        de depuración y pruebas.  Este retorna una lista de tuplas de
        la forma (depth, node) donde depth es un entero representando
        la profundidad del arból de sintaxis y node es un node AST
        asociado.
        '''
        class Flattener(NodeVisitor):
                def __init__(self):
                        self.depth = 0
                        self.nodes = []
                def generic_visit(self,node):
                        self.nodes.append((self.depth,node))
                        self.depth += 1
                        NodeVisitor.generic_visit(self,node)
                        self.depth -= 1

        d = Flattener()
        d.visit(top)
        return d.nodes