-- Orphan network uuids report between study-server and network-store-server:
--   - networks stored in the iidm database (network-store-server) that are not referenced by any study
--     (study database, root_network.network_uuid)
--   - network uuids referenced by a study that no longer exist in the network store

\copy (SELECT network_uuid, study_uuid, id FROM root_network) TO '/tmp/study_network_uuids.csv' WITH CSV

CREATE TEMP TABLE study_networks (network_uuid uuid, study_uuid uuid, root_network_uuid uuid);
\copy study_networks FROM '/tmp/study_network_uuids.csv' WITH CSV
CREATE INDEX ON study_networks (network_uuid);

SELECT (SELECT count(*) FROM network n WHERE n.variantnum = 0) AS nb_networks_in_network_store,
       (SELECT count(DISTINCT network_uuid) FROM study_networks) AS nb_networks_in_study,
       (SELECT count(*) FROM network n
        WHERE n.variantnum = 0
          AND NOT EXISTS (SELECT 1 FROM study_networks s WHERE s.network_uuid = n.uuid)) AS nb_orphans_in_network_store,
       (SELECT count(DISTINCT s.network_uuid) FROM study_networks s
        WHERE NOT EXISTS (SELECT 1 FROM network n WHERE n.uuid = s.network_uuid)) AS nb_missing_in_network_store;

SELECT n.uuid AS network_uuid,
       n.id   AS network_id,
       n.name,
       n.casedate,
       (SELECT count(*) FROM network v WHERE v.uuid = n.uuid) AS nb_variants
FROM network n
WHERE n.variantnum = 0
  AND NOT EXISTS (SELECT 1 FROM study_networks s WHERE s.network_uuid = n.uuid)
ORDER BY n.casedate;
