--
-- PostgreSQL database dump
--

\restrict PWP8t0jJkw6YBsgxelj23sur1BjiqogmireyvJ6wagb4srZObqlvMjKCr4KqjUr

-- Dumped from database version 15.17 (Debian 15.17-1.pgdg13+1)
-- Dumped by pg_dump version 15.17 (Debian 15.17-1.pgdg13+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: roles; Type: TABLE; Schema: public; Owner: pollux_user
--

CREATE TABLE public.roles (
    role_id uuid NOT NULL,
    role_name character varying(50) NOT NULL,
    description text,
    is_active boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT now(),
    modified_at timestamp with time zone DEFAULT now(),
    created_by uuid,
    modified_by uuid
);


ALTER TABLE public.roles OWNER TO pollux_user;

--
-- Name: users; Type: TABLE; Schema: public; Owner: pollux_user
--

CREATE TABLE public.users (
    user_id uuid NOT NULL,
    email character varying(255) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150),
    mobile character varying(50) NOT NULL,
    role_id uuid NOT NULL,
    is_active boolean DEFAULT true,
    created_at timestamp with time zone DEFAULT now(),
    modified_at timestamp with time zone DEFAULT now(),
    created_by uuid,
    modified_by uuid,
    title character varying(20),
    gender character varying(10),
    birthdate date,
    preferences jsonb
);


ALTER TABLE public.users OWNER TO pollux_user;

--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: pollux_user
--

INSERT INTO public.roles (role_id, role_name, description, is_active, created_at, modified_at, created_by, modified_by) VALUES ('11111111-1111-1111-1111-111111111111', 'Admin', 'Full access', true, '2026-04-22 21:41:20.487307+00', '2026-04-22 21:41:20.487307+00', NULL, NULL);
INSERT INTO public.roles (role_id, role_name, description, is_active, created_at, modified_at, created_by, modified_by) VALUES ('22222222-2222-2222-2222-222222222222', 'User', 'Limited access', true, '2026-04-22 21:41:20.487307+00', '2026-04-22 21:41:20.487307+00', NULL, NULL);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: pollux_user
--

INSERT INTO public.users (user_id, email, first_name, last_name, mobile, role_id, is_active, created_at, modified_at, created_by, modified_by, title, gender, birthdate, preferences) VALUES ('72e92d55-4c84-4676-90c1-8b1b9e395991', 'john.doe@example.com', 'John', 'Doe', '9876543210', '11111111-1111-1111-1111-111111111111', true, '2026-05-03 20:29:20.375946+00', '2026-05-03 20:29:20.375946+00', NULL, NULL, 'Mr', 'male', '1995-05-10', '{"language": "en", "themeMode": "light", "themeColor": "blue_theme"}');
INSERT INTO public.users (user_id, email, first_name, last_name, mobile, role_id, is_active, created_at, modified_at, created_by, modified_by, title, gender, birthdate, preferences) VALUES ('98c0c858-65c7-445d-a739-fdcc1ea37652', 'john.doe@example.com', 'John', 'Doe', '9876543210', '11111111-1111-1111-1111-111111111111', true, '2026-05-03 20:32:08.853178+00', '2026-05-03 20:32:08.853178+00', NULL, NULL, 'Mr', 'male', '1995-05-10', '{"language": "en", "themeMode": "light", "themeColor": "blue_theme"}');


--
-- PostgreSQL database dump complete
--

\unrestrict PWP8t0jJkw6YBsgxelj23sur1BjiqogmireyvJ6wagb4srZObqlvMjKCr4KqjUr

