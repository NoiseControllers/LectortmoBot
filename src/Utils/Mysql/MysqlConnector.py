import mysql.connector
import mysql.connector.locales.eng.client_error
from mysql.connector import InterfaceError, ProgrammingError

from src.Utils.ConfigManagement.ConfigManagement import ConfigManagement


class MysqlConnector:
    def __init__(self):
        self._config = ConfigManagement().config()

    def connect(self) -> mysql.connector.connect():
        try:
            return mysql.connector.connect(
                host=self._config.get('Mysql', 'hostname'),
                user=self._config.get('Mysql', 'user'),
                passwd=self._config.get('Mysql', 'password'),
                database=self._config.get('Mysql', 'database')
            )
        except InterfaceError:
            print("[-][ERROR][MYSQL] No se puede establecer una conexión ya que el equipo de destino denegó expresamente dicha conexión")
            print("Pulse cualquier tecla para salir...")
            input()
            exit(0)
        except ProgrammingError as e:
            print("[-][ERROR][MYSQL] ", e)
            print("Pulse cualquier tecla para salir...")
            input()
            exit(0)
