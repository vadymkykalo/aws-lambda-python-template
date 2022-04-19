
-- create your init query if you need

CREATE TABLE public.test_tester
(
    id                     uuid                                         not null
        constraint test_tester_pkey
            primary key,
    name              text                                         not null,
    created_on             timestamp with time zone                     not null
);

-- init table
INSERT INTO public.test_tester (id, name, created_on) VALUES ('f17e187d-fdb6-4bce-b787-58fa49fc5d1d', 'TEST', '2020-01-28 13:36:55.840000 +00:00');

