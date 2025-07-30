# string => "Hola, qué tal?"
# number => 23, 3.14
# booleans => True o False #En mayúsculas
# null o undefined => None

# Objeto literal(Diccionario en Python) => {"nombre": "Carlos", "apellido":"Guilarte"}

# Array (List en Python) => ["manzana", "pera"]

# funciones(JS vs Pythons) => function nombreFuncion(){  vs   def nombreFuncion():
#                                código                          código
#                           }

#    en python no hay llaves, el código de la funcion siempre tiene que ir tabulada dentro.
# La tabulación es muy importante, ya que no suele haber {} ni ; que delimiten el código

# Si en html y css usabamos kebab-case , en JS camelCase y en React PascalCase
# En Python se utiliza snake_case

# name = "Carlos"
# age = 29
# is_active = True
# user = None

# person = {
#     "name" : "Carlos",
#     "age" : 29
# }

# fruits = ["manzana", "pera"]
# fruits.append("naranja") #este sería el Array.push() de Python

# dias_semana = ("Lunes", "Martes", "...", "Domingo") #Esto se llama tupla, va entre paréntesis y es igual que una lista, pero es inmutable. No se podrá modificar

# def saludar(nombre):
#     print("Hola a todo el mundo, soy " + nombre)

# saludar("Carlos")

# print(name)   #print sería el console.log de Python
# print(age)
# print(is_active)
# print(person["name"]) #En python ya no se usa person.name, sino con corchetes person["name"]
# print(fruits[0])
# print(fruits)
# print(fruits[2])
# print(dias_semana[2])


def saludar(nombre):

    if nombre == "Judith":
        print("hola, " + nombre)
    else:  # así se declara un if-else. Observar las tabulaciones
        print("hola, extraño")


saludar("Judith")
saludar("Carlos")

fruits = ["manzana", "pera", "naranja"]

# array.map ((item)=>procesado)

# en python: map(funcion lambda, lista)

# function(){}
# ()=>{}
# lambda parametros:codigo que queremos que se ejecute

# results = map(lambda item : item + "s", fruits)  # Esto en JS sería results = fruits.map((item) => item + "s")

# print(results)                      #Lo devuelve en código máquina, ilegible para nosotros, es lo que devuelve un map, filter, etc

# #Lo que en JS era parse, en python es hacer cast
# #Estos son los cast(antes parse) más comununes: int(), list(), dictt(), str()

# print(list(results))                #Al castearlo a lista, ya se muestra correctamente para nosotros

# entonces para tener directamente la lista mapeada, sería mejor

results = list(map(lambda item: item + "s", fruits))

print(results)
