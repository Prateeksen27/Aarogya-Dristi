CREATE TABLE patient (
    email text PRIMARY key not null,
    password text,
    name text,
    age text,
    gender text
);
create table doctor(
    email text PRIMARY key not null,
    name text,
    specialization text,
    qualification text,
    exp text,
    workingat text,
    consultationhours text,
    password text
);

CREATE TABLE appointment (
    appointment_id SERIAL PRIMARY KEY, 
    patient_email TEXT ,  -- Adds foreign key constraint
    doctor_email TEXT ,  -- Adds foreign key constraint
    appointment_date DATE,
    status TEXT DEFAULT 'Pending',  -- Use single quotes for default values
    reason TEXT,
    patient_name TEXT,
    doctor_feedback TEXT
);