## 1. Learner Discovery API — Filter & View Learners

### GET company/learners/
### Description
Return paginated and sorting individual learner profile view for companies, company can filter learners details by filtering via karma_min, karma_max, skill_ids, ig_ids, level, location

#### Method: GET
Query params:
| parameter | type | description |
| :--- | :--- | :--- |
| pageIndex | number | Page number (default: 1) |
| perPage | number | Items per page (default: 25) |
| karma_min | number | Minimum karma filter |
| karma_max | number | Maximum karma filter |
| skill_ids | string | Comma-separated Skill IDs to filter by |
| ig_ids | string | Comma-separated Interest Group IDs to filter by |
| level | number | Learner level to filter by |
| location | string | Geographic filter (District ID) |
| sortBy | string | Sorting fields: `karma`, `level`, `activity` (prefix with `-` for descending) |

Response
```json
{
  "data": [
    {
      "user_id": "uuid",
      "muid": "john-doe@mulearn",
      "discord_id": "1234567890",
      "full_name": "John Doe",
      "email": "user@gmail.com",
      "mobile": "9876543210",
      "gender": "Male",
      "dob": "2000-01-01",
      "district": "District Name",
      "karma": 5000,
      "level": "Level 4",
      "interest_groups": [
        {
          "id": "uuid",
          "name": "Python"
        }
      ],
      "skills": [
        {
          "id": "uuid",
          "name": "Django"
        }
      ]
    }
  ],
  "pagination": {
    "pageIndex": 1,
    "perPage": 25,
    "totalCount": 120
  }
}
```

### Privacy & Access Control
* **Public Visibility**: Only learners who have enabled `is_public` in their settings should be discoverable by companies.
* **Sensitive Data**: Fields like `email` and `mobile` should be handled according to the platform's privacy policy (e.g., only show if the learner has explicitly consented to share with companies).

### Implementation Details
* **Sorting Logic**:
    * `karma`: Sort by `wallet_user__karma`
    * `level`: Sort by `user_lvl_link_user__level__level_order`
    * `activity`: Sort by `wallet_user__karma_last_updated_at`
* **Filtering Logic**:
    * `karma_min`/`karma_max`: Filter on `wallet_user__karma` range.
    * `skill_ids`: Filter `User` who have a `KarmaActivityLog` linked to `TaskList` which are linked to these `Skill` IDs via `TaskSkillLink`.
    * `ig_ids`: Filter via `UserIgLink` with provided IDs.
    * `level`: Filter via `UserLvlLink` for specific learner level ID/order.
    * `location`: Filter on `User.district_id`.
* **Pagination**: custom `pageIndex` and `perPage` handling.

---

# Job API Implementation Plan

## 2. Job Enhancements — Karma Rewards & Gig Support
### Description
Enable companies to incentivize applications by adding karma rewards for successful placements and specifically tagging roles as Gigs or Internships for targeted talent discovery.

### Requirements:
- **Model Updates**: Add `karma_reward` (Integer) to `CompanyJob` to allow companies to offer karma upon successful hiring/milestones.
```sql
ALTER TABLE company_jobs
    ADD COLUMN karma_reward INTEGER DEFAULT NULL;

COMMENT ON COLUMN company_jobs.karma_reward IS 'Optional karma points awarded to the learner upon successful hiring or milestone completion. NULL means no karma reward for this job.';
```
```py
karma_reward = models.IntegerField(blank=True, null=True)
```
- **Job Types**: Support diverse employment models including `Gig`, `Internship`, `Full-Time`, `Part-Time`, `Remote`, and `Hybrid`.
- **API: Job Creation/Update**: Update job posting APIs to accept these new fields, ensuring they are reflected in the Discovery API.

## 3. Job Application Tracking — Lifecycle Management
### Description
Track the end-to-end recruitment lifecycle within the platform, from the initial learner application to final status updates (Shortlisting, Interviewing, and Accept/Reject).

### Context & Implementation Strategy
The initial investigation revealed that tracking job applications required a more robust mechanism than simple flags on existing models. To support production-grade requirements, we are introducing a **Dynamic Form-Based Application System** that enables companies to define custom application requirements and track candidates through multiple hiring stages.

### API Architecture & Details

#### 1. Learner Job Application
- **Path**: `POST /api/v1/company/job/apply/`
- **Description**: Allows a learner to submit their application for a specific job by answering company-defined dynamic questions.
- **Payload**:
  ```json
  {
    "job_id": "uuid",
    "form_id": "uuid",
    "form_data": {
      "full_name": "Adarsh S",
      "graduation_year": "3",
      "github_portfolio": "https://github.com/adarsh-s"
    },
    "resume_url": "https://s3.link/resume.pdf"
  }
  ```
- **Status Codes**: `201 Created`, `400 Bad Request` (Validation errors).
- **Implementation Logic**:
    - **Validation**: Ensures the `form_id` belongs to the `job_id` and is marked `is_active`.
    - **Prerequisites**: Checks if the learner meets the `min_karma`, `min_level`, and any specific `CompanyJobRule` requirements.
    - **Constraint**: Enforces the `uq_cja_user_job` unique constraint (one application per user-job).
    - **Persistence**: Maps the learner responses into the `form_data` JSONB column.

#### 2. Company Applicant Pool View
- **Path**: `GET /api/v1/company/job/applications/{job_id}/`
- **Description**: Enables companies to view and filter candidates who have applied for their job postings.
- **Path Parameters**: `job_id` (String: UUID).
- **Query Parameters**:
    - `status`: Filter by application stage (`Applied`, `Shortlisted`, `Interview`, `Rejected`, etc.).
    - `pageIndex`: Pagination support (default: 1).
    - `perPage`: Items per page (default: 25).
- **Result**: A paginated list of `CompanyJobApplication` records, including nested learner profile details (muid, name, karma).
- **Implementation Logic**:
    - **Access Control**: Validates that the requester belongs to the company owning the `job_id`.
    - **Data Joining**: Efficiently fetches application data and user metadata in a single response for company dashboards.

#### 3. Shortlisting & Stage Progression
- **Path**: `PATCH /api/v1/company/job/applications/{application_id}/status/`
- **Description**: Allows recruiters to move candidates through the hiring pipeline (e.g., Shortlisting, Interviewing, and final Hired/Rejected status).
- **Path Parameters**: `application_id` (String: UUID).
- **Payload**:
  ```json
  {
    "status": "Shortlisted",
    "rejection_reason": "Optional feedback"
  }
  ```
- **Status Codes**: `200 OK`, `403 Forbidden` (Unauthorized recruiter).
- **Implementation Logic**:
    - **Lifecycle Update**: Updates the `status` Enum and the `updated_by` field.
    - **Audit Log**: Automatically populates the relevant timestamp (e.g., `shortlisted_at`, `interviewed_at`, `hired_at`) based on the new status.
    - **Feedback**: Records `rejection_reason` if the status is transitioned to `Rejected`.

---


## Technical Infrastructure & Specifications

### Database Schema (SQL)

```sql
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
```

### Example Data Storage

#### 1. `company_job_application_form` (Form Definition)
This example shows how a company-defined form with dynamic fields is stored in the `fields` (JSONB) column.
```json
{
  "id": "7b80cdbf-021a-4183-a978-1ab35700b4bc",
  "job_id": "job-uuid-12345",
  "title": "Summer Internship 2026",
  "fields": [
    {
      "field_key": "full_name",
      "type": "text",
      "title": "Full Name",
      "required": true
    },
    {
      "field_key": "graduation_year",
      "type": "singleselect",
      "title": "Year of Study",
      "options": [{"values": ["1", "2", "3", "4"]}],
      "required": true
    },
    {
      "field_key": "github_portfolio",
      "type": "url",
      "title": "Github Profile Link",
      "required": false
    }
  ],
  "form_order": 1
}
```

#### 2. `company_job_application` (User Submission)
This shows how a learner's response is captured in the `form_data` (JSONB) column, mapped to the keys defined in the form.
```json
{
  "id": "app-uuid-67890",
  "job_id": "job-uuid-12345",
  "user_id": "learner-uuid-abcde",
  "form_id": "7b80cdbf-021a-4183-a978-1ab35700b4bc",
  "form_data": {
    "full_name": "Adarsh S",
    "graduation_year": "3",
    "github_portfolio": "https://github.com/adarsh-s"
  },
  "status": "Shortlisted",
  "applied_at": "2026-04-03T10:00:00Z",
  "shortlisted_at": "2026-04-03T15:00:00Z"
}
```

### Why This is Scalable & Production Ready
- **Flexibility**: Companies can handle multiple job openings, each with completely different form requirements, without any database schema changes.
- **Efficiency**: Responses are stored in a single JSONB block per user-job-form, making reads fast and reducing table joins.
- **Data Integrity**: Unique constraints (`uq_cja_user_job`) ensure learners don't duplicate applications, while foreign keys maintain sync between jobs and applicants.
- **Stage Tracking**: Automatic timestamping for each state transition allows for advanced recruitment analytics (e.g., average time to hire).

---

<!-- ### Google Docs: API Requirements Summary (Submission Ready) -->

<!-- **Feature Set: Advanced Recruitment Tracking & Lifecycle Management** -->

<!-- **1. Job Enhancements**: -->
<!-- - **Karma Rewards**: Option to attach `karma_reward` points to job postings. -->
<!-- - **Engagement Types**: Native support for `Gig` and `Internship` roles to improve discovery accuracy. -->

<!-- **2. Dynamic Form Engine**: -->
<!-- - **Schema**: Uses `JSONB` for flexible form fields definition. -->
<!-- - **Validation**: Supports diverse input types (`phone`, `email`, `file`) as defined in `utils/form_util.py`. -->
<!-- - **Pipeline**: Supports sequential form stages via `form_order`. -->

<!-- **3. Candidate Lifecycle Management**: -->
<!-- - **Lifecycle tracking**: Atomic status updates using the `company_job_application_status` Enum (Apply → Shortlist → Accept/Reject). -->
<!-- - **Auditability**: Automated historical timestamping for stage-gate analysis. -->

<!-- **4. API Endpoints**: -->
<!-- - **Application Submission**: Validated POST for learner applications. -->
<!-- - **Pool Management**: GET for companies with filtering and pagination. -->
<!-- - **Flow Control**: PATCH for managing candidate progression with real-time stage tracking. -->
