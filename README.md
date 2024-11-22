# Pr-ctica-3-Lenguajes-de-Programaci-n

Integrantes:

-Sofía Vélez Ramírez

-David Alejandro Gutiérrez Leal


# Manual de Uso
Este programa, desarrollado en Python, implementa una interfaz gráfica que permite trabajar con gramáticas libres de contexto (CFG). A través de esta herramienta, puedes realizar las siguientes acciones:

-Derivación por la izquierda: Utilizando la gramática ingresada, se muestra el paso a paso para transformar la gramática inicial en la expresión deseada, derivando siempre desde el extremo izquierdo de la expresión.

-Derivación por la derecha: Similar a la derivación por la izquierda, pero comenzando y derivando siempre desde el lado derecho de la expresión.

-Generación de árboles de análisis sintáctico: Muestra el árbol completo con todas las derivaciones necesarias para llegar a la expresión deseada.

-Generación del árbol sintáctico abstracto (AST): Proporciona una representación más simplificada del árbol de análisis sintáctico.

# Materiales Utilizados
Entorno de desarrollo: Visual Studio Code.

Versión de Python: 3.11.

Bibliotecas necesarias:

PyQt5 (para la interfaz gráfica).

NLTK (para la manipulación de gramáticas libres de contexto).

# Instalación
1. Descarga e instala Python 3.11 desde python.org.
   
2. Instala PyQt5 y NLTK usando pip:

pip install pyqt5 

pip install nltk

3. Descarga el proyecto y ábrelo en Visual Studio Code.   


# Modo de uso
Ejecuta el archivo principal del programa (main.pyw) desde Visual Studio Code.

Esto abrirá la interfaz gráfica.

Ingresa la gramática y la expresión deseada en los campos proporcionados.

La gramática debe estar escrita en una sola linea y con comas separando las reglas para cada letra, los finales deben estar entre ''

Ejemplo de gramática: 
S -> E, E -> E '+' T | E '-' T | T, T -> T '*' F | T '/' F | F, F -> 'a' | 'b' | 'x' | 'y' | '(' E ')' | NUM, NUM -> '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '0'

Para la ingresar la expresion a derivar debe separar cada caracter con espacios.
ejemplo:
5 + 3 * 8

Seleccionar si se quiere derivar por izquierda o por derecha, solo se puede seleccionar una de estas opciones a la vez, no seleccionar ninguna tambien resultara en un error.

Seleccionar alguno de los arboles no es obligatorio, solo se puede seleccionar un arbol a la vez.

Pulsar el boton de "generar derivacion" y la derivacion aparecera en el campo de texto adyacente, si se selecciono un arbol este abrira una widget aparte.

# Entender la derivación:
Al derivar una expresion el resultado sera algo asi:

   S
   
   E
   
   E + T
   
   T + T
   
   F + T
   
   NUM + T
   
   5 + T
   
   5 + T * F
   }
   5 + F * F
   
   5 + NUM * F
   
   5 + 3 * F
   
   5 + 3 * NUM
   
   5 + 3 * 8
   
   
Dependiendo si se eligio derivar por derecha o izquierda, cada linea nueva es el cambio que se realizo, cada linea es el paso a paso y se puede verificar con las reglas de gramatica intrioducidas previamente.

