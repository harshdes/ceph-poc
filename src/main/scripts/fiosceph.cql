CREATE KEYSPACE IF NOT EXISTS fiosceph WITH replication={'class':'SimpleStrategy', 'replication_factor': 1};
use fiosceph;

CREATE TABLE IF NOT EXISTS users (
    name text PRIMARY KEY,
    password text,
    emails set<text>);

CREATE TABLE IF NOT EXISTS tasks (
    id text PRIMARY KEY,
    state text);