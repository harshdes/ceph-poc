create keyspace fiosceph with replication={'class':'SimpleStrategy', 'replication_factor': 1};
use fiosceph;
create table users (name text primary key,  password text,  emails set<text>);