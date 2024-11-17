-- init.sql
ALTER SYSTEM SET wal_level = 'logical';

CREATE PUBLICATION dbz_publication FOR ALL TABLES
WITH (publish = 'insert, update')