#!/usr/bin/env python3

import json
import os
import random

_STATE_FILE = 'state.json'


def main():
    state = _load_or_init_state()
    while True:
        _ask_question(_pick_question(state), state)
        _save_state(state)


def _load_or_init_state():
    if os.path.isfile(_STATE_FILE):
        with open(_STATE_FILE) as f:
            return json.load(f)
    else:
        return _init_state()


def _save_state(state):
    with open(_STATE_FILE, 'w') as f:
        json.dump(state, f)


def _pick_question(state):
    questions = list(state['q'])
    random.shuffle(questions)
    best = questions[0]

    for question in state['q']:
        if (question['correct'] + question['incorrect'] < best['correct'] + best['incorrect'] or 
            (question['correct'] + question['incorrect'] == best['correct'] + best['incorrect'] and
             question['incorrect'] > best['incorrect'])):
            best = question

    return best
            

def _ask_question(question, state):
    print('(correct: {}, incorrect: {}, total correct: {}, total incorrect: {})'.format(
        question['correct'],
        question['incorrect'],
        sum(q['correct'] for q in state['q']),
        sum(q['incorrect'] for q in state['q']),
    ))

    print(question['text'])
    print()

    letters = [answer['letter'] for answer in question['answers']]
    answers = list(question['answers'])
    correct_answer = answers[0]
    random.shuffle(answers)

    for letter, answer in zip(letters, answers):
        print('{} {}'.format(letter, answer['text']))
        if answer is correct_answer:
            correct_letter = letter

    print()

    while True:
        user_input = input('Answer: ').upper()
        if user_input in letters:
            break
    
    if user_input == correct_letter:
        print('Correct!')
        question['correct'] += 1
    else:
        print('Incorrect! The right answer was:')
        print('{} {}'.format(correct_letter, correct_answer['text']))
        question['incorrect'] += 1

    print()
        

def _init_state():
    state = {'q': []}
    lines = QUESTIONS.splitlines()
    line_index = 1
    question_index = 1

    while line_index < len(lines):
        question = lines[line_index]
        assert question.startswith('{} '.format(question_index)), question_index

        line_index += 2
        answers = []
        for letter in ['A', 'B', 'C', 'D']:
            answer = lines[line_index]
            prefix = '{} '.format(letter)
            assert answer.startswith(prefix), answer
            answers.append({'letter': letter, 'text': answer[len(prefix):]})
            line_index += 1

        line_index += 1
        question_index += 1

        state['q'].append({'text': question, 'answers': answers, 'correct': 0, 'incorrect': 0})
    
    return state
        


QUESTIONS = """
1 Welche zwischenstaatliche Organisation hat für den weltweiten Flugfunkdienst besondere Bedeutung?

A ITU
B IATA
C UNESCO
D NATO

2 Was ist die rechtliche Grundlage für das Errichten und Betreiben von Funkanlagen in der Bundesrepublik Deutschland?

A Das Telekommunikationsgesetz (TKG)
B Das Luftverkehrsgesetz
C Das Internationale Zivile Luftfahrtabkommen
D Die Verordnung über die Flugsicherungsausrüstung der Luftfahrzeuge

3 Wer ist in der Bundesrepublik Deutschland für Frequenzzuteilungen zum Betrieb von Boden- und Luftfunkstellen zuständig?

A Die Bundesnetzagentur
B Der Bundesminister des Innern
C Die Luftfahrtbehörden der Länder
D Das Flugsicherungsunternehmen (DFS)

4 Wer benötigt zur Durchführung des Sprechfunkverkehrs ein Flugfunkzeugnis?

A Der Luftsportgeräteführer im Luftraum D
B Der Flugschüler an Bord eines Ausbildungsluftfahrzeuges in der Platzrunde eines unkontrollierten Flugplatzes
C Der Betreiber einer Bodenfunkstelle, die ausschließlich der Übermittlung von Flugbetriebsmeldungen dient
D Der Flugschüler an Bord eines Ausbildungsluftfahrzeuges in der Platzrunde eines kontrollierten Flugplatzes

5 Wer benötigt zur Durchführung des Sprechfunkverkehrs kein Flugfunkzeugnis?

A Betreiber einer Funkstelle mit dem Rufzeichen "RÜCKHOLER"
B Fluglotse
C Flugleiter an einem Segelfluggelände
D Luftsportgeräteführer im Luftraum C

6 Wer benötigt zur Durchführung des Sprechfunkverkehrs kein Flugfunkzeugnis?

A Flugschüler in der Platzrunde von Flugplätzen mit / ohne Flugverkehrskontrolle
B Fluglotse
C Flugleiter an einem Landeplatz
D Beauftragte für Luftaufsicht

7 Wozu berechtigt das "Beschränkt Gültige Sprechfunkzeugnis II für den Flugfunkdienst" (BZF II)? Zur Ausübung des Sprechfunkverkehrs ...

A in deutscher Sprache innerhalb der Bundesrepublik Deutschland
B bei VFR-Flügen in englischer Sprache
C bei IFR-Flügen
D in deutscher und englischer Sprache bei allen deutschen Bodenfunkstellen

8 Wozu berechtigt das "Beschränkt Gültige Sprechfunkzeugnis II für den Flugfunkdienst" (BZF II)? Zur Ausübung des Sprechfunkverkehrs bei ...

A VFR-Flügen innerhalb der Bundesrepublik Deutschland in deutscher Sprache
B VFR-Flügen innerhalb der Bundesrepublik Deutschland in englischer Sprache
C IFR-Flügen
D VFR-Flügen in einer der ICAO-Sprachen

9 Welches Flugfunkzeugnis wird benötigt, um den Sprechfunkverkehr in deutscher und englischer Sprache nach Sichtflugregeln durchführen zu dürfen?

A BZF I
B BZF II
C Kein Flugfunkzeugnis, da es sich um einen VFR-Flug handelt
D Kein Flugfunkzeugnis, wenn der Fluglehrer einen schriftlichen Flugauftrag erteilt hat

10 Was ist eine Luftfunkstelle? Eine Funkstelle ...

A des beweglichen Flugfunkdienstes an Bord eines Luftfahrzeuges
B an Bord eines Flugzeugträgers
C des beweglichen Flugfunkdienstes an einem internationalen Verkehrsflughafen
D des beweglichen Flugfunkdienstes an einem Landeplatz

11 Was ist eine Bodenfunkstelle?

A Eine ortsfeste Funkstelle im beweglichen Flugfunkdienst. In bestimmten Fällen an Bord eines Seefahrzeugs oder auf einer Plattform auf See
B Eine Funkstelle des festen Flugfernmeldedienstes
C Jede Funkstelle zur Aussendung von Funksprüchen
D Eine Funkstelle des Flugfernmeldedienstes an Land oder an Bord eines Schiffes für den Austausch von Funkmeldungen

12 Was bedeutet der Begriff "BLINDSENDUNG"?

A Das Übermitteln einer Meldung an einen Empfänger, wenn Wechselsprechverkehr nicht hergestellt werden kann, unter der Annahme, dass die gerufene Station die Meldung empfangen kann
B Eine Übermittlung von meteorologischen und flugbetrieblichen Informationen für Flugzeuge über der hohen See oder Wüstengebieten außerhalb der Funküberdeckung von UKW-Bodenfunkstellen
C Eine Übermittlung von Informationen für die Luftfahrt, die nicht an einen bestimmten Empfänger gerichtet ist
D Ein Funkspruch, dessen Erhalt vom Empfänger wiederholt werden muss

13 Was bedeutet der Begriff "ALLGEMEINER ANRUF"?

A Eine Übermittlung von Informationen für die Luftfahrt, die nicht an eine oder mehrere bestimmte Stellen gerichtet ist
B Die Übermittlung von Meldungen über Wettererscheinungen, welche die Sicherheit des Flugbetriebes betreffen können, die an eine oder mehrere bestimmte Stellen gerichtet ist
C Eine Übermittlung, deren Empfang bestätigt werden muss
D Eine Meldung mittels Sprechfunk von einer Bodenfunkstelle an eine bestimmte Luftfunkstelle

14 Was bedeutet der Begriff "ROLLHALT"?

A Ein bezeichneter Ort zum Schutz einer Piste, einer Hindernisbegrenzungsfläche, an dem rollende Luftfahrzeuge und Fahrzeuge anhalten und warten müssen
B Eine nicht markierte Position auf dem Abstellplatz für die Allgemeine Luftfahrt
C Eine markierte Position auf einer Startbahn, wo der Startlauf begonnen wird
D Jeder markierte Abstellplatz auf dem Vorfeld eines Verkehrsflughafens

15 Welche Abkürzung wird für den Begriff "KONTROLLZONE" verwendet?

A CTR
B CZ
C CTZ
D CTA

16 Welche Bedeutung hat die Abkürzung "IMC"?

A Instrumentenwetterbedingungen
B Sichtwetterbedingungen
C Instrumentenflug
D Sichtflug

17 Welche Bedeutung hat die Abkürzung "FIR"?

A Fluginformationsgebiet
B Fluginformations-Radar
C Fluginformation erbeten
D Fluginformation erhalten

18 Was bedeutet die Abkürzung "H24"?

A Ununterbrochener Betrieb bei Tag und Nacht
B Sonnenuntergang bis Sonnenaufgang
C Keine festgelegte Betriebszeit
D Höhe 2400 Fuss

19 Was bedeutet die Abkürzung "HX"?

A Keine festgelegte Betriebszeit
B Höhe nicht festgelegt
C Sonnenaufgang bis Sonnenuntergang
D Ununterbrochener Betrieb bei Tag und Nacht

20 Was bedeutet die Abkürzung "HJ"?

A Sonnenaufgang bis Sonnenuntergang
B Keine festgelegte Betriebszeit
C Sonnenuntergang bis Sonnenaufgang
D Ununterbrochener Betrieb bei Tag und Nacht

21 Welche Bedeutung hat die Abkürzung "AIS"?

A Flugberatungsdienst
B Flughafeninformationssystem
C Allgemeine Informationsstelle
D Allwetter-Informationssystem

22 Welche Bedeutung hat die Abkürzung "SAR"?

A Such- und Rettungsdienst
B "STOPP AM ROLLHALT"
C Sekundär-Anflugradar
D Standardanflugroute

23 Welche Abkürzung wird für den Begriff "KOORDINIERTE WELTZEIT" verwendet?

A UTC
B GMT
C Z-Zeit
D CUT

24 Welche Bedeutung hat die Abkürzung "ATIS"?

A Automatische Ausstrahlung von Lande- und Startinformationen (AUTOMATIC TERMINAL INFORMATION SERVICE)
B Flugverkehrsinformationsdienst (AIR TRAFFIC INFORMATION SERVICE)
C Flughafengebäude Informationsdienst (AIRPORT TERMINAL INFORMATION SERVICE)
D Automatisches Informationssystem (AUTOMATIC INFORMATION SYSTEM)

25 Was bedeutet die Q-Gruppe "QFE"?

A Der Luftdruck in Flugplatzhöhe oder an der Start- und Landebahnschwelle
B Der Luftdruck bezogen auf einen Punkt auf der Erdoberfläche
C Der Luftdruck bezogen auf das höchste feste Hindernis eines Flugplatzes
D Die Höhenmesser-Skalaeinstellung, die nach der Landung die Platzhöhe anzeigt

26 Was bedeutet die Q-Gruppe "QNH"?

A Skaleneinstellung am Höhenmesser, damit bei der Landung die Flugplatzhöhe angezeigt wird
B Der Luftdruck in Flugplatzhöhe oder an der Landebahnschwelle
C Der am Flughafenbezugspunkt gemessene Luftdruck
D Der Luftdruck bezogen auf das höchste Hindernis auf einem Flughafen

27 Wenn Sie auf dem Höhenmesser die Höhe über NN ablesen wollen, welcher Luftdruckwert muss dann auf dem Höhenmesser eingestellt sein?

A QNH
B QFE
C QUJ
D QDM

28 Wenn Sie auf dem Höhenmesser die Höhe über dem Flugplatz ablesen wollen, welcher Luftdruckwert muss dann auf dem Höhenmesser eingestellt sein?

A QFE
B QDR
C QNH
D QTE

29 Was bedeutet die Q-Gruppe "QDM"?

A Missweisender Kurs zur Station
B Rechtweisende Peilung von der Station
C Missweisende Peilung von der Station
D Rechtweisender Steuerkurs zur Station (kein Wind)

30 Wie heißt die Q-Gruppe für "MISSWEISENDER KURS ZUR STATION"?

A QDM
B QNE
C QDR
D QTE

31 Was bedeutet die Q-Gruppe "QDR"?

A Missweisende Peilung von der Station
B Missweisender Steuerkurs zur Station (kein Wind)
C Rechtweisende Peilung / Funkstandlinie von der Station
D Rechtweisender Steuerkurs zur Station

32 Wie heißt die Q-Gruppe für "MISSWEISENDE PEILUNG VON DER STATION"?

A QDR
B QDM
C QTE
D QFE

33 Was sind Peilfunkmeldungen? Meldungen, die ...

A der Übermittlung von QDM-Werten dienen
B den Ausfall von Funknavigationsanlagen an Bord eines Luftfahrzeuges betreffen
C der Übermittlung von QNH-Werten dienen
D den Ausfall von Funknavigationsanlagen am Boden betreffen

34 Welche Meldungsart steht in der Rangfolge vor den Flugsicherheitsmeldungen?

A Peilfunkmeldung
B Staatstelegramm
C Wettermeldung
D Flugbetriebsmeldung

35 Meldungen, die bei der Durchführung der Flugverkehrskontrolle übermittelt werden, sind ...

A Flugsicherheitsmeldungen
B Peilfunkmeldungen
C Flugbetriebsmeldungen
D Dringlichkeitsmeldungen

36 Eine Meldung, welche die Sicherheit eines Luftfahrzeugs, eines Wasserfahrzeugs, eines anderen Fahrzeuges oder einer Person betrifft, ist eine ...

A Dringlichkeitsmeldung
B Flugbetriebsmeldung
C Notmeldung
D Flugsicherheitsmeldung

37 Eine Meldung betreffend dringend benötigter Luftfahrzeugteile ist eine ...

A Flugbetriebsmeldung
B Dringlichkeitsmeldung
C Flugsicherheitsmeldung
D Flugverkehrskontrollmeldung

38 Welche der aufgeführten Meldungen sind im beweglichen Flugfunkdienst zulässig?

A Peilfunkmeldungen
B Verwaltungsmeldungen der Luftfahrtbehörden
C Meldungen von Luftfahrzeughaltern
D Fernschreibmeldungen

39 Die Meldung eines Piloten an den Kontrollturm "MEINE VORAUSSICHTLICHE ANKUNFTSZEIT IST 1206, BESTELLEN SIE MIR BITTE EIN TAXI" ist ...

A eine unerlaubte Meldung im beweglichen Flugfunkdienst
B eine Dringlichkeitsmeldung
C eine Flugsicherheitsmeldung
D eine Flugbetriebsmeldung

40 Die Meldung eines Piloten an den Flugverkehrskontrolldienst "ERBITTE RADAR-FÜHRUNG ZUM UMFLIEGEN DES GEWITTERS" ist eine ...

A Flugsicherheitsmeldung
B Wettermeldung
C Dringlichkeitsmeldung
D Peilfunkmeldung

41 Die Freigabe "PISTE 05, START FREI" ist eine ...

A Flugsicherheitsmeldung
B unerlaubte Meldung
C Dringlichkeitsmeldung
D Flugbetriebsmeldung

42 Die Priorität der Meldung "ERBITTE QDM" ist ...

A höher als "START FREI"
B niedriger als "ERBITTE QNH"
C niedriger als "STEIGEN SIE AUF FLUGFLÄCHE 85"
D gleichwertig mit "PISTE 32, LANDUNG FREI"

43 Die Priorität der Anweisung "ROLLEN SIE ZUM ROLLHALT PISTE 12 ÜBER C" ist ...

A gleichwertig mit "ROLLEN SIE ZUM ABFLUGPUNKT PISTE 05, DORT HALTEN"
B niedriger als "LANDUNG FREI"
C höher als "SENDEN SIE FÜR PEILUNG"
D höher als "BEACHTEN SIE BAUARBEITEN LINKS DER ROLLBAHN G"

44 Wie wird die Uhrzeit im Flugfunkdienst übermittelt, wenn Verwechslungen ausgeschlossen sind?

A In Minuten, zweistellig
B In Stunden und Minuten
C In Minuten und Sekunden
D Nach Belieben

45 Zahlen sind grundsätzlich in einzelnen Ziffern zu übermitteln. Ausgenommen von dieser Regelung sind …

A Richtungsangaben nach Uhrzeigerstellung bei Verkehrshinweisen
B die Bezeichnung von Start-/Landebahnen
C Höhenangaben
D Kursangaben

46 Wie wird das Rufzeichen DIJYF richtig buchstabiert?

A DELTA INDIA JULIETT YANKEE FOXTROT
B DELTA YULIETT INDIA JANKEE FOXTROT
C DELTA INDIA JULIETT YANKEE FOX
D DELTA INDIA JANKEE YULIETT FOXTROT

47 Wie wird die Zahl 4500 richtig übermittelt?

A vier tausend fünf hundert
B vier füneff hundert
C vier fünf null null
D viertausend fünf null null

48 Wie übermittelt man "QNH 1001" richtig?

A QNH eins null null eins
B QNH ein tausend eins
C QNH eins zero zero eins
D QNH eintausend und eins

49 Wie wird die VHF-Frequenz 120,275 MHz übermittelt?

A eins zwo null Komma zwo sieben fünf
B eins zwanzig Komma zwo sieben
C eins zwei null Komma zwo sieben
D eins zwo null zwo sieben füneff

50 Wie übermittelt man die Zeit 1318, wenn man einen Irrtum oder eine Verwechslung ausschließen will?

A eins drei eins acht
B dreizehn eins acht
C dreizehn achtzehn
D eins acht nach dreizehn Uhr

51 Wie lautet das Rufzeichen einer Bodenfunkstelle an einem kontrollierten Flugplatz für die Bewegungslenkung auf dem Rollfeld?

A ROLLKONTROLLE
B INFORMATION
C RADAR
D TURM

52 Wie lautet das Rufzeichen einer Bodenfunkstelle an einem kontrollierten Flugplatz für die Bewegungslenkung in der Platzrunde?

A TURM
B RÜCKHOLER
C VORFELD
D INFORMATION

53 Wie werden die Rufzeichen von deutschen Bodenfunkstellen bei einem unkontrollierten Landeplatz gebildet? Aus dem Ortsnamen des Landeplatzes in Verbindung mit dem Begriff:

A INFO
B LUFTAUFSICHT
C TURM
D FLUGLEITUNG

54 Wie werden Rufzeichen von deutschen Bodenfunkstellen bei Segelfluggeländen gebildet? Aus dem Namen des Segelfluggeländes in Verbindung mit dem Begriff:

A SEGELFLUG
B INFO
C BODEN
D INFORMATION

55 Das Rufzeichen für den Fluginformationsdienst durch das Flugsicherungsunternehmen lautet:

A INFORMATION
B RADIO
C INFO
D FLUGINFORMATION

56 Was erhält man von einer Bodenfunkstelle mit dem Rufzeichen "INFORMATION"?

A Flugplatzwetter
B Rollanweisungen
C Landefreigaben
D Startfreigaben

57 Wann darf bei der Abwicklung des Sprechfunkverkehrs das Rufzeichen der Bodenfunkstelle weggelassen werden?

A Nach Herstellen der Sprechfunkverbindung
B Wenn sich das Luftfahrzeug in der Platzrunde befindet
C Bei jedem Funkanruf
D Wenn eine Verwechslung mit anderen Luftfunkstellen ausgeschlossen ist

58 Wie werden Rufzeichen deutscher Luftfunkstellen gebildet? Aus ...

A den Zeichen des Eintragungszeichen des Luftfahrzeugs
B der Musterbezeichnung des Luftfahrzeuges und den drei letzten Stellen des Eintragungszeichens
C der Flugnummer in Verbindung mit dem Eintragungszeichen
D dem Buchstaben "D" und drei weiteren Buchstaben

59 Ein Luftfahrzeug darf den Typ seines Rufzeichens im Sprechfunkverkehr während des Fluges nicht ändern, ausgenommen vorübergehend …

A auf Anweisung einer Flugverkehrskontrollstelle im Interesse der Sicherheit
B für Motorsegler beim Wechsel vom Motor- zum Segelflug
C auf Antrag des Piloten
D wenn der IFR-Flugplan aufgehoben und der Flug nach VFR fortgesetzt wird

60 Wie wird das abgekürzte Rufzeichen einer Luftfunkstelle gebildet? Aus ...

A dem ersten Zeichen des Eintragungszeichens und mindestens den zwei letzten Zeichen des Rufzeichens
B den drei letzten Stellen des Rufzeichens
C den beiden letzten Stellen des Eintragungszeichens
D der Bezeichnung des Luftfahrzeugmusters in Verbindung mit der letzten Stelle des Rufzeichens

61 Wann darf eine Luftfunkstelle ihr abgekürztes Rufzeichen verwenden?

A Nachdem die Bodenfunkstelle es bereits verwendet hat
B Nur bei Flügen in der Platzrunde
C Bei jedem Funkanruf
D Nach Herstellung der Sprechfunkverbindung mit der Bodenfunkstelle

62 Mit welchem Flugsicherungsbetriebsdienst kann man während des Fluges im Luftraum C Sprechfunkverbindung aufnehmen? Mit dem/der ...

A Flugverkehrskontrolldienst
B Flugnavigationsdienst
C Flugfernmeldedienst
D Flugberatungsdienst

63 Mit welchem Flugsicherungsbetriebsdienst kann man während des Fluges Sprechfunkverbindung aufnehmen? Mit dem …

A Fluginformationsdienst
B Flugfernmeldedienst
C Flugnavigationsdienst
D Flugberatungsdienst

64 Welche Redewendung ist anzuwenden, wenn bei einem Anruf das Rufzeichen der rufenden Funkstelle nicht verstanden wurde?

A WIEDERHOLEN SIE IHR RUFZEICHEN
B MONITOR IHR RUFZEICHEN
C ÜBERPRÜFEN SIE IHR RUFZEICHEN
D BESTÄTIGEN SIE IHR RUFZEICHEN

65 Eine Meldung wird von einem Pilot nicht vollständig wiederholt, obwohl es die Art der Meldung erfordert. Mit welcher Redewendung wird er zur Wiederholung aufgefordert?

A WIEDERHOLEN SIE WÖRTLICH
B KOMMEN
C BESTÄTIGEN SIE
D LESEN SIE ZURÜCK

66 Wie lautet die Redewendung für "JA"?

A POSITIV
B VERSTANDEN
C RICHTIG
D DAS IST RICHTIG

67 Wie lautet die Redewendung für "ERLAUBNIS WIRD NICHT ERTEILT"?

A NEGATIV
B FALSCH
C NICHT RICHTIG
D NEIN

68 Wie lautet die Redewendung für "ICH HABE IHRE LETZTE MELDUNG VOLLSTÄNDIG ERHALTEN"?

A VERSTANDEN
B POSITIV
C WIRD AUSGEFÜHRT
D WILCO

69 Der Inhalt einer klar verständlichen Meldung erscheint Ihnen zweifelhaft. Welche Redewendung wenden Sie an, um die Zweifel auszuräumen?

A BESTÄTIGEN SIE
B WIEDERHOLEN SIE WÖRTLICH
C ÜBERMITTELN SIE NOCHMALS
D BERICHTIGUNG

70 Der Höhenmesser ist auf den Druckwert 1013,2 hPa eingestellt und zeigt 7500 Fuss an. Die Bodenfunkstelle fragt nach der augenblicklichen Höhe des Luftfahrzeuges. Wie muss die Antwort des Piloten lauten?

A FL 75
B 7500 ft
C 7500 ft AGL
D 7500 ft AMSL

71 Welche Redewendung soll angewandt werden um auszudrücken: "BEI DER ÜBERMITTLUNG IST EIN FEHLER UNTERLAUFEN, ES MUSS RICHTIG HEIßEN ..."

A QNH 1003 BERICHTIGUNG QNH 1002
B QNH 1003 TRENNUNG TRENNUNG 1002
C QNH 1003 NEGATIV QNH 1002
D QNH 1003 ICH WIEDERHOLE 1002

72 Welche Redewendung wird angewandt um auszudrücken: "GENEHMIGUNG, UNTER FESTGESETZTEN BEDINGUNGEN ZU VERFAHREN"?

A FREI
B POSITIV
C GENEHMIGT
D KORREKT

73 Mit welcher Redewendung wird ein Pilot angewiesen, mit seinem SSR-Antwortgerät (Transponder) einen bestimmten Modus / Code zu senden?

A SQUAWK
B SENDEN SIE MITTELS TRANSPONDER
C TRANSPOND
D RESPOND MODE …. / CODE ….

74 Die Redewendung "WILCO" bedeutet:

A Ich habe Ihre Nachricht verstanden und werde entsprechend handeln
B Warten Sie, ich werde Sie rufen
C Ich habe Ihre letzte Meldung vollständig erhalten
D Ich wiederhole zur Klarstellung oder Betonung

75 Die Redewendung "MONITOR" bedeutet:

A Hören Sie (Frequenz / Kanal) ab
B Betrachten Sie diese Übermittlung als nicht gesendet
C Stellen Sie Funkverbindung her mit (Station)
D Teilen Sie mit, dass die Meldung empfangen und verstanden wurde

76 Wie bestätigt ein Pilot die Anweisung des Kontrollturmes: "STARTEN SIE DURCH PISTE BLOCKIERT!"?

A STARTE DURCH
B VERSTANDEN
C WILCO
D POSITIV

77 Mit welcher Sprechgruppe bestätigt ein Pilot die Anweisung "DEKMG HALTEN SIE POSITION STARTFREIGABE AUFGEHOBEN, ICH WIEDERHOLE STARTFREIGABE AUFGEHOBEN"?

A DEKMG HALTE
B DEKMG VERSTANDEN
C DEKMG
D DEKMG POSITIV

78 DEHOL erhält Startfreigabe am Abflugpunkt der Piste 24. Wie bestätigt der Pilot die Freigabe?

A DEHOL PISTE 24 START FREI
B DEHOL START FREI
C DEHOL WILCO
D DEHOL ICH STARTE

79 DEKUL hat seine Startvorbereitungen beendet. Mit welcher Sprechgruppe teilt er dies dem TOWER mit?

A DEKUL ABFLUGBEREIT
B DEKUL START FREI
C DEKUL STARTBEREIT
D DEKUL STARTET

80 Was bedeutet die Anweisung einer Flugverkehrskontrollstelle "(RUFZEICHEN) SQUAWK 1352"?

A Schalten Sie den Transponder auf Mode/Code 1352
B Zählen Sie 1-3-5-2- für Funkpeilung
C Erbitte Testsendung auf Frequenz 135,200 MHz
D Schalten Sie um auf Frequenz 135,200

81 Von der Radarkontrolle erhalten Sie folgenden Verkehrshinweis: "UNBEKANNTES FLUGZIEL ZEHN UHR ENTFERNUNG 4NM". Wo befindet sich das Flugziel, wenn Sie aus der Flugzeugkanzel sehen?

A Links voraus
B Querab rechts
C Rechts voraus
D In Flugrichtung voraus

82 Wann ist ein Einleitungsanruf abzusetzen?

A Bei Herstellung des ersten Funkkontaktes
B Nur in Notfällen
C Wenn eine Meldung nicht verstanden wurde
D Bei jedem Funkkontakt

83 Welches der folgenden Beispiele ist ein Einleitungsanruf?

A AACHEN INFO DELID
B SAARBRÜCKEN TURM HIER DIAMK
C HAMBURG TURM VON DER DEMIL KOMMEN
D D2468 FÜR WASSERKUPPE SEGELFLUG WIE HÖREN SIE MICH?

84 Muss ein "ALLGEMEINER ANRUF" bestätigt werden?

A Nein
B Ja, nur von dem zuerst gerufenen Piloten
C Ja, von allen Piloten in beliebiger Reihenfolge
D Ja, von allen Piloten in der Reihenfolge des Anrufs

85 Welcher der folgenden Funkanrufe ist ein "ALLGEMEINER ANRUF"?

A AN ALLE HAMBURG TURM ... ENDE
B DEKOF, DIEBS, DKARL NÜRNBERG ROLLKONTROLLE
C D8765 BERLIN INFORMATION
D LUFTHANSA 123, LUFTHANSA 456

86 Welcher der folgenden Anrufe ist ein "MEHRFACHANRUF"?

A DEABC, DGIAL, DHHIA LEIPZIG TURM
B DIENO DELLW
C AN ALLE DRESDEN TURM
D DEAMM ERFURT ROLLKONTROLLE

87 Muss ein "MEHRFACHANRUF" bestätigt werden?

A Ja, von allen Luftfahrzeugen in der Reihenfolge des Anrufes
B Ja, in beliebiger Reihenfolge
C Nein
D Ja, nur von dem zuerst angerufenen Luftfahrzeug

88 Ein Pilot empfängt einen Funkanruf, ist sich aber nicht sicher, ob er gerufen wurde. Wie verhält er sich richtig? Er ...

A wartet ab, bis der Anruf wiederholt wird
B nennt das eigene Rufzeichen und wartet dann ab
C nennt das eigene Rufzeichen mit der Sprechgruppe "WIEDERHOLEN SIE IHR RUFZEICHEN"
D antwortet mit der Sprechgruppe "WIEDERHOLEN SIE"

89 Was ist vor Aufnahme des Sprechfunkverkehrs zu beachten?

A Nach Wahl der richtigen Frequenz sicherstellen, dass kein laufender Funkverkehr gestört wird
B Es muss eine Funkprobe stattgefunden haben
C Das Luftfahrzeug muss sich in der Luft befinden
D Die Entfernung zwischen Boden- und Luftfunkstelle darf nicht weniger als 30 NM betragen

90 Vor Einflug in den Luftraum C unter FL 100 in der Umgebung von Verkehrsflughäfen muss Sprechfunkverbindung mit der zuständigen Flugverkehrskontrollstelle spätestens aufgenommen werden:

A 5 Minuten vor Einflug in diesen Luftraum
B Beim Einflug in diesen Luftraum
C Unmittelbar nach dem Start
D Oberhalb von 3500 ft AGL

91 Der Sprechfunkverkehr bei VFR-Flügen in und oberhalb Flugfläche 100 wird durchgeführt in ...

A englischer Sprache
B deutscher Sprache
C einer der ICAO-Sprachen
D deutscher oder englischer Sprache

92 DGIGA erhält die Anweisung, HAMBURG TURM auf Frequenz 126,850 MHz zu rufen. Wie lautet die richtige Bestätigung des Piloten?

A DGIGA rufe 126,850 
B DGIGA wechsele Frequenz
C DGIGA werde TURM rufen DGIGA
D HAMBURG TURM DGIGA

93 Dauernde Hörbereitschaft ist aufrechtzuerhalten bei VFR-Flügen im Luftraum:

A C und D
B nur D
C E
D G

94 Ein Pilot führt ein Luftfahrzeug nach Sichtflugregeln in der Platzrunde eines Flugplatzes mit Flugverkehrskontrolle. Wozu ist er grundsätzlich verpflichtet?

A Ständige Hörbereitschaft auf der Frequenz der Flugplatzkontrollstelle zu halten
B In jedem Teil der Platzrunde eine Standortmeldung abzusetzen
C Eine Wetterberatung einzuholen
D In jedem Fall vor Beginn des Fluges einen Flugplan abzugeben

95 Bei welchen Flügen muss ein Pilot ständige Hörbereitschaft halten? Bei VFR-Flügen ...

A bei Nacht in den Lufträumen C, D und E (außerhalb der Umgebung des Flugplatzes)
B bei Nacht im Luftraum G
C über geschlossenen Wolkendecken
D über den Alpen

96 Bei welchen Flügen nach Sichtflugregeln muss der Pilot ständige Hörbereitschaft auf der zugewiesenen Frequenz halten? Bei Flügen ...

A im Luftraum C
B im Luftraum F
C über geschlossenen Wolkendecken
D während der Nacht im Luftraum G

97 Wer ein Luftfahrzeug auf einem Flugplatz mit Flugverkehrskontrolle oder in dessen Umgebung führt, ist u.a. verpflichtet, durch Funk oder Zeichen die vorherige Genehmigung für alle Bewegungen einzuholen, durch die das ...

A Rollen, Starten und Landen eingeleitet werden oder damit in Zusammenhang stehen
B Starten und Landen eingeleitet werden
C Rollen, Starten und Landen eingeleitet werden
D Starten und Landen eingeleitet werden oder damit in Zusammenhang stehen

98 Wer ein Luftfahrzeug nach Sichtflugregeln auf einem Flugplatz mit Flugverkehrskontrolle oder in dessen Umgebung führt, ist verpflichtet ...

A dauernde Hörbereitschaft auf der vorgesehenen Funkfrequenz zu halten oder, falls dies nicht möglich ist, auf Anweisungen durch Licht- und Bodensignale sowie Zeichen zu achten
B in jedem Teil der Platzrunde eine Standortmeldung abzusetzen
C in jedem Fall vor Beginn des Fluges einen Flugplan abzugeben
D eine Wetter- und Flugberatung einzuholen

99 Was bedeutet bei einem Funktest der Hinweis "HÖRE SIE ZWO"? Der Funktest ist ...

A zeitweise verständlich
B schwer verständlich
C verständlich
D sehr gut verständlich

100 Was bedeutet bei einem Funktest der Hinweis "HÖRE SIE DREI"? Die Funktest ist ...

A schwer verständlich
B zeitweise verständlich
C verständlich
D sehr gut verständlich

101 Was bedeutet bei einem Funktest der Hinweis "HÖRE SIE VIER"? Die Funktest ist ...

A verständlich
B schwer verständlich
C unverständlich
D sehr gut verständlich

102 Was bedeutet bei einem Funktest der Hinweis "HÖRE SIE FÜNF"? Der Funktest ist ...

A sehr gut verständlich
B unverständlich
C zeitweise verständlich
D schlecht verständlich

103 Ein Funktest ist "verständlich". Wie wird die Verständlichkeit im Sprechfunkverkehr ausgedrückt?

A Höre Sie vier
B Höre Sie drei
C Höre Sie laut und deutlich
D Höre Sie

104 Ein Funktest ist "schwer verständlich". Wie wird die Verständlichkeit im Sprechfunkverkehr ausgedrückt?

A Höre Sie drei
B Höre Sie 
C Höre Sie zwo
D Höre Sie KOMMEN

105 Was muss bei einer Testübermittlung u.a. angegeben werden?

A Die Wörter "RADIO CHECK"
B Die Wörter "TRANSMISSION CHECK"
C Die Wörter "TEST CHECK"
D Die Wörter "CHECK CHECK"

106 Welche Meldung muss ein Pilot wiederholen?

A START FREI
B ACHTEN SIE AUF ENTGEGENKOMMENDEN HUBSCHRAUBER
C BAUARBEITEN LINKS DER ROLLBAHN
D SCHWERE GEWITTER IM RHEINTAL BEI MANNHEIM

107 Welche Meldungen müssen wiederholt werden?

A Höhenmessereinstellungen
B Verkehrshinweise
C Wettermeldungen
D Rollbahnzustand

108 Welche Meldungen müssen wiederholt werden?

A Die Frequenz bei Frequenzwechsel
B Hinweise auf Bauarbeiten an der Start-/Landebahn
C Wetterinformationen
D Windrichtung und -stärke

109 Wie wird der Empfang einer Flugverkehrskontrollfreigabe bestätigt? Durch ...

A wörtliche Wiederholung der Freigabe
B zweimaliges Drücken der Mikrofontaste
C Nennung des eigenen, abgekürzten Rufzeichens
D dreimaliges Drücken der Mikrofontaste

110 DESEL erhält die folgende Freigabe/Anweisung: "DEL NACH DEM ABHEBEN STEIGEN SIE GERADEAUS AUF FLUGHÖHE 3000 FUSS, MACHEN SIE DANN EINE RECHTSKURVE, WIND 250 GRAD, 7 KNOTEN, PISTE 22, START FREI". Wie lautet die richtige Bestätigung seitens DESEL?

A DEL GERADEAUS STEIGEN AUF FLUGHÖHE 3000 FUSS, DANN RECHTSKURVE, PISTE 22, START FREI
B DEL START FREI, PISTE 22, WIND 250 GRAD, 7 KNOTEN
C DEL WILCO, PISTE 22, START FREI
D DEL AUF 3000 FUSS STEIGEN, START FREI

111 Welche Teile der nachfolgenden Anweisungen oder Informationen müssen bestätigt werden?

A Freigaben, Rollanweisungen, Betriebspiste, QNH, SSR-Codes, Höhenanweisungen, Steuerkurs- und Geschwindigkeitsanweisungen, Frequenz bei Frequenzwechsel
B Betriebsstart-/Landebahn, Bodensicht, Taupunkt, Startfreigabe, Frequenz bei Frequenzwechsel
C Freigaben, Windrichtung/-geschwindigkeit, Steuerkursanweisungen, QNH, Frequenz bei Frequenzwechsel
D Anweisungen über Steuerkurs, Flughöhe, Geschwindigkeit, Höhenmessereinstellung, Flugsicht, Windrichtung, Startfreigabe und Frequenz bei Frequenzwechsel

112 Bei welchen VFR-Flügen ist in der Regel die Übermittlung von Standortmeldungen erforderlich?  Bei ...

A Einflügen in den Luftraum D
B allen Flügen im Luftraum E
C Flügen während der Nacht im Luftraum G
D Flügen über den Wolken im Luftraum E

113 Bei einem VFR-Flug zu einem Flughafen mit Flugverkehrskontrolle gelten die im "Luftfahrthandbuch VFR" festgelegten Verfahren.  Standortmeldungen über den Pflichtmeldepunkten müssen ...

A unabhängig von der erteilten Freigabe in jedem Fall abgesetzt werden, sofern nicht ausdrücklich darauf verzichtet wird
B nur abgesetzt werden, wenn es sich um einen Sonderflug nach Sichtflugregeln handelt
C unabhängig von der erteilten Freigabe nur dann abgesetzt werden, wenn die Platzkontrollstelle dazu auffordert
D nicht abgesetzt werden. Durch die Anweisung, in die Platzrunde einzufliegen, wird auf jede weitere Standortmeldung über Pflichtmeldepunkten verzichtet 

114 Wann hat ein Pilot bei einem VFR-Flug während des Tages der zuständigen Flugverkehrskontrollstelle eine Standortmeldung zu übermitteln?

A Beim Überflug von Pflichtmeldepunkten
B Beim Verlassen des Luftraumes D
C Nur beim Überflug von Funknavigationsanlagen (z.B. VOR, NDB)
D Beim Einflug in die Lufträume E und F

115 Eine Standortmeldung besteht normalerweise aus Funkrufzeichen des Luftfahrzeuges, Standort, Überflugzeit und Flughöhe. Welche Angabe kann unter bestimmten Voraussetzungen bei einem VFR-Flug entfallen?

A Die Zeitangabe, wenn die Meldung zum Zeitpunkt des Überfluges erfolgt
B Der Standort, wenn dieser auf der Sichtflugkarte veröffentlicht ist
C Die Flughöhe, wenn diese nicht höher als 3500 ft AGL ist
D Das Funkrufzeichen, wenn es sich um einen nichtgewerblichen Flug handelt

116 Welche Angaben enthält eine Standortmeldung bei Flügen in der Platzrunde?

A Funkrufzeichen des Luftfahrzeuges, Standort
B Funkrufzeichen des Luftfahrzeuges, Standort, Zeit
C Funkrufzeichen des Luftfahrzeuges, Standort, Höhe
D Funkrufzeichen des Luftfahrzeuges, Standort, Höhe, Zeit

117 Welche Bedeutung hat das abgebildete Symbol auf der Sichtflugkarte? (Filled triangle in a dashed circle.)

A Pflichtmeldepunkt
B Luftfahrthindernis
C Funknavigationsanlage
D Meldepunkt auf Anforderung (Bedarfsmeldepunkt)

118 Welche Bedeutung hat das abgebildete Symbol auf der Sichtflugkarte? (Non-filled triangle in a dashed circle.)

A Meldepunkt auf Anforderung (Bedarfsmeldepunkt)
B Pflichtmeldepunkt
C Militärflugplatz
D Beleuchtetes Hindernis

119 Wann kann, anstelle der Landemeldung, die voraussichtliche Landezeit mittels Sprechfunk der zuständigen Flugverkehrskontrollstelle übermittelt werden?

A Wenn sich das Luftfahrzeug in der Platzrunde befindet und die Landung sichergestellt erscheint
B Wenn der Verkehr in der Platzrunde beobachtet wird
C Auf Anforderung der Flugleitung des Landeplatzes, wenn die Landung sichergestellt erscheint
D Nach Zustimmung der Flugleitung des Landeplatzes

120 Bei Flugplanabgabe und Abflug von einem unkontrollierten Flugplatz kann die Startmeldung mittels Sprechfunk übermittelt werden. An wen erfolgt sie in diesem Fall?

A An die zuständige Flugverkehrskontrollstelle oder an den zuständigen FIS zur Weiterleitung an den AIS-C
B An den Funknavigationsdienst zur Weiterleitung an den AIS-C
C An den Flugberatungsdienst
D An die Bodenfunkstelle des Zielflugplatzes

121 Welche Angaben muss eine Startmeldung enthalten, wenn sie über Sprechfunk übermittelt wird?

A Luftfahrzeugkennung, Startflugplatz, Startzeit, Zielflugplatz
B Luftfahrzeugkennung, Startflugplatz, Startzeit
C Luftfahrzeugkennung, Startflugplatz, Zielflugplatz
D Luftfahrzeugkennung, Startzeit, Zielflugplatz

122 Wenn die Bewölkung über Sprechfunk mit "LOCKERE BEWÖLKUNG (SCATTERED)" angegeben wird, dann beträgt der Bedeckungsgrad:

A 3 bis 4 Achtel
B 8 Achtel
C 5 bis 7 Achtel
D 1 bis 2 Achtel

123 Wenn die Bewölkung über Sprechfunk mit "DURCHBROCHEN BEWÖLKT (BROKEN)" angegeben wird, dann beträgt der Bedeckungsgrad:

A 5 bis 7 Achtel
B 1 bis 2 Achtel
C 8 Achtel
D 3 bis 4 Achtel

124 Wenn die Bewölkung über Sprechfunk mit "BEDECKT (OVERCAST)" angegeben wird, dann beträgt der Bedeckungsgrad:

A 8 Achtel
B 5 bis 7 Achtel
C 3 bis 4 Achtel
D 1 bis 2 Achtel

125 Was bedeutet bei der Routinewettermeldung die Angabe "3 bis 4 ACHTEL"? Der Bedeckungsgrad beträgt …

A LOCKERE BEWÖLKUNG (SCATTERED)
B BEDECKT (OVERCAST)
C DURCHBROCHEN BEWÖLKT (BROKEN)
D KEINE MARKANTEN WOLKEN (NO SIGNIFICANT CLOUDS)

126 Was bedeutet bei der Routinewettermeldung die Angabe "5 bis 7 ACHTEL"? Der Bedeckungsgrad beträgt …

A DURCHBROCHEN BEWÖLKT (BROKEN)
B GERING BEWÖLKT (FEW)
C BEDECKT (OVERCAST)
D LOCKERE BEWÖLKUNG (SCATTERED)

127 Was bedeutet bei der Routinewettermeldung die Angabe "1 bis 2 ACHTEL"? Der Bedeckungsgrad beträgt …

A GERING BEWÖLKT (FEW)
B DURCHBROCHEN BEWÖLKT (BROKEN)
C LOCKERE BEWÖLKUNG (SCATTERED)
D KEINE MARKANTEN WOLKEN (NO SIGNIFICANT CLOUDS)

128 Wenn die Angabe "CAVOK" in einer Routinewettermeldung (METAR) steht, dann betragen die Werte für Sicht und Wolken:

A Sicht 10 km oder mehr, keine Bewölkung unter 5000 ft AGL
B Sicht 5000 m oder mehr, keine Bewölkung unter 5000 ft AGL
C Sicht 10 km oder mehr, keine Bewölkung unter 1500 ft AGL
D Sicht 5000 m oder mehr, keine Bewölkung unter 1500 ft AGL

129 Wie werden die Sichtweiten in einer Routinewettermeldung (METAR) im Klartext angegeben?

A Bis 5000 m in Metern, darüber in Kilometern
B In Fuss und NM
C Bis 1500 m in Metern, darüber in Kilometern
D Nur in NM

130 Welche Übermittlung der Bodensicht ist richtig?

A "SICHT DREI TAUSEND METER"
B "SICHT ETWA NEUN TAUSEND FUSS"
C "SICHT DREI KILOMETER"
D "SICHT EINS KOMMA ACHT SEEMEILEN"

131 Was versteht man unter VOLMET?

A Die Wetterrundsendungen für Flughafenwettermeldungen für Flughäfen
B Den Fluginformationsdienst
C Das Funkrufzeichen für eine Dienststelle des Deutschen Wetterdienstes (DWD)
D Das Rufzeichen des Flugverkehrsberatungsdienstes

132 Ein Pilot hat während des Fluges zu einem internationalen Verkehrsflughafen die Möglichkeit das Flugplatzwetter einzuholen über ...

A ATIS
B GAFOR
C AIS-C
D UHF

133 ATIS-Aussendungen dienen unter anderem der Unterrichtung von Piloten. Welche Angaben enthalten sie?

A Lande- und Startinformationen zur sicheren Durchführung von Flügen nach VFR und IFR
B Wetterinformationen für Überlandflüge unter VMC
C Wetterinformationen für mehrere Flughäfen
D Die rechtweisende Peilung zum Zielflugplatz

134 Wie werden SIGMET-Meldungen in der Zeit von 0700 (0600 während der gesetzlichen Sommerzei) bis SS+30 verbreitet?

A Als Flugrundfunksendung (broadcast) auf den Frequenzen des Fluginformationsdienstes zu jeder halben und vollen Stunde
B Als Flugrundfunksendung (broadcast) auf den für VOLMET veröffentlichten Frequenzen
C Auf Anforderung des Luftfahrzeugführers
D Als Flugrundfunksendung (broadcast) auf den Frequenzen der Flugverkehrskontrolle

135 SIGMET-Meldungen dienen der Sicherheit des Flugbetriebs der Allgemeinen Luftfahrt. Welche Angaben enthalten sie?

A Besondere Wettererscheinungen, z.B. Gewitter, Turbulenzen, Vereisung
B Angabe der Wolkenuntergrenze in Lufträumen der Klassen F und G
C Routinewettermeldungen
D Meteorologische Angaben in Kartenform, erhältlich bei Flugwetterwarten

136 Welche Angaben soll eine Notmeldung enthalten?

A Art der Notlage, Absichten des Luftfahrzeugführers, Art der gewünschten Hilfe, Angaben über Standort, Kurs und Flughöhe
B Art der Notlage, Ursache der Notlage, Bitte um Frequenzwechsel auf 121,500 MHz
C Steuerkurs, Absichten des Luftfahrzeugführers
D Absichten des Luftfahrzeugführers, TAS, Standort, Sinkflugrate

137 Das Notsignal MAYDAY bedeutet, dass ...

A ein Luftfahrzeug und dessen Insassen von schwerer und unmittelbarer Gefahr bedroht sind und sofortige Hilfe benötigen
B ein Luftfahrzeugführer eine außerplanmäßige Landung durchgeführt hat oder durchführen wird
C sich ein Luftfahrzeug in einer schwierigen Lage befindet
D sich ein schwerkranker Passagier an Bord eines Luftfahrzeuges befindet

138 Ein Notanruf soll übermittelt werden ...

A auf der Betriebsfrequenz oder einer Notfrequenz
B nur auf einer FIS-Frequenz
C immer auf der Notfrequenz 121,500 MHz
D auf einer SAR-Frequenz

139 Wie wird ein Notanruf eingeleitet?

A MAYDAY, vorzugsweise dreimaliges Aussenden
B MAYDAY NOTFALL MAYDAY
C PAN PAN, vorzugsweise dreimaliges Aussenden
D NOTFALL, vorzugsweise dreimaliges Aussenden

140 Welches der folgenden Signale ist ein Notsignal?

A Das durch Sprechfunk übermittelte Wort MAYDAY
B Das Abfeuern von grünen und roten Leuchtkugeln
C Das durch Sprechfunk übermittelte Wort PAN PAN
D Das wiederholte Ein- und Ausschalten der Landescheinwerfer oder der Positionslichter

141 Wie wird ein Dringlichkeitsanruf eingeleitet?

A PAN PAN, vorzugsweise dreimaliges Aussenden
B ACHTUNG, ICH HABE EINE DRINGENDE MELDUNG
C DRINGLICHKEIT DRINGLICHKEIT
D MAYDAY‚ vorzugsweise dreimaliges Aussenden

142 Das durch Sprechfunk übermittelte Signal PAN PAN bedeutet, dass ein Luftfahrzeug ...

A sich in einer schwierigen Lage befindet
B versehentlich in ein Gebiet mit Flugbeschränkungen eingeflogen ist
C entführt worden ist
D in schwerer und unmittelbarer Gefahr ist und sofortige Hilfe benötigt

143 Welcher Transpondercode soll in einer Notlage gesendet werden?

A A 7700
B A 7500
C A 7600
D A 7000

144 Was zeigt ein Luftfahrzeug der Bodenfunkstelle an, wenn es den Transpondercode A 7700 sendet?

A Das Luftfahrzeug befindet sich in einer Notlage
B Das Luftfahrzeug hat Funkausfall
C Das Luftfahrzeug wird entführt
D Das Luftfahrzeug fliegt in den Luftraum E ein

145 Bei Funkausfall vor Erhalt bzw. Bestätigung der Einflugfreigabe in eine Kontrollzone hat der Pilot ...

A den Transpondercode Mode A 7600 zu schalten, sofern möglich; auf dem nächstgelegenen geeigneten Flugplatz zu landen; und der zuständigen Flugverkehrskontrollstelle schnellstmöglich die Landezeit zu übermitteln
B den Transpondercode Mode A 7600 zu schalten, sofern möglich; und ein geeignetes Notlandegelände zu erkunden
C den Transpondercde Mode A 7600 zu schalten, sofern möglich; und durch Vollkreise nach links und rechts auf sich aufmerksam zu machen
D den Transpondercode Mode A 7600 zu schalten, sofern möglich; und nach einer Umkehrkurve von 180° zum Startflugplatz zurück zu kehren

146 Was ist ein besonderes Merkmal der Blindsendung?

A Die Meldung ist zweimal zu übermitteln
B Am Ende der Blindsendung wird das Rufzeichen des Luftfahrzeuges wiederholt
C Die Meldung ist dreimal zu übermitteln
D Am Ende der Blindsendung wird das Rufzeichen der Bodenfunkstelle wiederholt

147 Was ist ein besonderes Merkmal der Blindsendung?

A Angabe der Zeit und/oder der Position für die nächste Blindsendung
B Der Meldung wird dreimal die Redewendung BLINDSENDUNG vorangestellt
C Am Ende der Blindsendung wird das Rufzeichen der Luftfunkstelle wiederholt
D Am Ende einer Blindsendung wird das Rufzeichen der Bodenfunkstelle wiederholt

148 Welchen Transpondercode soll ein Luftfahrzeugführer bei Funkausfall senden?

A A 7600
B A 7700
C A 7500
D A 7000

149 Was zeigt ein Luftfahrzeug der Bodenfunkstelle an, wenn es den Transpondercode A 7600 sendet?

A Funkausfall
B Erbitte Landeanweisungen
C Notlage
D Fliege in den Luftraum C ein

150 Beobachtet ein Pilot ein auf ihn gerichtetes Lichtsignal, so hat er die vorgeschriebenen Maßnahmen zu treffen. Was hat er dabei grundsätzlich zu beachten?

A Anweisungen über Funk haben Vorrang vor Signalen und Zeichen, ausgenommen rote Feuerwerkskörper
B Auch akustische Signale können gegeben werden
C Signale und Zeichen haben Vorrang vor Anweisungen über Funk
D Bodensignale haben Vorrang vor Lichtsignalen

151 Nach der Luftverkehrsordnung haben Funkanweisungen Vorrang vor Licht- und Bodensignalen sowie Zeichen. Dies gilt nicht gegenüber ...

A roten Feuerwerkskörpern
B grünen Dauersignalen
C roten Dauersignalen
D roten Blinksignalen

152 Ein Pilot hat vorrangig zu befolgen:

A Funkanweisungen
B Lichtsignale
C Bodensignale
D Leuchtgeschosse, die in Abständen von ca. 10 Sekunden abgefeuert werden und sich in rote und grüne Lichter und Sterne zerlegen

153 In welchem Frequenzbereich wird der Sprechfunkverkehr im zivilen beweglichen Flugfunkdienst abgewickelt?

A 117,975 MHz – 137,000 MHz
B 108,000 kHz – 136,000 kHz
C 108,000 MHz – 117,975 MHz
D 200 - 490 kHz

154 Welcher Kanalabstand (Frequenzbereich 117,975 MHz - 137,000 MHz) wird im Flugfunkdienst im unteren Luftraum verwendet?

A 25 kHz + 8,33 kHz
B 25 MHz
C 25 MHz + 8,33 MHz
D 8,33 kHz

155 In welcher Betriebsart wird der Sprechfunkverkehr im Flugfunkdienst durchgeführt?

A Wechselsprechverkehr
B Duplexverkehr
C Wechsel- und Gegensprechverkehr
D Gegensprechverkehr

156 Welche Bezeichnung hat die Frequenz 121,500 MHz?

A Internationale Notfrequenz
B Schul- und Übungsfrequenz
C Bord-Bord-Frequenz
D Informationsfrequenz

157 Welche der angegebenen Frequenzen entspricht der einer deutschen Bodenfunkstelle mit dem Rufzeichen "INFO"?

A 130,780 MHz
B 121,500 MHz
C 109,550 MHz
D 200 kHz

158 Welche Frequenz wird im Kanalabstand von 8,33 kHz betrieben?

A 134,555 MHz
B 121,500 MHz
C 109,550 MHz
D 200 kHz

159 Wodurch kann eine Sprechfunkfrequenz blockiert werden?

A Klemmen der Sprechtaste
B Zu lautes Sprechen
C Zu leises Sprechen
D Ein- und Ausschalten der Sprechfunkanlage

160 Wie breiten sich Ultrakurzwellen (UKW) aus?

A Ähnlich wie das Licht, d.h. "quasi optisch"
B Wie Kurzwellen, wobei aber atmosphärische Störungen keinen Einfluss auf sie haben
C Sie breiten sich als Bodenwellen entlang der Erdoberfläche aus und dringen somit z.B. auch in Täler ein, so dass sie von topographischen Hindernissen nicht beeinflusst werden
D Sie werden von der Ionosphäre in ca. 100 km Höhe reflektiert und gelangen als sogenannte Raumwellen zur Erdoberfläche zurück

161 Welche Phänomene können beim Flugfunk die Empfangsqualität der UKW beeinflussen?

A Die Flughöhe des Luftfahrzeuges und topographische Verhältnisse
B Der Tag-/Nachteffekt
C Die Ionosphäre
D Atmosphärische Störungen, wie sie besonders bei Gewittern auftreten

162 In welcher der folgenden Situationen kann die Funkverbindung zwischen Luftfahrzeug und TURM auf Frequenz 118,250 MHz als problemlos erwartet werden?

A Das Flugzeug befindet sich in ausreichend großer Höhe und nahe der Bodenfunkstelle
B Das Luftfahrzeug befindet sich im Tiefflug in einem Tal, nahe der Bodenstation im "Funkschatten"
C Das Flugzeug befindet sich in geringer Flughöhe im "Funkschatten" eines Berges, in weiter Entfernung von der Bodenfunkstelle
D Das Flugzeug befindet sich in geringer Höhe sehr weit von der Bodenfunkstelle entfernt

163 Welches ist die maximal zu erwartende Entfernung für eine einwandfreie UKW-Funkverbindung über flachem Gelände in FL 65?

A Ca. 95 NM
B Ca. 20 NM
C Ca. 10 NM
D Ca. 150 NM

164 Welche Flugverkehrsdienste gibt es?

A Flugverkehrskontrolldienst, Flugalarmdienst, Fluginformationsdienst, Flugverkehrsberatungsdienst
B FS-Kontrolldienst, Such- und Rettungsdienst, Fernmeldedienst
C Alarm-, Rettungs-, Informations- und Beratungsdienst
D Wetterdienst, Beratungsdienst, Such- und Rettungsdienst (SAR) und Kontrolldienst

165 Der Fluginformationsdienst hat u. a. folgende Aufgaben:

A Annahme und Weiterleitung von Flugplan- und Flugplanfolgemeldungen
B Wettermeldungen zu verbreiten
C Freigaben zu erteilen
D Den Such- und Rettungsdienst (SAR) zu organisieren

166 Wer ist für die Bewegungslenkung des Luftverkehrs in der Bundesrepublik Deutschland zuständig?

A Die vom Bundesaufsichtsamt für Flugsicherung zugelassenen Flugsicherungsorganisationen
B Das Luftfahrtbundesamt
C Die Landesluftfahrtbehörden
D Die DFS Deutsche Flugsicherung GmbH

167 Wann steht der FIS dem Piloten zur Verfügung?

A Während des Fluges
B Während des Fluges, jedoch ausschließlich bei Flügen im Luftraum C und E
C Vor Antritt eines Fluges
D Während des Fluges, jedoch ausschließlich bei Flügen im Luftraum G

168 Zur Flugvorbereitung sind verpflichtet:

A Alle Luftfahrzeugführer
B Nur Luftfahrzeugführer, die Überlandflüge durchführen
C Nur die Luftfahrzeugführer von motorgetriebenen Luftfahrzeugen
D Unerfahrene Luftfahrzeugführer

169 Eine Wetterberatung ist grundsätzlich einzuholen bei ...

A Flügen, die über die Instrumentenflugregeln 
B zweifelhaften Wetterlagen
C Flügen, für die ein Flugplan zu übermitteln ist
D Flügen zu gewerblichen Zwecken

170 Worauf beziehen sich grundsätzlich Zeitangaben in der Luftfahrt? Auf ...

A Koordinierte Weltzeit (UTC)
B Ortszeit
C Zonenzeit (Z-Zeit)
D MEZ bzw. MESZ

171 Welches ist die Maßeinheit für Entfernungen in der Luftfahrt zum Zwecke der Navigation?

A Knoten
B Meilen je Minute
C Kilometer je Stunde
D Meter je Minute

172 Welches ist die Maßeinheit für die vertikale Geschwindigkeit in der Luftfahrt?

A Fuss je Minute
B Fuss je Sekunde
C Knoten
D Meter je Minute

173 Welches ist die Maßeinheit für Höhenangaben in der Luftfahrt?

A Fuss
B Zoll
C Meter
D Kilometer

174 Welches ist die Maßeinheit für Entfernungen in der Luftfahrt zum Zwecke der Navigation?

A Seemeile und Zehntel
B Knoten
C Kilometer
D Landmeile

175 Welches ist die Maßeinheit für den Luftdruck in der Luftfahrt?

A Hektopascal
B Atmosphäre Überdruck
C Millimeter Quecksilber
D Millibar

176 Welcher horizontale Mindestabstand ist im Fluge über dem höchsten Hindernis einzuhalten?

A 150 m
B 300 ft
C 600 ft
D 300 m

177 Ein motorgetriebenes Luftfahrzeug und ein Segelflugzeug nähern sich im Gegenflug. Wer muss ausweichen?

A Beide nach rechts
B Das Segelflugzeug
C Das schneller fliegende Luftfahrzeug
D Das motorgetriebene Luftfahrzeug

178 Luftfahrzeuge, die Gegenstände schleppen, haben Vorflugrecht vor ...

A motorgetriebenen Luftfahrzeugen
B allen Luftfahrzeugen
C Segelflugzeugen
D Motorseglern mit abgeschaltetem Motor

179 Ein Pilot beobachtet einen Motorsegler (Motor in Betrieb), der in nahezu gleicher Höhe von links kommt und seinen Flugweg kreuzen wird. Wer muss ausweichen?

A Der Motorsegler dem Flugzeug
B Das Flugzeug dem Motorsegler
C Das Luftfahrzeug mit der höheren Geschwindigkeit
D Beide Luftfahrzeuge müssen die Kurse ändern

180 Bei Luftfahrzeugen im Endanflug hat ...

A das tiefer fliegende Luftfahrzeug Vorflugrecht
B das höher fliegende Luftfahrzeug Vorflugrecht
C in jedem Fall das mehrsitzige Luftfahrzeug Vorflugrecht
D das tiefer fliegende Luftfahrzeug eine lange Landung zu machen

181 Wann müssen alle Luftfahrzeuge Positionslichter einschalten?

A Nachts
B Bei Nacht und schlechten Sichtverhältnissen
C Von SS+30 bis SR
D Von SS+30 bis SR+30

182 Das Zusammenstoß-Warnlicht (anti-collision light) ist ...

A von allen Luftfahrzeugen in der Nacht zu führen
B vom Start bis zur Landung von Luftfahrzeugen zu führen
C vom Start bis zur Landung in der Nacht und am Tage bei ungünstigen Sichtverhältnissen zu führen
D von in Betrieb befindlichen Luftfahrzeugen in der Nacht und am Tage bei ungünstigen Sichtverhältnissen zu führen

183 Ein in der Signalfläche ausgelegtes waagerechtes quadratisches rotes Feld mit zwei gelben Diagonalstreifen bedeutet:

A Landeverbot für längere Zeit
B Der Flugplatz ist für kurze Zeit gesperrt
C Der Flugplatz ist für längere Zeit unbenutzbar
D Start- und Landeverbot für längere Zeit

184 Eine in der Signalfläche ausgelegte waagerechte weiße Fläche in Form einer Hantel bedeutet:

A Zum Starten, Landen und Rollen dürfen nur Start- und Landebahnen und Rollbahnen benutzt werden
B Zum Starten ist die Rollbahn zu benutzen
C Landeverbot für Luftsportgeräte
D Rollbahn darf zur Zeit nicht benutzt werden

185 Ein weißes oder orangefarbenes "T" (Lande-T), das bei Nacht entweder beleuchtet oder durch weiße Lichter dargestellt ist, bedeutet:

A Starts und Landungen sind parallel zum Längsbalken des Lande-T in Richtung auf den Querbalken durchzuführen
B Startverbot
C Starts und Landungen nur auf der Piste durchführen
D Neben dem Lande-T aufsetzen

186 Eine zweistellige Zahl auf einer Tafel, die am Kontrollturm oder in dessen Nähe senkrecht angebracht ist, bedeutet:

A Die Startrichtung, gerundet auf die nächstliegenden 10° der missweisenden Kompassrose
B Die beiden Endziffern des QNH
C Die Landerichtung, abgerundet auf den missweisenden Steuerkurs
D Die Temperatur

187 Ein in der Signalfläche oder am Ende der Piste waagerecht ausgelegter und nach rechts abgewinkelter Pfeil in auffallender Farbe bedeutet:

A Nach dem Start und vor der Landung sind Richtungsänderungen nur nach rechts erlaubt
B Rollbewegungen nur nach rechts ausführen
C Rechts neben der Bahn starten und landen
D Vorflugrecht von rechts kommender Luftfahrzeuge beachten

188 Welche Bedeutung hat ein grünes Dauersignal, das auf ein Luftfahrzeug im Flug gerichtet ist?

A Landung freigegeben
B Auf diesem Flugplatz landen und zum Vorfeld rollen
C Platzrunde fortsetzen, anderes Luftfahrzeug hat Vorflug
D Zum Startflugplatz zurückkehren

189 Welche Bedeutung hat ein rotes Dauersignal, das auf ein Luftfahrzeug im Flug gerichtet ist?

A Anderes Luftfahrzeug hat Vorflug, Platzrunde fortsetzen
B Zwecks Landung zurückkehren (Lande- und Rollfreigaben werden zum gegebenen Zeitpunkt erteilt)
C Nicht landen, Flugplatz unbenutzbar
D Ungeachtet aller früheren Anweisungen und Freigaben zur Zeit nicht landen

190 Welche Bedeutung hat ein grünes Blinksignal, das auf ein Luftfahrzeug im Flug gerichtet ist?

A Zwecks Landung zurückkehren (Lande- und Rollfreigaben werden zum gegebenen Zeitpunkt erteilt)
B Landung freigegeben
C Platzrunde fortsetzen, anderes Luftfahrzeug hat Vorflug
D Auf diesem Flugplatz landen und zum Vorfeld rollen

191 Welche Bedeutung hat ein rotes Blinksignal, das auf ein Luftfahrzeug im Flug gerichtet ist?

A Nicht landen, Flugplatz unbenutzbar
B Platzrunde fortsetzen
C Platzrunde verlassen
D Sofort landen

192 Welche Bedeutung hat ein weißes Blinksignal, das auf ein Luftfahrzeug im Flug gerichtet ist?

A Auf diesem Flugplatz landen und zum Vorfeld rollen (Lande- und Rollfreigaben werden zum gegebenen Zeitpunkt erteilt)
B Auf diesem Flugplatz nicht landen
C Platzrunde verlassen
D Platzrunde fortsetzen

193 Welche Bedeutung hat ein roter Feuerwerkskörper, der auf ein Luftfahrzeug im Flug gerichtet ist?

A Ungeachtet aller früheren Anweisungen und Freigaben zur Zeit nicht landen
B Gefahr! Platzrunde sofort verlassen
C Flugbeschränkungsgebiet! Gebiet sofort verlassen
D Gefahrengebiet! Gebiet sofort verlassen

194 Welche Bedeutung hat ein grünes Dauersignal, das auf ein Luftfahrzeug am Boden gerichtet ist?

A Start freigegeben
B Halt!
C Zum Ausgangspunkt auf dem Flugplatz zurückkehren
D Rollerlaubnis erteilt

195 Welche Bedeutung hat ein rotes Dauersignal, das auf ein Luftfahrzeug am Boden gerichtet ist?

A Halt!
B Benutzte Landefläche freimachen
C Piste verlassen
D Rollbahn verlassen

196 Welche Bedeutung hat ein grünes Blinksignal, das auf ein Luftfahrzeug am Boden gerichtet ist?

A Rollerlaubnis erteilt
B Start freigegeben
C Piste frei von Hindernissen
D Zum Ausgangspunkt auf dem Flugplatz zurückrollen

197 Welche Bedeutung hat ein rotes Blinksignal, das auf ein Luftfahrzeug am Boden gerichtet ist?

A Benutzte Landefläche freimachen
B Halt!
C Start freigegeben
D Zum Ausgangspunkt auf dem Flugplatz zurückrollen

198 Welche Bedeutung hat ein weißes Blinksignal, das auf ein Luftfahrzeug am Boden gerichtet ist?

A Zum Ausgangspunkt auf dem Flughafen zurückkehren
B Start freigegeben
C Ungeachtet aller früheren Anweisungen und Freigaben zur Zeit nicht rollen und nicht starten
D Benutzte Landefläche freimachen

199 Flugplatzverkehr bezieht sich auf ...

A den gesamten Verkehr auf dem Rollfeld eines Flugplatzes und alle in der Nähe eines Flugplatzes fliegenden Luftfahrzeuge. Ein Luftfahrzeug ist in der Nähe eines Flugplatzes, wenn es sich unter anderem in einer Platzrunde befindet, in diese einfliegt oder sie verlässt
B alle Luftfahrzeuge, die sich in der Platzrunde befinden
C alle Luftfahrzeuge, die sich auf dem Rollfeld befinden
D den gesamten Verkehr auf dem Rollfeld eines Flugplatzes und alle Luftfahrzeuge, die in die Platzrunde einfliegen

200 Wann befindet sich ein Luftfahrzeug im “Gegenanflug 16“? Wenn es einen Kurs von ...

A 340° fliegt und der Flugplatz links vom Luftfahrzeug liegt
B 340° fliegt und der Flugplatz rechts vom Luftfahrzeug liegt
C 160° fliegt und der Flugplatz links vom Luftfahrzeug liegt
D 160° fliegt und der Flugplatz rechts vom Luftfahrzeug liegt

201 Richtungsänderungen in der Platzrunde sind normalerweise ...

A in Linkskurven auszuführen
B nach Süden auszuführen
C in Rechtskurven auszuführen
D nach Norden auszuführen

202 Richtungsänderungen beim An- und Abflug sind normalerweise ...

A in Linkskurven auszuführen
B nach Süden auszuführen
C in Rechtskurven auszuführen
D nach Norden auszuführen

203 Wessen Signale und Zeichen hat der Pilot auf dem Vorfeld und den Abstellflächen eines Flugplatzes mit Flugverkehrskontrolle zu befolgen? Die ...

A des Flugplatzunternehmers
B des Kontrollturmes
C der Landesluftfahrtbehörde
D des Luftfahrtbundesamtes

204 Ein Pilot befindet sich auf einem VFR-Flug zu einem Flugplatz mit Flugverkehrskontrolle. Mit dem Kontrollturm kann keine Funkverbindung hergestellt werden. Was muss der Pilot beachten?

A Er muss auf einem Flugplatz außerhalb der Kontrollzone landen. Nur aus flugbetrieblichen Gründen darf der Flug in die CTR fortgesetzt werden
B Er muss in jedem Fall zu dem im Flugplan angegebenen Ausweichflugplatz weiterfliegen
C Er darf in keinem Fall in die Kontrollzone einfliegen
D Er muss eine Blindsendung absetzen und den Flug entsprechend der im Luftfahrthandbuch festgelegten VFR-Einflugstrecke fortsetzen

205 Bei einem Flug nach Sichtflugregeln hat der Pilot eine Freigabe zum Einflug in die Kontrollzone und Landeanweisungen erhalten und bestätigt. Kurze Zeit danach fällt das Sprechfunkgerät aus.  Wie hat sich der Pilot zu verhalten?

A Den Flug entsprechend der Flugverkehrskontrollfreigabe fortsetzen
B Auf einem Flugplatz außerhalb der Kontrollzone landen und eine Landemeldung durchgeben
C Den Flug zu dem im Flugplan angegebenen Ausweichflugplatz fortsetzen
D 10 Minuten außerhalb der Kontrollzone kreisen und dann den Anflug fortsetzen

206 Die Flugsicht wird definiert als die ...

A Sicht in Flugrichtung aus dem Cockpit eines im Flug befindlichen Luftfahrzeuges
B maximale Voraussicht aus dem Cockpit eines Luftfahrzeuges am Boden
C Sicht aus dem Cockpit eines Luftfahrzeuges im Flug zum Erdboden
D mittlere Schrägsicht aus dem Cockpit eines Luftfahrzeuges im Flug

207 Der horizontale Mindestabstand zu Wolken bei einem VFR-Flug im Luftraum D (CTR) beträgt:

A 1500 m
B 300 m
C 1500 ft
D 300 ft

208 Im Luftraum E unterhalb FL 100 sind Flüge nach Sichtflugregeln so durchzuführen, dass ...

A der Pilot eine Flugsicht von mindestens 5 km hat und das Luftfahrzeug von den Wolken in waagerechter Richtung mindestens 1500 m, in senkrechter Richtung mindestens 300 m (1000 ft) Abstand hält
B eine Bodensicht von mindestens 5 km herrscht
C der Pilot eine Flugsicht von mindestens 5 km hat und das Luftfahrzeug von den Wolken in waagerechter Richtung mindestens 300 m, in senkrechter Richtung mindestens 300 ft Abstand hält
D der Pilot eine Flugsicht von mindestens 8 km hat und das Luftfahrzeug von den Wolken in waagerechter Richtung mindestens 1500 m, in senkrechter Richtung mindestens 300 m (1000 ft) Abstand hält, sowie eine Bodensicht von mindestens 5 km herrscht

209 Bei Flügen nach Sichtflugregeln im Luftraum G in und unter 3000 ft AMSL/1000 ft AGL müssen folgende Voraussetzungen erfüllt sein:

A Bodensicht, Flugsicht mindestens 1500 m, frei von Wolken, maximal 140 kt
B Flugsicht mindestens 1500 m, Wolken dürfen nicht berührt werden
C Bodensicht mindestens 5 km, Hauptwolkenuntergrenze mindestens 1500 ft, maximal 140 kt
D Flugsicht mindestens 1500 m, Abstand von Wolken in waagerechter Richtung 300 m, in senkrechter Richtung 2000 ft

210 Ist für einen VFR-Flug im Luftraum G in und unter 3000 ft AMSL/1000 ft AGL ein bestimmter Wolkenabstand vorgeschrieben?

A Nein, der Luftraum muss frei von Wolken sein
B Ja, mindestens 1,5 km in waagerechter und mindestens 1000 ft in senkrechter Richtung
C Ja, mindestens 1,5 km in waagerechter Richtung
D Ja, mindestens 1,5 NM in waagerechter Richtung

211 In welchem Luftraum können Sonderflüge nach Sichtflugregeln durchgeführt werden?

A Im Luftraum D (CTR)
B In den Lufträumen C und D
C Im Luftraum E
D Nur in FL 100 und darüber

212 Wann ist mit der Standard-Höhenmessereinstellung bei Flügen nach den Sichtflugregeln zu fliegen?

A Bei Flügen oberhalb 5000 ft AMSL oder 2000 ft AGL, sofern diese Flughöhe 5000 ft AMSL überschreitet
B Bei Flügen unter 5000 ft AMSL
C Bei Flügen bis zu 5000 ft AGL
D Hierfür gelten unterschiedliche Vorschriften

213 Bei VFR-Flügen oberhalb einer Höhe von 5000 ft AMSL oder 2000 ft AGL, sofern diese Flughöhe 5000 ft AMSL überschreitet, ist der Höhenmesser einzustellen auf:

A 1013,2 hPa
B QFF
C QNH
D QFE

214 Bei VFR-Flügen bis zu einer Höhe von 5000 ft AMSL oder 2000 ft AGL, sofern diese Flughöhe 5000 ft AMSL überschreitet, ist der Höhenmesser einzustellen auf:

A das QNH des zur Flugstrecke nächstgelegenen Flugplatzes mit Flugverkehrskontrolle
B das QNH des nächstgelegenen Flughafens
C das QFE des nächstgelegenen Flugplatzes mit Flugverkehrskontrolle
D 1013,2 hPa

215 Woraus ergibt sich die Festlegung des Sektors für die Halbkreisflughöhen nach Sichtflugregeln?  Aus dem ...

A missweisenden Kurs über Grund
B rechtweisenden Kartenkurs
C Kompasskurs
D rechtweisenden Kurs über Grund

216 Welche Flugfläche/n ist / sind bei einem VFR-Flug nach Standard-Höhenmessereinstellung bei einem missweisenden Kurs über Grund von 135° einzuhalten?

A 55, 75, 95
B 65, 85, 105
C 50, 70, 90
D 60, 80, 100

217 Welche Fluginformationsgebiete (FIR) unter deutscher Zuständigkeit gibt es im unteren Luftraum?

A Bremen, Langen, München
B Berlin, Hamburg, Frankfurt, München
C Bremen, Berlin, Hannover, Düsseldorf, Stuttgart
D Berlin, Hannover, Maastricht, Rhein, Langen

218 Eine Zone mit Funkkommunikationspflicht (RMZ) reicht bis zu einer Höhe von:

A 1000 ft AGL
B 1000 ft AMSL
C 3000 ft AMSL
D 2500 ft AGL

219 Eine Zone mit Funkkommunikationspflicht (RMZ) reicht vom Boden bis …

A 1000 ft AGL
B 1700 ft AGL
C 3000 ft AGL
D 2500 ft AGL

220 In Deutschland sind Kontrollzonen klassifiziert ...

A als Luftraum D
B überwiegend als Luftraum D, nur einige als Luftraum C
C um Flughäfen als Luftraum C, die übrigen als Luftraum D
D um Militärflugplätze als Luftraum B, um Flughäfen als Luftraum C, alle übrigen als Luftraum D

221 Eine mit "HX" gekennzeichnete Kontrollzone kann außerhalb der Betriebszeit ohne Freigabe durchflogen werden, wenn der Pilot ...

A sich vor dem Durchflug von der zuständigen Flugplatzkontrolle (TWR), außerhalb der TWR-Betriebszeiten beim Flugplatzinformationsdienst (INFO), oder beim Fluginformationsdienst (FIS) die Nichtwirksamkeit bestätigen lässt
B eine schriftliche Zustimmung des Flugplatzkommandanten erhalten hat
C sich vor Antritt des Fluges bei der militärischen Flugleitung die Nichtwirksamkeit nochmals bestätigen lässt
D sich über die Nichtwirksamkeit im Luftfahrthandbuch informiert

222 Welche Luftraumklassen sind kontrollierter Luftraum?

A C, D, E
B C, D, F
C E, F, G
D C, E, F

223 Der Luftraum E erstreckt sich, soweit nicht anders klassifiziert ...

A ab 1000 ft AGL und 1700 ft AGL, ansonsten ab 2500 ft AGL bis FL 100
B ab 1000 ft und 1700 ft AGL, ansonsten ab 5000 ft AMSL bis FL 200
C von 1000 ft und 1700 ft AGL bis 5000 ft AMSL
D ab 1000 ft und 1700 ft AGL, ansonsten ab 2500 ft AGL bis FL 200

224 Ein mit "ED-R... (TRA)" gekennzeichnetes Gebiet ist ein ...

A Gebiet mit Flugbeschränkungen
B Gefahrengebiet
C Sperrgebiet
D Segelflugbeschränkungsgebiet

225 Ein mit "ED-D..." gekennzeichnetes Gebiet ist ein ...

A Gefahrengebiet
B Gebiet mit Flugbeschränkungen
C Truppenübungsplatz
D Sperrgebiet

226 Wann müssen Luftfahrzeuge für Überlandflüge nach Sichtflugregeln mit einem UKW-Sende- und Empfangsgerät ausgerüstet sein?

A Stets
B Nur bei Flügen von und zu Flugplätzen ohne Flugverkehrskontrolle
C Nur bei Auslandsflügen
D Nur bei Flügen zu kontrollierten Flugplätzen

227 VFR-Flüge über geschlossenen Wolkendecken dürfen durchgeführt werden:

A wenn das Luftfahrzeug u.a. mit einem UKW-Sende-/Empfangsgerät und einer VOR-NavigationsEmpfangsanlage oder mit einem automatischen Funkpeilgerät (ADF) ausgerüstet ist
B grundsätzlich nicht
C nur mit einer CVFR-Berechtigung
D nur nach Freigabe durch die Flugverkehrskontrolle

228 Welcher Mode/Code muss von motorgetriebenen Luftfahrzeugen bei VFR-Flügen oberhalb 5000 ft AMSL oder oberhalb von 3500 ft AGL, wobei der höhere Wert maßgebend ist, unaufgefordert geschaltet werden?

A A/C 7000
B Der Transponder darf unaufgefordert nicht geschaltet werden
C A/C 7600
D A/C 7700

229 Beim Sinkflug von FL 85 auf Flughöhe 3500 ft AMSL hat der Pilot eines motorgetriebenen Luftfahrzeuges vor Erreichen der neuen Reiseflughöhe den Höhenmesser und den Transponder wie folgt einzustellen:

A QNH einstellen und den Mode/Code A/C 7000 beibehalten
B QNH 1013,2 hPa einstellen und Transponder auf "STAND-BY" schalten
C QNH einstellen und Mode/Code A/C 7600 beibehalten
D 1013,2 hPa einstellen und Mode/Code A/C 7600 einschalten

230 In Gebieten mit Transponderpflicht (TMZ) müssen Luftfahrzeuge bei VFR-Flügen mit einem ...

A Transponder mit automatischer Höhenübermittlung ausgerüstet sein und den Code 7000 unaufgefordert abstrahlen
B Transponder mit automatischer Höhenübermittlung ausgerüstet sein und den Code 7500 unaufgefordert abstrahlen
C Transponder mit automatischer Höhenübermittlung ausgerüstet sein und den Code 7600 unaufgefordert abstrahlen
D Transponder mit automatischer Höhenübermittlung ausgerüstet sein und den Code 7700 unaufgefordert abstrahlen

231 Was versteht man unter dem Begriff "EIGENPEILUNG"?

A Standortbestimmung durch bordeigene Navigationsempfangsanlagen
B Terrestrische Navigation
C Standortbestimmung durch bodenseitigen Einsatz von Radar
D Kreuzpeilung mittels Peilfunkstellen

232 Mit welcher Navigationsfunkanlage kann Fremdpeilung durchgeführt werden? Mit einer ...

A UKW-Peilstelle (VDF)
B VOR/DME-Anlage
C NDB-Anlage
D TACAN-Anlage

233 Die Kennung eines UKW-Drehfunkfeuers (VOR) besteht in der Regel aus ...

A drei Buchstaben im Morsecode
B einem Blinkzeichen
C einem Rufnamen
D zwei Buchstaben im Morsecode

234 Ein VOR-Anzeigegerät ist ein "Kommandogerät", wenn mit ...

A FROM-Anzeige von der VOR-Anlage abgeflogen wird
B TO-Anzeige von der VOR-Anlage abgeflogen wird
C OFF-Anzeige die VOR-Anlage angeflogen wird
D FROM-Anzeige die VOR-Anlage angeflogen wird

235 Wovon ist die Empfangsreichweite eines UKW-Drehfunkfeuers (VOR) abhängig? Von ...

A der Flughöhe des Luftfahrzeuges
B der Art des Luftfahrzeugmusters
C der Geschwindigkeit des Luftfahrzeuges
D dem Kurs des Luftfahrzeuges

236 Der mit "OBS" gekennzeichnete Knopf am VOR-Anzeigegerät ist der ...

A Kurswähler
B Frequenzwahlschalter
C Lautstärkeregler
D TO/FROM-Umschalter

237 Auf welche Richtung ist der Radial einer VOR-Station bezogen? Auf ...

A missweisend Nord
B QTE
C die Flugzeuglängsachse
D rechtweisend Nord

238 UKW-Drehfunkfeuer (VOR) arbeiten im Frequenzbereich von ...

A 108 MHz bis 117,975 MHz
B 200 MHz bis 1750 MHz
C 108 MHz bis 112 MHz
D 118 MHz bis 137 MHz

239 Wann wechselt am VOR-Anzeigegerät die Richtungsanzeige von "TO" auf "FROM"?

A Beim Überfliegen der VOR-Station
B Bei einer Änderung des Steuerkurses um 90°
C Bei einer Änderung des Steuerkurses um 180°
D Beim Betätigen des IDENT-Knopfes

240 Ein Luftfahrzeug befindet sich im Anflug auf eine VOR-Station. Eingestellt ist 320° bei einer Richtungsanzeige "TO". Der Ablageanzeiger (CDI) wandert nach links aus. Wo befindet sich das Luftfahrzeug?

A Rechts vom Radial
B Links vom Radial
C Auf dem Radial
D Südlich des Radiales

241 Ein mit einer VOR-Navigations-Empfangsanlage ausgerüstetes Luftfahrzeug will eine VOR-Station auf dem kürzesten Weg anfliegen. Welche Aussage ist richtig? Der Kurswähler wird so lange gedreht, bis die ...

A vertikale Nadel in Mittelstellung ist und der Richtungsanzeiger "TO" anzeigt. Der am Kurswähler angezeigte Zahlenwert gibt den direkten Kurs zur Station an
B vertikale Nadel in Mittelstellung ist und der Richtungsanzeiger "FROM" anzeigt. Der am Kurswähler angezeigte Zahlenwert gibt den direkten Kurs zur Station an
C horizontale Nadel in der Mitte steht und die "OFF-Anzeige" verschwindet. Der am Kurswähler angezeigte Zahlenwert gibt immer den direkten Kurs zur Station an
D vertikale Nadel bei einer "TO-Anzeige" voll links ausschlägt. Der am Kurswähler angezeigte Zahlenwert stellt die kürzeste Verbindung zur Station dar

242 Wie groß ist die Kursablage pro Punkt (dot) auf dem VOR-Anzeigegerät?

A 2°
B 10°
C 5°
D 1°

243 Auf der ICAO-Luftfahrtkarte 1:500000 finden Sie die Angabe "TRENT 108,45 TRT". Um welche Art von Funknavigationsanlage handelt es sich dabei? Um ein(e) ...

A UKW-Drehfunkfeuer (VOR)
B Peilfunkanlage (VDF)
C Ungerichtetes Funkfeuer (NDB)
D Instrumenten-Landesystem (ILS)

244 Beim Anflug auf eine VOR-Station erscheint kurz vor der berechneten Überflugzeit die OFF-Flagge.  Was ist wahrscheinlich die Ursache?

A Das Flugzeug befindet sich über der Station
B Der VOR-Empfänger ist ausgefallen
C Die VOR-Station ist ausgefallen
D Die TO/FROM-Anzeige ist defekt

245 Die Richtung eines VOR-Leitstrahls (Radial) entspricht dem ...

A QDR
B QDM
C QTE
D QUJ

246 Welche Kennung hat ein ungerichtetes Funkfeuer (NDB)?

A Zwei oder drei Buchstaben im Morsecode
B Zwei oder drei Ziffern im Morsecode
C Ziffern und Buchstaben im Morsecode
D Eine Sprachkennung

247 Ungerichtete Funkfeuer (NDB) haben eine festgelegte Betriebsentfernung von ...

A 15 NM bis 100 NM
B höchstens 25 NM
C mindestens 60 NM
D weit über 100 NM

248 Ungerichtete Funkfeuer (NDB) arbeiten im ...

A LW- und MW-Bereich
B UKW-Bereich
C KW-Bereich
D UHF-Bereich

249 Mit welcher bordseitigen Navigationsempfangsanlage kann ein NDB empfangen werden? Mit einem ...

A Funkkompass (ADF)
B Marker-Empfänger
C VOR-Empfänger
D ILS-Empfänger

250 Welcher Winkel wird am Anzeigegerät (RBI) des Funkkompasses (ADF) angezeigt? Der Winkel zwischen ...

A Flugzeuglängsachse und der Richtung zu dem eingestellten NDB
B recht- und missweisend Nord
C geographisch Nord und dem eingestellten NDB
D missweisend Nord und der Flugzeuglängsachse

251 Der missweisende Steuerkurs eines Luftfahrzeuges beträgt 155°. Die Bezugspeilung ist 025°. Wie groß ist das QDM?

A 180°
B 360°
C 130°
D 025°

252 Welche Ausrüstung an Bord eines Luftfahrzeuges ist erforderlich, um mit Hilfe von Peilfunkstellen navigieren zu können? Ein ...

A UKW-Sprechfunkgerät
B Transponder
C Funkkompass
D VOR-Empfänger

253 Ein Luftfahrzeug fliegt einen missweisenden Steuerkurs von 090°. Das übermittelte QDR beträgt 180°. Wo liegt die Peilfunkstelle?

A Links vom Flugweg
B Rechts vom Flugweg
C Voraus
D Südlich vom Flugweg

254 Von einer mit einem UKW-Peiler ausgestatteten Bodenfunkstelle erhält man ein QDM von 225°. Wo befindet sich das Luftfahrzeug?

A Nordöstlich der Station
B Südwestlich der Station
C Südöstlich der Station
D Nordwestlich der Station

255 Auf der ICAO-Luftfahrtkarte 1:500000 ist die Frequenz einer Bodenfunkstelle an einem Landeplatz unterstrichen. Was bedeutet die Unterstreichung der Frequenz?

A Peilungen sind auf Anforderung verfügbar
B Die Bodenfunkstelle ist H24 betriebsbereit
C Die Bodenfunkstelle wird nur auf Anforderung betrieben
D Auf dieser Frequenz ist ATIS verfügbar

256 Wozu dient Sekundärradar in der Flugsicherung? Zur ...

A Identifizierung von Luftfahrzeugen und Erlangung zusätzlicher Informationen über VFR-Flüge
B frühzeitigen Erkennung von Schlechtwettergebieten
C Erkennung der wahren Eigengeschwindigkeit von Luftfahrzeugen
D Standortbestimmung durch den Piloten

257 Welche Angaben kann ein Pilot von einer Flugverkehrskontrollstelle mit Radar erhalten? Angaben über ...

A den Standort des Luftfahrzeuges
B die wahre Eigengeschwindigkeit
C die Fluglage des Luftfahrzeuges
D den beabsichtigten Flugweg

258 Die Abkürzung "GPS" bedeutet in der Luftfahrt:

A Globales Positionsbestimmungssystem
B Geographisches Punktsystem
C Großkreis-Planungsschablone
D GAT-Positionierungssystem

259 Das "GLOBAL POSITIONSBESTIMMUNGSSYSTEM (GPS)" ist ein ...

A satellitengestütztes Navigationssystem
B weltweites System zur Vereinheitlichung der terrestrischen Navigation
C Verfahren zur Positionierung von Flugzeugen auf dem Vorfeld
D bodenabhängiges Funknavigationssystem

260 Wozu dienen GPS-Empfänger an Bord von Luftfahrzeugen?

A Der Auswertung und Anzeige von Satellitensignalen zu navigatorischen Zwecken (z.B. Position, Kurs, Geschwindigkeit, Entfernung)
B Der Standortbestimmung mittels bordeigenem Radar
C Der Bestimmung des Abstandes zu anderen Luftfahrzeugen
D Der Auswertung von Signalen bodenseitiger Funknavigationsanlagen zur Positions- und Kursbestimmung
"""

if __name__ == '__main__':
    main()
