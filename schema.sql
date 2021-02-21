DROP TABLE IF EXISTS JOBS;
CREATE TABLE JOBS (
    job_id varchar(1000) DEFAULT 'N/A',
    job_topic varchar(1000) DEFAULT 'N/A',
    job_link varchar(1000) DEFAULT 'N/A',
    job_title varchar(1000) DEFAULT 'N/A',
    job_description varchar(1000) DEFAULT 'N/A',
    job_requirements varchar(1000) DEFAULT 'N/A',
    job_location varchar(1000) DEFAULT 'N/A',
    job_salary varchar(1000) DEFAULT 'N/A',
    job_qualification varchar(1000) DEFAULT 'N/A',
    job_type varchar(1000) DEFAULT 'N/A',
    job_experience varchar(1000) DEFAULT 'N/A'
);
