Para la correcta ejecucion de la aplicacion, seran necesarios un archivo Json, el cual contendra informacion sobre la criticidad de diferentes bases de datos, como tambien informacion del owner.
En principio se verifica la infromacion que se posee sobre dicha base de datos, luego en caso de que se posean todos los datos necesarios, se le envia un correo al manager del owner para solicitarle la validacion de la clasificacion de la base de datos.
En caso de que la informacion se encuentre incompleta, se envia otro correo solicitando que completen la infromacion necesaria.

La clasificacion de la criticidad de la base de datos, viene dada por los tres pilares de la seguridad de la informacion:
Disponibilidad
Integridad
Confidencialidad

Se considera que con que uno de ellos sea alto la base de datos tendra una criticidad alta ya que la asuencia de alguno podria generar un incidente de seguridad de la infromacion.

Aclaracion sobre la falta de infromacion:
Si este aplicativo fuese utilizado en una corporacion que posee Active Directory o algun explorador de cliente como Softerra LDAP Administrator, lo utilizaria para realizar la consulta del email del colaborador.