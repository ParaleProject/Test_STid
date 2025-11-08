"""
@name : Robot_test.py
@description : Execution des tests robot avec une communication série
@author : Alexis Parquet
@email : parquetalexis.pro@outlook.fr
"""
import serial
import time

NB_CARACTERE = 60

class SerialCom:
    """ Classe pour la communication série """

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
        """ Fonction pour envoyer une commande """

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
        """ Fonction pour fermer la connexion """
        if self.com and self.com.isOpen():
            self.com.close()


class TestCase:
    """ Classe pour définir les tests """

    """ Variables """
    id_test = 0
    name_test = ""
    test_case_data = {'passed' : 0, 'failed' : 0, 'total' : 0}
    test_total_data = {}


    def __init__(self):
        """ Initialisation de la classe """
        print("Initialisation de la communication série")
        self.robot_com = SerialCom()
        time.sleep(1)
        if self.robot_com and self.robot_com.com.isOpen():
            print("#" * NB_CARACTERE)
            print("DEMARRAGE DES TESTS")
            print("#" * NB_CARACTERE)

    def close_com(self):
        """ Fonction de fermeture de la communication série """
        print("Fermeture de la communication série")
        self.robot_com.close_serial()

    def reset_count_test(self):
        self.test_case_data['passed'] = 0
        self.test_case_data['failed'] = 0
        self.test_case_data['total'] = 0

    def unit_test(self, test_name: str, command_to_send: str, expected_result: str, waiting_time: int = 0):
        """ Fonction de test unitaire """

        print("-" * NB_CARACTERE)
        print(f"Description : {test_name}")

        if waiting_time > 0:
            print(f"Temps d'attente : {waiting_time} secondes")
            time.sleep(waiting_time)

        print(f"Envoie : {command_to_send}")
        result_cmd = self.robot_com.send_command(command_to_send)
        print(f"Réponse : {result_cmd}")

        self.test_case_data['total'] += 1

        if result_cmd == expected_result:
            print(f"Result : ✅ PASS")
            self.test_case_data['passed'] += 1
        else:
            print(f"Result : ❌ FAIL")
            self.test_case_data['failed'] += 1

        print("-" * NB_CARACTERE)

    def set_case_test(self, case_number: int, case_name: str):
        """ Fonction pour afficher le titre du cas de test """
        self.id_test = case_number
        self.name_test = case_name
        print("=" * NB_CARACTERE)
        print(f"CAS DE TEST {case_number} : {case_name}")
        print("=" * NB_CARACTERE)

    def save_case_test_result(self):
        self.test_total_data[self.id_test] = {
            'title' : self.name_test,
            'passed' : self.test_case_data['passed'],
            'failed' : self.test_case_data['failed'],
            'total' : self.test_case_data['total']
        }
        self.reset_count_test()

    def get_result(self, id_case_test: int=None, all: bool=False):

        passed = 0
        failed = 0
        total = 0

        if all:
            print("#" * NB_CARACTERE)
            print("RESULTATS GLOBAL DES TESTS")
            print("#" * NB_CARACTERE)
            for keys, values in self.test_total_data.items():
                passed += values['passed']
                failed += values['failed']
                total += values['total']
            print(f"Nombre de test : {total}")
            print(f"Test réussis : {passed}")
            print(f"Test échoués : {failed}")
            percent = (passed / total * 100) if total else 0
            print(f"Taux de réussite : {percent:.2f} %")
            print("#" * NB_CARACTERE)
        elif id_case_test and self.test_total_data[id_case_test]:
            print("#" * NB_CARACTERE)
            print(f"RESULTATS DU CAS DE TEST {id_case_test} : {self.test_total_data[id_case_test]['title']}")
            print("#" * NB_CARACTERE)
            print(f"Nombre de test : {self.test_total_data[id_case_test]['total']}")
            print(f"Test réussis : {self.test_total_data[id_case_test]['passed']}")
            print(f"Test échoués : {self.test_total_data[id_case_test]['failed']}")
            percent = (self.test_total_data[id_case_test]['passed'] / self.test_total_data[id_case_test]['total'] * 100) if \
                self.test_total_data[id_case_test]['total'] else 0
            print(f"Taux de réussite : {percent:.2f} %")
            print("#" * NB_CARACTERE)
        elif not id_case_test and self.test_total_data[self.id_test]:
            print("#" * NB_CARACTERE)
            print(f"RESULTATS DU CAS DE TEST {self.id_test} (En cours): {self.test_total_data[self.id_test]['title']}")
            print("#" * NB_CARACTERE)
            print(f"Nombre de test : {self.test_total_data[self.id_test]['total']}")
            print(f"Test réussis : {self.test_total_data[self.id_test]['passed']}")
            print(f"Test échoués : {self.test_total_data[self.id_test]['failed']}")
            percent = (self.test_total_data[self.id_test]['passed'] / self.test_total_data[self.id_test][
                'total'] * 100) if \
                self.test_total_data[self.id_test]['total'] else 0
            print(f"Taux de réussite : {percent:.2f} %")
            print("#" * NB_CARACTERE)
        else:
            print("#" * NB_CARACTERE)
            print("[ERREUR] Aucun résultat n'est disponible")
            print("#" * NB_CARACTERE)
        print("\n")



if __name__ == "__main__":
    unit_tests_robot = TestCase()

    unit_tests_robot.set_case_test(1, "Syntax des commandes")

    unit_tests_robot.unit_test("Envoyer une commande correcte", "/01 get pos","@01 OK 0")
    unit_tests_robot.unit_test("Envoyer une commande incorrecte", "/01 run 10", "@01 RJ 0")
    unit_tests_robot.unit_test("Envoyer une commande avec un identifiant invalide", "/00 get pos", "")
    unit_tests_robot.unit_test("Envoyer une commande avec un identifiant inaccessible", "/20 get pos", "")
    unit_tests_robot.unit_test("Envoyer une commande sans « / »", "01 get pos", "")
    unit_tests_robot.unit_test("Envoyer une commande sans adresse", "/ get pos", "")
    unit_tests_robot.unit_test("Vérifier la tolérance de la commande en ajoutant un espace au début", " /01 get pos", "@01 OK 0")
    unit_tests_robot.unit_test("Vérifier la tolérance de la commande en ajoutant un espace à la fin", "/01 get pos ", "@01 OK 0")
    unit_tests_robot.unit_test("Vérifier la tolérance de la commande en ajoutant un espace au milieu", "/01 get  pos", "@01 OK 0")

    unit_tests_robot.save_case_test_result()
    unit_tests_robot.get_result()

    unit_tests_robot.set_case_test(2, "Commande get")

    unit_tests_robot.unit_test("Déterminer la valeur de la vitesse à 5", "/01 set speed 5", "@01 OK 0")
    unit_tests_robot.unit_test("Vérifier si la commande « get speed » récupère la bonne valeur (5)", "/01 get speed", "@01 OK 5")
    unit_tests_robot.unit_test("Récupérer la position du robot", "/01 get pos", "@01 OK 0")
    unit_tests_robot.unit_test("Effectuer un déplacement du robot de 100 unités", "/01 move 100", "@01 OK 0")
    unit_tests_robot.unit_test("Attendre la fin du déplacement et récupérer à nouveau la position du robot", "/01 get pos", "@01 OK 100", 0)
    unit_tests_robot.unit_test("Envoyer une commande « get » incomplète", "/01 get", "@01 RJ 0")
    unit_tests_robot.unit_test("Envoyer une mauvaise commande « get »", "/01 get status", "@01 RJ 0")

    unit_tests_robot.save_case_test_result()
    unit_tests_robot.get_result()

    unit_tests_robot.get_result(all=True)

    unit_tests_robot.close_com()