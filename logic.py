from PyQt5 import QtCore, QtGui, QtWidgets
import nltk
from nltk import CFG
from nltk.tree import Tree


class TreeWindow(QtWidgets.QWidget):
    def __init__(self, tree_text, parent=None):
        super(TreeWindow, self).__init__(parent)
        self.setWindowTitle("Árbol Sintáctico")
        self.setGeometry(200, 200, 400, 600)
        self.tree_display = QtWidgets.QTextBrowser(self)
        self.tree_display.setGeometry(10, 10, 380, 580)
        self.tree_display.setPlainText(tree_text)


class Ui_Interface(object):
    def setupUi(self, Interface):
        Interface.setObjectName("Interface")
        Interface.resize(826, 589)
        self.label = QtWidgets.QLabel(Interface)
        self.label.setGeometry(QtCore.QRect(70, 370, 131, 51))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Interface)
        self.label_2.setGeometry(QtCore.QRect(10, 390, 161, 61))
        self.label_2.setObjectName("label_2")
        self.textExpresion = QtWidgets.QTextEdit(Interface)
        self.textExpresion.setGeometry(QtCore.QRect(0, 320, 221, 61))
        self.textExpresion.setObjectName("textExpresion")
        self.IzquierdaCheck = QtWidgets.QCheckBox(Interface)
        self.IzquierdaCheck.setGeometry(QtCore.QRect(10, 430, 161, 31))
        self.IzquierdaCheck.setObjectName("IzquierdaCheck")
        self.DerechaCheck = QtWidgets.QCheckBox(Interface)
        self.DerechaCheck.setGeometry(QtCore.QRect(10, 460, 161, 21))
        self.DerechaCheck.setObjectName("DerechaCheck")
        self.textGramatica = QtWidgets.QTextEdit(Interface)
        self.textGramatica.setGeometry(QtCore.QRect(0, 0, 221, 311))
        self.textGramatica.setObjectName("textGramatica")
        self.textDerivacion = QtWidgets.QTextBrowser(Interface)
        self.textDerivacion.setGeometry(QtCore.QRect(230, 0, 271, 571))
        self.textDerivacion.setObjectName("textDerivacion")
        self.GenerarButton = QtWidgets.QPushButton(Interface)
        self.GenerarButton.setGeometry(QtCore.QRect(40, 520, 121, 31))
        self.GenerarButton.setObjectName("GenerarButton")
        self.textArbol = QtWidgets.QTextBrowser(Interface)
        self.textArbol.setGeometry(QtCore.QRect(510, 0, 291, 571))
        self.textArbol.setObjectName("textArbol")
        self.ArbolCheck = QtWidgets.QCheckBox(Interface)
        self.ArbolCheck.setGeometry(QtCore.QRect(10, 480, 111, 20))
        self.ArbolCheck.setObjectName("ArbolCheck")
        self.AbsCheck = QtWidgets.QCheckBox(Interface)
        self.AbsCheck.setGeometry(QtCore.QRect(10, 500, 161, 20))
        self.AbsCheck.setObjectName("AbsCheck")

        self.retranslateUi(Interface)
        QtCore.QMetaObject.connectSlotsByName(Interface)

        # Connect functionality
        self.GenerarButton.clicked.connect(self.generar_derivacion)

        # Initialize tree window variable
        self.tree_window = None

    def retranslateUi(self, Interface):
        _translate = QtCore.QCoreApplication.translate
        Interface.setWindowTitle(_translate("Interface", "Derivación con CFG"))
        self.label.setText(_translate("Interface", "Opciones de Derivación"))
        self.label_2.setText(_translate("Interface", "Seleccionar Derivación:"))
        self.IzquierdaCheck.setText(_translate("Interface", "Derivación por la Izquierda"))
        self.DerechaCheck.setText(_translate("Interface", "Derivación por la Derecha"))
        self.GenerarButton.setText(_translate("Interface", "Generar Derivación"))
        self.ArbolCheck.setText(_translate("Interface", "Dibujar árbol"))
        self.AbsCheck.setText(_translate("Interface", "Dibujar árbol abstracto"))

    def generar_ast(self, arbol):
        if isinstance(arbol, Tree):
            operadores = {"+", "-", "*", "/"}
            if arbol.label() in operadores:
                return Tree(arbol.label(), [self.generar_ast(hijo) for hijo in arbol])
            hijos_procesados = [self.generar_ast(hijo) for hijo in arbol]
            if len(hijos_procesados) == 1:
                return hijos_procesados[0]
            else:
                return Tree(arbol.label(), hijos_procesados)
        elif isinstance(arbol, str):
            return Tree(arbol, [])
        else:
            return arbol

    def generar_derivacion(self):
        texto_gramatica = self.textGramatica.toPlainText()
        texto_expresion = self.textExpresion.toPlainText().strip()

        if not self.IzquierdaCheck.isChecked() and not self.DerechaCheck.isChecked():
            QtWidgets.QMessageBox.warning(None, "Advertencia", "Selecciona al menos un método de derivación.")
            return
        if self.IzquierdaCheck.isChecked() and self.DerechaCheck.isChecked():
            QtWidgets.QMessageBox.warning(None, "Advertencia", "No puedes seleccionar ambos métodos de derivación a la vez.")
            return

        try:
            reglas = texto_gramatica.strip().split(',')
            gramatica_texto = "\n".join([regla.strip() for regla in reglas])
            gramatica = CFG.fromstring(gramatica_texto)
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Error al cargar la gramática: {e}")
            return

        expresion = texto_expresion.split()
        if not all(any(token in prod.rhs() for prod in gramatica.productions()) for token in expresion):
            QtWidgets.QMessageBox.critical(None, "Error", "La expresión contiene tokens no cubiertos por la gramática.")
            return

        parser = nltk.ChartParser(gramatica)
        modo = "izquierda" if self.IzquierdaCheck.isChecked() else "derecha"

        try:
            if modo == "izquierda":
                arbol = next(parser.parse(expresion))
            else:
                arbol = next(parser.parse(expresion[::-1]))

            pasos_derivacion = [arbol[0].label()]
            derivacion_actual = [arbol[0].label()]

            for produccion in arbol.productions():
                if modo == "izquierda":
                    index = next((i for i, simbolo in enumerate(derivacion_actual) if simbolo == str(produccion.lhs())), None)
                else:
                    index = next((i for i, simbolo in reversed(list(enumerate(derivacion_actual))) if simbolo == str(produccion.lhs())), None)

                if index is not None:
                    derivacion_actual = (
                        derivacion_actual[:index] +
                        [str(sym) for sym in produccion.rhs()] +
                        derivacion_actual[index + 1:]
                    )
                    pasos_derivacion.append(" ".join(derivacion_actual))

            resultado = f"Derivación por {'la izquierda' if modo == 'izquierda' else 'la derecha'}:\n\n"
            resultado += "\n".join(pasos_derivacion)
            self.textDerivacion.setPlainText(resultado)

            if self.AbsCheck.isChecked():
                ast = self.generar_ast(arbol)
                if ast is not None:
                    ast.draw()
                else:
                    QtWidgets.QMessageBox.critical(None, "Error", "No se pudo generar el Árbol Abstracto de Sintaxis.")
            elif self.ArbolCheck.isChecked():
                arbol.draw()
            else:
                self.textArbol.clear()

        except StopIteration:
            QtWidgets.QMessageBox.critical(None, "Error", "No se pudo derivar la expresión.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Error durante la derivación: {e}")

    def show_tree(self, tree):
        if self.tree_window is None:
            self.tree_window = TreeWindow(str(tree))
            self.tree_window.show()
        else:
            self.tree_window.tree_display.setPlainText(str(tree))
