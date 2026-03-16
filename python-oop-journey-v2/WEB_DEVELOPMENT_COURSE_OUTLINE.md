# Python Web Development Course Outline

A comprehensive 8-week course following the Python OOP Journey, taking learners from HTTP fundamentals to production-ready web applications.

---

## Course Overview

| Attribute | Details |
|-----------|---------|
| **Duration** | 8 weeks |
| **Days per Week** | 6 days |
| **Daily Commitment** | 2-4 hours |
| **Prerequisites** | Python OOP Journey (Weeks 1-4) or equivalent |
| **Total Exercises** | ~350 problems |
| **Total Tests** | ~4,500 tests |
| **Capstone** | Production-ready SaaS application |

---

## Prerequisites

### Required Knowledge
- Python fundamentals (variables, functions, collections)
- Object-oriented programming (classes, inheritance, polymorphism)
- Error handling and exceptions
- Testing with pytest
- Git basics

### Required Tools
- Python 3.10+
- VS Code or PyCharm
- Git
- Docker (Week 7+)

---

## Tooling Stack

### Core Stack
| Category | Technology | Purpose |
|----------|------------|---------|
| Web Framework (Intro) | Flask | Learning HTTP, routing, templates |
| Web Framework (Advanced) | FastAPI | Modern API development |
| Database | PostgreSQL | Production database |
| ORM | SQLAlchemy 2.0 | Database abstraction |
| Migrations | Alembic | Schema versioning |
| Testing | pytest, pytest-asyncio, httpx | Test suite |
| Frontend (Minimal) | HTMX / Vanilla JS | Interactivity without frameworks |
| Containerization | Docker & Docker Compose | Deployment |
| CI/CD | GitHub Actions | Automation |

### Development Tools
| Tool | Purpose |
|------|---------|
| `curl` / HTTPie | API testing |
| `pytest-flask` | Flask testing utilities |
| `pytest-asyncio` | Async test support |
| `factory-boy` | Test data generation |
| `black`, `ruff`, `mypy` | Code quality |
| `pre-commit` | Git hooks |

---

## Weekly Breakdown

---

## Week 1: Web Fundamentals & HTTP

**Week Objective:** Understand how the web works at the protocol level and build your first Flask application.

### Week 1 Overview
| Day | Topic | Problems | Difficulty |
|-----|-------|----------|------------|
| Day 1 | HTTP Protocol Deep Dive | 10 | Easy-Medium |
| Day 2 | REST API Principles | 10 | Medium |
| Day 3 | Flask Introduction | 10 | Easy-Medium |
| Day 4 | Request/Response Cycle | 10 | Medium |
| Day 5 | URL Routing & Views | 10 | Medium |
| Day 6 | Static Files & Configuration | 10 | Medium |

### Day 1: HTTP Protocol Deep Dive

**Learning Objectives:**
- Understand HTTP as a stateless request-response protocol
- Learn HTTP methods (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
- Master HTTP status codes (1xx, 2xx, 3xx, 4xx, 5xx)
- Understand headers and their purposes
- Learn about cookies and sessions

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `identify_http_method.py` | Match methods to use cases |
| 02 | `http_status_categories.py` | Categorize status codes |
| 03 | `parse_http_request.py` | Parse raw HTTP request strings |
| 04 | `build_http_response.py` | Construct HTTP responses |
| 05 | `extract_headers.py` | Parse header key-value pairs |
| 06 | `content_negotiation.py` | Accept header parsing |
| 07 | `cache_control_parser.py` | Parse Cache-Control headers |
| 08 | `url_encoding.py` | Percent-encoding/decoding |
| 09 | `http_redirect_chain.py` | Follow redirect sequences |
| 10 | `conditional_requests.py` | ETag and If-None-Match logic |

**Theory Coverage:**
- HTTP/1.1 vs HTTP/2 vs HTTP/3
- Request line, headers, body structure
- Response line, headers, body structure
- Common headers: Content-Type, Accept, Authorization, User-Agent
- Stateless nature and connection management

### Day 2: REST API Principles

**Learning Objectives:**
- Understand REST architectural constraints
- Design resource-oriented URLs
- Apply proper HTTP methods for CRUD operations
- Implement proper status code usage
- Understand idempotency and safety

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `identify_rest_violations.py` | Spot non-RESTful patterns |
| 02 | `design_resource_urls.py` | URL path design |
| 03 | `crud_to_http_methods.py` | Map operations to methods |
| 04 | `api_versioning_strategy.py` | Version URL designs |
| 05 | `pagination_design.py` | Offset vs cursor pagination |
| 06 | `filter_sort_parameters.py` | Query parameter design |
| 07 | `hateoas_links.py` | Generate navigation links |
| 08 | `idempotency_keys.py` | Idempotency implementation |
| 09 | `rate_limit_headers.py` | Rate limiting response headers |
| 10 | `api_error_format.py` | RFC 7807 Problem Details |

**Theory Coverage:**
- REST constraints: Client-Server, Stateless, Cacheable, Uniform Interface
- Resource naming conventions
- Richardson Maturity Model
- API versioning strategies
- Hypermedia (HATEOAS)

### Day 3: Flask Introduction

**Learning Objectives:**
- Set up a Flask development environment
- Create a basic Flask application
- Understand the application context
- Use the Flask development server
- Structure a Flask project

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `create_flask_app.py` | App factory pattern |
| 02 | `hello_world_route.py` | Basic route definition |
| 03 | `dynamic_routes.py` | URL variable rules |
| 04 | `route_decorators.py` | Multiple routes, methods |
| 05 | `url_building.py` | `url_for()` usage |
| 06 | `request_object.py` | Access request data |
| 07 | `json_responses.py` | Return JSON responses |
| 08 | `error_handlers.py` | Custom error pages |
| 09 | `application_context.py` | `app_context()`, `g` object |
| 10 | `before_after_request.py` | Request hooks |

**Theory Coverage:**
- WSGI and Flask's role
- Application vs Request context
- Flask application factory pattern
- Configuration management
- Debug mode and auto-reloading

### Day 4: Request/Response Cycle

**Learning Objectives:**
- Trace the complete request-response lifecycle
- Access request data (form, JSON, query params, headers)
- Build proper responses (JSON, HTML, redirects)
- Handle file uploads
- Work with cookies

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `parse_query_params.py` | Request.args handling |
| 02 | `form_data_parsing.py` | Request.form handling |
| 03 | `json_body_parsing.py` | Request.get_json() |
| 04 | `header_inspection.py` | Request.headers access |
| 05 | `cookie_handling.py` | Set/read cookies |
| 06 | `file_upload_handling.py` | Request.files handling |
| 07 | `response_objects.py` | Make_response usage |
| 08 | `redirect_responses.py` | Redirect implementations |
| 09 | `streaming_responses.py` | Generator responses |
| 10 | `custom_response_class.py` | Response subclassing |

**Theory Coverage:**
- Request context lifecycle
- ImmutableMultiDict and regular dict differences
- Response mimetypes
- Streaming vs buffered responses
- Security considerations (CSRF, XSS)

### Day 5: URL Routing & Views

**Learning Objectives:**
- Create complex URL patterns
- Use URL converters (string, int, float, path, uuid)
- Implement custom converters
- Build reusable view functions
- Handle 404 and error routing

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `converter_routing.py` | Built-in converters |
| 02 | `optional_parameters.py` | Default route values |
| 03 | `custom_url_converter.py` | Custom converter class |
| 04 | `subdomain_routing.py` | Subdomain matching |
| 05 | `path_prefixing.py` | url_prefix usage |
| 06 | `endpoint_resolution.py` | Endpoint naming strategies |
| 07 | `catch_all_routes.py` | Path converter usage |
| 08 | `route_ordering.py` | Route precedence |
| 09 | `http_method_routing.py` | Method-based dispatch |
| 10 | `trailing_slashes.py` | Strict_slashes handling |

**Theory Coverage:**
- Flask routing internals
- URL Map and Rules
- Route matching algorithm
- Endpoint naming best practices
- Blueprint registration patterns

### Day 6: Static Files & Configuration

**Learning Objectives:**
- Serve static files (CSS, JS, images)
- Configure Flask applications
- Use environment variables
- Implement configuration classes
- Cache static assets

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `static_file_routing.py` | Static file serving |
| 02 | `configuration_classes.py` | Config inheritance |
| 03 | `environment_variables.py` | os.environ usage |
| 04 | `instance_folders.py` | Instance path usage |
| 05 | `secret_key_management.py` | Secure key handling |
| 06 | `debug_configuration.py` | Debug mode controls |
| 07 | `testing_configuration.py` | Test config patterns |
| 08 | `asset_versioning.py` | Cache-busting URLs |
| 09 | `cdn_configuration.py` | External asset URLs |
| 10 | `settings_loader.py` | Multi-source config |

**Theory Coverage:**
- Flask configuration hierarchy
- Environment-based configuration
- Python-dotenv integration
- Static file caching strategies
- Production vs Development settings

### Week 1 Project: Personal Blog (Foundation)

**Project Requirements:**
- Static homepage with navigation
- About page
- Blog post listing page
- Individual blog post pages (read from markdown files)
- RSS feed endpoint
- Contact form (POST handling)
- 404 error page

**Technical Requirements:**
- Use Flask application factory
- Configuration via environment variables
- Jinja2 templates (preparation for Week 2)
- Static CSS styling
- Form data handling
- Proper HTTP status codes

**Project Structure:**
```
week01_project/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── config.py
│   ├── static/
│   │   ├── css/
│   │   └── images/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── about.html
│       ├── posts.html
│       ├── post.html
│       └── 404.html
├── posts/
│   └── *.md
├── tests/
└── run.py
```

---

## Week 2: Flask Deep Dive

**Week Objective:** Master advanced Flask features including templates, forms, sessions, and authentication.

### Week 2 Overview
| Day | Topic | Problems | Difficulty |
|-----|-------|----------|------------|
| Day 1 | Templates (Jinja2) | 10 | Medium |
| Day 2 | Template Inheritance & Macros | 10 | Medium |
| Day 3 | Forms and Validation | 10 | Medium-Hard |
| Day 4 | Sessions & Cookies | 10 | Medium |
| Day 5 | Authentication System | 10 | Hard |
| Day 6 | Flask Blueprints | 10 | Medium |

### Day 1: Templates (Jinja2)

**Learning Objectives:**
- Master Jinja2 template syntax
- Use template variables and expressions
- Implement control structures (if, for)
- Use template filters
- Create custom filters

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `template_variables.py` | Context passing |
| 02 | `jinja_expressions.py` | Expression syntax |
| 03 | `conditional_rendering.py` | If/elif/else in templates |
| 04 | `loop_rendering.py` | For loops, loop variable |
| 05 | `builtin_filters.py` | Default, length, safe filters |
| 06 | `chaining_filters.py` | Filter pipelines |
| 07 | `custom_filter_registration.py` | @app.template_filter |
| 08 | `date_formatting_filter.py` | Datetime formatting |
| 09 | `escape_html.py` | Auto-escaping, safe |
| 10 | `template_tests.py` | Selectattr, rejectattr |

**Theory Coverage:**
- Jinja2 environment configuration
- Autoescaping and XSS prevention
- Context processors
- Template loading from multiple sources
- Sandboxed execution

### Day 2: Template Inheritance & Macros

**Learning Objectives:**
- Build base templates with blocks
- Extend templates and override blocks
- Create and use macros
- Use include for partials
- Implement super() for parent content

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `base_template_blocks.py` | Block definition |
| 02 | `template_extension.py` | Extends keyword |
| 03 | `block_overriding.py` | Content replacement |
| 04 | `super_inheritance.py` | Super() usage |
| 05 | `nested_blocks.py` | Block nesting |
| 06 | `macro_definitions.py` | Macro creation |
| 07 | `macro_imports.py` | Import with context |
| 08 | `include_partials.py` | Include directive |
| 09 | `set_variables.py` | Set keyword |
| 10 | `with_scoping.py` | With statement |

**Theory Coverage:**
- Template inheritance chain
- Block naming conventions
- Macro scoping rules
- Context behavior in includes
- Template caching

### Day 3: Forms and Validation

**Learning Objectives:**
- Create HTML forms
- Validate form data server-side
- Use Flask-WTF for CSRF protection
- Build custom validators
- Handle form errors

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `html_form_generation.py` | Form HTML building |
| 02 | `form_data_validation.py` | Server-side validation |
| 03 | `wtform_classes.py` | Flask-WTF forms |
| 04 | `csrf_protection.py` | Token generation/validation |
| 05 | `field_validators.py` | Built-in validators |
| 06 | `custom_validators.py` | Validation functions |
| 07 | `cross_field_validation.py` | Multi-field validation |
| 08 | `file_upload_validation.py` | File type, size validation |
| 09 | `error_message_formatting.py` | Error display |
| 10 | `ajax_form_handling.py` | JSON form submission |

**Theory Coverage:**
- CSRF attack prevention
- Form security best practices
- WTForms field types
- Validation pipeline
- Client-side vs server-side validation

### Day 4: Sessions & Cookies

**Learning Objectives:**
- Understand session management
- Use Flask sessions (server-side)
- Implement flash messages
- Set and read cookies
- Configure secure sessions

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `session_basics.py` | Session dict usage |
| 02 | `flash_messages.py` | Flash categories |
| 03 | `session_persistence.py` | Data across requests |
| 04 | `cookie_setting.py` | Set_cookie parameters |
| 05 | `cookie_reading.py` | Request.cookies |
| 06 | `secure_cookies.py` | Secure, httponly, samesite |
| 07 | `session_timeout.py` | Permanent sessions |
| 08 | `session_storage_types.py` | Filesystem, redis, db |
| 09 | `session_encryption.py` | Secret key usage |
| 10 | `session_fixation_protection.py` | Regenerate session ID |

**Theory Coverage:**
- Signed cookies (Flask default)
- Server-side session storage
- Session security (httponly, secure, samesite)
- Session fixation attacks
- Session hijacking prevention

### Day 5: Authentication System

**Learning Objectives:**
- Build user registration
- Implement password hashing
- Create login/logout flow
- Protect routes with decorators
- Remember me functionality

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `password_hashing.py` | Werkzeug security |
| 02 | `verify_password.py` | Check_password_hash |
| 03 | `user_session_management.py` | Store user in session |
| 04 | `login_required_decorator.py` | Route protection |
| 05 | `role_based_access.py` | Admin decorators |
| 06 | `remember_me_tokens.py` | Secure token generation |
| 07 | `password_reset_flow.py` | Token-based reset |
| 08 | `login_attempt_limiting.py` | Rate limiting login |
| 09 | `session_invalidation.py` | Logout handling |
| 10 | `current_user_proxy.py` | Global user access |

**Theory Coverage:**
- Password hashing algorithms (pbkdf2, bcrypt, argon2)
- Timing attack prevention
- Session security best practices
- Authentication vs Authorization
- JWT vs Session-based auth

### Day 6: Flask Blueprints

**Learning Objectives:**
- Structure large Flask applications
- Create and register blueprints
- Use blueprint-specific templates/static
- Implement blueprint before_request
- Organize code by feature

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `blueprint_creation.py` | Blueprint() constructor |
| 02 | `blueprint_routes.py` | @bp.route decorator |
| 03 | `blueprint_registration.py` | App.register_blueprint |
| 04 | `url_prefix_blueprints.py` | Prefix mounting |
| 05 | `blueprint_templates.py` | Template folders |
| 06 | `blueprint_static.py` | Static folders |
| 07 | `nested_blueprints.py` | Blueprint composition |
| 08 | `blueprint_error_handlers.py` | Blueprint-local errors |
| 09 | `blueprint_hooks.py` | Before_request in bp |
| 10 | `application_factory_pattern.py` | Full app structure |

**Theory Coverage:**
- Monolith vs Modular architecture
- Domain-driven design with blueprints
- Blueprint deferred operations
- Circular import prevention
- Testing blueprint-based apps

### Week 2 Project: Personal Blog (Complete)

**Project Requirements:**
- All Week 1 features plus:
- Admin authentication system
- Create/edit/delete posts via web interface
- Flash messages for user feedback
- Comment system (moderated)
- Tag system for posts
- Search functionality
- RSS/Atom feeds
- Sitemap generation

**Technical Requirements:**
- Blueprint structure (main, auth, admin, api)
- WTForms for all forms
- Session-based authentication
- Template inheritance hierarchy
- CSRF protection on all forms
- Pagination for posts and comments

**New Features:**
```
week02_project/
├── app/
│   ├── __init__.py
│   ├── extensions.py      # db, login, etc.
│   ├── config.py
│   ├── blueprints/
│   │   ├── __init__.py
│   │   ├── main.py        # Public routes
│   │   ├── auth.py        # Login/logout
│   │   └── admin.py       # Post management
│   ├── models/            # Post, User, Comment (simplified)
│   ├── forms/             # WTForms classes
│   ├── static/
│   └── templates/
│       ├── base.html
│       ├── main/
│       ├── auth/
│       └── admin/
└── tests/
```

---

## Week 3: Databases & ORM (SQLAlchemy)

**Week Objective:** Master database design, ORM patterns, and migrations with SQLAlchemy 2.0.

### Week 3 Overview
| Day | Topic | Problems | Difficulty |
|-----|-------|----------|------------|
| Day 1 | SQLAlchemy ORM Basics | 10 | Medium |
| Day 2 | Models & CRUD Operations | 10 | Medium-Hard |
| Day 3 | Relationships | 10 | Hard |
| Day 4 | Advanced Queries | 10 | Hard |
| Day 5 | Database Migrations (Alembic) | 10 | Medium |
| Day 6 | Performance & Optimization | 10 | Medium-Hard |

### Day 1: SQLAlchemy ORM Basics

**Learning Objectives:**
- Understand ORM concepts
- Set up SQLAlchemy with Flask
- Create declarative models
- Map Python classes to database tables
- Configure database connections

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `engine_creation.py` | create_engine basics |
| 02 | `declarative_base.py` | Base class definition |
| 03 | `column_definitions.py` | Column types |
| 04 | `primary_keys.py` | PK configuration |
| 05 | `default_values.py` | Default, server_default |
| 06 | `nullable_constraints.py` | Nullable settings |
| 07 | `unique_constraints.py` | Unique columns |
| 08 | `index_creation.py` | Index definitions |
| 09 | `table_names.py` | __tablename__ |
| 10 | `metadata_inspection.py` | Reflect tables |

**Theory Coverage:**
- SQLAlchemy 2.0 style (new API)
- Engine, Connection, Session architecture
- Declarative vs Classical mapping
- Metadata and Table objects
- Database URL formats

### Day 2: Models & CRUD Operations

**Learning Objectives:**
- Create records (INSERT)
- Read records with queries (SELECT)
- Update existing records
- Delete records
- Understand the session lifecycle

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `create_records.py` | Session.add(), commit() |
| 02 | `bulk_insert.py` | Add multiple, bulk operations |
| 03 | `query_all.py` | select() basics |
| 04 | `query_filtering.py` | where() clauses |
| 05 | `query_by_id.py` | Primary key lookup |
| 06 | `query_first_scalar.py` | First(), scalar_one() |
| 07 | `update_records.py` | Update statements |
| 08 | `delete_records.py` | Delete statements |
| 09 | `upsert_operations.py` | On_conflict, merge |
| 10 | `transaction_rollback.py` | Rollback on error |

**Theory Coverage:**
- Unit of Work pattern
- Identity Map pattern
- Session commit/flush/expire
- ACID properties
- Optimistic vs Pessimistic locking

### Day 3: Relationships

**Learning Objectives:**
- Define one-to-many relationships
- Define many-to-one relationships
- Implement many-to-many with association tables
- Use one-to-one relationships
- Understand relationship loading strategies

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `one_to_many_setup.py` | relationship(), back_populates |
| 02 | `many_to_one_navigation.py` | Parent access from child |
| 03 | `many_to_many_association.py` | Association table |
| 04 | `one_to_one_relationship.py` | uselist=False |
| 05 | `self_referential.py` | Adjacency list |
| 06 | `lazy_loading.py` | Default loading |
| 07 | `eager_loading.py` | joinedload(), selectinload() |
| 08 | `dynamic_relationship.py` | lazy='dynamic' |
| 09 | `cascade_operations.py` | Cascade delete, save-update |
| 10 | `relationship_ordering.py` | order_by in relationship |

**Theory Coverage:**
- Foreign key constraints
- Relationship loading strategies (lazy, eager, dynamic)
- Association proxies
- Composite foreign keys
- Self-referential relationships

### Day 4: Advanced Queries

**Learning Objectives:**
- Build complex WHERE clauses
- Use aggregations (COUNT, SUM, AVG)
- Implement pagination
- Use subqueries
- Build CTEs (Common Table Expressions)

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `and_or_conditions.py` | and_(), or_(), not_() |
| 02 | `in_operators.py` | in_(), notin_() |
| 03 | `like_pattern_matching.py` | like(), ilike() |
| 04 | `null_checks.py` | is_(), isnot_(), is_(None) |
| 05 | `count_aggregation.py` | func.count() |
| 06 | `sum_avg_min_max.py` | Aggregate functions |
| 07 | `group_by_having.py` | Grouping, filtering groups |
| 08 | `limit_offset_pagination.py` | Limit, offset |
| 09 | `subqueries.py` | Subquery construction |
| 10 | `common_table_expressions.py` | CTE, recursive CTEs |

**Theory Coverage:**
- SQL expression language
- Query compilation
- Bind parameters
- Window functions overview
- Raw SQL execution

### Day 5: Database Migrations (Alembic)

**Learning Objectives:**
- Set up Alembic with Flask
- Create migration scripts
- Run upgrades and downgrades
- Auto-generate migrations
- Handle migration conflicts

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `alembic_init.py` | Environment setup |
| 02 | `create_migration.py` | Revision creation |
| 03 | `upgrade_downgrade.py` | Migration operations |
| 04 | `auto_generate.py` | Autogenerate detection |
| 05 | `add_column_migration.py` | op.add_column() |
| 06 | `alter_column_migration.py` | op.alter_column() |
| 07 | `create_index_migration.py` | op.create_index() |
| 08 | `foreign_key_migration.py` | op.create_foreign_key() |
| 09 | `data_migration.py` | Python data migrations |
| 10 | `migration_branching.py` | Merge branches |

**Theory Coverage:**
- Migration best practices
- Idempotent migrations
- Migration testing
- Production deployment strategies
- Rollback procedures

### Day 6: Performance & Optimization

**Learning Objectives:**
- Profile SQLAlchemy queries
- Use eager loading effectively
- Implement database indexing
- Batch operations
- Connection pooling

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `query_profiling.py` | Echo, logging queries |
| 02 | `n_plus_one_detection.py` | Identify N+1 problems |
| 03 | `eager_loading_solution.py` | Fix with joinedload |
| 04 | `index_usage.py` | Explain query plans |
| 05 | `bulk_insert_optimization.py` | Bulk operations |
| 06 | `bulk_update_delete.py` | Bulk ORM operations |
| 07 | `connection_pooling.py` | Pool configuration |
| 08 | `read_replicas.py` | Routing queries |
| 09 | `query_caching.py` | Dogpile.cache integration |
| 10 | `async_sqlalchemy.py` | AsyncSession basics |

**Theory Coverage:**
- N+1 query problem
- Query plan analysis
- Database indexing strategies
- Connection pool tuning
- Async SQLAlchemy architecture

### Week 3 Project: Task Manager with Auth

**Project Requirements:**
- User registration and login
- Create, read, update, delete tasks
- Task categories/tags
- Task priorities and due dates
- Task assignment (share with other users)
- Task status workflow (todo, in-progress, done)
- Comments on tasks
- Email notifications (mock)
- Task search and filtering

**Technical Requirements:**
- SQLAlchemy 2.0 style ORM
- PostgreSQL database
- Alembic migrations
- Flask-Login for session management
- Werkzeug for password hashing
- Proper relationship modeling
- Pagination for task lists
- Comprehensive test suite

**Database Schema:**
```python
# Core models
User
- id, username, email, password_hash, created_at

Task
- id, title, description, status, priority, due_date
- creator_id (FK to User)
- created_at, updated_at

Category
- id, name, color, user_id (FK)

TaskCategory (association)
- task_id, category_id

TaskShare
- task_id, user_id, permission (read/edit)

Comment
- id, task_id, user_id, content, created_at
```

---

## Week 4: Testing Web Applications

**Week Objective:** Master testing strategies for Flask applications including unit, integration, and end-to-end tests.

### Week 4 Overview
| Day | Topic | Problems | Difficulty |
|-----|-------|----------|------------|
| Day 1 | Flask Test Client | 10 | Medium |
| Day 2 | Database Testing | 10 | Medium-Hard |
| Day 3 | Factory Pattern for Tests | 10 | Medium |
| Day 4 | Mocking External Services | 10 | Medium |
| Day 5 | Integration Testing | 10 | Hard |
| Day 6 | Test Coverage & Quality | 10 | Medium |

### Day 1: Flask Test Client

**Learning Objectives:**
- Configure Flask for testing
- Use the test client
- Test different HTTP methods
- Handle authentication in tests
- Test JSON APIs

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `test_client_setup.py` | App fixture, test client |
| 02 | `get_request_tests.py` | Testing GET routes |
| 03 | `post_request_tests.py` | Testing POST routes |
| 04 | `json_api_tests.py` | Content-Type, JSON data |
| 05 | `status_code_assertions.py` | Assert response status |
| 06 | `response_data_assertions.py` | Assert response content |
| 07 | `header_assertions.py` | Response header checks |
| 08 | `follow_redirects_tests.py` | Redirect following |
| 09 | `cookie_testing.py` | Set/verify cookies |
| 10 | `session_testing.py` | Session in tests |

**Theory Coverage:**
- Test client vs LiveServer
- Request contexts in tests
- Application contexts in tests
- Testing configuration
- Fixture scopes

### Day 2: Database Testing

**Learning Objectives:**
- Set up test databases
- Rollback transactions after tests
- Use factories for test data
- Test database constraints
- Handle database fixtures

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `test_database_setup.py` | SQLite in-memory, test config |
| 02 | `transaction_rollback.py` | Rollback after each test |
| 03 | `database_fixtures.py` | Connection fixtures |
| 04 | `populate_test_data.py` | Setup method, fixtures |
| 05 | `test_constraints.py` | Unique, FK violations |
| 06 | `test_migrations.py` | Upgrade/downgrade tests |
| 07 | `isolated_database_tests.py` | Schema per test |
| 08 | `async_db_testing.py` | Async test patterns |
| 09 | `parallel_test_execution.py` | xdist configuration |
| 10 | `database_assertions.py` | Verify DB state |

**Theory Coverage:**
- Transaction isolation levels
- Savepoints in tests
- Database seeding strategies
- Fixture factories
- Test database performance

### Day 3: Factory Pattern for Tests

**Learning Objectives:**
- Use factory_boy for test data
- Define model factories
- Create factory relationships
- Override factory defaults
- Generate sequences

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `factory_boy_setup.py` | Factory base classes |
| 02 | `user_factory.py` | User model factory |
| 03 | `sequence_generation.py` | Sequence, Faker integration |
| 04 | `post_factory.py` | Related model factory |
| 05 | `factory_relationships.py` | SubFactory, RelatedFactory |
| 06 | `trait_definitions.py` | Factory traits |
| 07 | `batch_creation.py` | create_batch() |
| 08 | `factory_overrides.py` | Override at creation |
| 09 | `lazy_attributes.py` | LazyAttribute |
| 10 | `factory_hooks.py` | Post-generation hooks |

**Theory Coverage:**
- Factory vs Fixture tradeoffs
- Faker integration
- Factory inheritance
- Build vs Create strategies
- Factory best practices

### Day 4: Mocking External Services

**Learning Objectives:**
- Use unittest.mock for patching
- Mock HTTP requests with responses
- Mock email services
- Mock time-dependent code
- Use pytest-mock fixtures

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `mock_basics.py` | Mock, MagicMock |
| 02 | `patch_decorator.py` | @patch usage |
| 03 | `patch_context_manager.py` | with patch() |
| 04 | `requests_mock.py` | responses library |
| 05 | `httpx_mock.py` | respx for httpx |
| 06 | `mock_email_service.py` | Mail mock |
| 07 | `mock_file_system.py` | mock_open, patch open |
| 08 | `mock_datetime.py` | freeze_time |
| 09 | `mock_side_effects.py` | side_effect usage |
| 10 | `spy_assertions.py` | assert_called_with |

**Theory Coverage:**
- Where to patch (import paths)
- Mock spec and autospec
- Async mocking
- Mock call assertions
- Partial mocking

### Day 5: Integration Testing

**Learning Objectives:**
- Test full request flows
- Test authentication flows
- Test database transactions
- Test error handling
- Use test coverage tools

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `end_to_end_flow.py` | Full user journey |
| 02 | `authentication_flow.py` | Login -> action -> logout |
| 03 | `crud_flow_testing.py` | Create -> read -> update -> delete |
| 04 | `form_submission_flow.py` | Form -> validation -> success |
| 05 | `api_integration_test.py` | Multi-endpoint flow |
| 06 | `error_scenario_tests.py` | Error handling paths |
| 07 | `concurrent_request_tests.py` | Race conditions |
| 08 | `webhook_testing.py` | External callback testing |
| 09 | `file_upload_flow.py` | Upload -> process -> verify |
| 10 | `websocket_testing.py` | Socket.IO/flask-socketio tests |

**Theory Coverage:**
- Integration vs Unit test boundaries
- Test database isolation
- External service test doubles
- Contract testing concepts
- Consumer-driven contracts

### Day 6: Test Coverage & Quality

**Learning Objectives:**
- Generate coverage reports
- Configure coverage tools
- Identify untested code
- Write maintainable tests
- Use property-based testing

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `coverage_basics.py` | pytest-cov usage |
| 02 | `coverage_configuration.py` | .coveragerc setup |
| 03 | `branch_coverage.py` | Branch vs line coverage |
| 04 | `coverage_reporting.py` | HTML, XML reports |
| 05 | `exclusion_pragmas.py` | pragma: no cover |
| 06 | `test_parameterization.py` | pytest.mark.parametrize |
| 07 | `hypothesis_testing.py` | Property-based tests |
| 08 | `test_refactoring.py` | DRY test principles |
| 09 | `test_documentation.py` | Given-when-then style |
| 10 | `test_maintenance.py` | Flaky test detection |

**Theory Coverage:**
- Coverage targets and thresholds
- Mutation testing concepts
- TDD vs BDD approaches
- Test pyramid
- CI integration

### Week 4 Project: Tested API Service

**Project Requirements:**
- RESTful API for a resource (e.g., bookstore, inventory)
- Full CRUD operations
- Authentication/authorization
- Input validation
- Error handling
- Pagination
- Search/filtering
- Rate limiting

**Testing Requirements:**
- >90% code coverage
- Unit tests for business logic
- Integration tests for API endpoints
- Database fixture factories
- Mocked external services
- Authentication flow tests
- Error scenario coverage
- Performance/smoke tests

**Project Structure:**
```
week04_project/
├── app/
│   ├── __init__.py
│   ├── api/
│   ├── models/
│   ├── services/
│   └── extensions.py
├── tests/
│   ├── conftest.py
│   ├── factories/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── migrations/
└── pytest.ini
```

---

## Week 5: API Development (FastAPI)

**Week Objective:** Build high-performance APIs with FastAPI, leveraging modern Python features.

### Week 5 Overview
| Day | Topic | Problems | Difficulty |
|-----|-------|----------|------------|
| Day 1 | FastAPI Introduction | 10 | Medium |
| Day 2 | Pydantic Models | 10 | Medium-Hard |
| Day 3 | Dependency Injection | 10 | Hard |
| Day 4 | Async Endpoints | 10 | Hard |
| Day 5 | Advanced FastAPI | 10 | Hard |
| Day 6 | API Documentation | 10 | Medium |

### Day 1: FastAPI Introduction

**Learning Objectives:**
- Understand FastAPI vs Flask architecture
- Create basic FastAPI applications
- Use path and query parameters
- Return JSON responses
- Use automatic API documentation

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `fastapi_hello_world.py` | App creation |
| 02 | `path_parameters.py` | {item_id} syntax |
| 03 | `query_parameters.py` | Optional query params |
| 04 | `request_body_basics.py` | POST with body |
| 05 | `response_models.py` | Response_model parameter |
| 06 | `status_codes.py` | Status_code parameter |
| 07 | `http_exception_handling.py` | HTTPException |
| 08 | `background_tasks.py` | BackgroundTask |
| 09 | `static_files_mount.py` | Mount static files |
| 10 | `middleware_basics.py` | Custom middleware |

**Theory Coverage:**
- ASGI vs WSGI
- Starlette foundation
- Type hints as contract
- Automatic OpenAPI generation
- Performance characteristics

### Day 2: Pydantic Models

**Learning Objectives:**
- Define Pydantic models
- Validate input data
- Use field constraints
- Implement nested models
- Handle model inheritance

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `basic_model_definition.py` | BaseModel subclass |
| 02 | `field_validators.py` | Field() constraints |
| 03 | `type_validation.py` | Automatic coercion |
| 04 | `custom_validators.py` | @validator decorator |
| 05 | `nested_models.py` | Model composition |
| 06 | `model_inheritance.py` | Model subclassing |
| 07 | `optional_fields.py` | Optional, default values |
| 08 | `datetime_handling.py` | datetime parsing |
| 09 | `model_serialization.py` | dict(), json() |
| 10 | `model_configuration.py` | Config class |

**Theory Coverage:**
- Pydantic v1 vs v2 differences
- Validation timing (on init vs explicitly)
- Custom types and validators
- ModelConfig options
- JSON Schema generation

### Day 3: Dependency Injection

**Learning Objectives:**
- Create FastAPI dependencies
- Use Depends for injection
- Build dependency hierarchies
- Implement security dependencies
- Cache dependencies

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `simple_dependency.py` | Depends() function |
| 02 | `dependency_parameters.py` | Parametrized deps |
| 03 | `dependency_hierarchy.py` | Nested dependencies |
| 04 | `class_dependencies.py` | __call__ pattern |
| 05 | `database_dependency.py` | Session injection |
| 06 | `authentication_dependency.py` | Current user deps |
| 07 | `authorization_dependency.py` | Permission deps |
| 08 | `sub_dependencies.py` | Sub-dependency chain |
| 09 | `dependency_overrides.py` | Testing overrides |
| 10 | `cached_dependencies.py` | use_cache parameter |

**Theory Coverage:**
- DI container concepts
- Lifespan of dependencies
- Sub-dependencies and caching
- Override mechanism for testing
- Generator dependencies (cleanup)

### Day 4: Async Endpoints

**Learning Objectives:**
- Write async route handlers
- Use async database drivers
- Handle concurrent requests
- Implement async context managers
- Understand event loops

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `async_route_handlers.py` | async def endpoints |
| 02 | `await_coroutines.py` | Await syntax |
| 03 | `async_database_queries.py` | Async SQLAlchemy |
| 04 | `async_http_client.py` | httpx.AsyncClient |
| 05 | `gather_concurrent.py` | asyncio.gather |
| 06 | `async_context_managers.py` | async with |
| 07 | `background_tasks_async.py` | Async background tasks |
| 08 | `websocket_endpoints.py` | WebSocket support |
| 09 | `streaming_responses_async.py` | StreamingResponse |
| 10 | `async_generators.py` | yield in async |

**Theory Coverage:**
- asyncio fundamentals
- Async/await syntax
- Event loop management
- Concurrent vs Parallel execution
- Backpressure handling

### Day 5: Advanced FastAPI

**Learning Objectives:**
- Handle file uploads
- Implement authentication with OAuth2
- Use API versioning
- Implement rate limiting
- Handle CORS

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `file_upload_handling.py` | UploadFile, File |
| 02 | `multipart_forms.py` | Form + File combined |
| 03 | `oauth2_password_flow.py` | OAuth2PasswordBearer |
| 04 | `jwt_token_handling.py` | JWT creation/validation |
| 05 | `api_versioning.py` | Version in path/header |
| 06 | `cors_configuration.py` | CORSMiddleware |
| 07 | `rate_limiting.py` | Slowapi integration |
| 08 | `response_caching.py` | CacheControl |
| 09 | `custom_exceptions.py` | Exception handlers |
| 10 | `lifespan_events.py` | Startup/shutdown |

**Theory Coverage:**
- OAuth2 flows overview
- JWT best practices
- API versioning strategies
- Rate limiting algorithms
- Middleware chaining

### Day 6: API Documentation

**Learning Objectives:**
- Customize OpenAPI schema
- Add descriptions and examples
- Use tags for organization
- Implement response examples
- Export documentation

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `openapi_metadata.py` | Title, version, description |
| 02 | `endpoint_descriptions.py` | Docstrings, summary |
| 03 | `parameter_documentation.py` | Query/Path descriptions |
| 04 | `request_examples.py` | Example values |
| 05 | `response_examples.py` | Responses dictionary |
| 06 | `tag_organization.py` | Tags, tags_metadata |
| 07 | `schema_customization.py` | Custom OpenAPI schema |
| 08 | `security_schemes.py` | OAuth2 in docs |
| 09 | `webhook_documentation.py` | Webhook schema |
| 10 | `docs_export.py` | JSON/YAML export |

**Theory Coverage:**
- OpenAPI 3.0 specification
- Swagger UI customization
- ReDoc integration
- Documentation-driven development
- SDK generation from OpenAPI

### Week 5 Project: High-Performance API

**Project Requirements:**
- FastAPI-based REST API
- Async database operations (asyncpg)
- Full CRUD for complex resource
- Authentication with JWT
- Role-based access control
- Rate limiting
- Request/response validation
- Comprehensive OpenAPI docs
- Background task processing
- File upload/download

**Technical Stack:**
- FastAPI + Uvicorn
- SQLAlchemy 2.0 Async
- PostgreSQL with asyncpg
- Pydantic v2 models
- Redis for caching/rate limiting
- Celery for background tasks (optional)
- pytest-asyncio for testing

**Performance Targets:**
- <50ms p95 response time for simple queries
- Handle 1000+ concurrent connections
- Efficient database query patterns
- Connection pooling optimization

---

## Week 6: Frontend Integration & JavaScript

**Week Objective:** Connect Python backends to frontend interfaces using modern JavaScript patterns.

### Week 6 Overview
| Day | Topic | Problems | Difficulty |
|-----|-------|----------|------------|
| Day 1 | JavaScript for Python Devs | 10 | Easy-Medium |
| Day 2 | DOM Manipulation | 10 | Medium |
| Day 3 | AJAX & Fetch API | 10 | Medium |
| Day 4 | Template Rendering vs API | 10 | Medium |
| Day 5 | HTMX for Interactivity | 10 | Medium |
| Day 6 | Minimal Frontend Frameworks | 10 | Medium-Hard |

### Day 1: JavaScript for Python Devs

**Learning Objectives:**
- Map Python concepts to JavaScript
- Understand JS type system
- Use modern ES6+ features
- Handle async operations
- Work with modules

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `js_variables_scope.py` | let, const, var |
| 02 | `js_functions.py` | Arrow functions, this |
| 03 | `js_data_structures.py` | Arrays, Objects, Maps |
| 04 | `js_destructuring.py` | Destructuring assignment |
| 05 | `js_spread_rest.py` | ... operator |
| 06 | `js_promises.py` | Promise, async/await |
| 07 | `js_modules.py` | Import/export |
| 08 | `js_classes.py` | Class syntax |
| 09 | `js_error_handling.py` | Try/catch |
| 10 | `js_python_comparison.py` | Concept mapping |

**Theory Coverage:**
- JS vs Python: key differences
- Prototypal vs Classical inheritance
- Event loop and callbacks
- Module systems (ESM, CommonJS)
- TypeScript introduction

### Day 2: DOM Manipulation

**Learning Objectives:**
- Select DOM elements
- Modify element content
- Handle events
- Create and remove elements
- Use data attributes

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `element_selection.py` | querySelector, getElementById |
| 02 | `content_modification.py` | textContent, innerHTML |
| 03 | `attribute_handling.py` | getAttribute, setAttribute |
| 04 | `class_manipulation.py` | classList API |
| 05 | `event_listeners.py` | addEventListener |
| 06 | `event_delegation.py` | Delegation pattern |
| 07 | `element_creation.py` | createElement |
| 08 | `element_removal.py` | removeChild, remove |
| 09 | `data_attributes.py` | dataset API |
| 10 | `form_interaction.py` | Form element access |

**Theory Coverage:**
- DOM tree structure
- Event bubbling and capturing
- Reflow and repaint
- Virtual DOM concept
- Accessibility (ARIA)

### Day 3: AJAX & Fetch API

**Learning Objectives:**
- Make HTTP requests from JS
- Handle JSON responses
- Send form data
- Upload files
- Handle errors

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `fetch_get_request.py` | fetch() GET |
| 02 | `fetch_post_json.py` | POST with JSON |
| 03 | `fetch_headers.py` | Custom headers |
| 04 | `fetch_form_data.py` | FormData object |
| 05 | `fetch_file_upload.py` | File upload |
| 06 | `fetch_error_handling.py` | Response.ok, catch |
| 07 | `fetch_async_await.py` | Async fetch pattern |
| 08 | `fetch_abort_controller.py` | Request cancellation |
| 09 | `fetch_parallel.py` | Promise.all for multiple |
| 10 | `csrf_token_handling.py` | CSRF in AJAX |

**Theory Coverage:**
- XMLHttpRequest vs Fetch
- CORS preflight
- Request/Response lifecycle
- Streaming responses
- Service Workers

### Day 4: Template Rendering vs API

**Learning Objectives:**
- Compare SSR vs SPA approaches
- Implement server-side rendering
- Build API-first backends
- Use JSON for data exchange
- Choose rendering strategy

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `ssr_basics.py` | Server-rendered HTML |
| 02 | `api_json_response.py` | JSON API design |
| 03 | `hydration_concept.py` | Client-side hydration |
| 04 | `template_partial_updates.py` | HTML fragment responses |
| 05 | `json_api_consumption.py` | JS rendering from API |
| 06 | `hybrid_approach.py` | Mixing SSR and API |
| 07 | `progressive_enhancement.py` | No-JS fallback |
| 08 | `form_submission_modes.py` | Traditional vs AJAX form |
| 09 | `content_negotiation.py` | Accept header routing |
| 10 | `rendering_tradeoffs.py` | When to use which |

**Theory Coverage:**
- SSR vs CSR vs SSG
- Time to First Byte (TTFB)
- Time to Interactive (TTI)
- SEO considerations
- Complexity tradeoffs

### Day 5: HTMX for Interactivity

**Learning Objectives:**
- Use HTMX attributes
- Handle HTMX requests in Flask/FastAPI
- Implement partial page updates
- Handle HTMX events
- Build interactive UI without complex JS

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `htmx_get_request.py` | hx-get attribute |
| 02 | `htmx_post_request.py` | hx-post, hx-target |
| 03 | `htmx_trigger_events.py` | hx-trigger |
| 04 | `htmx_swapping.py` | hx-swap strategies |
| 05 | `htmx_indicator.py` | Loading states |
| 06 | `htmx_confirm.py` | Confirmation dialogs |
| 07 | `htmx_oob_swaps.py` | Out-of-band updates |
| 08 | `htmx_history.py` | hx-push-url |
| 09 | `htmx_validation.py` | Server validation |
| 10 | `htmx_polling.py` | Periodic updates |

**Theory Coverage:**
- Progressive enhancement philosophy
- HTML-over-the-wire
- HATEOAS with HTMX
- Accessibility with HTMX
- Performance considerations

### Day 6: Minimal Frontend Frameworks

**Learning Objectives:**
- Use Alpine.js for reactivity
- Implement Vue.js components
- Build React components
- Understand component lifecycle
- State management basics

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `alpinejs_basics.py` | x-data, x-show |
| 02 | `alpinejs_bindings.py` | x-model, x-on |
| 03 | `alpinejs_fetch.py` | x-init with fetch |
| 04 | `vuejs_component.py` | Vue component structure |
| 05 | `vuejs_reactivity.py` | Refs, reactive |
| 06 | `react_component.py` | JSX component |
| 07 | `react_hooks.py` | useState, useEffect |
| 08 | `react_fetching.py` | Data fetching pattern |
| 09 | `component_props.py` | Passing data down |
| 10 | `minimal_framework_choice.py` | When to use what |

**Theory Coverage:**
- Reactive programming
- Virtual DOM
- Component composition
- State lifting
- Framework selection criteria

### Week 6 Project: Interactive Dashboard

**Project Requirements:**
- Real-time data visualization dashboard
- Multiple chart types (line, bar, pie)
- Data filtering and date ranges
- Auto-refresh capability
- Export to CSV/Excel
- Responsive design

**Technical Approach:**
- Flask or FastAPI backend
- HTMX for most interactions
- Chart.js or D3.js for visualization
- Server-Sent Events for real-time updates (optional)
- Alpine.js for complex UI state
- Responsive CSS Grid/Flexbox

**Features:**
```
Dashboard Components:
├── Header with date range selector
├── KPI cards (auto-updating)
├── Line chart (time series)
├── Bar chart (comparisons)
├── Data table with pagination
└── Export controls
```

---

## Week 7: Deployment & Production

**Week Objective:** Prepare applications for production deployment with containerization and CI/CD.

### Week 7 Overview
| Day | Topic | Problems | Difficulty |
|-----|-------|----------|------------|
| Day 1 | Docker Fundamentals | 10 | Medium |
| Day 2 | Dockerizing Flask/FastAPI | 10 | Medium-Hard |
| Day 3 | Docker Compose | 10 | Medium |
| Day 4 | Environment Variables | 10 | Medium |
| Day 5 | Logging & Monitoring | 10 | Medium-Hard |
| Day 6 | CI/CD Pipelines | 10 | Medium |

### Day 1: Docker Fundamentals

**Learning Objectives:**
- Understand containerization concepts
- Write Dockerfiles
- Use Docker commands
- Understand layers and caching
- Optimize image size

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `dockerfile_basics.py` | FROM, RUN, CMD |
| 02 | `docker_build_context.py` | .dockerignore |
| 03 | `docker_image_layers.py` | Layer caching |
| 04 | `docker_commands.py` | build, run, ps, exec |
| 05 | `docker_ports_volumes.py` | -p, -v flags |
| 06 | `docker_networking.py` | Network creation |
| 07 | `multi_stage_builds.py` | Production optimization |
| 08 | `docker_env_vars.py` | ENV, --env |
| 09 | `docker_health_checks.py` | HEALTHCHECK |
| 10 | `docker_best_practices.py` | Security, size |

**Theory Coverage:**
- Containers vs VMs
- Docker architecture
- Image vs Container
- Registry and tagging
- Security scanning

### Day 2: Dockerizing Flask/FastAPI

**Learning Objectives:**
- Create production-ready Dockerfiles
- Configure WSGI/ASGI servers
- Handle static files
- Use non-root users
- Multi-stage builds

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `flask_dockerfile.py` | Gunicorn setup |
| 02 | `fastapi_dockerfile.py` | Uvicorn setup |
| 03 | `requirements_optimization.py` | Layer caching deps |
| 04 | `static_files_docker.py` | Nginx or Whitenoise |
| 05 | `non_root_user.py` | USER directive |
| 06 | `python_version_pinning.py` | Specific Python tag |
| 07 | `entrypoint_scripts.py` | Migration handling |
| 08 | `hot_reload_docker.py` | Dev vs Prod configs |
| 09 | `docker_security.py` | Secrets, scanning |
| 10 | `image_optimization.py` | Slim, alpine images |

**Theory Coverage:**
- WSGI (Gunicorn, uWSGI)
- ASGI (Uvicorn, Hypercorn)
- Process vs Thread workers
- Static file serving strategies
- Container security hardening

### Day 3: Docker Compose

**Learning Objectives:**
- Write docker-compose.yml files
- Define multi-service applications
- Use environment files
- Manage data volumes
- Scale services

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `compose_basics.py` | services, networks |
| 02 | `compose_dependencies.py` | depends_on |
| 03 | `compose_volumes.py` | Named volumes |
| 04 | `compose_environment.py` | env_file, environment |
| 05 | `compose_database.py` | PostgreSQL service |
| 06 | `compose_redis.py` | Redis service |
| 07 | `compose_profiles.py` | Dev vs prod profiles |
| 08 | `compose_scaling.py` | --scale flag |
| 09 | `compose_healthchecks.py` | Service health |
| 10 | `compose_override.py` | docker-compose.override.yml |

**Theory Coverage:**
- Service discovery
- Network isolation
- Persistent storage
- Configuration management
- Development vs Production compose

### Day 4: Environment Variables

**Learning Objectives:**
- Use 12-factor app methodology
- Manage secrets securely
- Load configuration from environment
- Validate configuration
- Handle different environments

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `env_var_loading.py` | os.environ access |
| 02 | `python_dotenv.py` | .env file loading |
| 03 | `pydantic_settings.py` | Settings class |
| 04 | `env_validation.py` | Required vs optional |
| 05 | `env_type_coercion.py` | Int, bool from env |
| 06 | `env_defaults.py` | Default values |
| 07 | `secret_management.py` | Docker secrets |
| 08 | `env_file_separation.py` | .env.example |
| 09 | `config_inheritance.py` | Base, Dev, Prod |
| 10 | `env_security.py` | Never commit secrets |

**Theory Coverage:**
- 12-factor app principles
- Secrets management (Vault, AWS SM)
- Configuration injection
- Environment-specific settings
- Security best practices

### Day 5: Logging & Monitoring

**Learning Objectives:**
- Configure Python logging
- Structure logs as JSON
- Use centralized logging
- Implement health checks
- Set up basic monitoring

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `logging_configuration.py` | DictConfig |
| 02 | `log_levels.py` | DEBUG to CRITICAL |
| 03 | `structured_logging.py` | JSON formatter |
| 04 | `request_logging.py` | Middleware logging |
| 05 | `error_logging.py` | Exception logging |
| 06 | `health_check_endpoint.py` | /health endpoint |
| 07 | `application_metrics.py` | Prometheus basics |
| 08 | `log_aggregation.py` | ELK/Loki concepts |
| 09 | `distributed_tracing.py` | Trace IDs |
| 10 | `alerting_basics.py` | Alert thresholds |

**Theory Coverage:**
- Log aggregation systems
- Metrics vs Logs vs Traces
- Observability pillars
- Alerting strategies
- SLI/SLO/SLA concepts

### Day 6: CI/CD Pipelines

**Learning Objectives:**
- Write GitHub Actions workflows
- Run tests in CI
- Build and push Docker images
- Deploy to staging/production
- Implement rollback strategies

**Exercise Specifications:**

| # | Problem | Concepts |
|---|---------|----------|
| 01 | `github_actions_basics.py` | .github/workflows |
| 02 | `ci_test_pipeline.py` | pytest in CI |
| 03 | `linting_in_ci.py` | Black, ruff, mypy |
| 04 | `docker_build_ci.py` | Build and tag |
| 05 | `docker_push_registry.py` | Push to GHCR/DockerHub |
| 06 | `security_scanning.py` | Trivy, CodeQL |
| 07 | `deploy_staging.py` | Staging deployment |
| 08 | `deploy_production.py` | Prod deployment |
| 09 | `rollback_strategy.py` | Rollback mechanisms |
| 10 | `matrix_builds.py` | Multiple Python versions |

**Theory Coverage:**
- Continuous Integration principles
- Continuous Deployment strategies
- Blue-green deployment
- Canary releases
- Infrastructure as Code

### Week 7 Project: Containerized App

**Project Requirements:**
- Complete containerized application
- Multi-service Docker Compose setup
- Production-ready Dockerfile
- GitHub Actions CI/CD pipeline
- Environment-based configuration
- Health check endpoints
- Structured logging
- Basic monitoring setup

**Infrastructure:**
```yaml
# docker-compose.yml
services:
  web:        # Flask/FastAPI app
  db:         # PostgreSQL
  redis:      # Redis (caching/sessions)
  nginx:      # Reverse proxy
  
# CI/CD Pipeline:
- Lint and test
- Build and scan image
- Push to registry
- Deploy to staging
- Deploy to production
```

---

## Week 8: Capstone - Full SaaS Application

**Week Objective:** Build a production-ready multi-tenant SaaS application integrating all learned concepts.

### Week 8 Overview
| Day | Topic | Focus |
|-----|-------|-------|
| Day 1 | Planning & Architecture | Design and scaffolding |
| Day 2 | Core Implementation | Models, auth, base features |
| Day 3 | API Development | REST API with FastAPI |
| Day 4 | Frontend & Integration | Templates + HTMX |
| Day 5 | Testing & Polish | Full test coverage |
| Day 6 | Deployment | Production deployment |

### Capstone Project: Team Collaboration SaaS

**Project Concept:** A team collaboration tool similar to Trello/Asana with:
- Multi-tenant workspaces (teams)
- Project boards with tasks
- Real-time updates
- Role-based permissions
- Billing integration (mock)

### Day 1: Planning & Architecture

**Activities:**
1. **Requirements Analysis**
   - Define user stories
   - Create data models
   - Design API contracts

2. **Architecture Design**
   - Database schema design
   - Service boundaries
   - Authentication strategy
   - Deployment architecture

3. **Project Scaffolding**
   - Repository structure
   - Docker Compose setup
   - CI/CD pipeline skeleton
   - Documentation structure

**Deliverables:**
- Database schema diagram
- API specification (OpenAPI)
- Project structure
- README with setup instructions

### Day 2: Core Implementation

**Implementation Areas:**

1. **Database Layer**
   - SQLAlchemy models
   - Alembic migrations
   - Relationship setup
   - Indexes and constraints

2. **Authentication System**
   - User registration/login
   - JWT token handling
   - Password reset flow
   - Email verification

3. **Authorization**
   - Workspace membership
   - Role definitions (admin, member, viewer)
   - Permission checking
   - Resource-level access control

**Models:**
```python
User
Workspace
WorkspaceMember (User <-> Workspace)
Project
Board
Task
Comment
ActivityLog
```

### Day 3: API Development

**API Implementation:**

1. **Core Endpoints**
   - Auth: POST /auth/login, /auth/register, /auth/refresh
   - Users: GET/PUT /users/me
   - Workspaces: CRUD /workspaces
   - Projects: CRUD /workspaces/{id}/projects
   - Boards: CRUD /projects/{id}/boards
   - Tasks: CRUD /boards/{id}/tasks

2. **Advanced Features**
   - Search with filters
   - Pagination
   - Sorting
   - Batch operations
   - Webhook endpoints

3. **Documentation**
   - OpenAPI specification
   - Example requests/responses
   - Authentication documentation

### Day 4: Frontend & Integration

**Frontend Implementation:**

1. **Base Templates**
   - Layout with navigation
   - Workspace switcher
   - User menu
   - Flash message handling

2. **Dashboard Views**
   - Workspace overview
   - Project list
   - Board view (Kanban)
   - Task detail modal

3. **Interactive Features**
   - HTMX for task operations
   - Drag-and-drop (SortableJS)
   - Real-time updates (SSE)
   - Form validation

**Key Pages:**
```
/                    → Landing page
/login               → Login form
/register            → Registration
/dashboard           → Workspace selector
/w/{id}              → Workspace dashboard
/w/{id}/p/{id}       → Project view
/w/{id}/b/{id}       → Board (Kanban)
/settings            → User settings
```

### Day 5: Testing & Polish

**Testing:**

1. **Unit Tests**
   - Model tests
   - Service layer tests
   - Utility function tests

2. **Integration Tests**
   - API endpoint tests
   - Authentication flow tests
   - Database operation tests

3. **End-to-End Tests**
   - User journey tests
   - Critical path validation

4. **Quality Assurance**
   - Code formatting (Black)
   - Linting (ruff)
   - Type checking (mypy)
   - Security scanning
   - Coverage reporting (>90%)

**Polish:**
- Error page styling
- Loading states
- Confirmation dialogs
- Toast notifications
- Mobile responsiveness

### Day 6: Deployment

**Production Deployment:**

1. **Infrastructure**
   - Docker images built and pushed
   - Cloud server provisioned (or Heroku/Railway)
   - Domain configured
   - SSL certificate (Let's Encrypt)

2. **Environment Setup**
   - Production environment variables
   - Database migration
   - Static files collection
   - Initial admin user

3. **Monitoring**
   - Health checks configured
   - Logging aggregation
   - Error tracking (Sentry)
   - Performance monitoring

4. **Documentation**
   - Deployment guide
   - API documentation live
   - User guide
   - Changelog

**Deployment Checklist:**
```
□ Environment variables configured
□ Database migrations run
□ Static files served
□ SSL certificate installed
□ Health checks passing
□ Monitoring active
□ Backups configured
□ Documentation complete
```

### Final Project Structure

```
capstone_saas/
├── .github/
│   └── workflows/
│       ├── test.yml
│       └── deploy.yml
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── workspace.py
│   │   ├── project.py
│   │   ├── board.py
│   │   └── task.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── workspaces.py
│   │   ├── projects.py
│   │   ├── boards.py
│   │   └── tasks.py
│   ├── web/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── templates/
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── workspace_service.py
│   │   └── task_service.py
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
├── migrations/
├── tests/
│   ├── conftest.py
│   ├── factories/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docker/
│   ├── Dockerfile
│   └── entrypoint.sh
├── docker-compose.yml
├── docker-compose.prod.yml
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .env.example
├── .gitignore
└── README.md
```

### Evaluation Criteria

| Category | Criteria | Weight |
|----------|----------|--------|
| **Functionality** | All features working | 25% |
| **Code Quality** | Clean, documented, tested | 25% |
| **Architecture** | Proper separation, patterns | 20% |
| **Security** | Auth, validation, best practices | 15% |
| **Deployment** | Production-ready, documented | 15% |

---

## Course Summary

### Learning Path

```
Week 1-2: Foundation (Flask Basics)
    ↓
Week 3: Data Persistence (SQLAlchemy)
    ↓
Week 4: Quality Assurance (Testing)
    ↓
Week 5: Modern APIs (FastAPI)
    ↓
Week 6: Frontend Integration (JS + HTMX)
    ↓
Week 7: Production Readiness (Docker + CI/CD)
    ↓
Week 8: Integration (Full SaaS)
```

### Skill Progression

| Week | Skills Gained |
|------|---------------|
| 1 | HTTP, REST, Flask basics |
| 2 | Templates, Forms, Auth, Blueprints |
| 3 | Database design, ORM, Migrations |
| 4 | Testing strategies, Mocking, Coverage |
| 5 | FastAPI, Pydantic, Async, DI |
| 6 | JavaScript, HTMX, Frontend integration |
| 7 | Docker, Deployment, Monitoring |
| 8 | Full-stack development, Production systems |

### Project Portfolio

Upon completion, students will have built:

1. **Personal Blog** - Traditional server-rendered app
2. **Task Manager** - Database-driven CRUD app
3. **Tested API Service** - Fully tested REST API
4. **High-Performance API** - Async FastAPI service
5. **Interactive Dashboard** - Data visualization
6. **Containerized App** - Production-ready deployment
7. **SaaS Application** - Multi-tenant collaboration tool

### Next Steps

After completing this course:
- **Specialize**: Django, React/Vue, DevOps, Data Engineering
- **Build**: Portfolio projects, Open source contributions
- **Career**: Junior to Mid-level web developer roles
- **Continue**: Microservices, GraphQL, Real-time systems

---

## Appendix A: Daily Exercise Template

Each day follows this structure:

```markdown
# Day X: Topic Name

## Learning Objectives
- Objective 1
- Objective 2

## Theory (20-30 minutes)
Explanations, code examples, common pitfalls

## Exercises (10 problems)
1. `problem_01_name.py` - Concept focus
2. ...
10. `problem_10_name.py` - Advanced concept

## Running Tests
```bash
pytest week0X/tests/day0X/ -v
```

## Solutions
Available in `week0X/solutions/day0X/`
```

## Appendix B: Project Template

Each weekly project includes:

```
project/
├── README.md              # Requirements & specs
├── SETUP.md              # Setup instructions
├── starter/              # Skeleton code
│   └── *.py
├── reference_solution/   # Complete solution
│   └── *.py
└── tests/                # Project tests
    └── test_*.py
```

## Appendix C: Recommended Resources

### Books
- "Flask Web Development" by Miguel Grinberg
- "Architecture Patterns with Python" by Harry Percival
- "Robust Python" by Patrick Viafore

### Documentation
- Flask: flask.palletsprojects.com
- FastAPI: fastapi.tiangolo.com
- SQLAlchemy: docs.sqlalchemy.org
- HTMX: htmx.org

### Tools
- httpie: CLI HTTP client
- Postman: API testing
- TablePlus: Database GUI
- Docker Desktop: Container management

---

*This course outline follows the pedagogical structure established in the Python OOP Journey, maintaining consistency in daily problem sets, comprehensive testing, and progressive project complexity.*
