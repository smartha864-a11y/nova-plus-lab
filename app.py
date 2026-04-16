create table if not exists patients (
  id bigserial primary key,
  name text not null,
  age int,
  gender text,
  phone text,
  notes text default '',
  created_at timestamp default now()
);

create table if not exists test_catalog (
  id bigserial primary key,
  test_name text not null unique,
  category text default '',
  sell_price int not null default 0,
  active boolean default true,
  created_at timestamp default now()
);

create table if not exists orders (
  id bigserial primary key,
  patient_id bigint references patients(id) on delete cascade,
  patient_name text not null,
  total_price int not null default 0,
  paid_amount int not null default 0,
  due_amount int not null default 0,
  status text not null default 'آجل',
  created_at timestamp default now()
);

create table if not exists order_items (
  id bigserial primary key,
  order_id bigint references orders(id) on delete cascade,
  test_id bigint references test_catalog(id) on delete set null,
  test_name text not null,
  price int not null default 0
);

create table if not exists purchases (
  id bigserial primary key,
  item_name text not null,
  qty int not null default 0,
  unit_cost int not null default 0,
  total_cost int not null default 0,
  supplier text default '',
  notes text default '',
  created_at timestamp default now()
);
