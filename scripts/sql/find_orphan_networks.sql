--  psql --single-transaction -h host_name -U user_name -d iidm -f find_orphan_networks.sql

CREATE EXTENSION IF NOT EXISTS postgres_fdw;
CREATE SERVER lnk_study FOREIGN DATA WRAPPER postgres_fdw OPTIONS (dbname 'study');
CREATE USER MAPPING FOR CURRENT_USER SERVER lnk_study OPTIONS (user 'user_name');
IMPORT FOREIGN SCHEMA public LIMIT TO (root_network) FROM SERVER lnk_study INTO public;

SELECT n.uuid, n.id, n.name, n.casedate
FROM network n
WHERE n.variantnum = 0
  AND NOT EXISTS (SELECT 1 FROM root_network r WHERE r.network_uuid = n.uuid)
ORDER BY n.casedate;

DROP SERVER lnk_study CASCADE;
