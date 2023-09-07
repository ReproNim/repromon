--
-- PostgreSQL database dump
--

-- Dumped from database version 15.4
-- Dumped by pg_dump version 15.4

-- Started on 2023-09-07 10:31:03 EEST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5 (class 2615 OID 2200)
-- Name: repromon; Type: SCHEMA; Schema: -; Owner: pg_database_owner
--

CREATE SCHEMA repromon;


ALTER SCHEMA repromon OWNER TO pg_database_owner;

--
-- TOC entry 3709 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA repromon; Type: COMMENT; Schema: -; Owner: pg_database_owner
--

COMMENT ON SCHEMA repromon IS 'ReproMon app schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 214 (class 1259 OID 16470)
-- Name: data_provider; Type: TABLE; Schema: repromon; Owner: postgres
--

CREATE TABLE repromon.data_provider (
    id integer NOT NULL,
    provider character varying(15) NOT NULL
);


ALTER TABLE repromon.data_provider OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16473)
-- Name: device; Type: TABLE; Schema: repromon; Owner: postgres
--

CREATE TABLE repromon.device (
    id integer NOT NULL,
    kind character varying(15) NOT NULL,
    description character varying(128) NOT NULL
);


ALTER TABLE repromon.device OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16476)
-- Name: message_category; Type: TABLE; Schema: repromon; Owner: postgres
--

CREATE TABLE repromon.message_category (
    id integer NOT NULL,
    category character varying(45) NOT NULL
);


ALTER TABLE repromon.message_category OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16479)
-- Name: message_level; Type: TABLE; Schema: repromon; Owner: postgres
--

CREATE TABLE repromon.message_level (
    id integer NOT NULL,
    level character varying(8) NOT NULL
);


ALTER TABLE repromon.message_level OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16536)
-- Name: message_log; Type: TABLE; Schema: repromon; Owner: postgres
--

CREATE TABLE repromon.message_log (
    id integer NOT NULL,
    level_id integer NOT NULL,
    category_id integer NOT NULL,
    device_id integer NOT NULL,
    provider_id integer NOT NULL,
    study_id integer,
    study_name character varying(255),
    is_visible character(1) DEFAULT 'Y'::bpchar NOT NULL,
    visible_updated_on timestamp without time zone,
    visible_updated_by character varying(15),
    description character varying(255),
    payload json,
    event_on timestamp without time zone NOT NULL,
    registered_on timestamp without time zone NOT NULL,
    recorded_on timestamp without time zone NOT NULL,
    recorded_by character varying(15) NOT NULL
);


ALTER TABLE repromon.message_log OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16535)
-- Name: message_log_id_seq; Type: SEQUENCE; Schema: repromon; Owner: postgres
--

CREATE SEQUENCE repromon.message_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE repromon.message_log_id_seq OWNER TO postgres;

--
-- TOC entry 3710 (class 0 OID 0)
-- Dependencies: 220
-- Name: message_log_id_seq; Type: SEQUENCE OWNED BY; Schema: repromon; Owner: postgres
--

ALTER SEQUENCE repromon.message_log_id_seq OWNED BY repromon.message_log.id;


--
-- TOC entry 218 (class 1259 OID 16487)
-- Name: role; Type: TABLE; Schema: repromon; Owner: postgres
--

CREATE TABLE repromon.role (
    id integer NOT NULL,
    rolename character varying(45) NOT NULL,
    description character varying(128) NOT NULL
);


ALTER TABLE repromon.role OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16551)
-- Name: sec_user_device; Type: TABLE; Schema: repromon; Owner: postgres
--

CREATE TABLE repromon.sec_user_device (
    id integer NOT NULL,
    user_id integer NOT NULL,
    device_id integer NOT NULL
);


ALTER TABLE repromon.sec_user_device OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16550)
-- Name: sec_user_device_id_seq; Type: SEQUENCE; Schema: repromon; Owner: postgres
--

CREATE SEQUENCE repromon.sec_user_device_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE repromon.sec_user_device_id_seq OWNER TO postgres;

--
-- TOC entry 3711 (class 0 OID 0)
-- Dependencies: 222
-- Name: sec_user_device_id_seq; Type: SEQUENCE OWNED BY; Schema: repromon; Owner: postgres
--

ALTER SEQUENCE repromon.sec_user_device_id_seq OWNED BY repromon.sec_user_device.id;


--
-- TOC entry 225 (class 1259 OID 16560)
-- Name: sec_user_role; Type: TABLE; Schema: repromon; Owner: postgres
--

CREATE TABLE repromon.sec_user_role (
    id integer NOT NULL,
    user_id integer NOT NULL,
    role_id integer NOT NULL
);


ALTER TABLE repromon.sec_user_role OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16559)
-- Name: sec_user_role_id_seq; Type: SEQUENCE; Schema: repromon; Owner: postgres
--

CREATE SEQUENCE repromon.sec_user_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE repromon.sec_user_role_id_seq OWNER TO postgres;

--
-- TOC entry 3712 (class 0 OID 0)
-- Dependencies: 224
-- Name: sec_user_role_id_seq; Type: SEQUENCE OWNED BY; Schema: repromon; Owner: postgres
--

ALTER SEQUENCE repromon.sec_user_role_id_seq OWNED BY repromon.sec_user_role.id;


--
-- TOC entry 227 (class 1259 OID 16569)
-- Name: study_data; Type: TABLE; Schema: repromon; Owner: postgres
--

CREATE TABLE repromon.study_data (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    device_id integer,
    status_id integer,
    start_ts timestamp without time zone,
    end_ts timestamp without time zone,
    info json
);


ALTER TABLE repromon.study_data OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16568)
-- Name: study_data_id_seq; Type: SEQUENCE; Schema: repromon; Owner: postgres
--

CREATE SEQUENCE repromon.study_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE repromon.study_data_id_seq OWNER TO postgres;

--
-- TOC entry 3713 (class 0 OID 0)
-- Dependencies: 226
-- Name: study_data_id_seq; Type: SEQUENCE OWNED BY; Schema: repromon; Owner: postgres
--

ALTER SEQUENCE repromon.study_data_id_seq OWNED BY repromon.study_data.id;


--
-- TOC entry 219 (class 1259 OID 16511)
-- Name: study_status; Type: TABLE; Schema: repromon; Owner: postgres
--

CREATE TABLE repromon.study_status (
    id integer NOT NULL,
    status character varying(45) NOT NULL
);


ALTER TABLE repromon.study_status OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16578)
-- Name: user; Type: TABLE; Schema: repromon; Owner: postgres
--

CREATE TABLE repromon."user" (
    id integer NOT NULL,
    username character varying(15) NOT NULL,
    is_active character(1) DEFAULT 'N'::bpchar NOT NULL,
    is_system character(1) DEFAULT 'N'::bpchar NOT NULL,
    first_name character varying(45),
    last_name character varying(45),
    email character varying(128),
    phone character varying(16),
    description character varying(128),
    password character varying(128),
    password_changed_on timestamp without time zone,
    last_login timestamp without time zone
);


ALTER TABLE repromon."user" OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 16577)
-- Name: user_id_seq; Type: SEQUENCE; Schema: repromon; Owner: postgres
--

CREATE SEQUENCE repromon.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE repromon.user_id_seq OWNER TO postgres;

--
-- TOC entry 3714 (class 0 OID 0)
-- Dependencies: 228
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: repromon; Owner: postgres
--

ALTER SEQUENCE repromon.user_id_seq OWNED BY repromon."user".id;


--
-- TOC entry 3483 (class 2604 OID 16539)
-- Name: message_log id; Type: DEFAULT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.message_log ALTER COLUMN id SET DEFAULT nextval('repromon.message_log_id_seq'::regclass);


--
-- TOC entry 3485 (class 2604 OID 16554)
-- Name: sec_user_device id; Type: DEFAULT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.sec_user_device ALTER COLUMN id SET DEFAULT nextval('repromon.sec_user_device_id_seq'::regclass);


--
-- TOC entry 3486 (class 2604 OID 16563)
-- Name: sec_user_role id; Type: DEFAULT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.sec_user_role ALTER COLUMN id SET DEFAULT nextval('repromon.sec_user_role_id_seq'::regclass);


--
-- TOC entry 3487 (class 2604 OID 16572)
-- Name: study_data id; Type: DEFAULT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.study_data ALTER COLUMN id SET DEFAULT nextval('repromon.study_data_id_seq'::regclass);


--
-- TOC entry 3488 (class 2604 OID 16581)
-- Name: user id; Type: DEFAULT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon."user" ALTER COLUMN id SET DEFAULT nextval('repromon.user_id_seq'::regclass);


--
-- TOC entry 3688 (class 0 OID 16470)
-- Dependencies: 214
-- Data for Name: data_provider; Type: TABLE DATA; Schema: repromon; Owner: postgres
--

COPY repromon.data_provider (id, provider) FROM stdin;
1	ReproIn
2	ReproStim
3	ReproEvents
4	PACS
5	Noisseur
6	DICOM/QA
7	MRI
\.


--
-- TOC entry 3689 (class 0 OID 16473)
-- Dependencies: 215
-- Data for Name: device; Type: TABLE DATA; Schema: repromon; Owner: postgres
--

COPY repromon.device (id, kind, description) FROM stdin;
1	MRI	DBIC 3T Siemens Prisma MRI
\.


--
-- TOC entry 3690 (class 0 OID 16476)
-- Dependencies: 216
-- Data for Name: message_category; Type: TABLE DATA; Schema: repromon; Owner: postgres
--

COPY repromon.message_category (id, category) FROM stdin;
1	Feedback
\.


--
-- TOC entry 3691 (class 0 OID 16479)
-- Dependencies: 217
-- Data for Name: message_level; Type: TABLE DATA; Schema: repromon; Owner: postgres
--

COPY repromon.message_level (id, level) FROM stdin;
1	INFO
2	WARNING
3	ERROR
\.


--
-- TOC entry 3695 (class 0 OID 16536)
-- Dependencies: 221
-- Data for Name: message_log; Type: TABLE DATA; Schema: repromon; Owner: postgres
--

COPY repromon.message_log (id, level_id, category_id, device_id, provider_id, study_id, study_name, is_visible, visible_updated_on, visible_updated_by, description, payload, event_on, registered_on, recorded_on, recorded_by) FROM stdin;
1	1	1	1	2	\N	\N	Y	\N	\N	stimuli display dis-connected	\N	2023-06-07 10:49:31	2023-06-07 10:50:01	2023-06-07 10:50:31	reprostim
2	1	1	1	2	\N	\N	Y	\N	\N	stimuli display connected(1024x768, …)\n	\N	2023-06-07 10:50:22	2023-06-07 10:51:02	2023-06-07 10:51:22	reprostim
3	3	1	1	5	1	Halchenko/Horea/1020_animal_mri	Y	\N	\N	subject “John” is not conformant, must match [0-9]{6} regular expression. [link to screen with highlight]\n	\N	2023-06-07 10:51:44	2023-06-07 10:52:04	2023-06-07 10:52:44	noisseur
4	1	1	1	5	1	Halchenko/Horea/1020_animal_mri	Y	\N	\N	proceeded with compliant data on study Halchenko/Horea/1020_animal_mri	\N	2023-06-07 10:54:17	2023-06-07 10:55:07	2023-06-07 10:55:17	noisseur
5	1	1	1	3	\N	\N	Y	\N	\N	MRI trigger event received	\N	2023-06-07 10:55:45	2023-06-07 10:56:05	2023-06-07 10:56:45	reproevt
6	3	1	1	6	\N	\N	Y	\N	\N	MRI data lacks rear head coils data [link to PACS recording to review]	\N	2023-06-07 10:58:01	2023-06-07 10:59:00	2023-06-07 10:59:01	dicomqa
7	1	1	1	3	\N	\N	Y	\N	\N	MRI trigger event received	null	2023-09-05 23:32:10.244539	2023-09-05 23:34:52.263282	2023-09-05 23:34:52.26329	poweruser
\.


--
-- TOC entry 3692 (class 0 OID 16487)
-- Dependencies: 218
-- Data for Name: role; Type: TABLE DATA; Schema: repromon; Owner: postgres
--

COPY repromon.role (id, rolename, description) FROM stdin;
1	admin	Administrator
2	data_collector	Data Collector
3	mri_operator	MRI Operator
4	participant	Participant
5	sys_data_entry	System Data Entry
6	tester	Automatic System Tester
\.


--
-- TOC entry 3697 (class 0 OID 16551)
-- Dependencies: 223
-- Data for Name: sec_user_device; Type: TABLE DATA; Schema: repromon; Owner: postgres
--

COPY repromon.sec_user_device (id, user_id, device_id) FROM stdin;
1	1	1
2	2	1
3	3	1
4	4	1
5	5	1
6	6	1
\.


--
-- TOC entry 3699 (class 0 OID 16560)
-- Dependencies: 225
-- Data for Name: sec_user_role; Type: TABLE DATA; Schema: repromon; Owner: postgres
--

COPY repromon.sec_user_role (id, user_id, role_id) FROM stdin;
1	4	1
2	1	2
3	2	3
4	3	4
5	5	4
6	5	2
7	5	3
8	6	5
9	1	1
10	5	5
\.


--
-- TOC entry 3701 (class 0 OID 16569)
-- Dependencies: 227
-- Data for Name: study_data; Type: TABLE DATA; Schema: repromon; Owner: postgres
--

COPY repromon.study_data (id, name, device_id, status_id, start_ts, end_ts, info) FROM stdin;
1	Halchenko/Horea/1020_animal_mri	1	101	2023-06-07 10:41:25	\N	{\n\t"data_collector": ["user1", "poweruser"],\n\t"mri_operator": ["user2"],\n\t"participant": ["user3"]\n}
\.


--
-- TOC entry 3693 (class 0 OID 16511)
-- Dependencies: 219
-- Data for Name: study_status; Type: TABLE DATA; Schema: repromon; Owner: postgres
--

COPY repromon.study_status (id, status) FROM stdin;
100	New
101	Collecting MRI Data
190	Completed
191	Failed
200	Entering Participant Data
300	Designing Sequences
\.


--
-- TOC entry 3703 (class 0 OID 16578)
-- Dependencies: 229
-- Data for Name: user; Type: TABLE DATA; Schema: repromon; Owner: postgres
--

COPY repromon."user" (id, username, is_active, is_system, first_name, last_name, email, phone, description, password, password_changed_on, last_login) FROM stdin;
1	user1	Y	N	John	Smith	user1@repromon.com	321	\N	$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq	\N	\N
2	user2	Y	N	Dave	Cooper	user2@repromon.com	231	\N	$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq	\N	\N
3	user3	Y	N	Lucy	Nelson	user3@repromon.com	111	\N	$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq	\N	\N
4	admin	Y	N	Admin	Admin	admin@repromon.com	\N	Administrator	$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq	\N	\N
5	poweruser	Y	N	Power	User	poweruser@repromon.com	\N	Power user	$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq	\N	\N
6	noisseur	Y	Y	noisseur	noisseur		\N	System con/noisseur user	$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq	\N	\N
7	reprostim	Y	Y	reprostim	reprostim	\N	\N	ReproStim Screen Capture\n	$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq	\N	\N
8	reproevt	Y	Y	reproevt	reproevt	\N	\N	ReproEvents Capture\n	$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq	\N	\N
9	dicomqa	Y	Y	dicomqa	dicomqa	\N	\N	DICOMS/QA	$2b$12$ShaYDykDo9yJe0sLxBCMqe0f4OhUXD9iZf4FYFhQIwNTt9/WNBkfq	\N	\N
\.


--
-- TOC entry 3715 (class 0 OID 0)
-- Dependencies: 220
-- Name: message_log_id_seq; Type: SEQUENCE SET; Schema: repromon; Owner: postgres
--

SELECT pg_catalog.setval('repromon.message_log_id_seq', 7, true);


--
-- TOC entry 3716 (class 0 OID 0)
-- Dependencies: 222
-- Name: sec_user_device_id_seq; Type: SEQUENCE SET; Schema: repromon; Owner: postgres
--

SELECT pg_catalog.setval('repromon.sec_user_device_id_seq', 6, true);


--
-- TOC entry 3717 (class 0 OID 0)
-- Dependencies: 224
-- Name: sec_user_role_id_seq; Type: SEQUENCE SET; Schema: repromon; Owner: postgres
--

SELECT pg_catalog.setval('repromon.sec_user_role_id_seq', 10, true);


--
-- TOC entry 3718 (class 0 OID 0)
-- Dependencies: 226
-- Name: study_data_id_seq; Type: SEQUENCE SET; Schema: repromon; Owner: postgres
--

SELECT pg_catalog.setval('repromon.study_data_id_seq', 1, false);


--
-- TOC entry 3719 (class 0 OID 0)
-- Dependencies: 228
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: repromon; Owner: postgres
--

SELECT pg_catalog.setval('repromon.user_id_seq', 9, true);


--
-- TOC entry 3492 (class 2606 OID 16526)
-- Name: data_provider data_provider_pkey; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.data_provider
    ADD CONSTRAINT data_provider_pkey PRIMARY KEY (id);


--
-- TOC entry 3495 (class 2606 OID 16528)
-- Name: device device_pkey; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.device
    ADD CONSTRAINT device_pkey PRIMARY KEY (id);


--
-- TOC entry 3497 (class 2606 OID 16530)
-- Name: message_category message_category_pkey; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.message_category
    ADD CONSTRAINT message_category_pkey PRIMARY KEY (id);


--
-- TOC entry 3499 (class 2606 OID 16532)
-- Name: message_level message_level_pkey; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.message_level
    ADD CONSTRAINT message_level_pkey PRIMARY KEY (id);


--
-- TOC entry 3516 (class 2606 OID 16544)
-- Name: message_log message_log_pkey; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.message_log
    ADD CONSTRAINT message_log_pkey PRIMARY KEY (id);


--
-- TOC entry 3502 (class 2606 OID 16547)
-- Name: role role_pkey; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);


--
-- TOC entry 3520 (class 2606 OID 16556)
-- Name: sec_user_device sec_user_device_pkey; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.sec_user_device
    ADD CONSTRAINT sec_user_device_pkey PRIMARY KEY (id);


--
-- TOC entry 3522 (class 2606 OID 16558)
-- Name: sec_user_device sec_user_device_unique_constraint; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.sec_user_device
    ADD CONSTRAINT sec_user_device_unique_constraint UNIQUE (user_id, device_id);


--
-- TOC entry 3526 (class 2606 OID 16565)
-- Name: sec_user_role sec_user_role_pkey; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.sec_user_role
    ADD CONSTRAINT sec_user_role_pkey PRIMARY KEY (id);


--
-- TOC entry 3528 (class 2606 OID 16567)
-- Name: sec_user_role sec_user_role_unique_constraint; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.sec_user_role
    ADD CONSTRAINT sec_user_role_unique_constraint UNIQUE (user_id, role_id);


--
-- TOC entry 3533 (class 2606 OID 16576)
-- Name: study_data study_data_pkey; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.study_data
    ADD CONSTRAINT study_data_pkey PRIMARY KEY (id);


--
-- TOC entry 3505 (class 2606 OID 16549)
-- Name: study_status study_status_pkey; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.study_status
    ADD CONSTRAINT study_status_pkey PRIMARY KEY (id);


--
-- TOC entry 3507 (class 2606 OID 16610)
-- Name: study_status unique_study_status_status; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon.study_status
    ADD CONSTRAINT unique_study_status_status UNIQUE (status);


--
-- TOC entry 3541 (class 2606 OID 16589)
-- Name: user user_email_unique_constraint; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon."user"
    ADD CONSTRAINT user_email_unique_constraint UNIQUE (email);


--
-- TOC entry 3543 (class 2606 OID 16585)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 3545 (class 2606 OID 16587)
-- Name: user user_username_unique_constraint; Type: CONSTRAINT; Schema: repromon; Owner: postgres
--

ALTER TABLE ONLY repromon."user"
    ADD CONSTRAINT user_username_unique_constraint UNIQUE (username);


--
-- TOC entry 3493 (class 1259 OID 16592)
-- Name: idx_data_provider_provider; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_data_provider_provider ON repromon.data_provider USING btree (provider);


--
-- TOC entry 3508 (class 1259 OID 16593)
-- Name: idx_message_log_category_id; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_message_log_category_id ON repromon.message_log USING btree (category_id);


--
-- TOC entry 3509 (class 1259 OID 16599)
-- Name: idx_message_log_device_id; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_message_log_device_id ON repromon.message_log USING btree (device_id);


--
-- TOC entry 3510 (class 1259 OID 16595)
-- Name: idx_message_log_event_on; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_message_log_event_on ON repromon.message_log USING btree (event_on);


--
-- TOC entry 3511 (class 1259 OID 16594)
-- Name: idx_message_log_is_visible; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_message_log_is_visible ON repromon.message_log USING btree (is_visible);


--
-- TOC entry 3512 (class 1259 OID 16598)
-- Name: idx_message_log_provider_id; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_message_log_provider_id ON repromon.message_log USING btree (provider_id);


--
-- TOC entry 3513 (class 1259 OID 16596)
-- Name: idx_message_log_study_id; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_message_log_study_id ON repromon.message_log USING btree (study_id);


--
-- TOC entry 3514 (class 1259 OID 16597)
-- Name: idx_message_log_study_name; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_message_log_study_name ON repromon.message_log USING btree (study_name);


--
-- TOC entry 3500 (class 1259 OID 16600)
-- Name: idx_role_rolename; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_role_rolename ON repromon.role USING btree (rolename);


--
-- TOC entry 3517 (class 1259 OID 16602)
-- Name: idx_sec_user_device_device_id; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_sec_user_device_device_id ON repromon.sec_user_device USING btree (device_id);


--
-- TOC entry 3518 (class 1259 OID 16601)
-- Name: idx_sec_user_device_user_id; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_sec_user_device_user_id ON repromon.sec_user_device USING btree (user_id);


--
-- TOC entry 3523 (class 1259 OID 16604)
-- Name: idx_sec_user_role_role_id; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_sec_user_role_role_id ON repromon.sec_user_role USING btree (role_id);


--
-- TOC entry 3524 (class 1259 OID 16603)
-- Name: idx_sec_user_role_user_id; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_sec_user_role_user_id ON repromon.sec_user_role USING btree (user_id);


--
-- TOC entry 3529 (class 1259 OID 16606)
-- Name: idx_study_data_device_id; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_study_data_device_id ON repromon.study_data USING btree (device_id);


--
-- TOC entry 3530 (class 1259 OID 16605)
-- Name: idx_study_data_name; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_study_data_name ON repromon.study_data USING btree (name);


--
-- TOC entry 3531 (class 1259 OID 16607)
-- Name: idx_study_data_status_id; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_study_data_status_id ON repromon.study_data USING btree (status_id);


--
-- TOC entry 3503 (class 1259 OID 16608)
-- Name: idx_study_status_status; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_study_status_status ON repromon.study_status USING btree (status);


--
-- TOC entry 3534 (class 1259 OID 16616)
-- Name: idx_user_email; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_user_email ON repromon."user" USING btree (email);


--
-- TOC entry 3535 (class 1259 OID 16614)
-- Name: idx_user_first_name; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_user_first_name ON repromon."user" USING btree (first_name);


--
-- TOC entry 3536 (class 1259 OID 16612)
-- Name: idx_user_is_active; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_user_is_active ON repromon."user" USING btree (is_active);


--
-- TOC entry 3537 (class 1259 OID 16613)
-- Name: idx_user_is_system; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_user_is_system ON repromon."user" USING btree (is_system);


--
-- TOC entry 3538 (class 1259 OID 16615)
-- Name: idx_user_last_name; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_user_last_name ON repromon."user" USING btree (last_name);


--
-- TOC entry 3539 (class 1259 OID 16611)
-- Name: idx_user_username; Type: INDEX; Schema: repromon; Owner: postgres
--

CREATE INDEX idx_user_username ON repromon."user" USING btree (username);


-- Completed on 2023-09-07 10:31:03 EEST

--
-- PostgreSQL database dump complete
--
