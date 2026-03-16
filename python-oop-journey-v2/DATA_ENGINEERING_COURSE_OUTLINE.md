# Python for Data Engineering - Course Outline

A comprehensive 8-week course following the Python OOP Journey, designed to transform Python developers into data engineers capable of building production-grade data pipelines.

---

## Course Overview

| Attribute | Details |
|-----------|---------|
| **Duration** | 8 weeks (48 days) |
| **Difficulty** | Intermediate to Advanced |
| **Prerequisites** | Python OOP Journey completion or equivalent |
| **Total Exercises** | ~350 |
| **Total Tests** | ~400 |
| **Weekly Projects** | 8 |
| **Capstone** | End-to-end analytics platform |

---

## Prerequisites (From OOP Journey)

Students should be proficient in:

- **Python Fundamentals**: Variables, data types, control flow, functions
- **Data Structures**: Lists, dictionaries, sets, tuples
- **Object-Oriented Programming**: Classes, inheritance, polymorphism, composition
- **Testing**: pytest, unit testing, test-driven development
- **Project Structure**: Package organization, imports, virtual environments
- **Functional Programming**: Comprehensions, generators, higher-order functions
- **Error Handling**: Exceptions, defensive programming
- **File I/O**: JSON, CSV, text processing

---

## Tooling Requirements

### Core Development Stack

| Tool | Purpose | Version |
|------|---------|---------|
| Python | Primary language | 3.11+ |
| Docker | Containerization | 24.0+ |
| Docker Compose | Multi-service orchestration | 2.20+ |
| PostgreSQL | Relational database | 15+ |
| MongoDB | Document database | 7.0+ |
| Redis | Caching & message broker | 7.0+ |

### Python Libraries

| Category | Libraries |
|----------|-----------|
| **Data Processing** | pandas, polars, pyarrow, numpy |
| **Databases** | psycopg2, SQLAlchemy, pymongo, redis-py |
| **Orchestration** | apache-airflow |
| **Streaming** | kafka-python, confluent-kafka |
| **Big Data** | pyspark, py4j |
| **Data Quality** | pandera, great_expectations |
| **Transformation** | dbt-core |
| **Testing** | pytest, pytest-docker, moto |
| **CLI/Config** | click, pydantic, python-dotenv |

### Infrastructure (Local Development)

- Docker Desktop or equivalent
- 8GB+ RAM recommended
- 20GB+ free disk space

---

## Weekly Breakdown

---

## Week 1: Data Engineering Fundamentals & Environment

**Week Goal**: Establish a production-ready development environment and understand core data engineering concepts.

**Theme**: "From Scripts to Pipelines"

### Learning Objectives

1. Understand the data engineering lifecycle
2. Set up containerized development environments
3. Differentiate ETL vs ELT paradigms
4. Learn data pipeline architecture patterns
5. Implement basic data ingestion patterns

### Day-by-Day Breakdown

#### Day 1: Introduction to Data Engineering

**Theory**: `day01_de_intro.md`

- What is Data Engineering?
- The modern data stack
- Data engineer vs Data scientist vs Data analyst
- Data lifecycle: ingestion, storage, processing, serving
- Batch vs streaming processing

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_data_pipeline_stages.py` | Pipeline stages identification | Easy |
| 02 | `problem_02_batch_vs_streaming.py` | Processing paradigm comparison | Easy |
| 03 | `problem_03_data_quality_dimensions.py` | Data quality (accuracy, completeness) | Easy |
| 04 | `problem_04_latency_requirements.py` | Latency classification | Medium |
| 05 | `problem_05_storage_tier_selection.py` | Hot/warm/cold storage | Medium |
| 06 | `problem_06_pipeline_orchestration_flow.py` | Task dependency modeling | Medium |
| 07 | `problem_07_data_lineage_tracking.py` | Lineage basics | Hard |
| 08 | `problem_08_sla_calculator.py` | SLA breach detection | Hard |

#### Day 2: Docker for Data Engineers

**Theory**: `day02_docker_for_de.md`

- Containerization fundamentals
- Docker images vs containers
- Dockerfile best practices for data workloads
- Docker Compose for multi-service stacks
- Volume mounting for data persistence

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_dockerfile_parser.py` | Dockerfile instruction parsing | Easy |
| 02 | `problem_02_container_health_check.py` | Health check logic | Easy |
| 03 | `problem_03_image_layer_optimizer.py` | Layer optimization analysis | Medium |
| 04 | `problem_04_compose_service_dependency.py` | Service startup order | Medium |
| 05 | `problem_05_volume_mount_validator.py` | Volume configuration validation | Medium |
| 06 | `problem_06_container_resource_limits.py` | Resource constraint parsing | Medium |
| 07 | `problem_07_multi_stage_build_analyzer.py` | Multi-stage Dockerfile analysis | Hard |
| 08 | `problem_08_container_network_isolation.py` | Network segmentation logic | Hard |

#### Day 3: Virtual Environments & Dependency Management

**Theory**: `day03_envs_and_deps.md`

- Python virtual environments (venv, conda, poetry)
- Requirements.txt vs pyproject.toml
- Dependency resolution and conflicts
- Environment reproducibility
- Lock files and deterministic builds

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_requirements_parser.py` | Parse requirements format | Easy |
| 02 | `problem_02_version_constraint_checker.py` | SemVer constraint validation | Easy |
| 03 | `problem_03_dependency_tree_builder.py` | Simple dependency resolution | Medium |
| 04 | `problem_04_environment_diff_analyzer.py` | Compare environment states | Medium |
| 05 | `problem_05_lock_file_generator.py` | Generate dependency locks | Medium |
| 06 | `problem_06_conflict_detector.py` | Detect version conflicts | Medium |
| 07 | `problem_07_transitive_dependency_resolver.py` | Full dependency graph | Hard |
| 08 | `problem_08_environment_reproducibility_score.py` | Reproducibility metrics | Hard |

#### Day 4: ETL vs ELT & Pipeline Patterns

**Theory**: `day04_etl_vs_elt.md`

- Extract-Transform-Load (ETL) patterns
- Extract-Load-Transform (ELT) patterns
- When to use each approach
- Data pipeline design patterns
- Idempotency and rerunnability

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_etl_pipeline_designer.py` | ETL flow design | Easy |
| 02 | `problem_02_elt_pipeline_designer.py` | ELT flow design | Easy |
| 03 | `problem_03_pipeline_pattern_selector.py` | Pattern selection logic | Medium |
| 04 | `problem_04_idempotency_checker.py` | Idempotent operation design | Medium |
| 05 | `problem_05_incremental_load_strategy.py` | Incremental extraction | Medium |
| 06 | `problem_06_scd_type_implementation.py` | Slowly Changing Dimensions | Medium |
| 07 | `problem_07_data_partitioning_strategy.py` | Partition scheme design | Hard |
| 08 | `problem_08_pipeline_rollback_planner.py` | Rollback strategy design | Hard |

#### Day 5: Data Formats & Serialization

**Theory**: `day05_data_formats.md`

- CSV, JSON, Parquet, Avro, ORC
- Schema evolution
- Compression algorithms
- Format selection criteria
- Binary vs text formats

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_csv_schema_inferencer.py` | CSV type inference | Easy |
| 02 | `problem_02_json_validator.py` | JSON Schema validation | Easy |
| 03 | `problem_03_parquet_metadata_reader.py` | Parquet metadata extraction | Medium |
| 04 | `problem_04_format_converter.py` | Format conversion logic | Medium |
| 05 | `problem_05_compression_selector.py` | Compression algorithm choice | Medium |
| 06 | `problem_06_schema_evolution_detector.py` | Schema change detection | Medium |
| 07 | `problem_07_columnar_vs_row_storage.py` | Storage layout analysis | Hard |
| 08 | `problem_08_format_optimization_advisor.py` | Format recommendation engine | Hard |

#### Day 6: Data Ingestion Patterns

**Theory**: `day06_ingestion_patterns.md`

- Full loads vs incremental loads
- Change Data Capture (CDC)
- API pagination and rate limiting
- File-based ingestion
- Database replication basics

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_full_load_calculator.py` | Full load resource estimation | Easy |
| 02 | `problem_02_incremental_extractor.py` | Incremental extraction logic | Easy |
| 03 | `problem_03_api_paginator.py` | Pagination handling | Medium |
| 04 | `problem_04_rate_limit_handler.py` | Rate limiting with backoff | Medium |
| 05 | `problem_05_cdc_event_parser.py` | CDC event processing | Medium |
| 06 | `problem_06_file_watcher_pattern.py` | File system monitoring | Medium |
| 07 | `problem_07_watermark_tracker.py` | High-water mark tracking | Hard |
| 08 | `problem_08_ingestion_orchestrator.py` | Multi-source ingestion coord | Hard |

### Week 1 Project: Database Migration Tool

**Project Directory**: `project/`

**Overview**: Build a CLI tool that migrates data between different storage systems (CSV to PostgreSQL, JSON to MongoDB) with schema validation and progress tracking.

**Features**:
- Source connectors (CSV, JSON, API)
- Destination connectors (PostgreSQL, MongoDB, Parquet files)
- Schema validation and transformation
- Batch processing with progress bars
- Error handling and resume capability
- Docker Compose setup for databases

**Estimated Tests**: 50 tests

---

## Week 2: Working with Databases (SQL & NoSQL)

**Week Goal**: Master database interactions, connection management, and schema design for analytics workloads.

**Theme**: "Data Persistence Foundations"

### Learning Objectives

1. Connect to PostgreSQL using psycopg2 and SQLAlchemy
2. Design schemas for analytical queries
3. Work with MongoDB for document storage
4. Implement connection pooling
5. Write efficient SQL for data engineering
6. Understand ACID vs BASE trade-offs

### Day-by-Day Breakdown

#### Day 1: PostgreSQL Fundamentals

**Theory**: `day01_postgresql_basics.md`

- PostgreSQL architecture for DE
- psycopg2 basics
- Parameterized queries
- Transactions and isolation levels
- COPY command for bulk operations

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_connection_factory.py` | Connection creation patterns | Easy |
| 02 | `problem_02_safe_query_builder.py` | SQL injection prevention | Easy |
| 03 | `problem_03_transaction_manager.py` | Transaction context manager | Medium |
| 04 | `problem_04_bulk_copy_wrapper.py` | COPY command wrapper | Medium |
| 05 | `problem_05_isolation_level_selector.py` | Isolation level selection | Medium |
| 06 | `problem_06_upsert_implementation.py` | INSERT ON CONFLICT | Medium |
| 07 | `problem_07_partition_manager.py` | Table partition automation | Hard |
| 08 | `problem_08_query_performance_analyzer.py` | EXPLAIN plan parsing | Hard |

#### Day 2: SQLAlchemy ORM & Core

**Theory**: `day02_sqlalchemy.md`

- SQLAlchemy Core vs ORM
- Engine configuration
- Session management
- Declarative models
- Alembic migrations basics

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_engine_factory.py` | Engine configuration | Easy |
| 02 | `problem_02_session_context_manager.py` | Session lifecycle | Easy |
| 03 | `problem_03_declarative_model_builder.py` | Model definition | Medium |
| 04 | `problem_04_query_builder_pattern.py` | Dynamic query building | Medium |
| 05 | `problem_05_bulk_insert_optimizer.py` | Batch insert optimization | Medium |
| 06 | `problem_06_relationship_loader.py` | Eager vs lazy loading | Medium |
| 07 | `problem_07_migration_generator.py` | Schema change detection | Hard |
| 08 | `problem_08_connection_pool_monitor.py` | Pool statistics tracking | Hard |

#### Day 3: Database Design for Analytics

**Theory**: `day03_analytics_schema_design.md`

- Normalization vs denormalization
- Star and snowflake schemas
- Fact and dimension tables
- Indexing strategies
- Columnar considerations

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_normalization_analyzer.py` | Normal form detection | Easy |
| 02 | `problem_02_star_schema_builder.py` | Star schema generation | Easy |
| 03 | `problem_03_fact_table_designer.py` | Fact table structure | Medium |
| 04 | `problem_04_dimension_table_designer.py` | Dimension table patterns | Medium |
| 05 | `problem_05_index_recommendation_engine.py` | Index suggestions | Medium |
| 06 | `problem_06_materialized_view_planner.py` | MV design logic | Medium |
| 07 | `problem_07_query_optimization_advisor.py` | Query tuning advice | Hard |
| 08 | `problem_08_schema_benchmark_generator.py` | Schema performance testing | Hard |

#### Day 4: MongoDB & Document Databases

**Theory**: `day04_mongodb_basics.md`

- Document model vs relational
- pymongo fundamentals
- CRUD operations
- Aggregation pipeline
- Schema design patterns

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_mongo_connection_manager.py` | Connection handling | Easy |
| 02 | `problem_02_document_validator.py` | Schema validation | Easy |
| 03 | `problem_03_aggregation_builder.py` | Pipeline construction | Medium |
| 04 | `problem_04_embedded_vs_reference.py` | Relationship modeling | Medium |
| 05 | `problem_05_change_stream_processor.py` | Real-time change feeds | Medium |
| 06 | `problem_06_sharding_key_selector.py` | Sharding strategy | Medium |
| 07 | `problem_07_compound_index_optimizer.py` | Index optimization | Hard |
| 08 | `problem_08_mongo_migration_tool.py` | Data migration logic | Hard |

#### Day 5: Connection Pooling & Performance

**Theory**: `day05_connection_pooling.md`

- Why connection pooling matters
- Pool configuration parameters
- Connection lifecycle
- Monitoring and tuning
- Circuit breaker patterns

**Exercises (7)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_pool_configuration_calculator.py` | Pool sizing | Easy |
| 02 | `problem_02_connection_lifecycle_tracker.py` | Connection states | Easy |
| 03 | `problem_03_pool_exhaustion_handler.py` | Overflow handling | Medium |
| 04 | `problem_04_circuit_breaker_impl.py` | Circuit breaker pattern | Medium |
| 05 | `problem_05_retry_with_backoff.py` | Retry strategies | Medium |
| 06 | `problem_06_pool_metrics_collector.py` | Performance metrics | Hard |
| 07 | `problem_07_database_failover_manager.py` | Failover logic | Hard |

#### Day 6: Advanced SQL for Data Engineering

**Theory**: `day06_advanced_sql.md`

- Window functions
- CTEs and recursive queries
- Pivot/unpivot operations
- Time-series analysis in SQL
- Query optimization techniques

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_window_function_generator.py` | Window clause builder | Easy |
| 02 | `problem_02_cte_query_builder.py` | CTE construction | Easy |
| 03 | `problem_03_running_total_calculator.py` | Running calculations | Medium |
| 04 | `problem_04_moving_average_engine.py` | Moving averages | Medium |
| 05 | `problem_05_pivot_table_generator.py` | Pivot operations | Medium |
| 06 | `problem_06_gap_filling_strategy.py` | Time-series gaps | Medium |
| 07 | `problem_07_recursive_hierarchy_query.py` | Tree traversals | Hard |
| 08 | `problem_08_sql_optimization_analyzer.py` | Query rewrite suggestions | Hard |

### Week 2 Project: Database Migration Tool v2

**Project Directory**: `project/`

**Overview**: Extend Week 1's migration tool with advanced database features.

**New Features**:
- PostgreSQL-specific optimizations (COPY, partitioning)
- MongoDB as a source/destination
- Schema transformation rules engine
- Connection pooling integration
- Performance benchmarking
- Migration validation and checksums

**Estimated Tests**: 55 tests

---

## Week 3: Data Processing with Pandas & Polars

**Week Goal**: Master efficient data manipulation with modern DataFrame libraries.

**Theme**: "The DataFrame Arsenal"

### Learning Objectives

1. Efficient pandas operations for large datasets
2. Memory optimization techniques
3. Polars for high-performance processing
4. Chunking strategies for big data
5. Data validation with Pandera
6. Arrow as a common data format

### Day-by-Day Breakdown

#### Day 1: Pandas Fundamentals for DE

**Theory**: `day01_pandas_for_de.md`

- pandas architecture and dtypes
- Vectorized operations
- Indexing and selection
- GroupBy operations
- Merge and join strategies

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_dtype_optimizer.py` | Automatic dtype optimization | Easy |
| 02 | `problem_02_memory_usage_calculator.py` | Memory profiling | Easy |
| 03 | `problem_03_vectorized_transform.py` | Vectorized operations | Medium |
| 04 | `problem_04_efficient_groupby.py` | GroupBy optimization | Medium |
| 05 | `problem_05_merge_strategy_selector.py` | Join algorithm selection | Medium |
| 06 | `problem_06_pivot_optimization.py` | Pivot performance | Medium |
| 07 | `problem_07_time_series_resampler.py` | Time-based aggregation | Hard |
| 08 | `problem_08_multiindex_manager.py` | Hierarchical indexing | Hard |

#### Day 2: Memory Optimization & Chunking

**Theory**: `day02_memory_optimization.md`

- Understanding pandas memory usage
- Category dtype for strings
- Downcasting numeric types
- Working with large files in chunks
- Iterator patterns

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_category_converter.py` | String to categorical | Easy |
| 02 | `problem_02_numeric_downcaster.py` | Integer/float optimization | Easy |
| 03 | `problem_03_chunk_size_calculator.py` | Optimal chunk sizing | Medium |
| 04 | `problem_04_chunked_processor.py` | Chunk processing pattern | Medium |
| 05 | `problem_05_lazy_evaluation_simulator.py` | Lazy computation | Medium |
| 06 | `problem_06_memory_mapping_handler.py` | Memory-mapped files | Medium |
| 07 | `problem_07_out_of_core_strategy.py` | Out-of-core processing | Hard |
| 08 | `problem_08_memory_profiler_pipeline.py` | Pipeline memory tracking | Hard |

#### Day 3: Polars for High Performance

**Theory**: `day03_polars_intro.md`

- Polars vs pandas architecture
- Lazy API and query optimization
- Expression API
- Streaming mode
- When to use Polars

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_polars_expression_builder.py` | Expression construction | Easy |
| 02 | `problem_02_lazy_query_planner.py` | Query plan analysis | Easy |
| 03 | `problem_03_polars_groupby_optimizer.py` | Optimized aggregations | Medium |
| 04 | `problem_04_window_function_polars.py` | Window expressions | Medium |
| 05 | `problem_05_streaming_mode_handler.py` | Large dataset streaming | Medium |
| 06 | `problem_06_polars_pandas_bridge.py` | Interoperability | Medium |
| 07 | `problem_07_query_plan_optimizer.py` | Plan optimization hints | Hard |
| 08 | `problem_08_polars_udf_manager.py` | Custom functions | Hard |

#### Day 4: Data Validation with Pandera

**Theory**: `day04_data_validation.md`

- Schema validation importance
- Pandera DataFrameSchema
- Validation strategies (lazy vs eager)
- Custom validators
- Statistical validation

**Exercises (7)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_schema_definition_builder.py` | Schema construction | Easy |
| 02 | `problem_02_dtype_validator.py` | Type validation | Easy |
| 03 | `problem_03_range_constraint_validator.py` | Numeric constraints | Medium |
| 04 | `problem_04_regex_pattern_validator.py` | String patterns | Medium |
| 05 | `problem_05_nullable_strategy.py` | Null handling rules | Medium |
| 06 | `problem_06_custom_check_factory.py` | Custom validation logic | Hard |
| 07 | `problem_07_validation_report_generator.py` | Error reporting | Hard |

#### Day 5: Data Cleaning & Transformation

**Theory**: `day05_data_cleaning.md`

- Handling missing data
- Outlier detection
- Data type coercion
- Standardization and normalization
- Duplicate detection and removal

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_missing_value_strategy.py` | Imputation strategies | Easy |
| 02 | `problem_02_outlier_detector.py` | Statistical outlier detection | Easy |
| 03 | `problem_03_type_coercion_engine.py` | Safe type conversion | Medium |
| 04 | `problem_04_standardization_pipeline.py` | Z-score normalization | Medium |
| 05 | `problem_05_duplicate_detector.py` | Fuzzy deduplication | Medium |
| 06 | `problem_06_data_quality_profiler.py` | Quality metrics | Medium |
| 07 | `problem_07_schema_drift_detector.py` | Schema change detection | Hard |
| 08 | `problem_08_cleaning_pipeline_orchestrator.py` | Pipeline composition | Hard |

#### Day 6: Apache Arrow Integration

**Theory**: `day06_apache_arrow.md`

- Arrow columnar format
- Zero-copy data sharing
- Arrow Flight basics
- Interoperability ecosystem
- Future of dataframes

**Exercises (7)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_arrow_schema_builder.py` | Arrow schema construction | Easy |
| 02 | `problem_02_zero_copy_converter.py` | Memory-efficient conversion | Easy |
| 03 | `problem_03_arrow_recordbatch_processor.py` | Batch processing | Medium |
| 04 | `problem_04_arrow_ipc_handler.py` | IPC format handling | Medium |
| 05 | `problem_05_arrow_parquet_bridge.py` | Parquet integration | Medium |
| 06 | `problem_06_flight_client_simulator.py` | Flight protocol basics | Hard |
| 07 | `problem_07_cross_library_serializer.py` | Universal serialization | Hard |

### Week 3 Project: Data Cleaning Pipeline

**Project Directory**: `project/`

**Overview**: Build a configurable data cleaning pipeline that processes messy real-world datasets with validation, transformation, and quality reporting.

**Features**:
- Pluggable cleaning steps
- Pandera schema validation integration
- Memory-optimized processing (Polars for large files)
- Data quality dashboard generation
- Config-driven transformations (YAML/JSON)
- Profiling and statistics output
- Parallel processing for large datasets

**Estimated Tests**: 50 tests

---

## Week 4: Workflow Orchestration (Apache Airflow)

**Week Goal**: Build production-grade data pipelines with Apache Airflow.

**Theme**: "The Conductor's Baton"

### Learning Objectives

1. Understand DAG design principles
2. Create tasks and dependencies
3. Use sensors and operators effectively
4. Implement error handling and retries
5. Manage pipeline state and XComs
6. Monitor and alert on pipeline health

### Day-by-Day Breakdown

#### Day 1: Airflow Fundamentals

**Theory**: `day01_airflow_basics.md`

- Airflow architecture (Scheduler, Worker, Webserver, Metadata DB)
- DAG definition and scheduling
- Task lifecycle
- Backfilling and catchup
- Airflow CLI basics

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_dag_structure_validator.py` | DAG syntax validation | Easy |
| 02 | `problem_02_cron_expression_parser.py` | Schedule parsing | Easy |
| 03 | `problem_03_task_dependency_builder.py` | Dependency graph construction | Medium |
| 04 | `problem_04_dag_cycle_detector.py` | Cycle detection | Medium |
| 05 | `problem_05_execution_date_calculator.py` | Execution date logic | Medium |
| 06 | `problem_06_backfill_planner.py` | Backfill scheduling | Medium |
| 07 | `problem_07_dag_partitioning_strategy.py` | DAG organization | Hard |
| 08 | `problem_08_dynamic_dag_generator.py` | Dynamic DAG creation | Hard |

#### Day 2: Operators & Tasks

**Theory**: `day02_operators.md`

- Operator types (Python, Bash, SQL)
- TaskFlow API vs traditional
- Custom operators
- Task groups
- Task execution context

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_python_callable_wrapper.py` | Python operator patterns | Easy |
| 02 | `problem_02_bash_command_templater.py` | Bash templating | Easy |
| 03 | `problem_03_sql_operator_builder.py` | SQL operator construction | Medium |
| 04 | `problem_04_custom_operator_skeleton.py` | Custom operator base | Medium |
| 05 | `problem_05_task_group_organizer.py` | Task grouping | Medium |
| 06 | `problem_06_branching_logic_impl.py` | BranchPythonOperator | Medium |
| 07 | `problem_07_dynamic_task_mapping.py` | Dynamic task generation | Hard |
| 08 | `problem_08_cross_dag_dependency.py` | DAG dependencies | Hard |

#### Day 3: Sensors & External Triggers

**Theory**: `day03_sensors.md`

- Sensor patterns and modes (poke vs reschedule)
- File sensors
- SQL sensors
- External task sensors
- Deferrable operators

**Exercises (7)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_sensor_mode_selector.py` | Poke vs reschedule | Easy |
| 02 | `problem_02_file_sensor_logic.py` | File detection | Easy |
| 03 | `problem_03_sql_sensor_impl.py` | SQL condition checking | Medium |
| 04 | `problem_04_external_task_sensor.py` | Cross-DAG sensing | Medium |
| 05 | `problem_05_timeout_handler.py` | Sensor timeout logic | Medium |
| 06 | `problem_06_deferrable_operator_base.py` | Async operator patterns | Hard |
| 07 | `problem_07_smart_sensor_orchestrator.py` | Sensor optimization | Hard |

#### Day 4: Error Handling & Retries

**Theory**: `day04_error_handling.md`

- Retry policies and backoff
- Failure callbacks
- SLA monitoring
- Alerting mechanisms
- Circuit breakers in pipelines

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_retry_policy_calculator.py` | Retry configuration | Easy |
| 02 | `problem_02_exponential_backoff_impl.py` | Backoff strategies | Easy |
| 03 | `problem_03_failure_callback_handler.py` | Error callbacks | Medium |
| 04 | `problem_04_sla_breach_detector.py` | SLA monitoring | Medium |
| 05 | `problem_05_alert_notification_builder.py` | Alert formatting | Medium |
| 06 | `problem_06_circuit_breaker_task.py` | Failure isolation | Medium |
| 07 | `problem_07_dead_letter_queue_impl.py` | Error routing | Hard |
| 08 | `problem_08_graceful_degradation_planner.py` | Fallback strategies | Hard |

#### Day 5: XComs & Data Sharing

**Theory**: `day05_xcoms.md`

- XCom architecture
- Pushing and pulling data
- XCom backends
- Large data handling
- TaskFlow API and XComs

**Exercises (7)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_xcom_push_pull_pattern.py` | Basic XCom usage | Easy |
| 02 | `problem_02_xcom_backend_selector.py` | Backend selection | Easy |
| 03 | `problem_03_large_xcom_handler.py` | Big data strategies | Medium |
| 04 | `problem_04_taskflow_data_passing.py` | TaskFlow patterns | Medium |
| 05 | `problem_05_xcom_cleanup_strategy.py` | Data retention | Medium |
| 06 | `problem_06_cross_dag_xcom_sharing.py` | Inter-DAG communication | Hard |
| 07 | `problem_07_xcom_performance_optimizer.py` | Optimization strategies | Hard |

#### Day 6: Monitoring & Observability

**Theory**: `day06_airflow_monitoring.md`

- Metrics and statsd
- Logging configuration
- UI-based monitoring
- Programmatic monitoring
- Performance tuning

**Exercises (7)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_metrics_collector.py` | Custom metrics | Easy |
| 02 | `problem_02_log_parser_analyzer.py` | Log analysis | Easy |
| 03 | `problem_03_dag_run_reporter.py` | Run status reporting | Medium |
| 04 | `problem_04_performance_profiler.py` | Task profiling | Medium |
| 05 | `problem_05_resource_usage_tracker.py` | Resource monitoring | Medium |
| 06 | `problem_06_cost_estimator.py` | Infrastructure costs | Hard |
| 07 | `problem_07_health_check_orchestrator.py` | System health | Hard |

### Week 4 Project: Automated Reporting DAG

**Project Directory**: `project/`

**Overview**: Build a production Airflow DAG that extracts data from multiple sources, transforms it, and generates automated reports with email delivery.

**Features**:
- Multi-source extraction (DB, API, files)
- Data transformation and validation
- Report generation (HTML, PDF, CSV)
- Email distribution with SMTP
- Error handling with retries and alerts
- SLA monitoring
- Configurable schedule and parameters
- Unit tests for DAG logic

**Estimated Tests**: 45 tests

---

## Week 5: Streaming Data (Apache Kafka)

**Week Goal**: Understand stream processing and build real-time data pipelines with Kafka.

**Theme**: "The Flow of Data"

### Learning Objectives

1. Understand streaming vs batch processing
2. Implement producer/consumer patterns
3. Design Kafka topics and partitions
4. Handle message delivery semantics
5. Build stream processing applications
6. Manage consumer groups and rebalancing

### Day-by-Day Breakdown

#### Day 1: Streaming Concepts

**Theory**: `day01_streaming_fundamentals.md`

- Stream vs batch processing
- Event-driven architecture
- Time concepts (event time, processing time)
- Windowing strategies
- Stream processing frameworks overview

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_stream_vs_batch_analyzer.py` | Processing paradigm comparison | Easy |
| 02 | `problem_02_event_time_extractor.py` | Timestamp handling | Easy |
| 03 | `problem_03_windowing_strategy_selector.py` | Window type selection | Medium |
| 04 | `problem_04_tumbling_window_calculator.py` | Fixed windows | Medium |
| 05 | `problem_05_sliding_window_calculator.py` | Overlapping windows | Medium |
| 06 | `problem_06_session_window_detector.py` | Session gap detection | Medium |
| 07 | `problem_07_late_data_handler.py` | Watermark and lateness | Hard |
| 08 | `problem_08_stream_join_planner.py` | Stream-stream joins | Hard |

#### Day 2: Kafka Architecture

**Theory**: `day02_kafka_architecture.md`

- Kafka ecosystem (Brokers, Topics, Partitions)
- Replication and ISR
- Producer internals
- Consumer groups
- Log compaction

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_partition_calculator.py` | Partition count planning | Easy |
| 02 | `problem_02_replication_factor_validator.py` | Replication configuration | Easy |
| 03 | `problem_03_isr_availability_checker.py` | ISR management | Medium |
| 04 | `problem_04_leader_election_simulator.py` | Leader failover | Medium |
| 05 | `problem_05_log_retention_planner.py` | Retention policies | Medium |
| 06 | `problem_06_compaction_strategy_impl.py` | Log compaction | Medium |
| 07 | `problem_07_partition_reassignment_planner.py` | Rebalancing | Hard |
| 08 | `problem_08_kafka_cluster_sizer.py` | Capacity planning | Hard |

#### Day 3: Kafka Producers

**Theory**: `day03_kafka_producers.md`

- Producer configuration
- Serialization (Avro, JSON, Protobuf)
- Message keys and partitioning
- Acknowledgment levels
- Idempotent producers

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_producer_config_validator.py` | Configuration validation | Easy |
| 02 | `problem_02_partition_key_selector.py` | Key-based routing | Easy |
| 03 | `problem_03_avro_serializer_impl.py` | Avro serialization | Medium |
| 04 | `problem_04_ack_level_selector.py` | Durability trade-offs | Medium |
| 05 | `problem_05_batch_size_optimizer.py` | Batch optimization | Medium |
| 06 | `problem_06_idempotent_producer_impl.py` | Exactly-once semantics | Medium |
| 07 | `problem_07_transactional_producer.py` | Transaction support | Hard |
| 08 | `problem_08_producer_performance_tuner.py` | Throughput optimization | Hard |

#### Day 4: Kafka Consumers

**Theory**: `day04_kafka_consumers.md`

- Consumer configuration
- Offset management
- Consumer group rebalancing
- Manual vs automatic commits
- Seeking and replay

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_consumer_config_validator.py` | Configuration validation | Easy |
| 02 | `problem_02_offset_commit_strategy.py` | Commit strategies | Easy |
| 03 | `problem_03_rebalance_listener_impl.py` | Rebalance handling | Medium |
| 04 | `problem_04_consumer_lag_calculator.py` | Lag monitoring | Medium |
| 05 | `problem_05_dead_letter_topic_impl.py` | Error handling | Medium |
| 06 | `problem_06_exactly_once_consumer.py` | EOS implementation | Medium |
| 07 | `problem_07_partition_assignment_strategy.py` | Custom assignors | Hard |
| 08 | `problem_08_consumer_group_coordinator.py` | Group management | Hard |

#### Day 5: Stream Processing with Kafka

**Theory**: `day05_stream_processing.md`

- Kafka Streams concepts
- Stateless vs stateful processing
- KTables and KStreams
- Joins and aggregations
- Interactive queries

**Exercises (7)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_stream_topology_builder.py` | Topology design | Easy |
| 02 | `problem_02_state_store_manager.py` | Local state management | Easy |
| 03 | `problem_03_stream_aggregation_impl.py` | Aggregation patterns | Medium |
| 04 | `problem_04_stream_table_join.py` | Stream-table joins | Medium |
| 05 | `problem_05_stream_stream_join.py` | Stream-stream joins | Medium |
| 06 | `problem_06_windowed_aggregation.py` | Time-windowed ops | Hard |
| 07 | `problem_07_interactive_query_handler.py` | Query serving | Hard |

#### Day 6: Real-World Kafka Patterns

**Theory**: `day06_kafka_patterns.md`

- Event sourcing
- CQRS with Kafka
- Schema Registry integration
- Multi-datacenter replication
- Security (SASL/SSL)

**Exercises (7)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_event_sourcing_pattern.py` | Event store design | Easy |
| 02 | `problem_02_schema_registry_client.py` | Schema evolution | Easy |
| 03 | `problem_03_cqrs_read_model_updater.py` | CQRS implementation | Medium |
| 04 | `problem_04_mirrormaker_configurator.py` | Cross-DC replication | Medium |
| 05 | `problem_05_sasl_ssl_config_builder.py` | Security configuration | Medium |
| 06 | `problem_06_kafka_connect_integration.py` | Connect framework | Hard |
| 07 | `problem_07_kafka_ksql_planner.py` | KSQL design | Hard |

### Week 5 Project: Real-Time Log Processor

**Project Directory**: `project/`

**Overview**: Build a real-time log processing pipeline that ingests application logs, processes them, and generates alerts for anomalies.

**Features**:
- Log producer (simulating application logs)
- Kafka topic design (raw, processed, alerts)
- Log parsing and enrichment
- Anomaly detection (rate thresholds, error patterns)
- Alert generation and routing
- Real-time dashboard metrics
- Exactly-once processing guarantees
- Consumer group scaling

**Estimated Tests**: 45 tests

---

## Week 6: Big Data Processing (Spark with PySpark)

**Week Goal**: Process large-scale datasets using Apache Spark and PySpark.

**Theme**: "Taming the Data Ocean"

### Learning Objectives

1. Understand Spark architecture and execution model
2. Work with RDDs, DataFrames, and Datasets
3. Optimize Spark jobs for performance
4. Handle distributed data processing challenges
5. Implement ETL pipelines with Spark
6. Understand Spark SQL and Catalyst optimizer

### Day-by-Day Breakdown

#### Day 1: Spark Architecture

**Theory**: `day01_spark_architecture.md`

- Spark ecosystem overview
- Driver, Executors, and Cluster Manager
- RDD lineage and DAG execution
- Shuffle operations
- Storage levels and caching

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_spark_job_analyzer.py` | Job stage identification | Easy |
| 02 | `problem_02_executor_sizing_calculator.py` | Resource allocation | Easy |
| 03 | `problem_03_dag_visualization_parser.py` | Execution plan parsing | Medium |
| 04 | `problem_04_shuffle_operation_detector.py` | Shuffle analysis | Medium |
| 05 | `problem_05_storage_level_selector.py` | Persistence strategies | Medium |
| 06 | `problem_06_partition_tuner.py` | Partition optimization | Medium |
| 07 | `problem_07_broadcast_hint_optimizer.py` | Broadcast join tuning | Hard |
| 08 | `problem_08_spark_ui_metrics_parser.py` | Performance metrics | Hard |

#### Day 2: PySpark DataFrames

**Theory**: `day02_pyspark_dataframes.md`

- DataFrame API vs RDDs
- Schema inference and definition
- Transformations and actions
- Column operations and expressions
- UDFs and vectorized UDFs (Pandas UDFs)

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_schema_validator.py` | Schema validation | Easy |
| 02 | `problem_02_column_expression_builder.py` | Column operations | Easy |
| 03 | `problem_03_transformation_chain_optimizer.py` | Lazy evaluation | Medium |
| 04 | `problem_04_window_function_pyspark.py` | Window operations | Medium |
| 05 | `problem_05_udf_vs_pandas_udf_selector.py` | UDF selection | Medium |
| 06 | `problem_06_pandas_udf_impl.py` | Vectorized UDFs | Medium |
| 07 | `problem_07_complex_type_handler.py` | Arrays, Maps, Structs | Hard |
| 08 | `problem_08_catalyst_optimizer_explainer.py` | Query optimization | Hard |

#### Day 3: Spark SQL

**Theory**: `day03_spark_sql.md`

- Spark SQL engine
- SQL vs DataFrame API
- Views and temporary tables
- Hive integration
- Delta Lake introduction

**Exercises (7)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_sql_to_dataframe_converter.py` | API translation | Easy |
| 02 | `problem_02_view_manager.py` | Temporary views | Easy |
| 03 | `problem_03_hive_metastore_connector.py` | Hive integration | Medium |
| 04 | `problem_04_sql_function_registry.py` | Custom functions | Medium |
| 05 | `problem_05_delta_table_manager.py` | Delta Lake basics | Medium |
| 06 | `problem_06_time_travel_query_builder.py` | Delta time travel | Hard |
| 07 | `problem_07_sql_optimization_advisor.py` | SQL tuning | Hard |

#### Day 4: Spark Performance Tuning

**Theory**: `day04_spark_performance.md`

- Narrow vs wide transformations
- Data skew detection and handling
- Salting technique
- Adaptive Query Execution
- Dynamic allocation

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_narrow_wide_classifier.py` | Transformation types | Easy |
| 02 | `problem_02_skew_detector.py` | Data skew identification | Easy |
| 03 | `problem_03_salting_strategy_impl.py` | Skew mitigation | Medium |
| 04 | `problem_04_aqe_configurator.py` | AQE settings | Medium |
| 05 | `problem_05_join_strategy_selector.py` | Join algorithm choice | Medium |
| 06 | `problem_06_spill_monitor.py` | Memory spill tracking | Medium |
| 07 | `problem_07_dynamic_allocation_tuner.py` | Elastic scaling | Hard |
| 08 | `problem_08_performance_bottleneck_analyzer.py` | Bottleneck detection | Hard |

#### Day 5: ETL with Spark

**Theory**: `day05_spark_etl.md`

- Batch ETL patterns
- Incremental processing
- Multi-hop architecture (Bronze, Silver, Gold)
- Data quality checks in Spark
- Checkpointing and recovery

**Exercises (7)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_bronze_ingestion_pattern.py` | Raw data ingestion | Easy |
| 02 | `problem_02_silver_transformation_impl.py` | Cleansed layer | Easy |
| 03 | `problem_03_gold_aggregation_builder.py` | Business aggregates | Medium |
| 04 | `problem_04_incremental_load_spark.py` | Delta processing | Medium |
| 05 | `problem_05_data_quality_validator.py` | DQ in Spark | Medium |
| 06 | `problem_06_checkpoint_manager.py` | Fault tolerance | Hard |
| 07 | `problem_07_multi_hop_pipeline_orchestrator.py` | Layered architecture | Hard |

#### Day 6: Structured Streaming

**Theory**: `day06_structured_streaming.md`

- Streaming DataFrames
- Source and sink types
- Output modes
- Stateful streaming
- Windowed aggregations

**Exercises (7)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_streaming_source_selector.py` | Source selection | Easy |
| 02 | `problem_02_output_mode_selector.py` | Output mode logic | Easy |
| 03 | `problem_03_trigger_interval_calculator.py` | Trigger tuning | Medium |
| 04 | `problem_04_foreach_batch_handler.py` | Batch operations | Medium |
| 05 | `problem_05_stateful_stream_processor.py` | State management | Medium |
| 06 | `problem_06_stream_join_impl.py` | Stream joins | Hard |
| 07 | `problem_07_streaming_etl_builder.py` | End-to-end streaming | Hard |

### Week 6 Project: Big Data Aggregation Job

**Project Directory**: `project/`

**Overview**: Build a PySpark application that processes terabyte-scale e-commerce data for analytics.

**Features**:
- Multi-source ingestion (CSV, Parquet, JDBC)
- Bronze/Silver/Gold medallion architecture
- Complex aggregations and windowing
- Data quality validation at each layer
- Performance-optimized joins
- Incremental processing support
- Checkpoint and recovery
- Unit tests with pytest-spark

**Estimated Tests**: 50 tests

---

## Week 7: Data Warehousing & Analytics

**Week Goal**: Design and implement data warehouse solutions with modern analytics engineering practices.

**Theme**: "The Analytics Foundation"

### Learning Objectives

1. Understand data warehouse architecture
2. Implement dimensional modeling
3. Work with cloud data warehouses (Snowflake/BigQuery)
4. Use dbt for data transformations
5. Build analytics models
6. Implement data governance practices

### Day-by-Day Breakdown

#### Day 1: Data Warehouse Concepts

**Theory**: `day01_data_warehousing.md`

- OLTP vs OLAP
- Data warehouse architectures (Kimball, Inmon, Data Vault)
- Columnar storage benefits
- Cloud data warehouse comparison
- Cost-performance trade-offs

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_oltp_vs_olap_analyzer.py` | Workload classification | Easy |
| 02 | `problem_02_warehouse_architecture_selector.py` | Architecture selection | Easy |
| 03 | `problem_03_columnar_storage_calculator.py` | Storage efficiency | Medium |
| 04 | `problem_04_warehouse_sizing_estimator.py` | Capacity planning | Medium |
| 05 | `problem_05_query_pattern_classifier.py` | Workload analysis | Medium |
| 06 | `problem_06_cost_optimizer.py` | Cost reduction strategies | Medium |
| 07 | `problem_07_hybrid_warehouse_planner.py` | Multi-platform design | Hard |
| 08 | `problem_08_warehouse_migration_planner.py` | Migration strategy | Hard |

#### Day 2: Dimensional Modeling

**Theory**: `day02_dimensional_modeling.md`

- Fact tables (transactional, periodic snapshot, accumulating snapshot)
- Dimension tables (conformed, slowly changing, degenerate)
- Star vs snowflake schema
- Surrogate keys
- Bridge tables

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_fact_table_classifier.py` | Fact table types | Easy |
| 02 | `problem_02_dimension_type_detector.py` | Dimension categories | Easy |
| 03 | `problem_03_surrogate_key_generator.py` | Key generation | Medium |
| 04 | `problem_04_scd_type_impl.py` | Slowly changing dimensions | Medium |
| 05 | `problem_05_bridge_table_designer.py` | Many-to-many handling | Medium |
| 06 | `problem_06_junk_dimension_builder.py` | Junk dimensions | Medium |
| 07 | `problem_07_mini_dimension_manager.py` | Rapidly changing dims | Hard |
| 08 | `problem_08_outrigger_validator.py` | Snowflake validation | Hard |

#### Day 3: Cloud Data Warehouses (Snowflake/BigQuery)

**Theory**: `day03_cloud_warehouses.md`

- Snowflake architecture (storage, compute, services)
- BigQuery architecture (serverless, slots)
- Virtual warehouses and scaling
- Zero-copy cloning
- Time travel and fail-safe

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_warehouse_size_selector.py` | Compute sizing | Easy |
| 02 | `problem_02_auto_scaling_configurator.py` | Elastic scaling | Easy |
| 03 | `problem_03_zero_clone_planner.py` | Clone strategy | Medium |
| 04 | `problem_04_time_travel_calculator.py` | Data recovery | Medium |
| 05 | `problem_05_resource_monitor_impl.py` | Cost controls | Medium |
| 06 | `problem_06_data_sharing_configurator.py` | Secure sharing | Medium |
| 07 | `problem_07_query_acceleration_optimizer.py` | Performance tuning | Hard |
| 08 | `problem_08_multi_cluster_warehouse_planner.py` | Concurrency scaling | Hard |

#### Day 4: dbt (Data Build Tool)

**Theory**: `day04_dbt_intro.md`

- Analytics engineering paradigm
- dbt models and materializations
- Tests and documentation
- Snapshots and incremental models
- dbt packages and macros

**Exercises (8)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_model_materialization_selector.py` | Materialization choice | Easy |
| 02 | `problem_02_ref_resolver.py` | Model dependencies | Easy |
| 03 | `problem_03_dbt_test_writer.py` | Schema and data tests | Medium |
| 04 | `problem_04_incremental_model_logic.py` | Incremental builds | Medium |
| 05 | `problem_05_snapshot_strategy_impl.py` | Change tracking | Medium |
| 06 | `problem_06_macro_developer.py` | Reusable SQL | Medium |
| 07 | `problem_07_dbt_package_manager.py` | Package dependencies | Hard |
| 08 | `problem_08_exposure_configurator.py` | Lineage documentation | Hard |

#### Day 5: Data Governance

**Theory**: `day05_data_governance.md`

- Data cataloging
- Data lineage
- Data quality frameworks
- Access control and RBAC
- Data retention and privacy

**Exercises (7)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_data_classifier.py` | Sensitivity classification | Easy |
| 02 | `problem_02_lineage_tracker.py` | Data lineage capture | Easy |
| 03 | `problem_03_quality_rule_engine.py` | DQ rule framework | Medium |
| 04 | `problem_04_rbac_policy_builder.py` | Access control | Medium |
| 05 | `problem_05_retention_policy_manager.py` | Data lifecycle | Medium |
| 06 | `problem_06_pii_detector.py` | Privacy compliance | Hard |
| 07 | `problem_07_governance_dashboard_calculator.py` | Metrics and KPIs | Hard |

#### Day 6: Analytics Engineering Best Practices

**Theory**: `day06_analytics_engineering.md`

- Code organization in dbt
- CI/CD for analytics
- Documentation as code
- Testing strategies
- Performance optimization

**Exercises (7)**:

| # | Problem | Topic | Difficulty |
|---|---------|-------|------------|
| 01 | `problem_01_project_structure_validator.py` | Folder conventions | Easy |
| 02 | `problem_02_cicd_pipeline_builder.py` | Automated testing | Easy |
| 03 | `problem_03_documentation_coverage_calculator.py` | Doc coverage | Medium |
| 04 | `problem_04_test_coverage_analyzer.py` | Test metrics | Medium |
| 05 | `problem_05_model_performance_ranker.py` | Performance tracking | Medium |
| 06 | `problem_06_sql_style_checker.py` | Code quality | Hard |
| 07 | `problem_07_debt_calculator.py` | Technical debt metrics | Hard |

### Week 7 Project: Data Warehouse Models

**Project Directory**: `project/`

**Overview**: Build a complete dbt project that transforms raw data into analytics-ready models for a retail business.

**Features**:
- Staging models (clean source data)
- Intermediate models (business logic)
- Mart models (facts and dimensions)
- Comprehensive tests (schema, data, freshness)
- Documentation and exposures
- Incremental models for large tables
- Snapshots for slowly changing dimensions
- Macros for reusable logic
- CI/CD-ready structure

**Estimated Tests**: 45 tests

---

## Week 8: Capstone - End-to-End Data Pipeline

**Week Goal**: Integrate all learned concepts into a production-grade analytics platform.

**Theme**: "The Complete Picture"

### Learning Objectives

1. Design a complete data architecture
2. Implement multi-source ingestion
3. Build transformation pipelines with Spark
4. Orchestrate with Airflow
5. Load to cloud data warehouse
6. Create analytics layer with dbt
7. Build observability and monitoring

### Capstone Project: Complete Analytics Platform

**Project Directory**: `project/`

**Overview**: Build a complete analytics platform for an e-commerce company that ingests data from multiple sources, processes it through multiple layers, and serves it to business users.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                              │
├──────────────┬──────────────┬──────────────┬────────────────────┤
│  PostgreSQL  │    Kafka     │     S3       │       API          │
│ (OLTP DB)    │ (Events)     │ (Files)      │  (External)        │
└──────┬───────┴──────┬───────┴──────┬───────┴─────────┬──────────┘
       │              │              │                 │
       └──────────────┴──────────────┴─────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │  INGESTION LAYER   │
                    │   (Airflow DAGs)   │
                    └─────────┬──────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
┌──────▼──────┐     ┌─────────▼─────────┐  ┌────────▼────────┐
│   Kafka     │     │   Landing Zone    │  │  Stream Proc    │
│  (Buffer)   │     │   (S3/Parquet)    │  │  (Spark Stream) │
└─────────────┘     └─────────┬─────────┘  └─────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │  PROCESSING LAYER  │
                    │   (Spark/PySpark)  │
                    │  Bronze→Silver→Gold│
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │   WAREHOUSE LAYER  │
                    │  (Snowflake/BQ)    │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │  TRANSFORM LAYER   │
                    │       (dbt)        │
                    │   Marts & Metrics  │
                    └─────────┬──────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
┌──────▼──────┐     ┌─────────▼─────────┐  ┌────────▼────────┐
│  Dashboard  │     │   Reverse ETL     │  │   ML Feature    │
│  (BI Tool)  │     │   (Activation)    │  │     Store       │
└─────────────┘     └───────────────────┘  └─────────────────┘
```

### Milestones

#### Milestone 1: Infrastructure & Ingestion (Days 1-2)

**Theory**: `milestone01_infrastructure.md`

- Docker Compose for all services
- Airflow DAGs for data ingestion
- Kafka setup for event streaming
- S3/minIO for data lake storage

**Components**:
- Docker Compose configuration
- Airflow connection setup
- Initial DAG skeletons
- Health checks and monitoring

#### Milestone 2: Stream Processing (Day 3)

**Theory**: `milestone02_stream_processing.md`

- Kafka producer for events
- Spark Structured Streaming job
- Real-time aggregations
- Stream-to-storage sink

**Components**:
- Event producer simulation
- Spark streaming application
- Windowed analytics

#### Milestone 3: Batch Processing (Day 4)

**Theory**: `milestone03_batch_processing.md`

- PySpark batch jobs
- Bronze/Silver/Gold architecture
- Data quality checks
- Incremental processing

**Components**:
- Bronze ingestion job
- Silver transformation job
- Gold aggregation job
- Quality validation

#### Milestone 4: Orchestration (Day 5)

**Theory**: `milestone04_orchestration.md`

- Master Airflow DAG
- Cross-DAG dependencies
- Error handling and alerting
- SLAs and monitoring

**Components**:
- Master orchestration DAG
- Sensor-based triggers
- Alerting configuration
- Retry policies

#### Milestone 5: Analytics & Serving (Day 6)

**Theory**: `milestone05_analytics.md`

- dbt models for marts
- Data warehouse loading
- API for data serving
- Dashboard preparation

**Components**:
- dbt project
- Fact and dimension models
- Metrics layer
- Documentation

### Capstone Deliverables

1. **Infrastructure** (`infrastructure/`)
   - Docker Compose files
   - Configuration management
   - Service initialization scripts

2. **Ingestion** (`ingestion/`)
   - Database extractors
   - API connectors
   - File watchers
   - Kafka producers

3. **Processing** (`processing/`)
   - PySpark jobs
   - Transformation logic
   - Quality checks
   - Configuration

4. **Orchestration** (`orchestration/`)
   - Airflow DAGs
   - Dependencies
   - Sensors

5. **Analytics** (`analytics/`)
   - dbt project
   - Models (staging, intermediate, marts)
   - Tests and docs

6. **Monitoring** (`monitoring/`)
   - Data quality dashboards
   - Pipeline health checks
   - Alerting rules

### Capstone Testing

| Category | Test Count | Description |
|----------|------------|-------------|
| Unit Tests | 60 | Individual component tests |
| Integration Tests | 30 | Cross-component tests |
| Data Quality Tests | 25 | dbt tests, great_expectations |
| End-to-End Tests | 10 | Full pipeline tests |
| **Total** | **125** | |

---

## Course Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Weeks** | 8 |
| **Total Days** | 48 |
| **Total Exercises** | ~350 |
| **Total Projects** | 8 |
| **Estimated Tests** | ~400 |
| **Theory Documents** | 48 |
| **Main Technologies** | 12+ |

### Technology Coverage

| Technology | Week | Hours (Est.) |
|------------|------|--------------|
| Docker | 1 | 8 |
| PostgreSQL | 2 | 12 |
| MongoDB | 2 | 6 |
| Pandas | 3 | 8 |
| Polars | 3 | 6 |
| Pandera | 3 | 4 |
| Apache Airflow | 4 | 16 |
| Apache Kafka | 5 | 16 |
| Apache Spark | 6 | 16 |
| dbt | 7 | 12 |
| Cloud DW (Snowflake/BigQuery) | 7 | 8 |

### Weekly Exercise Distribution

| Week | Exercises | Tests | Project |
|------|-----------|-------|---------|
| Week 1 | 48 | 50 | Migration Tool v1 |
| Week 2 | 47 | 55 | Migration Tool v2 |
| Week 3 | 46 | 50 | Cleaning Pipeline |
| Week 4 | 45 | 45 | Reporting DAG |
| Week 5 | 45 | 45 | Log Processor |
| Week 6 | 45 | 50 | Big Data Job |
| Week 7 | 45 | 45 | DWH Models |
| Week 8 | - | 125 | Capstone |
| **Total** | **321** | **415** | **8 Projects** |

---

## Learning Path Recommendations

### For OOP Journey Graduates

1. **Week 1-2**: Review and reinforce Python patterns in new context
2. **Week 3**: Focus on performance optimization (new concepts)
3. **Week 4-5**: Heavy infrastructure weeks - allocate extra time
4. **Week 6**: Leverage pandas knowledge for PySpark transition
5. **Week 7**: Apply SQL skills to dimensional modeling
6. **Week 8**: Synthesis - expect to spend 1.5-2x normal week time

### For Standalone Learners

**Prerequisites to complete first**:
- Python programming (functions, classes, modules)
- Basic SQL
- Command line basics
- Git fundamentals

**Estimated prep time**: 2-4 weeks

---

## Assessment Strategy

### Weekly Assessments

| Week | Assessment Type | Weight |
|------|-----------------|--------|
| 1-7 | Project Completion | 70% |
| 1-7 | Code Review | 20% |
| 1-7 | Theory Quiz | 10% |
| 8 | Capstone Defense | 100% |

### Capstone Evaluation Criteria

1. **Architecture Design** (25%)
   - Scalability considerations
   - Technology choices
   - Data flow design

2. **Implementation Quality** (25%)
   - Code organization
   - Testing coverage
   - Documentation

3. **Data Quality** (20%)
   - Validation strategies
   - Error handling
   - Monitoring

4. **Performance** (15%)
   - Optimization techniques
   - Resource efficiency
   - Throughput

5. **Presentation** (15%)
   - Architecture explanation
   - Demo quality
   - Q&A handling

---

## Resources & References

### Essential Reading

1. "Designing Data-Intensive Applications" - Martin Kleppmann
2. "The Data Warehouse Toolkit" - Ralph Kimball
3. "Spark: The Definitive Guide" - Bill Chambers & Matei Zaharia

### Documentation

- Apache Airflow: https://airflow.apache.org/docs/
- Apache Kafka: https://kafka.apache.org/documentation/
- Apache Spark: https://spark.apache.org/docs/
- dbt: https://docs.getdbt.com/

### Community

- dbt Slack: analytics-engineering
- Apache Airflow Slack
- r/dataengineering (Reddit)

---

## Certification

Upon completion, students will be able to:

- ✅ Design and implement production data pipelines
- ✅ Work with batch and streaming data processing
- ✅ Orchestrate complex workflows with Airflow
- ✅ Process large-scale data with Spark
- ✅ Build analytics models with dbt
- ✅ Deploy data infrastructure with Docker
- ✅ Implement data quality and governance

---

*Course Version: 1.0*  
*Last Updated: 2026-03-12*  
*Prerequisite: Python OOP Journey v2 or equivalent*
