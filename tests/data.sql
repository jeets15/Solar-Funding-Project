-- Data to add into separate test database for unit tests

-- Use werkzeug.security.generate_password_hash to generate hashes to insert
-- Don't forget to write down the plain text test passwords or the hashes are useless

INSERT INTO user (id, user_type, email_username, display_name, password_hash)
VALUES
    ('47fa9dc4-cb7a-44c0-ace2-a65d8705495e', 'householder', 'john.smith977@example.co.uk', 'John Smith',
        'scrypt:32768:8:1$mrhixSkl8zpgEzjw$1d0eb679f0627b2ad0aff80bae7f9b3b724519715da197de555c136b6f4a275510a31e8099ae5e7ed96c7f08e922fa75c56e4146294b8fcf45891bfa183c025e'), -- Password = "john!Smith977"
    ('3d1886b7-abec-49b9-b849-99ceb616b127', 'householder', 'jane.doe15@example.com', 'Jane Doe',
        'scrypt:32768:8:1$NzKNPOundEOjypTn$dd9534ea0c7eae235f329d3c699c99963cb8186cb6fd6ea91b4509d84f6367aac3e45cf01b5381413b2024c76bdba1405d684d53a639b753165bfc0cb09ec3b4'); -- Password = "12Jane!DoeDoe"