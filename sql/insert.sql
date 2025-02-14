INSERT INTO public.mitarbeiter (vorname, nachname, stunden, rolle, krank, telefonnummer) VALUES
('Anna', 'Müller', 0, 2, false, '0123456789'),
('Bernd', 'Schmidt', 0, 2, false, '0123456790'),
('Claudia', 'Schneider', 0, 2, false, '0123456791'),
('David', 'Fischer', 0, 2, false, '0123456792'),
('Eva', 'Weber', 0, 2, false, '0123456793'),
('Frank', 'Wagner', 0, 2, false, '0123456794'),
('Gisela', 'Becker', 0, 2, false, '0123456795'),
('Hans', 'Hoffmann', 0, 2, false, '0123456796'),
('Inge', 'Schäfer', 0, 2, false, '0123456797'),
('Jochen', 'Koch', 0, 2, false, '0123456798'),
('Karla', 'Richter', 0, 2, false, '0123456799'),
('Lena', 'Klein', 0, 2, false, '0123456800'),
('Martin', 'Wolf', 0, 2, false, '0123456801'),
('Nina', 'Schwarz', 0, 3, false, '0123456802'), -- Rolle 3
('Olaf', 'Zimmermann', 0, 4, false, '0123456803'); -- Rolle 4

INSERT INTO public.student (vorname, nachname, rolle) VALUES
('Max', 'Mustermann', 1),
('Anna', 'Schmidt', 1),
('Julia', 'Müller', 1),
('Kevin', 'Hoffmann', 1),
('Lena', 'Becker', 1),
('Felix', 'Schulz', 1),
('Laura', 'Wagner', 1),
('Paul', 'Koch', 1),
('Sarah', 'Schneider', 1),
('Tim', 'Bauer', 1),
('Marie', 'Richter', 1),
('Tom', 'Wolf', 1),
('Hannah', 'Neumann', 1),
('Simon', 'Lange', 1),
('Melanie', 'Schwarz', 1),
('Markus', 'Weber', 1),
('Lisa', 'Zimmermann', 1),
('Christian', 'Fischer', 1),
('Nicole', 'Herrmann', 1),
('Andreas', 'Scholz', 1),
('Sandra', 'Lehmann', 1),
('Stefan', 'Jäger', 1),
('Carina', 'Huber', 1),
('Daniel', 'Krause', 1),
('Jana', 'Vogel', 1),
('Patrick', 'Stein', 1),
('Jessica', 'Bergmann', 1),
('Martin', 'Günther', 1),
('Julian', 'Kaiser', 1),
('Vanessa', 'Peters', 1);

INSERT INTO public.veranstaltung (fachname, dauer) VALUES
('Mathe I', 2),
('Informatik Grundlagen', 4),
('Chemie Anfänger', 2),
('Physik Einführung', 4),
('Literaturgeschichte', 2),
('Psychologie Einführung', 4),
('Kunstgeschichte', 2),
('BWL Grundlagen', 4),
('Marketing-Strategien', 2),
('Internationales Recht', 4),
('Makroökonomie', 2),
('Mikroökonomie', 4),
('Statistik', 2),
('Lineare Algebra', 4),
('Java Programmierung', 2),
('Webentwicklung HTML/CSS', 4),
('Medizinische Ethik', 2),
('Biologie Mediziner', 4),
('Geschichte Einführung', 2),
('Gegenwartssoziologie', 4),
('Philosophie Aufklärung', 2),
('Digitale Transformation', 4),
('Künstliche Intelligenz', 2),
('Nachhaltiges Management', 4),
('Architektur Geschichte', 2),
('Englische Literatur', 4),
('Gesundheitsökonomie', 2),
('Marketing', 4),
('Physikalische Chemie', 2),
('Kognitive Psychologie', 4);

INSERT INTO public.raum (name, campus) VALUES
('Raum A1', 'A'),
('Raum A2', 'A'),
('Raum A3', 'A'),
('Raum A4', 'A'),
('Raum A5', 'A'),
('Raum B1', 'B'),
('Raum B2', 'B'),
('Raum B3', 'B'),
('Raum B4', 'B'),
('Raum B5', 'B');











