ALTER TABLE company_jobs
    ADD COLUMN karma_reward INTEGER DEFAULT NULL;

CREATE TABLE company_job_application_form
(
    id          VARCHAR(36) PRIMARY KEY                     NOT NULL DEFAULT gen_random_uuid()::text,
    job_id      VARCHAR(36)                                 NOT NULL,
    title       VARCHAR(300)                                NOT NULL,
    fields      JSONB                   DEFAULT '[]'::jsonb NOT NULL,
    form_order  INTEGER                 DEFAULT 1           NOT NULL,
    is_active   BOOLEAN                 DEFAULT TRUE        NOT NULL,
    created_at  TIMESTAMP WITH TIME ZONE                    NOT NULL DEFAULT now(),
    updated_at  TIMESTAMP WITH TIME ZONE                    NOT NULL DEFAULT now(),
    created_by  VARCHAR(36)                                 NOT NULL,
    updated_by  VARCHAR(36)                                 NOT NULL,

    CONSTRAINT fk_cjaf_job_id FOREIGN KEY (job_id) REFERENCES company_jobs (id) ON DELETE CASCADE,
    CONSTRAINT fk_cjaf_created_by FOREIGN KEY (created_by) REFERENCES "user" (id) ON DELETE CASCADE,
    CONSTRAINT fk_cjaf_updated_by FOREIGN KEY (updated_by) REFERENCES "user" (id) ON DELETE CASCADE,
    CONSTRAINT uq_cjaf_job_form_order UNIQUE (job_id, form_order)
);

CREATE TYPE company_job_application_status AS ENUM (
    'Applied',
    'Shortlisted',
    'Interview',
    'Rejected',
    'Offered',
    'Hired',
    'Withdrawn'
);

CREATE TABLE company_job_application
(
    id                  VARCHAR(36) PRIMARY KEY                     NOT NULL DEFAULT gen_random_uuid()::text,
    job_id              VARCHAR(36)                                 NOT NULL,
    user_id             VARCHAR(36)                                 NOT NULL,
    form_id             VARCHAR(36)                                 NOT NULL,
    form_data           JSONB                   DEFAULT '{}'::jsonb NOT NULL,
    resume_url          TEXT,
    status              company_job_application_status              NOT NULL DEFAULT 'Applied',
    rejection_reason    TEXT,
    shortlisted_at      TIMESTAMP WITH TIME ZONE,
    interviewed_at      TIMESTAMP WITH TIME ZONE,
    offered_at          TIMESTAMP WITH TIME ZONE,
    hired_at            TIMESTAMP WITH TIME ZONE,
    applied_at          TIMESTAMP WITH TIME ZONE                    NOT NULL DEFAULT now(),
    updated_at          TIMESTAMP WITH TIME ZONE                    NOT NULL DEFAULT now(),
    updated_by          VARCHAR(36),

    CONSTRAINT fk_cja_job_id FOREIGN KEY (job_id) REFERENCES company_jobs (id) ON DELETE CASCADE,
    CONSTRAINT fk_cja_user_id FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE,
    CONSTRAINT fk_cja_form_id FOREIGN KEY (form_id) REFERENCES company_job_application_form (id) ON DELETE RESTRICT,
    CONSTRAINT fk_cja_updated_by FOREIGN KEY (updated_by) REFERENCES "user" (id) ON DELETE SET NULL,
    CONSTRAINT uq_cja_user_job UNIQUE (user_id, job_id)
);