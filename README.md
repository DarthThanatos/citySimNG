# citySimNG
Silnik gry ekonomicznej

Projekt dotyczy silnika gier strategicznych typu RTS, który będzie umożliwiał tworzenie i późniejsze wczytywanie zdefiniowanych przez użytkownika zasad gry oraz prowadzanie rozgrywki. Podczas rozgrywki gracz będzie miał możliwość rozwoju poprzez budowę budynków, opracowanie nowych technologii, udział w giełdzie sterowanej częściowo przez AI, pozyskiwanie zasobów i zarządzanie mieszkańcami miasta. Wszystkie akcje użytkownika będą odbywały się przy użyciu prostego interfejsu graficznego.

Podstawowe funkcjonalności:
* stworzenie zestawu zasad rozgrywki, w tym wpływ na wygląd utworzonych budynków
* uruchomienie rozgrywki w określonymi zasadami
* prowadzanie rozgrywki jednoosobowej
* korzystanie z interaktywnego samouczka dla gracza
* wyjście z gry

Wykorzystywane technologie:
* Java 8
* Python 2.7
* Pygame (można pobrać przy użyciu komendy pip install pygame)
* WxPython (najlepiej pobrać z https://wxpython.org/download.php#msw, może nie współpracować z komendą pip)
* Matplotlib (można pobrać przy użyciu pip install matplotlib)
* JSON (w katalogu lib, plik json.jar)
* gradle 
(opis instalacji: https://gradle.org/install
pobrać wersję 3.5 binary-only z: https://gradle.org/releases)

Problemy:
Jeśli po pobraniu projektów i otworzeniu ich w środowisku Eclipse dostajemy powiadomienie o błędach, należy:
* Rozwinąć panel projektów w Eclipse 
* Poniższe operacje wykonać na projektach: SkeletonModule, MapModule i CreatorModule
1. Kliknąć PPM, wybrać Build Path > Configure Build Path ...
2. Przejść do zakładki libraries, podkreślony plik jar usunąć
3. Dodać ścieżkę do pliku (idąc od głównego katalogu projektu): lib/json.jar

Jak uruchomić:
Implementacja  modułów javowych zalecana jest wewnątrz środowiska Eclipse (zapewnia to odpowiednią strukturę projektu niezbędną
dla modułu SystemMainController). Do modułów implementowanych w języku Python nie ma preferencji (chociaż autorzy polecają
Pycharma bądź edytor Sublime).
 
Po dokonaniu zmian w projekcie najłatwiej jest go uruchomić poprzez dwukrotne kliknięcie
na skrypt run.bat znajdującym się w głównym katalogu. Jest to zalecany sposób uruchamiania projektu.

W przypadku prób uruchomienia w poszczególnych środowiskach łatwo zapomnieć, że część javowa i pythonowa
muszą być obie uruchomione - np. użytkownik uruchomi widok i może minąć chwila zanim uświadomi sobie, że 
kontroler nie został włączony; to samo dotyczy niszczenia procesów; żeby włączyć poprawnie projekt, wcześniejsze
procesy skojarzone bgEngine muszą zostać unicestwione; najprościej jest to osiągnąć poprzez zniszczenie okna towarzyszącego
aplikacji po uruchomieniu skryptu. 

UWAGA: katalogiem "domowym" projektu zakłada się katalog bgEngine; znajdują się tutaj pliki które są niezbędne 
przy uruchamianiu widoku, takie jak tekstury, jar, .mp3 itp.
Próba uruchomienia w różnych środowiskach może poskutkować nierozwiązanymi ścieżkami, natomiast zmienianie struktury katalogów
może spowodować utratę kompatybilności z już napisanym kodem; nie wspominając, że zmieniając strukturę, możemy doprowadzić
do bałaganu. Zachęcamy do korzystania z już ustalonych przez twórców wzorców.


