"""
@name : Robot_test.py
@description : Execution des tests robot avec une communication série
@author : Alexis Parquet
@email : parquetalexis.pro@outlook.fr
"""
import serial
import time

NB_CARACTERE = 60

""" Classe pour la communication série """
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

""" Classe pour définir les tests """
class TestCase:

    """ Initialisation de la classe """
    def __init__(self):
        print("Initialisation de la communication série")
        self.robot_com = SerialCom()
        time.sleep(1)
        if self.robot_com.com.isOpen():
            print("#" * NB_CARACTERE)
            print("DEMARRAGE DES TESTS")
            print("#" * NB_CARACTERE)

    """ Fonction de fermeture de la communication série """
    def close_com(self):
        print("Fermeture de la communication série")
        self.robot_com.close_serial()

    """ Fonction de test unitaire """
    def unit_test(self, test_name: str, command_to_send: str, expected_result: str, waiting_time: int = 0):

        print("-" * NB_CARACTERE)
        print(f"Description : {test_name}")

        if waiting_time > 0:
            print(f"Temps d'attente : {waiting_time} secondes")

        print(f"Envoie : {command_to_send}")
        result_cmd = self.robot_com.send_command(command_to_send)
        print(f"Réponse : {result_cmd}")

        print(f"Result : {"✅ PASS" if expected_result == result_cmd else "❌ FAIL"}")

        print("-" * NB_CARACTERE)

    def title_test(self, case_number: int, case_name: str):
        print("=" * NB_CARACTERE)
        print(f"CAS DE TEST {case_number} : {case_name}")
        print("=" * NB_CARACTERE)

if __name__ == "__main__":
    unit_tests_robot = TestCase()

    unit_tests_robot.title_test(1, "Communication")

    unit_tests_robot.unit_test("Envoyer une commande correcte", "/01 get pos","@01 OK 0")
    unit_tests_robot.unit_test("Envoyer une commande incorrecte", "/01 run 10", "@01 RJ 0")
    unit_tests_robot.unit_test("Envoyer une commande avec un identifiant invalide", "/00 get pos", "")
    unit_tests_robot.unit_test("Envoyer une commande avec un identifiant inaccessible", "/20 get pos", "")
    unit_tests_robot.unit_test("Envoyer une commande sans « / »", "01 get pos", "")
    unit_tests_robot.unit_test("Envoyer une commande sans adresse", "/ get pos", "")
    unit_tests_robot.unit_test("Vérifier la tolérance de la commande en ajoutant un espace au début", " /01 get pos", "@01 OK 0")
    unit_tests_robot.unit_test("Vérifier la tolérance de la commande en ajoutant un espace à la fin", "/01 get pos ", "@01 OK 0")
    unit_tests_robot.unit_test("Vérifier la tolérance de la commande en ajoutant un espace au milieu", "/01 get  pos", "@01 OK 0")

    unit_tests_robot.close_com()