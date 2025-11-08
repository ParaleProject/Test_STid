"""
@name : Robot_test.py
@description : Execution des tests robot avec une communication série
@author : Alexis Parquet
@email : parquetalexis.pro@outlook.fr
"""
import serial
import time


""" Classe pour la communication série"""
class SerialCom:

    def __init__(self,port="COM3",bauds=9600, timeout=1):
        try:
            self.com = serial.Serial(
                port=port,
                baudrate=bauds,
                timeout=timeout,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_ODD,
                stopbits=serial.STOPBITS_ONE
            )
            time.sleep(1)
        except serial.SerialException as err:
            print(f"[ERREUR] Impossible de communiquer avec le port {port} : {err}")
            self.com = None

    def send_command(self, cmd: str) -> str:

        if not self.com or not self.com.isOpen():
            print(f"[ERREUR] Port série non disponible, la commande n'a pas pu être envoyée")
            return ""

        try:
            send_command = f"{cmd}\n".encode("ascii")
            self.com.write(send_command)
            self.com.flush()
            receive_command = self.com.readline().decode("ascii", errors="ignore").strip()
            return receive_command
        except serial.SerialException as err:
            print(f"[ERREUR] L'envoie de la commande {cmd} n'a pas abouti : {err}")
            return ""
        except Exception as err:
            print(f"[ERREUR] {err}")
            return ""

    def close_serial(self):
        if self.com and self.com.isOpen():
            self.com.close()


if __name__ == "__main__":
    serial_com = SerialCom()
    response = serial_com.send_command("TEST")
    print(response)